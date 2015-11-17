# -*- coding: utf-8 -*-
from collections import OrderedDict

from flask import Blueprint, request, render_template, jsonify, send_from_directory
from src.api.model.post import Post

bp = Blueprint(
    'home',
    __name__
)


@bp.route('/', methods=['GET'])
def home(_request=request):

    content_count = 3
    featured_tags = ['stocking-stuffer', 'rush', 'gadgets', 'star wars', 'foodie', 'him', 'her']
    featured_posts = OrderedDict()

    for tag in featured_tags:
        posts = Post.objects(tags=tag)
        featured_posts[tag] = posts[max(0, len(posts) - content_count):len(posts)]

    all_tags = Post.objects.distinct('tags')
    return render_template('home.html', featured_posts=featured_posts, all_tags=all_tags)


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

