# Tijn Schuitevoerder 2024

import sys
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from controls import MotorControl, ServoControl
import gpsd


# from controller_sim import MotorControlSim
# controller = MotorControlSim()

gpsd.connect()
controller = MotorControl()
servo_controller = ServoControl()
controller.setup_sig_handler()


# intialize the Flask app
app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def handle_index():
    return render_template("index.html")


@socketio.on("req")
def handle_req(data):
    if "stop" in data:
        emit("rsp", {"status": "Stopping"})
        controller.stop()
        return
    if "sound" in data:
        if data["sound"] == "PLAY":
            controller.play_sound()
        elif data["sound"] == "STOP":
            controller.stop_sound()

    if "joy_x" in data and "joy_y" in data:
        joy_x = data["joy_x"]
        joy_y = data["joy_y"]

        # print(f"Received request: joy_x={joy_x}, joy_y={joy_y}")
        # emit("rsp", {"status": "OK"})
        controller.motor_instructions_new(joy_y, joy_x)


@socketio.on("servo")
def handle_servo(data):
    if "angle" in data:
        servo = data["angle"]
        servo_controller.move(servo)


@socketio.on("connect")
def handle_connect():
    print("Client connected")
    emit("rsp", {"status": "CONNECTED"})


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


# Use this function to get the current GPS data
def get_gps_data():
    current = gpsd.get_current()

    # Check if nofix
    if current.mode < 2:
        return {"lat": 0, "lon": 0, "speed": 0, "heading": 0,
                "mode": current.mode,
        "status": "NOFIX"}

    return {
        "lat": current.lat,
        "lon": current.lon,
        "speed": current.hspeed,
        "heading": current.track,
        "mode": current.mode,
        "status": "OK",
    }


@socketio.on("gps")
def handle_gps(data):
    gps_data = get_gps_data()
    print(gps_data)
    return gps_data


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", allow_unsafe_werkzeug=True)
