import os
from flask import Flask, render_template, redirect, request, url_for, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "cinema_db"
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost")

mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def home():
    return render_template("index.html", title="Listings")


@app.route("/now-showing")
def now_showing():
    return render_template("now-showing.html", title="Now Showing")


@app.route("/coming-soon")
def coming_soon():
    return render_template("coming-soon.html", title="Coming Soon")


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
