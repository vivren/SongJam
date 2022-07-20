from flask import Flask
from flask_socketio import SocketIO

def createApp():
    socketio = SocketIO()
    app = Flask(__name__)
    app.debug = True
    app.config['SECRET_KEY'] = '1234'
    socketio.init_app(app)

    from .main import main as mainBP
    app.register_blueprint(mainBP)

    return app, socketio



 
