from flask import Flask, render_template, request

from page_analyzer import db
from page_analyzer.environ import env
from page_analyzer import filters


def create_app() -> Flask:
    env.read_env()
    app = Flask(__name__)
    filters.setup(app)
    db.connection.setup(app)
    return app


app = create_app()


@app.route("/")
def main():
    return render_template('main.html')


@app.route("/urls", methods=['GET', 'POST'])
def urls():
    if request.method == 'GET':
        return render_template('urls.html')
    url_name = request.form['url']
    url = db.entities.url.create(url_name)
    return render_template('url.html', url=url)


@app.get("/urls/<int:url_id>", endpoint='url')
def url(url_id):
    url = db.entities.url.get_by_id(url_id)
    return render_template('url.html', url=url)
