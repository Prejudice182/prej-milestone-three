# Import required modules
from flask import Flask
from flask_pymongo import PyMongo
from flask_session import Session
from dotenv import load_dotenv

# Define global database object
mongo = PyMongo()

# Load environment variables from file
load_dotenv()

def create_app():
    ''' Initialize core application '''
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    mongo.init_app(app)

    with app.app_context():
        # Import all routes
        from . import routes, favs

        # Register blueprints from routes
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(favs.favs_bp)

        return app
