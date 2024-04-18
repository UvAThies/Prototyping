# Tijn Schuitevoerder 2024

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from controls import MotorControl

# intialize the Flask app
app = Flask(__name__)
socketio = SocketIO(app)

# connect to the motor controller
controller = MotorControl()
controller.setup_sig_handler()


@app.route("/")
def handle_index():
    return render_template("index.html")


@socketio.on("req")
def handle_req(data):
    if "stop" in data:
        emit("rsp", {"status": "Stopping"})
        controller.stop()
        return

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
