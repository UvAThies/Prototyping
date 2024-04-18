# Tijn Schuitevoerder 2024

import sys
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

if "RPi.GPIO" not in sys.modules:
    print("RPi.GPIO not found, running in debug mode")
    from controller_sim import MotorControlSim

    controller = MotorControlSim()

else:
    # connect to the motor controller
    from controls import MotorControl

    controller = MotorControl()

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
        if data['sound'] == 'PLAY':
            controller.play_sound()
        elif data['sound'] == 'STOP':
            controller.stop_sound()

    if "joy_x" in data and "joy_y" in data:
        joy_x = data["joy_x"]
        joy_y = data["joy_y"]

        # print(f"Received request: joy_x={joy_x}, joy_y={joy_y}")
        # emit("rsp", {"status": "OK"})
        controller.motor_instructions(joy_y, joy_x)


@socketio.on("connect")
def handle_connect():
    print("Client connected")
    emit("rsp", {"status": "CONNECTED"})


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", allow_unsafe_werkzeug=True)
