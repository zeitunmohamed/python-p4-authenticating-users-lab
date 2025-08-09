#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

# ----------- Session & Auth Resources -----------

class Login(Resource):
    def post(self):
        username = request.get_json().get("username")
        user = User.query.filter_by(username=username).first()

        if user:
            session["user_id"] = user.id
            return user.to_dict(), 200
        return {"error": "Invalid username"}, 401


class Logout(Resource):
    def delete(self):
        session.pop("user_id", None)
        return {}, 204


class CheckSession(Resource):
    def get(self):
        user_id = session.get("user_id")
        if user_id:
            user = User.query.get(user_id)
            return user.to_dict(), 200
        return {}, 401


# ----------- Article Resources -----------

class ClearSession(Resource):
    def delete(self):
        session.clear()
        return {}, 204


class IndexArticle(Resource):
    def get(self):
        articles = [article.to_dict() for article in Article.query.all()]
        return articles, 200


class ShowArticle(Resource):
    def get(self, id):
        session["page_views"] = session.get("page_views", 0) + 1

        if session["page_views"] <= 3:
            article = Article.query.filter_by(id=id).first()
            if article:
                return article.to_dict(), 200
            return {"error": "Article not found"}, 404

        return {"message": "Maximum pageview limit reached"}, 401


# ----------- Routes -----------

api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(CheckSession, "/check_session")

api.add_resource(ClearSession, "/clear")
api.add_resource(IndexArticle, "/articles")
api.add_resource(ShowArticle, "/articles/<int:id>")


if __name__ == '__main__':
    app.run(port=5555, debug=True)
