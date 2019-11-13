from flask import Flask, render_template, redirect, request, url_for, flash, jsonify
from flask_pymongo import PyMongo, pymongo
from forms import EntryForm
import os
import requests
import requests_cache

app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
app.config['MONGO_DBNAME'] = os.getenv('MONGO_DB')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


mongo = PyMongo(app)

requests_cache.install_cache(
    'requests-cache', backend='mongodb', expire_after=85600, connection=mongo.cx)
OMDB_KEY = os.getenv('OMDB_KEY')


@app.route('/')
@app.route('/index')
def home():
    movies = mongo.db.movie.find()
    tvshows = mongo.db.series.find()
    return render_template('index.html', title='Home', movies=movies.sort('votes', pymongo.DESCENDING).limit(3), tvshows=tvshows.sort('votes', pymongo.DESCENDING).limit(3))


@app.route('/add-favourite', methods=['GET', 'POST'])
def add_favourite():
    entry_form = EntryForm()
    if entry_form.validate_on_submit():
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
            return redirect(url_for('home'))
    return render_template('add-favourite.html', title='Add Favourite', form=entry_form)


if __name__ == '__main__':
    app.run(host=os.getenv('IP'),
            port=int(os.getenv('PORT')),
            debug=True)
