# Tijn Schuitevoerder 2024

# Use socketio for real-time communication using websockets
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from time import sleep
import controls

app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def handle_index():
    return render_template("index.html")


@socketio.on("req")
def handle_req(data):
    joy_x = data["joy_x"]
    joy_y = data["joy_y"]

    print(f"Received request: joy_x={joy_x}, joy_y={joy_y}")
    controls.motor_instructions(joy_y, joy_x)

    emit("rsp", {"status": "OK"})


@socketio.on("connect")
def handle_connect():
    print("Client connected")
    emit("rsp", {"status": "CONNECTED"})


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", allow_unsafe_werkzeug=True)
