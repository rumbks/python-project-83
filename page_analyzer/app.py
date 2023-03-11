from flask import Flask, render_template, request

from page_analyzer import db
from page_analyzer.environ import env
from page_analyzer import flash
from page_analyzer import filters


def create_app() -> Flask:
    env.read_env()
    app = Flask(__name__)
    filters.setup(app)
    db.connection.setup(app)
    app.secret_key = env("SECRET_KEY")
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
    if (url := db.entities.url.get_by_name(url_name)) is not None:
        flash.info('Страница уже существует')
    else:
        url = db.entities.url.create(url_name)
        flash.success('Страница успешно добавлена')
    return render_template('url.html', url=url)


@app.get("/urls/<int:url_id>", endpoint='url')
def url(url_id):
    url = db.entities.url.get_by_id(url_id)
    return render_template('url.html', url=url)
