from flask import Blueprint, render_template
from ..data import flights
from ..routes import login_required

passenger_bp = Blueprint('passenger', __name__, template_folder='templates')

@passenger_bp.route('/passenger')
@login_required
def passenger_home():
    return render_template('passenger/home.html', flights=flights.values())

@passenger_bp.route('/passenger/profile')
@login_required
def passenger_profile():
    return render_template('passenger/profile.html')

@passenger_bp.route('/passenger/myflights')
@login_required
def passenger_cart():
    return render_template('passenger/myflights.html')