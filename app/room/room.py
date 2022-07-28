from flask import session, redirect, url_for, render_template, request
from . import roomBP

@roomBP.route('/room', methods=['GET', 'POST'])

def room():
    name = session.get('name', '')
    roomName = session.get('room', '')
    roomId = session.get('roomId', '')

    if name == '' or roomName == '' or roomId == '':
        return redirect(url_for('roomAction.createRoom'))
    return render_template('room/room.html', name=name, roomName=roomName)
