from flask import Flask, render_template, url_for

# Configure app - Static folder is where images and javascript live
app = Flask(__name__, static_folder='public', static_url_path='')
# app.config.from_pyfile('cfg.py')


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
