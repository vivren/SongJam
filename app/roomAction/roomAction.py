from flask import Flask, Blueprint, session, redirect, url_for, render_template, request
from . import roomActionBP, rooms
from .forms import CreateForm, JoinPrivateForm, JoinPublicForm
import shortuuid

@roomActionBP.route('/createRoom', methods=['GET', 'POST'])
def createRoom():
    form = CreateForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.roomName.data
        roomId = shortuuid.ShortUUID().random(length=4 if form.roomType.data == 'Private Room' else 5)
        session['roomId'] = roomId
        rooms.addRoom(roomId, form.name.data, form.roomType.data, form.roomPassword.data)
        return redirect(url_for('room.room', roomId=roomId))

    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.roomName.data = session.get('room', '')
    return render_template('roomAction/createRoom.html', form=form)


@roomActionBP.route('/joinPrivateRoom', methods=['GET', 'POST'])
def joinPrivateRoom():
    form = JoinPrivateForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['roomId'] = form.roomId.data
        return redirect(url_for('room.room', roomId=form.roomId.data))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
    return render_template('roomAction/joinPrivateRoom.html', form=form)


@roomActionBP.route('/joinPublicRoom', methods=['GET', 'POST'])
def joinPublicRoom():
    form = JoinPublicForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['roomId'] = form.roomId.data
        return redirect(url_for('room.room', roomId=form.roomId.data))
    return render_template('roomAction/joinPublicRoom.html', form=form)


@roomActionBP.route('/browseRoom')
def browseRoom():
    ids = rooms.getAllID('Public Room')
    names = rooms.getAllName('Public Room')
    numConnected = rooms.getAllUser('Public Room')
    if len(ids) == 0 or len(names) == 0:
        return render_template('error/noRoom.html')
    return render_template('roomAction/browseRoom.html', ids=ids, rooms=names, users=numConnected)
