try:
    from flask import Flask, render_template, request, redirect, url_for
    from dotenv import load_dotenv
    from flask_bcrypt import Bcrypt
    from projectModule.authentications.userAuthApi import userAuth_blueprint
    from flask_talisman import Talisman
    from flask_socketio import SocketIO, join_room, leave_room
    from flask_cors import CORS
    from flask_mail import Mail
    import os
    from flask_jwt_extended import JWTManager
except Exception as e:
    print("Modules are Missing : {} ".format(e))

app = Flask(__name__)

cors_config = {
    "origins": ["http://localhost:5000", "https://fornaxbackend.herokuapp.com/"],
    "methods": ["GET", "HEAD", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"],
    "allow_headers": ["Authorization"]
}
CORS(app, resources={"/*": cors_config})

JWTManager(app)

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_ID')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASS')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config["UPLOAD_FOLDER"] = "/static/uploads/"
mail = Mail(app)


socketio = SocketIO(app)


load_dotenv()
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")


Talisman(app, content_security_policy=None)
bcrypt = Bcrypt(app)


app.register_blueprint(userAuth_blueprint, url_prefix="/user")
# here "sp" stands for service provider


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/chat')
def chat():
    username = request.args.get('username')
    room = request.args.get('room')

    if username and room:
        return render_template('chat.html', username=username, room=room)
    else:
        return redirect(url_for('home'))


@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'],
                                                                    data['room'],
                                                                    data['message']))
    socketio.emit('receive_message', data, room=data['room'])


@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(
        data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])


@socketio.on('leave_room')
def handle_leave_room_event(data):
    app.logger.info("{} has left the room {}".format(
        data['username'], data['room']))
    leave_room(data['room'])
    socketio.emit('leave_room_announcement', data, room=data['room'])
