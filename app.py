import random

from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from pymongo import MongoClient
# Imports for Amazon SES
import boto3
from botocore.exceptions import ClientError

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


def get_cart():
    # Get the items from the session and pull details from Mongo
    cart_list = []
    if "cart" in session:
        # Iterate over every item and check if the item is in the cart
        # Not very performant, but we aren't working at that kind of scale
        for document in db.get_collection("items").find({}):
            # The str wraps are very necessary don't ask
            if str(document["productID"]) in session["cart"]:
                # Add the cart quantity to the item and put it in the list
                document["quantity"] = session["cart"][str(document["productID"])]
                cart_list.append(document)
    return cart_list


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

    # Check if the sending page has specified where to return to
    referrer = request.form.get("referrer")
    if referrer:
        # Redirect back to referrer with 302 status
        return redirect(url_for(referrer), code=303)
    else:
        # Redirect back to shop page with 302 status
        return redirect(url_for('shop'), code=303)


@app.route('/shop')
def shop():
    items = []
    for document in db.get_collection("items").find({}):
        # print(document)
        items.append(document)

    sort = "pop"
    print(request.args)

    # See if user wants a specific sort
    if request.args.get("sorts"):
        sort = request.args.get("sorts")
        print("sorting by " + sort)
        if sort == "arr":
            # They arrived in this order trust me bro
            random.seed(5318008)
            random.shuffle(items)
        elif sort == "low":
            # Sort low to high
            items = sorted(items, key=lambda d: d['Price'])
        elif sort == "high":
            # Sort high to low
            items = sorted(items, key=lambda d: d['Price'] * -1)
    return render_template("shop.html", items=items, sort=sort)


@app.route('/item/<id>')
def item_detail(id):
    # Get the item details from Mongo
    # Dont feel like looking up the docs for find() so watch this
    item = {}
    for document in db.get_collection("items").find({}):
        if str(document["productID"]) == id:
            item = document
    if item["Size"] is None:
        item["Size"] = "One size/style", ""
    return render_template("itemPage.html", item=item)


@app.route('/checkout')
def checkout():
    return render_template("checkout.html", items=get_cart())


@app.route('/sendCheckout', methods=['POST'])
def send_checkout():
    email = request.form.get("email")
    if email and "cart" in session:
        # Send an email
        # Create a new SES resource and specify a region.
        aws_client = boto3.client('ses', region_name="us-east-1",
                                  aws_access_key_id=app.config['AWS_ID'],
                                  aws_secret_access_key=app.config['AWS_SECRET'],
                                  # aws_session_token=app.config['AWS_TOKEN']
                                  )
        SENDER = "goose@emily.engineer"
        # Try to send the email.
        try:
            # Provide the contents of the email.
            response = aws_client.send_email(
                Destination={
                    'ToAddresses': [
                        email,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': "UTF-8",
                            'Data': render_template("emailReceipt.html", items=get_cart()),
                        },
                        'Text': {
                            'Charset': "UTF-8",
                            'Data': "Hi! Your email doesn't support HTML",
                        },
                    },
                    'Subject': {
                        'Charset': "UTF-8",
                        'Data': "Hackathon project receipt",
                    },
                },
                Source=SENDER
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            return e.response['Error']['Message']
        else:
            # Clear the cart, we've bought it already
            session["cart"] = {}
            return render_template("checkoutConfirm.html")
    else:
        return "You have either no email or nothing in bag. Wyd even?"


@app.route('/deleteBag', methods=['POST'])
def delete_item():
    item_id = request.form.get("cartItem")
    if item_id in session["cart"]:
        del session["cart"][item_id]
    # Redirect back to bag
    return redirect(url_for('bag'), code=303)


@app.route('/bag')
def bag():
    return render_template("bag.html", items=get_cart())


@app.route('/about')
def about():
    return render_template("about.html")
