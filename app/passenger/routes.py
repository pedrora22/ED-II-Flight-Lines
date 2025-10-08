from flask import Blueprint, render_template, flash
from ..data import flights
from ..routes import login_required

passenger_bp = Blueprint('passenger', __name__, template_folder='templates')

@passenger_bp.route('/passenger')
@login_required
def passenger_home():
    return render_template('passenger/pHome.html', flights=flights)

@passenger_bp.route('/passenger/profile')
@login_required
def profile():
    return render_template('passenger/profile.html')

@passenger_bp.route('/passenger/book_flight/<flight_id>')
@login_required
def book_flight(flight_id):
    if flight_id in flights and flights[flight_id]['available_seats'] > 0:
        flights[flight_id]['available_seats'] -= 1
        flash('Flight booked successfully!', 'success')
    else:
        flash('Flight not found or no available seats!', 'danger')
    return render_template('passenger/pHome.html', flights=flights)