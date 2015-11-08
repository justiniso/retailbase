# -*- coding: utf-8 -*-
import datetime
import locale

from flask_restful import Resource, abort, Api, fields, marshal_with, reqparse
from mongoengine import ValidationError, queryset_manager

from . import Base
from src.api import api_app, db


class Post(Base, db.Document):

    __tablename__ = 'post'

    title = db.StringField(max_length=255, required=True)
    description = db.StringField(max_length=255)
    slug = db.StringField(max_length=255, required=True)
    link_url = db.StringField(max_length=2080, required=True)
    price = db.FloatField(min_value=0)
    thumbnail_url = db.StringField(max_length=2080)
    create_date = db.DateTimeField(default=datetime.datetime.now)
    publish_date = db.DateTimeField()
    delete_date = db.DateTimeField()

    @queryset_manager
    def objects(cls, queryset):
        """Default order of posts by descending date"""
        return queryset.order_by('-date')

    def format_price(self):
        locale.setlocale(locale.LC_ALL, '')
        return locale.currency(self.price) if self.price else ''

public_fields = {
    'id': fields.String,
    'title': fields.String,
    'slug': fields.String,
    'description': fields.String,
    'price': fields.Float,
    'thumbnail_url': fields.String,
    'link_url': fields.String,
    'publish_date': fields.DateTime,
    'create_date': fields.DateTime,
    'delete_date': fields.DateTime,
}


class PostResource(Resource):

    @marshal_with(public_fields)
    def get(self, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except ValidationError:
            post = Post.objects.get_or_404(slug=post_id)

        if post is None:
            abort(404)

        return post

    @marshal_with(public_fields)
    def put(self, post_id):
        post = Post.objects.get_or_404(id=post_id)

        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('slug', type=str)
        parser.add_argument('price', type=float)
        parser.add_argument('thumbnail_url', type=str)
        parser.add_argument('link_url', type=str)
        parser.add_argument('publish_date', type=str)

        data = parser.parse_args(strict=True)
        # TODO: figure out a way to handle explicitly setting a certain property to none
        for key in data.keys():
            if data[key] is None:
                data.pop(key)
        post.update(**data)

        return post


class PostsResource(Resource):

    @marshal_with(public_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        parser.add_argument('slug', type=str, required=True)
        parser.add_argument('price', type=float)
        parser.add_argument('thumbnail_url', type=str)
        parser.add_argument('link_url', type=str)
        parser.add_argument('publish_date', type=str)

        data = parser.parse_args(strict=True)
        data['slug'] = data['slug'].replace(' ', '-')

        pst = Post(**data)
        pst.save()

        return pst

    @marshal_with({'posts': fields.List(fields.Nested(public_fields))})
    def get(self, limit=100):
        """Query endpoint"""
        posts = Post.objects().limit(limit)
        return posts


api = Api(api_app)
api.add_resource(PostsResource, '/post')
api.add_resource(PostResource, '/post/<post_id>')