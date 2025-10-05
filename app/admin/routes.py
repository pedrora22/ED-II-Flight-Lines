from flask import Blueprint, render_template

admin_bp = Blueprint('admin', __name__, template_folder='templates')

@admin_bp.route('/admin')
def admin_home():
    return render_template('admin/home.html')

@admin_bp.route('/admin/flights')
def admin_flights():
    return render_template('admin/flights.html')

@admin_bp.route('/admin/bookings')
def admin_bookings():
    return render_template('admin/bookings.html')

@admin_bp.route('/admin/users')
def admin_users():
    return render_template('admin/users.html')

