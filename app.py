from flask import Flask, render_template
from pymongo import MongoClient

# Configure app - Static folder is where images and javascript live
app = Flask(__name__, static_folder='static', static_url_path='')
app.config.from_pyfile('cfg.py')

# Connect to Mongo
client = MongoClient(app.config.get("CONNECTION_STRING"))
db = client.hackathon
print(client.list_database_names())
print(client.server_info())


@app.route('/')
def home():
    return render_template("index.html", number=7)

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
