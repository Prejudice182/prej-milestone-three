# Import required modules
from flask import redirect, render_template, flash, Blueprint, request, url_for, abort
from bson.objectid import ObjectId
import requests
import os
from .forms import EntryForm, EditForm
from .youtube import youtube_search
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
        try:
            # Check if title with this name already exists, flash message if it does
            if not favs.count_documents({'Title': entry_details["Title"]}, limit=1):
                trailer = youtube_search(entry_details["Title"] + ' trailer')
                entry_details.update({'Reason': request.form.get(
                    'reason'), 'AddedBy': request.form.get('username'), 'Votes': 1, 'Trailer': trailer})

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
                return redirect(url_for('favs_bp.add_favourite'))
        except:
            flash('No listing with that title found, please try again!')
            
    return render_template('add-fav.html', title='Add Favourite', form=entry_form)


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
            return redirect(url_for('main_bp.view_all', entry_type=entry_type))
        return render_template('edit-fav.html', title='Edit Favourite', entry=entry, form=edit_form)
    else:
        abort(404)


@favs_bp.route('/delete-fav/<entry_id>', methods=['POST'])
def delete_fav(entry_id):
    entry = favs.find_one({'_id': ObjectId(entry_id)}, {'Type': 1})
    if entry is not None:
        try:
            favs.delete_one({'_id': ObjectId(entry_id)})
        except:
            flash('Something went wrong! Please try again.')
        else:
            flash('Favourite deleted!')
    else:
        flash('No record with that ID found!')
    return redirect(request.referrer or url_for('main_bp.home'))


@favs_bp.route('/view-fav/<entry_id>', methods=['GET'])
def view_fav(entry_id):
    req_fields = {'_id': 1, 'Title': 1, 'Rated': 1, 'Released': 1, 'Runtime': 1, 'Genre': 1, 'Director': 1, 'Actors': 1,
                  'Plot': 1, 'Poster': 1, 'imdbRating': 1, 'imdbID': 1, 'Reason': 1, 'AddedBy': 1, 'Votes': 1, 'Type': 1, 'Trailer': 1}
    entry = favs.find_one({'_id': ObjectId(entry_id)}, req_fields)
    if entry is not None:
        entry_type = 'movies' if entry['Type'] == 'movie' else 'tvshows'
        return render_template('view-fav.html', title='View Favourite', entry=entry, entry_type=entry_type)
    else:
        abort(404)


@favs_bp.route('/vote-<direction>/<entry_id>', methods=['GET'])
def vote(direction, entry_id):
    entry = favs.find_one({'_id': ObjectId(entry_id)}, {'Votes': 1})
    if entry is not None:
        if direction == 'up':
            votes = entry['Votes'] + 1
        elif direction == 'down':
            votes = entry['Votes'] - 1
        else:
            abort(404)
        try:
            favs.update_one({'_id': ObjectId(entry_id)}, {
                '$set': {
                    'Votes': votes
                }
            })
        except:
            flash('Something is wrong with the database. Please try again!')
        else:
            flash('Thank you for voting!')
        return redirect(request.referrer)
    else:
        abort(404)
