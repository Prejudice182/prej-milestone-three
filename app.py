from flask import Flask, render_template, redirect, request, url_for, flash, jsonify
from flask_pymongo import PyMongo
from forms import ListingsForm
import os
import requests
import requests_cache

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "cinema_db"
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "thisismysecretkey")


mongo = PyMongo(app)

requests_cache.install_cache(
    'requests-cache', backend='mongodb', expire_after=85600, connection=mongo.cx)
OMDB_KEY = os.getenv("OMDB_KEY")


@app.route("/")
@app.route("/index")
def home():
    raw_listings = mongo.db.listings.find({}, {'_id': 0, 'film_name': 1})
    listings = []
    for raw_listing in raw_listings:
        listing = {}
        listing['film_name'] = raw_listing['film_name']
        url = f'http://www.omdbapi.com/?apikey={OMDB_KEY}&t={listing["film_name"]}'
        r = requests.get(url).json()
        listing['poster'] = r['Poster']
        listings.append(listing)
    return render_template("index.html", title="Listings", listings=listings)


@app.route("/now-showing")
def now_showing():
    return render_template("now-showing.html", title="Now Showing")


@app.route("/coming-soon")
def coming_soon():
    return render_template("coming-soon.html", title="Coming Soon")


@app.route("/create-listings", methods=['GET', 'POST'])
def create_listings():
    listings_form = ListingsForm(request.form)
    if request.method == 'POST':
        if listings_form.validate():
            data = request.form.to_dict()
            try:
                mongo.db.listings.insert_one(data)
            except Exception as e:
                flash(str(e))
            flash("Listing added.")
            return redirect(url_for('home'))
    return render_template("create-listings.html", form=listings_form, title="Create Listings")


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
