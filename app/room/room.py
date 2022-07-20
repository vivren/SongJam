@room.route('/listen', methods=['GET', 'POST'])
def listen():
    name = session.get('name', '')
    room = session.get('room', '')

    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('room.html', name=name, room=room)
