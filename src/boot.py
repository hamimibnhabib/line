from machine import Pin
from time import sleep

from server import start_server
from engine import start_engine

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
SENSOR_PIN_NUMBER = 13

MOTOR_LEFT_PIN_NUMBERS = [
    4,
    18,
]

MOTOR_RIGHT_PIN_NUMBERS = [
    19,
    23,
]

FUNCTION_SWITCH_PIN_NUMBER = 34

# sensor_pins = [Pin(p, Pin.IN) for p in SENSOR_PIN_NUMBERS]

# def read_sensor_state():
#     return [p.value() for p in sensor_pins]

# while True:
#     print(read_sensor_state())
#     sleep(0.1)

STATUS_LED_PIN_NUMBER = 26

status_led_pin = Pin(STATUS_LED_PIN_NUMBER, Pin.OUT)
sensor_pin = Pin(SENSOR_PIN_NUMBER, Pin.IN)
function_pin = Pin(FUNCTION_SWITCH_PIN_NUMBER, Pin.IN)
motor_left_in_1_pin = Pin(MOTOR_LEFT_PIN_NUMBERS[0], Pin.OUT)
motor_left_in_2_pin = Pin(MOTOR_LEFT_PIN_NUMBERS[1], Pin.OUT)
motor_right_in_1_pin = Pin(MOTOR_RIGHT_PIN_NUMBERS[0], Pin.OUT)
motor_right_in_2_pin = Pin(MOTOR_RIGHT_PIN_NUMBERS[1], Pin.OUT)

if function_pin.value():
    start_server(
        status_led_pin,
        motor_left_in_1_pin,
        motor_left_in_2_pin,
        motor_right_in_1_pin,
        motor_right_in_2_pin,
    )
else:
    start_engine(
        status_led_pin, 
        sensor_pin,
        motor_left_in_1_pin,
        motor_left_in_2_pin,
        motor_right_in_1_pin,
        motor_right_in_2_pin,
    )
