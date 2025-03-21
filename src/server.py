import network
import socket
import json
from time import sleep
from machine import Pin

# WiFi credentials
SSID = "Mitochondria"
PASSWORD = "**atp33adp22amp**"

MAX_TRIAL_COUNT = 10
DIRECTION_FORWARD = "forward"
DIRECTION_BACKWARD = 'backward'
DIRECTION_LEFT = 'left'
DIRECTION_RIGHT = 'right'

# Default motor state
motor_running = False
motor_direction = DIRECTION_FORWARD

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESP32 Control</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <style>
        body {
            margin: 0;
            background-image: url('https://fastly.picsum.photos/id/16/2500/1667.jpg?hmac=uAkZwYc5phCRNFTrV_prJ_0rP0EdwJaZ4ctje2bY7aE');
            background-size: cover;
            font-family: Monospace;
            font-size: 13px;
            line-height: 24px;
            overscroll-behavior: none;
            text-rendering: optimizeLegibility;
            user-select: none;
            font-smooth: always;
        }
        .container {
            margin: 20px;
        }
        .row {
            margin-bottom: 20px;
        }
        .btn {
            width: 100px;
            height: 100px;
            background-color: #333;
            color: #fff;
            border: none;
            display: inline-block;
            text-align: center;
            line-height: 100px;
            cursor: pointer;
            transition: background-color 0.2s ease-in-out, transform 0.2s ease-in-out;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
        }
        .btn:hover {
            background-color: #444;
            transform: scale(1.1);
        }
        .btn:active {
            background-color: #555;
            transform: scale(0.9);
        }
        .logo {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background-color: #fff;
            border: 1px solid #ccc;
            display: inline-block;
            text-align: center;
            line-height: 100px;
            cursor: pointer;
            background-image: url('https://picsum.photos/200/300');
            background-size: cover;
        }
        #connection-status {
            font-size: 18px;
            font-weight: bold;
        }
        #joystick {
            position: relative;
            width: 200px;
            height: 200px;
            border: 1px solid #ccc;
            border-radius: 50%;
            background-color: #fff;
        }
        #joystick .handle {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 50px;
            height: 50px;
            border: 1px solid #ccc;
            border-radius: 50%;
            background-color: #fff;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row">
            <div class="col-md-12 text-center">
                <div class="logo" id="logo"></div>
                <h1>ESP32 Control</h1>
            </div>
        </div>
        <div class="row">
            <div class="col-md-3">
                <button type="button" class="btn" id="start-button" name="Start" onclick="setDirection('start')">Start</button>
            </div>
            <div class="col-md-3">
                <button type="button" class="btn" id="stop-button" name="Stop" onclick="setDirection('stop')">Stop</button>
            </div>
        </div>
        <div class="row">
            <div class="col-md-3">
                <button type="button" class="btn" id="forward-button" name="Forward" onclick="setDirection('forward')">forward</button>
            </div>
            <div class="col-md-3">
                <button type="button" class="btn" id="backward-button" name="Backward" onclick="setDirection('backward')">backward</button>
            </div>
        </div>
        <div class="row">
            <div class="col-md-3">
                <button type="button" class="btn" id="left-button" name="Left" onclick="setDirection('left')">left</button>
            </div>
            <div class="col-md-3">
                <button type="button" class="btn" id="right-button" name="Right" onclick="setDirection('right')">right</button>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12 text-center">
                <button type="button" class="btn" id="switch-button" name="Switch" onclick="switchController()">Switch</button>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12 text-center">
                <div id="joystick" style="display: none;">
                    <div class="handle" id="handle"></div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
            </div>
        <div class="row">
            <div class="col-md-12 text-center">
                <p id="joystick-direction"></p>
            </div>
        </div>
    </div>
    <!-- Modal -->
    <div class="modal fade" id="connection-modal" tabindex="-1" aria-labelledby="connection-modal-label" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="connection-modal-label">Connection Status</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p id="connection-status"></p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
    <script>
        let controller = 'button';

        async function setDirection(direction) {
            const response = await fetch("/direction", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ direction: direction })
            });
            const data = await response.json();
        }

        function switchController() {
            if (controller === 'button') {
                controller = 'joystick';
                document.getElementById('start-button').style.display = 'none';
                document.getElementById('stop-button').style.display = 'none';
                document.getElementById('forward-button').style.display = 'none';
                document.getElementById('backward-button').style.display = 'none';
                document.getElementById('left-button').style.display = 'none';
                document.getElementById('right-button').style.display = 'none';
                document.getElementById('joystick').style.display = 'block';
            } else {
                controller = 'button';
                document.getElementById('start-button').style.display = 'block';
                document.getElementById('stop-button').style.display = 'block';
                document.getElementById('forward-button').style.display = 'block';
                document.getElementById('backward-button').style.display = 'block';
                document.getElementById('left-button').style.display = 'block';
                document.getElementById('right-button').style.display = 'block';
                document.getElementById('joystick').style.display = 'none';
            }
        }

        let joystick = document.getElementById('joystick');
        let handle = document.getElementById('handle');
        let radius = 90; // joystick-এর ব্যাসার্ধ

        joystick.addEventListener('mousedown', (e) => {
            let rect = joystick.getBoundingClientRect();
            let x = e.clientX - rect.left;
            let y = e.clientY - rect.top;
            let angle = Math.atan2(y - rect.height / 2, x - rect.width / 2);
            let length = Math.sqrt(Math.pow(x - rect.width / 2, 2) + Math.pow(y - rect.height / 2, 2));

            if (length > radius) {
                x = rect.width / 2 + Math.cos(angle) * radius;
                y = rect.height / 2 + Math.sin(angle) * radius;
            }

            handle.style.top = `${y}px`;
            handle.style.left = `${x}px`;

            let direction = Math.floor(angle * 180 / Math.PI);

            if (direction > -45 && direction < 45) {
                setDirection('forward');
                document.getElementById('joystick-direction').innerText = 'Joystick Direction: Forward';
            } else if (direction > 45 && direction < 135) {
                setDirection('right');
                document.getElementById('joystick-direction').innerText = 'Joystick Direction: Right';
            } else if (direction > 135 || direction < -135) {
                setDirection('backward');
                document.getElementById('joystick-direction').innerText = 'Joystick Direction: Backward';
            } else if (direction > -135 && direction < -45) {
                setDirection('left');
                document.getElementById('joystick-direction').innerText = 'Joystick Direction: Left';
            }

            document.addEventListener('mousemove', moveJoystick);
            document.addEventListener('mouseup', stopJoystick);
        });

        function moveJoystick(e) {
            let rect = joystick.getBoundingClientRect();
            let x = e.clientX - rect.left;
            let y = e.clientY - rect.top;
            let angle = Math.atan2(y - rect.height / 2, x - rect.width / 2);
            let length = Math.sqrt(Math.pow(x - rect.width / 2, 2) + Math.pow(y - rect.height / 2, 2));

            if (length > radius) {
                x = rect.width / 2 + Math.cos(angle) * radius;
                y = rect.height / 2 + Math.sin(angle) * radius;
            }

            handle.style.top = `${y}px`;
            handle.style.left = `${x}px`;

            let direction = Math.floor(angle * 180 / Math.PI);

            if (direction > -45 && direction < 45) {
                setDirection('forward');
                document.getElementById('joystick-direction').innerText = 'Joystick Direction: Forward';
            } else if (direction > 45 && direction < 135) {
                setDirection('right');
                document.getElementById('joystick-direction').innerText = 'Joystick Direction: Right';
            } else if (direction > 135 || direction < -135) {
                setDirection('backward');
                document.getElementById('joystick-direction').innerText = 'Joystick Direction: Backward';
            } else if (direction > -135 && direction < -45) {
                setDirection('left');
                document.getElementById('joystick-direction').innerText = 'Joystick Direction: Left';
            }
        }

        function stopJoystick() {
            handle.style.top = '50%';
            handle.style.left = '50%';
            document.getElementById('joystick-direction').innerText = 'Joystick Direction: Neutral';
            document.removeEventListener('mousemove', moveJoystick);
            document.removeEventListener('mouseup', stopJoystick);
        }
    </script>
