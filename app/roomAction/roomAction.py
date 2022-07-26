from flask import Flask, Blueprint, session, redirect, url_for, render_template, request
from . import roomActionBP
from .forms import CreateForm, JoinForm
from .classes import Rooms
import shortuuid

rooms = Rooms()

@roomActionBP.route('/createRoom', methods=['GET', 'POST'])
def createRoom():
    form = CreateForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.roomName.data
        roomId = shortuuid.ShortUUID().random(length=5)
        session['roomId'] = roomId
        rooms.addRoom(Room(roomId, form.name.data, form.roomType.data, form.roomPassword.data))
        return redirect(url_for('room.room', roomId=roomId))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.roomName.data = session.get('room', '')
        return render_template('roomAction/createRoom.html', form=form)


@roomActionBP.route('/joinRoom', methods=['GET', 'POST'])
def joinRoom():
    form = JoinForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['roomId'] = form.roomId.data
        return redirect(url_for('room.room', roomId=roomId))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.roomId.data = session.get('roomId', '')
        return render_template('roomAction/joinRoom.html', form=form)

@roomActionBP.route('/browseRoom')
def browseRoom():
    return render_template('roomAction/browseRoom.html')
