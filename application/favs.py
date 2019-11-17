# Import required modules
from flask import redirect, render_template, flash, Blueprint, request, url_for, abort
from bson.objectid import ObjectId
import requests
import os
from .forms import EntryForm, EditForm
from . import mongo

# Define favs blueprint
favs_bp = Blueprint('favs_bp', __name__,
                    template_folder='templates', static_folder='static')

# Define favs for ease of access
favs = mongo.db.favourites

# Add Favourite route
@favs_bp.route('/add-favourite', methods=['GET', 'POST'])
def add_favourite():
    # Create form with EntryForm class
    entry_form = EntryForm()

    # Flask-WTF provides wrapper for method=POST AND validate()
    if entry_form.validate_on_submit():
        # Get details for this entry from OMDB API: http://www.omdbapi.com/
        OMDB_KEY = os.getenv('OMDB_KEY')
        url = f'http://www.omdbapi.com/?apikey={OMDB_KEY}&t={request.form["entry_name"]}&type={request.form["entry_type"]}'
        entry_details = requests.get(url).json()

        # Check if title with this name already exists, flash message if it does
        if not favs.count_documents({'Title': entry_details["Title"]}, limit=1):
            entry_details.update({'Reason': request.form.get(
                'reason'), 'AddedBy': request.form.get('username'), 'Votes': 1})

            # Try insert to DB, flash error message on fail, flash and redirect on success
            try:
                favs.insert_one(entry_details)
            except:
                flash('Something went wrong! Please try again')
            else:
                flash("Favourite saved!")
                return redirect(url_for('main_bp.home'))
        else:
            flash('Someone already added that one!')
    return render_template('add-fav.html', title='Add Favourite', form=entry_form)


# View all entries route, with type sent in URL
@favs_bp.route('/view-all/<entry_type>', methods=['GET'])
def view_all(entry_type):
    # Get correct collection name for database
    if entry_type == 'movies':
        entry_type = entry_type[:-1]
        title = 'Movies'
    elif entry_type == 'tvshows':
        entry_type = 'series'
        title = 'TV Shows'
    else:
        # If someone trys a malformed URL, send to 404 page
        abort(404)

    # Retrieve entries from database
    entries = favs.find({'Type': entry_type})

    return render_template('view-all.html', title=title, entries=entries)


@favs_bp.route('/edit-fav/<entry_id>', methods=['GET', 'POST'])
def edit_fav(entry_id):
    entry = favs.find_one({'_id': ObjectId(entry_id)},
                          {'Type': 1, 'Reason': 1, 'AddedBy': 1})
    if entry is not None:
        entry_type = 'movies' if entry['Type'] == 'movie' else 'tvshows'
        edit_form = EditForm()
        if edit_form.validate_on_submit():
            try:
                favs.update_one({'_id': ObjectId(entry_id)}, {
                    '$set': {
                        'AddedBy': request.form.get('username'),
                        'Reason': request.form.get('reason')
                    }
                })
            except:
                flash('Something went wrong! Please try again.')
            else:
                flash('Favourite updated!')
                return redirect(url_for('favs_bp.view_all', entry_type=entry_type))
        return render_template('edit-fav.html', title='Edit Favourite', entry=entry, form=edit_form)
    else:
        abort(404)


@favs_bp.route('/delete-fav/<entry_id>', methods=['POST'])
def delete_fav(entry_id):
    entry = favs.find_one({'_id': ObjectId(entry_id)}, {'Type': 1})
    if entry is not None:
        entry_type = 'movies' if entry['Type'] == 'movie' else 'tvshows'
        try:
            favs.delete_one({'_id': ObjectId(entry_id)})
        except:
            flash('Something went wrong! Please try again.')
        else:
            flash('Favourite deleted!')
            return redirect(url_for('favs_bp.view_all', entry_type=entry_type))
    else:
        flash('Something went wrong! Please try again.')
