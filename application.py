import os
from collections import deque
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
socketio = SocketIO(app)

# Server-side memory
users = set()
channels = {"general": deque([], maxlen=100)}

# for development
channels["general"].append("Welcome to Chatterbox")
channels["general"].append("This is general channel")
channels["channel1"] = deque([], maxlen=100)
channels["channel1"].append("This is channel 1")
channels["channel2"] = deque([], maxlen=100)
channels["channel2"].append("This is channel 2")

@app.route("/")
def index():
    ''' delete users in production '''
    return render_template("index.html", channels=list(channels), users=list(users))

# Join in a user
@socketio.on("join")
def join(data):
    name = data["name"]
    if name in users:
        return False
    else:
        users.add(name)
        emit("new user", {"name": name}, broadcast=True)

# Send a message
@socketio.on("send")
def send(data):
    channel = data["channel"]
    message = data["message"]
    channels[channel].append(message)
    time = datetime.now().strftime("%I:%M%p")
    emit("new message", {"message": message, "time": time}, broadcast=True)

# Create a channel
@socketio.on("create")
def create(data):
    channel = data["channel"]
    if channel in channels:
        return False
    else:
        channels[channel] = deque([], maxlen=100)
        emit("new channel", {"channel": channel}, broadcast=True)

# Change the channel
@socketio.on("change")
def change(data):
    if "channel" in data:
        channel = data["channel"]
        emit("change channel", {"channel": channel, "messages": list(channels[channel])})

# leave the user
@socketio.on("leave")
def leave(data):
    name = data["name"]
    if name in users:
        users.remove(name)
        emit("remove name", {"name": name}, broadcast=True)
