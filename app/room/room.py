from flask import session, redirect, url_for, render_template, request
from . import roomBP

@roomBP.route('/room/<roomId>', methods=['GET', 'POST'])
def room(roomId):
    name = session.get('name', '')
    roomData = session.get('room', '')

    if name == '' or roomData == '':
        return redirect(url_for('roomAction.createRoom'))
    return render_template('room/room.html', name=name, room=roomData[0])
