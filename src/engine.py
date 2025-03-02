

def start_engine(
    status_led_pin,
    sensor_pin,
    motor_left_in_1_pin,
    motor_left_in_2_pin,
    motor_right_in_1_pin,
    motor_right_in_2_pin,
):
    def move_motor_forward(motor_in_1_pin, motor_in_2_pin):
        motor_in_1_pin.value(0)
        motor_in_2_pin.value(1)

    def move_left_motor_forward():
        move_motor_forward(motor_left_in_1_pin, motor_left_in_2_pin)

    def move_right_motor_forward():
        move_motor_forward(motor_right_in_1_pin, motor_right_in_2_pin)

    def stop_motor(motor_in_1_pin, motor_in_2_pin):
        motor_in_1_pin.value(0)
        motor_in_2_pin.value(0)

    def stop_left_motor():
        stop_motor(motor_left_in_1_pin, motor_left_in_2_pin)

    def stop_right_motor():
        stop_motor(motor_right_in_1_pin, motor_right_in_2_pin)
    
    def move_forward():
        move_left_motor_forward()
        move_right_motor_forward()

    def move_right():
        move_left_motor_forward()
        stop_right_motor()

    try:
        while True:
            if sensor_pin.value():
                move_forward()
            else:
                move_right()
    except KeyboardInterrupt:
        stop_left_motor()
        stop_right_motor()

        raise
