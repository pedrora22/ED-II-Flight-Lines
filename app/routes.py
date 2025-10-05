from flask import Flask, render_template, Blueprint, session, redirect, url_for, flash, request
from functools import wraps


app = Flask(__name__)

bp = Blueprint('main', __name__, template_folder='templates')

CLIENTS = {
    'cliente1@gmail.com': '123456',
    'cliente2@gmail.com': '123456',
}

ADMINS = {
    'funcionario1@gmail.com': '123456',
    'funcionario2@gmail.com': '123456'
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'warning')
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in CLIENTS and CLIENTS[email] == password:
            session['user'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('passenger.passenger_home'))
        if email in ADMINS and ADMINS[email] == password:
            session['user'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('admin.admin_home'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('main.login'))

    return render_template('login.html')

