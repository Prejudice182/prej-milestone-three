# Import required modules
from flask import redirect, render_template, flash, Blueprint, request, url_for, abort
from flask import current_app as app
import requests
import os
from .forms import EntryForm
from . import mongo

# Define favs blueprint
favs_bp = Blueprint('favs_bp', __name__,
                    template_folder='templates', static_folder='static')

# Add Favourite route
@favs_bp.route('/add-favourite', methods=['GET', 'POST'])
def add_favourite():
    # Create form with EntryForm class
    entry_form = EntryForm()

    # Flask-WTF provides wrapper for method=POST AND validate()
    if entry_form.validate_on_submit():
        # Check if title with this name already exists, flash message if it does
        if not mongo.db[request.form.get('entry_type')].count_documents({'title': request.form.get('entry_name')}, limit=1):
            # Get details for this entry from OMDB API: http://www.omdbapi.com/
            OMDB_KEY = os.getenv('OMDB_KEY')
            url = f'http://www.omdbapi.com/?apikey={OMDB_KEY}&t={request.form["entry_name"]}&type={request.form["entry_type"]}'
            entry_details = requests.get(url).json()

            # Try insert to DB, flash error message on fail, flash and redirect on success
            try:
                coll_name = mongo.db[request.form['entry_type']]
                coll_name.insert_one({
                    'title': entry_details['Title'],
                    'year': entry_details['Year'],
                    'release': entry_details['Released'],
                    'genres': entry_details['Genre'],
                    'plot': entry_details['Plot'],
                    'poster': entry_details['Poster'],
                    'imdbRating': entry_details['imdbRating'],
                    'reason': request.form['reason'],
                    'addedBy': request.form['username'],
                    'votes': 1
                })
            except:
                flash('Something went wrong! Please try again')
            else:
                flash("Favourite saved!")
                return redirect(url_for('main_bp.home'))
        else:
            flash('Someone already added that one!')
    return render_template('add-favourite.html', title='Add Favourite', form=entry_form)


# View all entries route, with type sent in URL
@favs_bp.route('/view-all/<entry_type>', methods=['GET'])
def view_all(entry_type):
    # Get correct collection name for database
    if entry_type == 'movies':
        coll_name = entry_type[:-1]
        title = entry_type.capitalize()
    elif entry_type == 'tvshows':
        coll_name = 'series'
        title = 'TV Shows'
    else:
        # If someone trys a malformed URL, send to 404 page
        abort(404)

    # Retrieve entries from database
    entries = mongo.db[coll_name].find()

    return render_template('view-all.html', title=title, entries=entries)
