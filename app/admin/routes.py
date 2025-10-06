from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..data import flights
from ..routes import admin_required 

admin_bp = Blueprint('admin', __name__, template_folder='templates')

@admin_bp.route('/admin')
@admin_required
def admin_home():
    return render_template('admin/flights.html', flights=flights)

@admin_bp.route('/admin/add_flight', methods=['POST'])
@admin_required

def add_flight():
    flight_id = request.form.get('flight_id')
    origin = request.form.get('origin')
    destination = request.form.get('destination')
    departure_time = request.form.get('departure_time')
    arrival_time = request.form.get('arrival_time')
    price = request.form.get('price')
    available_seats = request.form.get('available_seats')

    if not all([flight_id, origin, destination, departure_time, arrival_time, price, available_seats]):
        flash('All fields are required!', 'danger')
        return redirect(url_for('admin.admin_home'))
    if flight_id in flights:
        flash('Flight ID already exists!', 'danger')
        return redirect(url_for('admin.admin_home'))
    else:
        flights[flight_id] = {
            'origin': origin,
            'destination': destination,
            'departure_time': departure_time,
            'arrival_time': arrival_time,
            'price': float(price),
            'available_seats': int(available_seats)
        }
        flash('Flight added successfully!', 'success')

    return redirect(url_for('admin.admin_home'))   

@admin_bp.route('/admin/delete_flight/<flight_id>')
@admin_required
def delete_flight(flight_id):
    if flight_id in flights:
        del flights[flight_id]
        flash('Flight deleted successfully!', 'success')
    else:
        flash('Flight not found!', 'danger')
    return redirect(url_for('admin.admin_home'))

@admin_bp.route('/admin/users')
@admin_required
def admin_users():
    return render_template('admin/users.html')

