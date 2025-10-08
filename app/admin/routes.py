from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from ..data import flights, save_user_data, find_user_by_email, delete_user_data, get_all_users
from ..routes import admin_required 

admin_bp = Blueprint('admin', __name__, template_folder='templates')

@admin_bp.route('/')
@admin_required
def admin_home():
    return render_template('admin/flights.html', flights=flights)

@admin_bp.route('/add_flight', methods=['POST', 'GET'])
@admin_required

def add_flight():
    flight_id = request.form.get('flight_id')
    origin = request.form.get('origin')
    destination = request.form.get('destination')
    airline_miles = request.form.get('airline_miles')
    plane_model = request.form.get('plane_model')
    price = request.form.get('price')
    available_seats = request.form.get('available_seats')

    if not all([flight_id, origin, destination, airline_miles, plane_model, price, available_seats]):
        flash('All fields are required!', 'danger')
        return redirect(url_for('admin.admin_home'))
    if flight_id in flights:
        flash('Flight ID already exists!', 'danger')
        return redirect(url_for('admin.admin_home'))
    else:
        flights[flight_id] = {
            'origin': origin,
            'destination': destination,
            'airline_miles': airline_miles,
            'plane_model': plane_model,
            'price': float(price),
            'available_seats': int(available_seats)
        }
        flash('Flight added successfully!', 'success')

    return redirect(url_for('admin.admin_home'))   

@admin_bp.route('/delete_flight/<flight_id>')
@admin_required
def delete_flight(flight_id):
    if flight_id in flights:
        del flights[flight_id]
        flash('Flight deleted successfully!', 'success')
    else:
        flash('Flight not found!', 'danger')
    return redirect(url_for('admin.admin_home'))

@admin_bp.route('/users')
@admin_required
def admin_users():
    users = get_all_users()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/add_user', methods=['POST'])
@admin_required
def add_user():
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')
    if not all([email, password, role]):
        flash('All fields are required.', 'danger')
        return redirect(url_for('admin.admin_users'))
    if find_user_by_email(email):
        flash(f'User with email {email} already exists.', 'danger')
    else:
        save_user_data(email, password, role)
        flash(f'User {email} added successfully.', 'success')
    return redirect(url_for('admin.admin_users'))

@admin_bp.route('/delete_user/<email>')
@admin_required
def delete_user(email):
    if session.get('user') == email:
        flash('You cannot delete your own account.', 'danger')
    elif not find_user_by_email(email):
        flash(f'User {email} not found.', 'danger')
    else:
        delete_user_data(email)
        flash(f'User {email} deleted successfully.', 'success')
    
    return redirect(url_for('admin.admin_users'))

    
