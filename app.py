import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from monitor import start_monitor, stop_monitor, set_target

app = Flask(__name__)
socketio = SocketIO(app, async_mode="eventlet")

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("start_monitor")
def start(data):
    target = data.get("target")
    set_target(target)
    start_monitor(socketio)
    emit("monitor_status", {"running": True})

@socketio.on("stop_monitor")
def stop():
    stop_monitor()
    emit("monitor_status", {"running": False})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)