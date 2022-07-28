from flask import render_template
from . import errorBP

@errorBP.route('/noRoomsFound')
def noRooms():
    return render_template('error/noRoom.html')

@errorBP.route('/pageNotFound')
def pageNotFound():
    return render_template('error/pageNotFound.html')
