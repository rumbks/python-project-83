from flask import Flask, render_template, request, redirect, url_for

from page_analyzer import db
from page_analyzer.environ import env
from page_analyzer import flash
from page_analyzer import filters
from page_analyzer.url import is_valid as is_valid_url, normalize


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
        urls = db.entities.url.get_all()
        return render_template('urls.html', urls=urls)
    url_name = request.form['url']
    if not is_valid_url(url_name):
        flash.error('Некорректный URL')
        return render_template('main.html', url_name=url_name)

    url_name = normalize(url_name)
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
