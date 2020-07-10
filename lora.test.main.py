
from network import LoRa
import socket
import time
import ubinascii
import binascii
import struct
import json
import pycom
from machine import Pin
from lib.dth import DTH # https://github.com/JurassicPork/DHT_PyCom

# enable debug
# pycom.nvs_set('pybytes_debug', 0)

# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
# lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
# lora = LoRa(mode=LoRa.LORAWAN)

# SET HERE THE VALUES OF YOUR APP AND DEVICE
# THE_DEV_EUI = ubinascii.hexlify(lora.mac()).decode('utf-8').upper()


# dev_addr = struct.unpack(">l", binascii.unhexlify(devAddr))[0]
# dev_addr = struct.unpack(">l", ubinascii.unhexlify(devAddr))[0]
# nwk_swkey = ubinascii.unhexlify(nwkSKey)
# app_swkey = ubinascii.unhexlify(appSKey)

with open('pybytes_config.json') as f:
    config = json.load(f)
print('dev_eui:' + config['lora']['otaa']['app_device_eui'])
print('app_eui:' + config['lora']['otaa']['app_eui'])
print('app_key:' + config['lora']['otaa']['app_key'])

RED    = 0xFF0000
GREEN  = 0x00FF00
BLUE   = 0x0000FF
YELLOW = 0xFFFF00

def join_lora(force_join = False):
    '''Joining The Things Network '''
    print('Joining TTN')

    # restore previous state
    if not force_join:
        lora.nvram_restore()

    if not lora.has_joined() or force_join == True:

        # create an OTA authentication params
        dev_eui = ubinascii.unhexlify(config['lora']['otaa']['app_device_eui'])
        app_eui = ubinascii.unhexlify(config['lora']['otaa']['app_eui']) # these settings can be found from TTN
        app_key = ubinascii.unhexlify(config['lora']['otaa']['app_key']) # these settings can be found from TTN
        # print('key:{}, eui:{}'.format(app_key, app_eui))
        # join a network using OTAA (Over the Air Activation) if not previously done
        lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0, dr=0)
        # lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)
        # lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

        # wait until the module has joined the network
        while not lora.has_joined():
            print('Not yet joined...')
            pycom.rgbled(0xcc00ff)
            time.sleep(3)
            pycom.rgbled(0x000000)
            time.sleep(0.5)

        # saving the state
        lora.nvram_save()

        # returning whether the join was successful
        if lora.has_joined():
            flash_led_to(BLUE)
            print('LoRa Joined')
            return True
        else:
            flash_led_to(RED)
            print('LoRa Not Joined')
            return False

    else:
        return True


def lora_cb(lora):
    events = lora.events()
    if events & LoRa.RX_PACKET_EVENT:
        print('Lora packet received')
        data = s.recv(64)
        print(data)
    if events & LoRa.TX_PACKET_EVENT:
        print('Lora packet sent')

def flash_led_to(color):
    pycom.rgbled(color)

pycom.heartbeat(False) # Disable the heartbeat LED

# Getting the LoRa MAC
# lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
lora = LoRa(mode=LoRa.LORAWAN)

# pybytes.connect_lora_otaa(timeout=15, nanogateway=False)

flash_led_to(BLUE)
# joining TTN
join_lora(True)

# Type 0 = dht11
# Type 1 = dht22
dht11 = 0
dht22 = 1
dht_type = dht11

th = DTH(Pin('P23', mode=Pin.OPEN_DRAIN), dht_type)

# py = Pysense()
#tempHum = SI7006A20(py)
# ambientLight = LTR329ALS01(py)

while True:
    # create a LoRa socket
    # create socket to be used for LoRa communication
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    # configure data rate
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
    # make the socket blocking
    # (waits for the data to be sent and for the 2 receive windows to expire)
    s.setblocking(True)
    #define which port with the socket bind
    # s.bind(2)
    # read sensor DTH
    result = th.read()
    while not result.is_valid():
        time.sleep(.5)
        result = th.read()
    temperature = result.temperature
    humidity = result.humidity
    # print('Temp:', result.temperature)
    # print('RH:', result.humidity)
    # luxval = raw2Lux(ambientLight.light())

    print("Read sensors: temp. {} hum. {} ".format(temperature, humidity))

    # Packing sensor data as byte sequence using 'struct'
    # Data is represented as 3 float values, each of 4 bytes, byte orde 'big-endian'
    # for more infos: https://docs.python.org/3.6/library/struct.html
    payload = struct.pack(">HH", int(temperature), int(humidity))

    s.send(payload)
    flash_led_to(GREEN)

    s.setblocking(False)
    # get any data received...
    # data = s.recv(64)
    # print(data)

    time.sleep(600)
