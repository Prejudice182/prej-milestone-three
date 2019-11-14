from flask import redirect, render_template, flash, Blueprint, request, url_for
from flask import current_app as app
import requests
import os
from .forms import EntryForm
from . import mongo


favs_bp = Blueprint('favs_bp', __name__,
                    template_folder='templates', static_folder='static')


@favs_bp.route('/add-favourite', methods=['GET', 'POST'])
def add_favourite():
    entry_form = EntryForm()
    if entry_form.validate_on_submit():
        if not mongo.db[request.form.get('entry_type')].count_documents({'title': request.form.get('entry_name')}, limit=1):
            OMDB_KEY = os.getenv('OMDB_KEY')
            url = f'http://www.omdbapi.com/?apikey={OMDB_KEY}&t={request.form["entry_name"]}&type={request.form["entry_type"]}'
            entry_details = requests.get(url).json()
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
