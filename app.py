from flask import Flask, render_template

# Configure app - Static folder is where images and javascript live
app = Flask(__name__, static_folder='public', static_url_path='')
# app.config.from_pyfile('cfg.py')


@app.route('/')
def home():
    return render_template("index.html", number=7)
