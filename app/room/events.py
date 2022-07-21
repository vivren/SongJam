from flask import Flask, Blueprint, session, redirect, url_for, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from classes import Playlist
from apiclient.discovery import build
import html
import time


@socketio.on('joined', namespace='/chat')
def joined(message):
    global users
    users += 1
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room'}, room=room)
    if users != 1:
        emit('update', room=room)


@socketio.on('addSong', namespace='/chat')
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
    room = session.get('room')

    if len(response["items"]) == 0:
        emit("searchResults", {"results": False, "search": message["song"]}, room=room)
    else:
        emit("searchResults", {"results": True}, room=room)
        playlist.addSong(room, html.unescape(response["items"][0]["snippet"]["title"]), response["items"][0]["id"]["videoId"])
        emit('status', {'msg': html.unescape(response["items"][0]["snippet"]["title"]) + ' has been queued by ' + session.get('name')}, room=room)


@socketio.on('displayPlaylist', namespace='/chat')
def displayPlaylist():
    room = session.get('room')
    emit('playlist', {'playlist': playlist.getPlaylist(room)}, room=room)


@socketio.on('displayVideo', namespace='/chat')
def displayVideo(message):
    room = session.get('room')
    if not playlist.isEmpty(room):
        emit('video', {'id': playlist.getCurrentSong(room).split(",")[-1], 'video': playlist.getCurrentSong(room).rsplit(",", 1)[0], 'firstOnly': message["firstOnly"]}, room=room)
        # emit('unmute', room=room)


@socketio.on('pause', namespace='/chat')
def pause():
    room = session.get('room')
    emit('pauseVideo', room=room)


@socketio.on('end', namespace='/chat')
def stop():
    room = session.get('room')
    playlist.getNextSong(room)
    if not playlist.isEmpty(room):
        emit('video', {'id': playlist.getCurrentSong(room).split(",")[-1], 'video': playlist.getCurrentSong(room).rsplit(",", 1)[0], 'firstOnly': False}, room=room)


@socketio.on('timeUpdate', namespace='/chat')
def timeUpdate(message):
    room = session.get('room')
    if not playlist.isEmpty(room):
        emit('time', {'time': message["time"]}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room'}, room=room)