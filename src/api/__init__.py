# -*- coding: utf-8 -*-


from flask_mongoengine import MongoEngine

from src import appfactory


def create_api_app():

    app = appfactory.create_app('api')
    return app


api_app = create_api_app()

with api_app.app_context():
    db = MongoEngine(api_app)


# Ensure models are loaded
# According to flask, these sort of circular imports are valid:
# http://flask.pocoo.org/docs/0.10/patterns/packages/
from .model import post