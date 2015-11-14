# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template, jsonify, send_from_directory
from src.api.model.post import Post

bp = Blueprint(
    'home',
    __name__
)


@bp.route('/', methods=['GET'])
def home(_request=request):
    posts = Post.objects[max(0, len(Post.objects) - 100): max(1, len(Post.objects))]
    posts = reversed(posts)
    return render_template('home.html', posts=posts)


@bp.route('/healthcheck')
def healthcheck(_request=request):
    return jsonify(result={'status': 'ok'})


@bp.route('/styleguide')
def styleguide(_request=request):
    return render_template('styleguide.html')

@bp.route('/robots.txt')
def robots(_request=request):
    import os
    template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    return send_from_directory(template_dir, 'robots.txt')

@bp.errorhandler(404)
def page_not_found(*args, **kwargs):
    return render_template('404.html'), 404

