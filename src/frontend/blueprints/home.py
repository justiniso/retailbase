# -*- coding: utf-8 -*-
from collections import OrderedDict

from flask import Blueprint, request, render_template
from src.api.model.post import Post


bp = Blueprint(
    'home',
    __name__
)

@bp.route('/', methods=['GET'])
def home(_request=request):

    content_count = 3
    featured_tags = ['gadgets', 'stocking-stuffer', 'rush', 'star wars', 'foodie', 'her', 'him',
                     'alcohol', 'photographer', 'kids', 'hipster', 'coworker']
    featured_posts = OrderedDict()

    for tag in featured_tags:
        posts = Post.objects(tags=tag)
        featured_posts[tag] = posts[max(0, len(posts) - content_count):len(posts)]

    all_tags = Post.objects.distinct('tags')
    return render_template('home.html', featured_posts=featured_posts, all_tags=all_tags)