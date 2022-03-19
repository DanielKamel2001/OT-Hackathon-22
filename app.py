from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from pymongo import MongoClient

# Configure app - Static folder is where images and javascript live
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config.from_pyfile('cfg.py')

# Configure sessions for keeping track of user data
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = 'flask_session_files'
Session(app)

# Connect to Mongo
client = MongoClient(app.config.get("CONNECTION_STRING"))
db = client.get_database("hackathon")
print(db.list_collection_names())


@app.route('/', methods=['POST', 'GET'])
def home():
    # Get the items from the db
    items = []
    for document in db.get_collection("items").find({}):
        items.append(document)
    return render_template("index.html", number=7, items=items)


@app.route('/addToCart', methods=['POST'])
def add_to_cart():
    item_id = request.form.get("cartItem")

    # Check if cart has been created
    if "cart" in session:
        # Check if item exists in cart
        if item_id in session["cart"]:
            session["cart"][item_id] += 1
        else:
            session["cart"][item_id] = 1
    else:
        # Create a new cart
        session["cart"] = {item_id: 1}

    # Redirect back to shop page with 302 status
    return redirect(url_for('shop'), code=303)


@app.route('/shop')
def shop():
    items = []
    for document in db.get_collection("items").find({}):
        # print(document)
        items.append(document)
    return render_template("shop.html", items=items)


@app.route('/itemPage')
def itemPage():
    return render_template("itemPage.html")


@app.route('/checkout')
def checkout():
    return render_template("checkout.html")


@app.route('/bag')
def bag():
    return render_template("bag.html")


@app.route('/about')
def about():
    return render_template("about.html")
