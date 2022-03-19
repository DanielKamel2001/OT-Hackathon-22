from flask import Flask, render_template
from pymongo import MongoClient

# Configure app - Static folder is where images and javascript live
app = Flask(__name__, static_folder='static', static_url_path='')
app.config.from_pyfile('cfg.py')

# Connect to Mongo
client = MongoClient(app.config.get("CONNECTION_STRING"))
db = client.get_database("hackathon")
print(db.list_collection_names())


@app.route('/')
def home():
    # Get the items from the db
    items = []
    for document in db.get_collection("items").find({}):
        print(document)
        items.append(document)
    return render_template("index.html", number=7, items=items)


@app.route('/shop')
def shop():
    return render_template("shop.html")


@app.route('/checkout')
def checkout():
    return render_template("checkout.html")


@app.route('/bag')
def bag():
    return render_template("bag.html")


@app.route('/about')
def about():
    return render_template("about.html")
