# Import required modules
from flask import Blueprint, render_template
from . import mongo
from flask_pymongo import pymongo
from flask import current_app as app

# Define main blueprint
main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates', static_folder='static')

# Homepage route
@main_bp.route('/', methods=['GET'])
def home():
    # Fetch entries from database
    movies = mongo.db.movie.find()
    tvshows = mongo.db.series.find()

    return render_template('index.html', title="Home", movies=movies.sort('votes', pymongo.DESCENDING).limit(3), tvshows=tvshows.sort('votes', pymongo.DESCENDING).limit(3))

# Error handler for entire app if page not found
@main_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404'), 404
