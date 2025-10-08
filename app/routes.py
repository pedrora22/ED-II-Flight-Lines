from flask import Flask, render_template, Blueprint, session, redirect, url_for, flash, request
from functools import wraps
from .data import find_user_by_email


app = Flask(__name__)

bp = Blueprint('main', __name__, template_folder='templates')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'warning')
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'warning')
            return redirect(url_for('main.login'))
        if session.get('role') != 'admin':
            flash('Acesso restrito a administradores.', 'danger')
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_data = find_user_by_email(email)
        if user_data and user_data['password'] == password:
            session['user'] = email
            session['role'] = user_data['role']
            flash('Login successful!', 'success')
            if user_data['role'] == 'admin':
                return redirect(url_for('admin.admin_home'))
            else:
                return redirect(url_for('passenger.passenger_home'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')
