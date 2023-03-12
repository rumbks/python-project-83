from flask import Flask, render_template, request, redirect, url_for
import requests

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
    url_ = db.entities.url.get_by_id(url_id)
    url_checks = db.entities.url_check.get_all_for_url(url_.id)
    return render_template('url.html', url=url_, url_checks=url_checks)


@app.post("/urls/<int:url_id>/checks", endpoint='check_url')
def check_url(url_id):
    url = db.entities.url.get_by_id(url_id)
    try:
        response = requests.get(url.name)
        response.raise_for_status()
    except requests.RequestException:
        flash.error('Произошла ошибка при проверке')
        return redirect(url_for('url', url_id=url_id))

    status_code = requests.get(url.name).status_code
    db.entities.url_check.create_for_url(url_id, status_code=status_code)
    flash.success('Страница успешно проверена')
    return redirect(url_for('url', url_id=url_id))


