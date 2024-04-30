# Tijn Schuitevoerder 2024

import sys
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from controls import MotorControl, ServoControl
# from controls_sim import MotorControl, ServoControl
import gpsd


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
        controller.motor_instructions(joy_y, joy_x)


@socketio.on("servo")
def handle_servo(data):
    if "servo_x" in data:
        servo = data["servo_x"]
        servo_controller.move(servo)
    if "stop" in data:
        servo_controller.stop()


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
    # return {
    #     "lat": 52.3553194,
    #     "lon": 4.9571569,
    #     "hspeed": 0,
    #     "track": 0,
    #     "mode": 3,
    #     "time": "2024-01-01T00:00:00.000Z",
    #     "error": {
    #         "x": 0.1,
    #         "y": 0.1,
    #         "z": 0.1,
    #     }
    # }

    # Check if nofix
    if current.mode < 2:
        return {"lat": 0, "lon": 0, "speed": 0, "heading": 0,
                "mode": current.mode, "time": current.time}

    return {
        "lat": current.lat,
        "lon": current.lon,
        "speed": current.hspeed,
        "heading": current.track,
        "mode": current.mode,
        "time": current.time,
        "error": current.error
    }


@socketio.on("gps")
def handle_gps():
    gps_data = get_gps_data()
    print(gps_data)
    return gps_data


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", allow_unsafe_werkzeug=True)
