#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: nesko
main.py för test av mqtt-protokollet
uppladdad sensorernas mätdata används sedan av node-red och TIG-stack

"""

from network import WLAN
import machine
from machine import Pin
import time
import pycom
import json
import _thread
import ubinascii
import hashlib
from lib.dth import DTH
from lib.umqtt.robust import MQTTClient

pycom.heartbeat(False)

# skapa objekt th (temperatur/humidity) av klassen DTH samt ange att det är Pin 23 som skall användas
# Type 0 = dht11
dht_type = 0
th = DTH(Pin('P23', mode=Pin.OPEN_DRAIN), dht_type)
time.sleep(2)

# läs konfigurationsvärdena
with open('my_config.json') as f:
    config = json.load(f)

# för att inte ständigt ändra pycom_config (nätverk hemma och på jobbet)
# kolla vilket nätverk som är tillgängligt och anslut till det
def connect_wlan():
    wlan = WLAN(mode=WLAN.STA)
    print('Scanning wlan!')
    nets = wlan.scan()
    time.sleep(5)
    for net in nets:
        if net.ssid == config['wifi_work']['ssid']:
            print('Network found: ', net.ssid)
            wlan.connect(net.ssid, auth=(net.sec, config['wifi_work']['password']), timeout=5000)
            while not wlan.isconnected():
                machine.idle() # save power while waiting
            print('WLAN connection succeeded!')
            break
        elif net.ssid == config['wifi_home']['ssid']:
            print('Network found: ', net.ssid)
            wlan.connect(net.ssid, auth=(net.sec, config['wifi_home']['password']), timeout=5000)
            while not wlan.isconnected():
                machine.idle() # save power while waiting
            print('WLAN connection succeeded!')
            break

connect_wlan()

# används för att visa med LED att data skickas ut
def blink_led():
    for n in range(1):
        pycom.rgbled(0xfcfc03)
        time.sleep(0.5)
        pycom.rgbled(0x000000)
        time.sleep(0.2)

# för att visa med LED att kommandot har mottagit (olika färger för olika kommandon)
def sub_cb(topic, msg):
   if msg == b'{"Command":"Red"}': pycom.rgbled(0xff0000)
   if msg == b'{"Command":"Blue"}': pycom.rgbled(0x0004ff)
   if msg == b'{"Command":"Green"}': pycom.rgbled(0x00ff04)
   if msg == b'{"Command":"Yellow"}': pycom.rgbled(0xe5ff00)
   if msg == b'{"Command":"White"}': pycom.rgbled(0xe5ff00)
   if msg == b'{"Command":"Off"}': pycom.rgbled(0x000000)
   print((topic, msg))

# skicka data med jämna mellanrum t_ i tråden
def interval_send(t_):
    while True:
        send_value()
        time.sleep(t_)

# skicka data till sjolab
def send_value():
    try:
        print("Sending sensor data")
        result = th.read()
        while not result.is_valid():
            time.sleep(.5)
            result = th.read()

        client.publish(topic_pub,'{"fipy_nc_sensor": {"dht temp":' + str(result.temperature) +
                                                ',"dht RH":' + str(result.humidity) +
                          '}}')
        print('Sensor data sent! Temperature: {} | Humidity: {}'.format(result.temperature,result.humidity))
        blink_led()
        client.check_msg()

    except (NameError, ValueError, TypeError) as err:
        print('Failed to send!', err)

# ange topic/sub för mqtt
topic_pub = 'nenad/home-sens/'
topic_sub = 'nenad/home-sens/control'
broker_url = 'sjolab.lnu.se'
client_name = ubinascii.hexlify(hashlib.md5(machine.unique_id()).digest()) # create a md5 hash of the pycom WLAN mac
print('client_name:',client_name)

# skapa client-objekt för mqtt-kommunikation (data från config-filen)
client = MQTTClient(client_name, broker_url, user=config['sjolab_mqtt']['user_mqtt'], password=config['sjolab_mqtt']['pass_mqtt'], keepalive=600)

# förberedd för kommunikation
client.set_callback(sub_cb)
client.connect()
client.subscribe(topic_sub)

# skapa tråd som skall köra var 30:e sekund (skicka sensordata)
_thread.start_new_thread(interval_send,[30])