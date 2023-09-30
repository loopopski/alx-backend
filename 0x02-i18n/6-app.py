#!/usr/bin/env python3
"""This script starts a Flask web application"""
from flask import Flask, render_template, request, g
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config(object):
    """The Languages Config class"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)


def get_user():
    """The get_user function"""
    user = request.args.get('login_as')
    if user and int(user) in users.keys():
        return users.get(int(user))
    return None


@app.before_request
def before_request():
    """The before_request function"""
    user = get_user()
    if user:
        g.user = user


@babel.localeselector
def get_locale():
    """The get_locale function"""
    langQuery = request.args.get('locale')
    user = getattr(g, 'user', None)
    if user:
        langUser = user.get('locale')
    else:
        langUser = None
    langHeader = request.headers.get('locale')

    if langQuery:
        lang = langQuery
    elif langUser:
        lang = langUser
    elif langHeader:
        lang = langHeader
    else:
        return request.accept_languages.best_match(app.config['LANGUAGES'])
    if lang in app.config['LANGUAGES']:
        return lang


# babel = Babel(app, locale_selector=get_locale)


@app.route('/', strict_slashes=False)
def hello_world():
    """This function executes when the 0.0.0.0:5000/ is requested"""
    user = getattr(g, 'user', None)
    if user:
        username = user.get('name')
    else:
        username = None
    return render_template('5-index.html', username=username)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
