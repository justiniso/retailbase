# -*- coding: utf-8 -*-
import datetime

from flask_restful import Resource, abort, Api, fields, marshal_with, reqparse

from . import Base
from mongoengine import ValidationError
from src.api import api_app, db


class Post(Base, db.Document):

    __tablename__ = 'post'

    title = db.StringField(max_length=255, required=True)
    description = db.StringField(max_length=255)
    slug = db.StringField(max_length=255, required=True)
    link_url = db.StringField(max_length=2080)
    thumbnail_url = db.StringField(max_length=2080)
    create_date = db.DateTimeField(default=datetime.datetime.now)
    publish_date = db.DateTimeField()
    delete_date = db.DateTimeField()

    # def load(self, data):
    #     self.link_url = data.get('link_url')
    #     self.thumbnail_url = data.get('thumbnail_url')
    #     self.title = data.get('title')
    #     self.description = data.get('description')
    #     self.slug = data.get('slug')

public_fields = {
    'id': fields.String,
    'title': fields.String,
    'slug': fields.String,
    'description': fields.String,
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

        # TODO: update

        return post


class PostsResource(Resource):

    @marshal_with(public_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        parser.add_argument('slug', type=str, required=True)

        data = parser.parse_args()
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