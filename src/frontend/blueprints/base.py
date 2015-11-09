# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, jsonify, send_from_directory
from src.api.model.post import Post

bp = Blueprint(
    'home',
    __name__
)


@bp.route('/', methods=['GET'])
def home(_request=request):
    posts = Post.objects[:100]
    return render_template('home.html', posts=posts)


@bp.route('/gifts/<tag>', methods=['GET'])
def gifts(tag, _request=request):
    posts = Post.objects(tags=tag)
    return render_template('home.html', posts=posts, tag=tag)


@bp.route('/healthcheck')
def healthcheck(_request=request):
    return jsonify(result={'status': 'ok'})


@bp.route('/styleguide')
def styleguid(_request=request):
    return render_template('styleguide.html')


@bp.errorhandler(404)
def page_not_found(*args, **kwargs):
    return render_template('404.html'), 404


# TODO: don't serve static files from flask; use nginx or something
import os

@bp.route('/fonts/<path:path>')
def static_fonts(path):
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'static', 'fonts'), path)
