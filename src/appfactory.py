# -*- coding: utf-8 -*-

import pkgutil

from flask import Flask, Blueprint


def _register_blueprints(app, blueprints):
    """Register all Blueprint instances on the specified Flask application found
    in all modules for the specified package.

    :param app: the Flask application
    """
    rv = []

    for importer, name, _ in pkgutil.iter_modules(blueprints.__path__):
        m = importer.find_module(name).load_module(name)
        for attr in dir(m):
            item = getattr(m, attr)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
                rv.append(item)
    return rv


def create_app(package_name, blueprints=None, **kwargs):
    """Returns a :class:`Flask` application instance configured with common
    functionality for the Overholt platform.

    :param package_name: application package name
    :param blueprints: blueprint module
    """
    app = Flask(package_name, instance_relative_config=True, **kwargs)

    if blueprints:
        _register_blueprints(app, blueprints)

    return app