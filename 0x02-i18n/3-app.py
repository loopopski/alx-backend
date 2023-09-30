#!/usr/bin/env python3
"""This script starts a Flask web application"""
from flask import Flask, render_template, request
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app)


class Config(object):
    """The Languages Config class"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """The get_locale function"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


# babel = Babel(app, locale_selector=get_locale)

@app.route('/', strict_slashes=False)
def hello_world():
    """This function executes when the 0.0.0.0:5000/ is requested"""
    return render_template('3-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
