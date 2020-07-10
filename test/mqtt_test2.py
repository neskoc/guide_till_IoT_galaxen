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

# Type 0 = dht11
dht_type = 0
th = DTH(Pin('P23', mode=Pin.OPEN_DRAIN), dht_type)
time.sleep(2)

with open('my_config.json') as f:
    config = json.load(f)

def blink_led():
    for n in range(1):
        pycom.rgbled(0xfcfc03)
        time.sleep(0.5)
        pycom.rgbled(0x000000)
        time.sleep(0.2)

def sub_cb(topic, msg):
   if msg == b'{"Command":"Red"}': pycom.rgbled(0xff0000)
   if msg == b'{"Command":"Blue"}': pycom.rgbled(0x0004ff)
   if msg == b'{"Command":"Green"}': pycom.rgbled(0x00ff04)
   if msg == b'{"Command":"Yellow"}': pycom.rgbled(0xe5ff00)
   if msg == b'{"Command":"White"}': pycom.rgbled(0xe5ff00)
   if msg == b'{"Command":"Off"}': pycom.rgbled(0x000000)
   print((topic, msg))

def interval_send(t_):
    while True:
        send_value()
        time.sleep(t_)

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
        print('Sensor data sent ..')
        blink_led()
        client.check_msg()

    except (NameError, ValueError, TypeError) as err:
        print('Failed to send!', err)

topic_pub = 'nenad/home-sens/'
topic_sub = 'nenad/home-sens/control'
broker_url = 'sjolab.lnu.se'
client_name = ubinascii.hexlify(hashlib.md5(machine.unique_id()).digest()) # create a md5 hash of the pycom WLAN mac
print('client_name:',client_name)

client = MQTTClient(client_name, broker_url, user=config['user_mqtt'], password=config['pass_mqtt'], keepalive=600)

client.set_callback(sub_cb)
client.connect()
client.subscribe(topic_sub)


_thread.start_new_thread(interval_send,[30])
