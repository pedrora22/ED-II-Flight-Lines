from flask import Flask
from .data import load_users_into_btree

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.secret_key = 'supersecretkey1234'

    with app.app_context():
        # Import parts of our application
        from . import routes
        from .admin import routes as admin_routes
        from .passenger import routes as passenger_routes

        load_users_into_btree()
        # Register Blueprints
        app.register_blueprint(routes.bp, url_prefix='/')
        app.register_blueprint(admin_routes.admin_bp, url_prefix='/admin')
        app.register_blueprint(passenger_routes.passenger_bp, url_prefix='/passenger')

    return app