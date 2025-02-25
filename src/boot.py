from machine import Pin
from time import sleep

from server import start_server

# SENSOR_PIN_NUMBERS = [
#     # left to right
#     14,
#     27,
#     26,
#     25,
#     33,
#     32,
#     35,
#     34,
# ]

MOTOR_LEFT_PIN_NUMBERS = [
    4,
    18,
]

MOTOR_RIGHT_PIN_NUMBERS = [
    19,
    23,
]

# sensor_pins = [Pin(p, Pin.IN) for p in SENSOR_PIN_NUMBERS]

# def read_sensor_state():
#     return [p.value() for p in sensor_pins]

# while True:
#     print(read_sensor_state())
#     sleep(0.1)


start_server(Pin(MOTOR_LEFT_PIN_NUMBERS[0], Pin.OUT), Pin(MOTOR_LEFT_PIN_NUMBERS[1], Pin.OUT), Pin(MOTOR_RIGHT_PIN_NUMBERS[0], Pin.OUT), Pin(MOTOR_RIGHT_PIN_NUMBERS[1], Pin.OUT))