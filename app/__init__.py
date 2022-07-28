from flask import Flask, render_template
from flask_socketio import SocketIO

socketio = SocketIO()


def pageNotFound(e):
    return render_template('error/pageNotFound.html'), 404


def createApp():
    app = Flask(__name__)
    app.debug = True
    app.config['SECRET_KEY'] = '1234'
    app.register_error_handler(404, pageNotFound)
    socketio.init_app(app)

    from .main import mainBP
    app.register_blueprint(mainBP)

    from .room import roomBP
    app.register_blueprint(roomBP)

    from .roomAction import roomActionBP
    app.register_blueprint(roomActionBP)

    from .error import errorBP
    app.register_blueprint(errorBP)

    return app
