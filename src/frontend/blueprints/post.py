# -*- coding: utf-8 -*-
import random
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

    related_tag = random.choice(pst.tags)
    related_posts = Post.objects(tags=related_tag, id__ne=pst.id)[0:6]
    related_posts = related_posts if len(related_posts) >= 3 else []
    title = '{} - Last Minute Gifts'.format(pst.title.capitalize())
    print related_posts
    return render_template('post.html', post=pst, title=title, related_tag=related_tag, related_posts=related_posts)


@bp.route('/gifts/<tag>', methods=['GET'])
def gifts(tag, _request=request):
    posts = Post.objects(tags=tag)
    title = 'Last Minute {} Gifts for {}'.format(tag.capitalize(), date.today().year)
    h1 = '{} Gift Guide'.format(tag.title())
    return render_template('gallery.html', posts=posts, tag=tag, title=title, h1=h1)