# -*- coding: utf-8 -*-
from datetime import date

from flask import Blueprint, request, render_template
from src.api.model.post import Post

from src.frontend.blueprints import base
from src.frontend.blueprints.base import bp

bp = Blueprint(
    'post',
    __name__
)


@bp.route('/gift/<slug>', methods=['GET'])
def post(slug, _request=request):

    try:
        pst = Post.objects(slug=slug)[0]
    except IndexError:
        return base.page_not_found()

    title = '{} - Last Minute Gifts'.format(pst.title.capitalize())
    return render_template('post.html', post=pst, title=title)


@bp.route('/gifts/<tag>', methods=['GET'])
def gifts(tag, _request=request):
    posts = Post.objects(tags=tag)
    title = 'Last Minute {} Gifts for {}'.format(tag.capitalize(), date.today().year)
    h1 = '{} Gift Guide'.format(tag.title())
    return render_template('gallery.html', posts=posts, tag=tag, title=title, h1=h1)