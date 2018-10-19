import os

from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
socketio = SocketIO(app)

# list of all users and channels
users = []
channels = ['general']

@app.route("/")
def index():
    ''' delete users in production '''
    return render_template("index.html", channels=channels, users=users)

# When a user wants to create a new display name,
@app.route("/join", methods=["POST"])
def join():
    user = request.form.get('name')
    if user in users:
        return 'overlap'
    else:
        users.append(user)
        return 'ok'
        
# When the user wants to create a new channel,
@app.route("/create", methods=["POST"])
def create():
    channel = request.form.get('channel')
    if channel in channels:
        return 'overlap'
    else:
        channels.append(channel)

# When the user leaves
@app.route("/leave", methods=["POST"])
def leave():
    user = request.form.get('name')
    if user in users:
        users.remove(user)
    else:
        # Error
        return redirect(url_for('index'))