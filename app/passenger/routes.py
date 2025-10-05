from flask import Blueprint, render_template

passenger_bp = Blueprint('passenger', __name__, template_folder='templates')

@passenger_bp.route('/passenger')
def passenger_home():
    return render_template('passenger/home.html')

@passenger_bp.route('/passenger/profile')
def passenger_profile():
    return render_template('passenger/profile.html')

@passenger_bp.route('/passenger/myflights')
def passenger_cart():
    return render_template('passenger/myflights.html')