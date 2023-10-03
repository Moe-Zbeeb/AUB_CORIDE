from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from website import db, mail
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('Name')
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Invalid credentials, try again.', category='error')
        else:
            if User.query.filter_by(first_name=name).first():
                flash('Username Taken', category='error')
            else:
                create_new_user(email, password, name) 
                send_welcome_email(email) 
                
                return redirect(url_for('views.home'))

    return render_template("log.html", user=current_user)

def create_new_user(email, password, name):
    new_user = User(email=email, password=generate_password_hash(password), first_name=name ,points=0) 
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user, remember=True)

def send_welcome_email(recipient):
    subject = "Hello_AUB_Community"   
    user = current_user  
    body =     body = f'''
Hey { user.first_name } 🌟,

Driving towards a greener future, one ride at a time.

We're thrilled to have you onboard AUB_coride, the premier carpooling platform for the AUB community. Whether you're looking to share a ride, save on fuel, reduce your carbon footprint, or simply enjoy the company of fellow travelers, we've got you covered.

Feel free to contact our engineers:
aubcoride_technical_team
Mohamad
81/534672
'''

    msg = Message(subject, sender='mbz02@mail.aub.edu', recipients=[recipient])
    msg.body = body
    mail.send(msg)    

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))