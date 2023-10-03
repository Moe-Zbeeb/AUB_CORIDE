from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Carpool
from . import db 
from .models import Carpool, User
from datetime import datetime, timedelta
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html')


@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        fromloc = request.form.get('from')
        toloc = request.form.get('to')
        totals = request.form.get('seats')
        name = request.form.get('name')  # Get the 'name' from the form
        # Get the 'phone_number' from the form
        phone_number = request.form.get('phone_number')

        # Parse the 'departure_time' string and convert it to a datetime object
        departure_time_str = request.form.get('time')
        current_date = datetime.now().date()
        departure = datetime.strptime(
            f"{current_date} {departure_time_str}", "%Y-%m-%d %H:%M")

        # Check if all fields have been filled out
        if not fromloc  or not totals or not departure or not name or not phone_number:
            flash('Please fill out all the fields!', category='error')
            return render_template('input.html', user=current_user)
        else:
            # Create a new carpool instance with 'name' and 'phone_number'
            new_carpool = Carpool(
                from_location=fromloc,
                to_location=toloc,
                total_seats=totals,
                available_seats=totals,
                departure_time=departure,
                name=name,
                phone_number=phone_number,  # Add 'phone_number' to the instance
                owner_id = current_user.id
            )

            # Add new carpool to the user's carpools and commit to the database

            current_user.carpools.append(new_carpool)
            db.session.add(new_carpool)
            db.session.commit()
            flash('Carpool added successfully!', category='success')

    carpools = Carpool.query.all()
    return render_template("home.html", user=current_user, carpools=carpools)


@views.route('/confirm_reservation/<int:carpool_id>', methods=['POST'])
@login_required
def confirm_reservation(carpool_id):
    carpool = Carpool.query.get_or_404(carpool_id)
    owner = User.query.get(carpool.owner_id) # Access the owner of the carpool
    # Increment the driver's points
    if current_user in carpool.passengers:
        flash('You are already a passenger for this carpool!.', 'error')
        return redirect(url_for('views.home'))
    # Check if seats are available for the carpool
    if carpool.available_seats <= 0:
        flash('No available seats for this carpool!,try another.', 'error')
        return redirect(url_for('views.home'))
    owner.points+=100
    carpool.available_seats -= 1
    current_user.carpools.append(carpool)
    db.session.commit()

    flash('Seat reserved successfully!', 'success')
    return redirect(url_for('views.home'))


@views.route('/new', methods=['GET', 'POST'])
@login_required
def reserve():
    return render_template("input.html", user=current_user)
  

@views.route('/carpool_info/<int:carpool_id>')
@login_required
def carpool_info(carpool_id):
    carpool = Carpool.query.get_or_404(carpool_id)

    return render_template('carpool_info.html', carpool=carpool, user=current_user)


@views.route('/remove_carpool_route/<int:carpool_id>', methods=['POST'])
@login_required
def remove_carpool_route(carpool_id):
    x = Carpool.query.get_or_404(carpool_id)
    if current_user.id == x.owner_id:
        db.session.delete(x)
    else:
        current_user.carpools.remove(x)
        x.available_seats += 1
    db.session.commit()
    return redirect(url_for('views.home'))


@views.route('/contact')
def con():
    return render_template('contact.html', user=current_user)


@views.route('/about')
def ab():
    return render_template('about.html', user=current_user)


@views.route('/moved<int:carpool_id>', methods=['POST', 'GET'])
@login_required
def moved(carpool_id):
    x = Carpool.query.get_or_404(carpool_id)
    if current_user.id == x.owner_id:
        db.session.delete(x)
        db.session.commit()
    else:
        flash('only driver can declare start of trip', 'error')
    return redirect(url_for('views.home'))


@views.route('/chat/<room>')
@login_required
def chat(room):
    return render_template('chat.html', room=room, username=current_user.first_name)    
@views.route('/points')
@login_required
def user_points():
    
    user = current_user  
    user_points = user.points    
    user_name = user.first_name 
  
    return render_template('points.html'  , user_points=user_points  , user_name = user.first_name  )  
@views.route('/emer')     
def show():  
    return  render_template('emer.html')

