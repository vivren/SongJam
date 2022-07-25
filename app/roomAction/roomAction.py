from flask import Flask, Blueprint, session, redirect, url_for, render_template, request
from . import roomActionBP
from .forms import CreateForm, JoinForm
import shortuuid

rooms = 0

@roomActionBP.route('/createRoom', methods=['GET', 'POST'])
def createRoom():
    form = CreateForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        roomId = shortuuid.uuid()
        session['room'] = [form.roomName.data, roomId, form.roomType.data, form.roomPassword.data]
        return redirect(url_for('room.room', roomId=roomId))
    elif request.method == 'GET':
        print(form.errors)
        form.name.data = session.get('name', '')
        form.roomName.data = session.get('room', '')[0]
        form.roomType.data = session.get('room', '')[2]
        form.roomPassword.data = session.get('room', '')[3]
    return render_template('roomAction/createRoom.html', form=form)


@roomActionBP.route('/joinRoom')
def joinRoom():
    form = JoinForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for('room.room'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.roomName.data = session.get('roomName', '')
    return render_template('roomAction/joinRoom.html', form=form)

@roomActionBP.route('/browseRoom')
def browseRoom():
    return render_template('roomAction/browseRoom.html')
