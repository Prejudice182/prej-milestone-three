from flask import Flask
from flask_pymongo import PyMongo
from flask_session import Session

mongo = PyMongo()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    mongo.init_app(app)

    with app.app_context():
        from . import routes
        from . import favs

        app.register_blueprint(routes.main_bp)
        app.register_blueprint(favs.favs_bp)

        return app
