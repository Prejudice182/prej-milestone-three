from flask import Blueprint, render_template
from . import mongo
from flask_pymongo import pymongo
from flask import current_app as app

main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates', static_folder='static')


@main_bp.route('/', methods=['GET'])
def home():
    movies = mongo.db.movie.find()
    tvshows = mongo.db.series.find()
    return render_template('index.html', title="Home", movies=movies.sort('votes', pymongo.DESCENDING).limit(3), tvshows=tvshows.sort('votes', pymongo.DESCENDING).limit(3))