</body>
</html>
"""

# Connect to WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    current_trial_number = 0
    
    while current_trial_number < MAX_TRIAL_COUNT and not wlan.isconnected():
        current_trial_number = current_trial_number + 1

        sleep(1)

    if not wlan.isconnected():
        print("Failed to connect to WiFi")

        return False
    
    print("Connected to WiFi:", wlan.ifconfig())

    return True

def update_motor_pin_values(motor_left_in_1_pin, motor_left_in_2_pin, motor_right_in_1_pin, motor_right_in_2_pin):
    global motor_running, motor_direction, DIRECTION_FORWARD
    print(motor_running, motor_direction)
    if motor_running:
        if motor_direction == DIRECTION_FORWARD:
            motor_left_in_1_pin.value(0)
            motor_left_in_2_pin.value(1)
            motor_right_in_1_pin.value(0)
            motor_right_in_2_pin.value(1)
        elif motor_direction == DIRECTION_BACKWARD:
            motor_left_in_1_pin.value(1)
            motor_left_in_2_pin.value(0)
            motor_right_in_1_pin.value(1)
            motor_right_in_2_pin.value(0)
        elif motor_direction == DIRECTION_RIGHT:
            motor_left_in_1_pin.value(0)
            motor_left_in_2_pin.value(1)
            motor_right_in_1_pin.value(0)
            motor_right_in_2_pin.value(0)
        elif motor_direction == DIRECTION_LEFT:
            motor_left_in_1_pin.value(0)
            motor_left_in_2_pin.value(0)
            motor_right_in_1_pin.value(0)
            motor_right_in_2_pin.value(1)
    else:
        motor_left_in_1_pin.value(0)
        motor_left_in_2_pin.value(0)
        motor_right_in_1_pin.value(0)
        motor_right_in_2_pin.value(0)

# Handle HTTP requests
def handle_request(client, request):
    global motor_running, motor_direction, DIRECTION_FORWARD

    try:
        # Read and parse request
        request = request.decode()
        print("Received request:", request)

        if "GET / " in request or "GET / HTTP" in request:
            client.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + HTML_PAGE)
        elif "POST /direction" in request:
            # Extract JSON payload
            length = int(request.split("Content-Length: ")[1].split("\r\n")[0])
            body = request.split("\r\n\r\n")[1][:length]
            data = json.loads(body)

            if "direction" in data:
                if data["direction"] == DIRECTION_FORWARD:
                    motor_direction = DIRECTION_FORWARD
                    print("Motor direction set to FORWARD")
                elif data["direction"] == DIRECTION_BACKWARD:
                    motor_direction = DIRECTION_BACKWARD
                    print("Motor direction set to BACKWARD")
                elif data["direction"] == DIRECTION_LEFT:
                    motor_direction = DIRECTION_LEFT
                    print("Motor direction set to LEFT")
                elif data["direction"] == DIRECTION_RIGHT:
                    motor_direction = DIRECTION_RIGHT
                    print("Motor direction set to RIGHT")
                elif data["direction"] == "start":
                    motor_running = True
                elif data["direction"] == "stop":
                    motor_running = False
                client.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{\"status\": \"direction set\"}")
            else:
                client.send("HTTP/1.1 400 Bad Request\r\n\r\n")

        elif "POST /start" in request:
            motor_running = True

            print("Motor started:", motor_direction)
            client.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{\"status\": \"motor started\"}")

        elif "POST /stop" in request:
            motor_running = False

            print("Motor stopped")
            client.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{\"status\": \"motor stopped\"}")

        else:
            client.send("HTTP/1.1 404 Not Found\r\n\r\n")

    except Exception as e:
        print("Error:", e)
        client.send("HTTP/1.1 500 Internal Server Error\r\n\r\n")

# Start the server
def start_server(status_led_pin, motor_left_in_1_pin, motor_left_in_2_pin, motor_right_in_1_pin, motor_right_in_2_pin):
    status_led_pin.value(0)

    if not connect_wifi():
        return

    status_led_pin.value(1)
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", 80))
    server.listen(5)
    
    print("Server started on port 80")

    status_led_value = 0

    while True:
        status_led_value = 0 if status_led_value else 1

        status_led_pin(status_led_value)

        client, addr = server.accept()
        print("Cstlient connected:", addr)
        request = client.recv(1024)
        handle_request(client, request)
        client.close()
        update_motor_pin_values(motor_left_in_1_pin, motor_left_in_2_pin, motor_right_in_1_pin, motor_right_in_2_pin)
        print("pin values",motor_left_in_1_pin.value(), motor_left_in_2_pin.value(), motor_right_in_1_pin.value(), motor_right_in_2_pin.value())
        print(motor_direction)