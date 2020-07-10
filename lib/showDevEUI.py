from network import LoRa
import ubinascii

print("DevEUI: %s" % ubinascii.hexlify(LoRa().mac()).decode('ascii').upper())
