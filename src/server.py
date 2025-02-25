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

# Default motor state
motor_running = False
motor_direction = DIRECTION_FORWARD

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESP32 Motor Control</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 20px; background-color: #f4f4f4; }
        h2 { color: #333; }
        button { padding: 15px; margin: 10px; font-size: 18px; border: none; cursor: pointer; border-radius: 5px; }
        .btn-start { background-color: green; color: white; }
        .btn-stop { background-color: red; color: white; }
        .btn-direction { background-color: blue; color: white; }
    </style>
</head>
<body>

    <h2>ESP32 Motor Control</h2>

    <button class="btn-direction" onclick="setDirection('forward')">Set Forward</button>
    <button class="btn-direction" onclick="setDirection('backward')">Set Backward</button>
    <br>
    <button class="btn-start" onclick="startMotor()">Start Motor</button>
    <button class="btn-stop" onclick="stopMotor()">Stop Motor</button>

    <script>
        async function setDirection(direction) {
            const response = await fetch("/direction", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ direction: direction })
            });
            const data = await response.json();
            // alert(data.status);
        }

        async function startMotor() {
            const response = await fetch("/start", { method: "POST" });
            const data = await response.json();
            // alert(data.status);
        }

        async function stopMotor() {
            const response = await fetch("/stop", { method: "POST" });
            const data = await response.json();
            // alert(data.status);
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
    
    print("Connected to WiFi:", wlan.ifconfig())

def update_motor_pin_values(motor_left_in_1_pin, motor_left_in_2_pin, motor_right_in_1_pin, motor_right_in_2_pin):
    global motor_running, motor_direction

    if motor_running:
        if motor_direction == DIRECTION_FORWARD:
            motor_left_in_1_pin.value(1)
            motor_left_in_2_pin.value(0)
            motor_right_in_1_pin.value(1)
            motor_right_in_2_pin.value(0)
        else:
            motor_left_in_1_pin.value(0)
            motor_left_in_2_pin.value(1)
            motor_right_in_1_pin.value(0)
            motor_right_in_2_pin.value(1)
    else:
        motor_left_in_1_pin.value(0)
        motor_left_in_2_pin.value(0)
        motor_right_in_1_pin.value(0)
        motor_right_in_2_pin.value(0)

# Handle HTTP requests
def handle_request(client, request):
    global motor_running, motor_direction

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
def start_server(motor_left_in_1_pin, motor_left_in_2_pin, motor_right_in_1_pin, motor_right_in_2_pin):
    connect_wifi()
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", 80))
    server.listen(5)
    
    print("Server started on port 80")

    while True:
        client, addr = server.accept()
        print("Client connected:", addr)
        request = client.recv(1024)
        handle_request(client, request)
        client.close()
        update_motor_pin_values(motor_left_in_1_pin, motor_left_in_2_pin, motor_right_in_1_pin, motor_right_in_2_pin)
