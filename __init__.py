from app import createApp

app, socketio = createApp()

if __name__ == '__main__':
    socketio.run(app)
