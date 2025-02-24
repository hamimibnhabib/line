from machine import Pin
from time import sleep

SENSOR_PIN_NUMBERS = [
    # left to right
    14,
    27,
    26,
    25,
    33,
    32,
    35,
    34,
]

sensor_pins = [Pin(p, Pin.IN) for p in SENSOR_PIN_NUMBERS]

def read_sensor_state():
    return [p.value() for p in sensor_pins]

while True:
    print(read_sensor_state())
    sleep(0.5)
