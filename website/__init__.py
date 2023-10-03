from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from os import path  
import os 
from flask import Flask, render_template, request, jsonify

from flask_socketio import SocketIO, emit, join_room, leave_room

socketio = SocketIO()




room_histories = {}

@socketio.on('message')
def handle_message(message):
    username = message['username']
    text = message['text']
    room = message['room']

    # Ensure the room history exists
    if room not in room_histories:
        room_histories[room] = []

    # Add the message to the room's chat history
    room_histories[room].append({'username': username, 'text': text})

    # Emit the updated chat history for this room to all clients in the room
    emit('chat_history', room_histories[room], room=room)
@socketio.on('join')
def join(data):
    room = data['room']
    join_room(room)






# Initialize extensions outside of create_app
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

DB_NAME = "database.db"

def create_app():
    app = Flask(__name__, template_folder='template', static_folder='/static')
    app.config['SECRET_KEY'] = 'replace_this_with_a_more_secure_key76.2*39'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['MAIL_SERVER']='smtp-mail.outlook.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'mbz02@mail.aub.edu'
    app.config['MAIL_PASSWORD'] = '@ilikelinuxkali123'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] =False
    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app) 
    socketio.init_app(app)
    
    # Blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views)
    app.register_blueprint(auth)

    # Ensure the database exists
    create_database(app)

    # Login manager setup
    login_manager.login_view = 'auth.login'

    from .models import User  # Import here to avoid circular imports

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')