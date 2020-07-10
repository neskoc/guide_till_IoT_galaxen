
from network import LoRa
import socket
import time
import ubinascii
import binascii
import struct
import pycom
from machine import Pin
from lib.dth import DTH # https://github.com/JurassicPork/DHT_PyCom

# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

print("DevEUI: " + ubinascii.hexlify(lora.mac()).decode('utf-8').upper())

# SET HERE THE VALUES OF YOUR APP AND DEVICE
THE_APP_EUI = 'ange app eui'
THE_APP_KEY = 'ange app key'


def join_lora(force_join = False):
    '''Joining The Things Network '''
    print('Joining TTN')

    # restore previous state
    if not force_join:
        lora.nvram_restore()

    if not lora.has_joined() or force_join == True:

        # create an OTA authentication params
        app_eui = binascii.unhexlify(THE_APP_EUI.replace(' ','')) # these settings can be found from TTN
        app_key = binascii.unhexlify(THE_APP_KEY.replace(' ','')) # these settings can be found from TTN

        # join a network using OTAA if not previously done
        lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

        # wait until the module has joined the network
        while not lora.has_joined():
            time.sleep(2.5)

        # saving the state
        lora.nvram_save()

        # returning whether the join was successful
        if lora.has_joined():
            flash_led_to(GREEN)
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

pycom.heartbeat(False) # Disable the heartbeat LED

# Getting the LoRa MAC
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
print("Device LoRa MAC:", binascii.hexlify(lora.mac()))
print("DevEUI: " + ubinascii.hexlify(lora.mac()).decode('utf-8').upper())


flash_led_to(YELLOW)
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
    s.bind(2)
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
    payload = struct.pack(">fff", temperature, humidity)

    s.send(payload)
    flash_led_to(GREEN)

    s.setblocking(False)
    # get any data received...
    data = s.recv(64)
    print(data)

    time.sleep(15)
