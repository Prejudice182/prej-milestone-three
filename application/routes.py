# Import required modules
from flask import Blueprint, render_template, abort, request, send_from_directory
import os
from . import mongo
from flask_pymongo import pymongo
from flask import current_app as app

# Define main blueprint
main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates', static_folder='static')

favs = mongo.db.favourites

# Homepage route
@main_bp.route('/', methods=['GET'])
def home():
    # Fetch entries from database
    movies = favs.find({'Type': 'movie'}).sort(
        'Votes', pymongo.DESCENDING).limit(3)
    tvshows = favs.find({'Type': 'series'}).sort(
        'Votes', pymongo.DESCENDING).limit(3)

    return render_template('index.html', title="Home", movies=movies, tvshows=tvshows)

# View all entries route, with type sent in URL
@main_bp.route('/view-all/<entry_type>', methods=['GET'])
def view_all(entry_type):
    # Get correct collection name for database
    if entry_type == 'movies':
        db_type = entry_type[:-1]
        title = 'Movies'
    elif entry_type == 'tvshows':
        db_type = 'series'
        title = 'TV Shows'
    else:
        # If someone trys a malformed URL, send to 404 page
        abort(404)

    # Get skip argument from URL
    if request.args.get('skip') is not None:
        # Change skip from str to int if its a number, else 0
        skip = int(request.args.get('skip')) if request.args.get(
            'skip').isnumeric() else 0
        # Check if skip has been set to negative by malicious actor
        skip = 0 if skip < 0 else skip
    else:
        skip = 0

    # Retrieve entries from database
    entries_count = favs.count_documents({'Type': db_type}, skip=skip)
    entries = favs.find({'Type': db_type}).sort(
        'Votes', pymongo.DESCENDING).skip(skip).limit(6)
    return render_template('view-all.html', title=title, entries=entries, entry_type=entry_type, entries_count=entries_count, skip=skip)

# Error handler for entire app if page not found
@main_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404'), 404


@main_bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/images'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
