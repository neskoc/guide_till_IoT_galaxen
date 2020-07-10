# Data is sent to Pybytes. Needs first to be flashed with Pybyte firmware
import time
from machine import Pin
from lib.dth import DTH # https://github.com/JurassicPork/DHT_PyCom

# Type 0 = dht11
# Type 1 = dht22
dht11 = 0
dht22 = 1
dht_type = dht11

th = DTH(Pin('P23', mode=Pin.OPEN_DRAIN), dht_type)
time.sleep(2)

while True:
    result = th.read()
    while not result.is_valid():
        time.sleep(.5)
        result = th.read()
    print('Temp:', result.temperature)
    print('RH:', result.humidity)
    pybytes.send_signal(1,result.temperature)
    pybytes.send_signal(2,result.humidity)

    time.sleep(120)
