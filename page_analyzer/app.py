from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def render_main_page():
    return render_template('base.html')
