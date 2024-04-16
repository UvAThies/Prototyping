# Tijn Schuitevoerder 2024

# Use socketio for real-time communication using websockets
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from time import sleep

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def handle_index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('rsp', {'status':'CONNECTED'})
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', allow_unsafe_werkzeug=True)