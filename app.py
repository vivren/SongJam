from flask import Flask, Blueprint, session, redirect, url_for, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from forms import LoginForm
from classes import Song, Playlist
from apiclient.discovery import build
import os

socketio = SocketIO()
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '1234'
socketio.init_app(app)
playlist = Playlist()

# main = Blueprint('main', __name__)
# app.register_blueprint(main)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for('.listen'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('index.html', form=form)


@app.route('/listen', methods=['GET', 'POST'])
def listen():
    name = session.get('name', '')
    room = session.get('room', '')

    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('room.html', name=name, room=room)


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('addSong', namespace='/chat')
def song(message):
    youtube = build('youtube', 'v3', developerKey="AIzaSyBOXu8v48fZ5j_9SIGCkqZoO9pZ39PlwoU")

    search = youtube.search().list(
        part="snippet",
        maxResults=1,
        type="video",
        q=message
    )

    response = search.execute()
    newSong = Song(response["items"][0]["snippet"]["title"], response["items"][0]["id"]["videoId"])
    playlist.addSong(newSong)

    # room = session.get('room')
    # emit('playlist', {'msg': playlist.getPlaylist()}, room=room)
    # emit('message', {'msg': response["items"][0]["snippet"]["title"] + ' has been queued by ' + session.get('name') + '*' + response["items"][0]["id"]["videoId"]}, room=room)

@socketio.on('displayPlaylist', namespace='/chat')
def displayPlaylist():
    room = session.get('room')
    emit('playlist', {'msg': playlist.getPlaylist()}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)


if __name__ == '__main__':
    socketio.run(app)
