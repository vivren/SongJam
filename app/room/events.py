from flask import session
from flask_socketio import emit, join_room, leave_room, SocketIO
from apiclient.discovery import build
import html
from .classes import Playlist
from ..roomAction import rooms
from .. import socketio
from . import playlist

@socketio.on('joined', namespace='/room')
def joined(message):
    room = session.get('roomId')
    rooms.newConnection(room)
    join_room(room)
    emit('newConnection', {'users': rooms.getNumUsersConnected(room)}, room=room)
    emit('status', {'msg': session.get('name') + ' has entered the room'}, room=room)
    if rooms.getNumUsersConnected(room) != 1:
        emit('update', room=room)


@socketio.on('addSong', namespace='/room')
def song(message):
    youtube = build('youtube', 'v3', developerKey="AIzaSyBOXu8v48fZ5j_9SIGCkqZoO9pZ39PlwoU")
    search = youtube.search().list(
        part="snippet",
        maxResults=1,
        type="video",
        q=message["song"],
        videoLicense="creativeCommon"
    )

    response = search.execute()
    room = session.get('roomId')

    if len(response["items"]) == 0:
        emit("searchResults", {"results": False, "search": message["song"]}, room=room)
    else:
        emit("searchResults", {"results": True}, room=room)
        playlist.addSong(room, html.unescape(response["items"][0]["snippet"]["title"]), response["items"][0]["id"]["videoId"])
        emit('status', {'msg': html.unescape(response["items"][0]["snippet"]["title"]) + ' has been queued by ' + session.get('name')}, room=room)


@socketio.on('displayPlaylist', namespace='/room')
def displayPlaylist():
    room = session.get('roomId')
    emit('playlist', {'playlist': playlist.getPlaylist(room)}, room=room)


@socketio.on('displayVideo', namespace='/room')
def displayVideo(message):
    room = session.get('roomId')
    if not playlist.isEmpty(room):
        emit('video', {'id': playlist.getCurrentSong(room).split(",")[-1], 'video': playlist.getCurrentSong(room).rsplit(",", 1)[0], 'firstOnly': message["firstOnly"]}, room=room)
        # emit('unmute', room=room)


@socketio.on('pause', namespace='/room')
def pause():
    room = session.get('roomId')
    emit('pauseVideo', room=room)


@socketio.on('end', namespace='/room')
def stop():
    room = session.get('roomId')
    playlist.getNextSong(room)
    if not playlist.isEmpty(room):
        emit('video', {'id': playlist.getCurrentSong(room).split(",")[-1], 'video': playlist.getCurrentSong(room).rsplit(",", 1)[0], 'firstOnly': False}, room=room)


@socketio.on('timeUpdate', namespace='/room')
def timeUpdate(message):
    room = session.get('roomId')
    if not playlist.isEmpty(room):
        emit('time', {'time': message["time"]}, room=room)


@socketio.on('left', namespace='/room')
def left(message):
    room = session.get('roomId')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room'}, room=room)
