import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from flask_migrate import Migrate

from .database.models import setup_db, Book, Author
from .auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    db = setup_db(app)
    migrate = Migrate(app, db)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,-Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    # ROUTES

    @app.route('/authors', methods=['GET'])
    @requires_auth('get:authors')
    def get_authors(jwt):
        try:
            authors = Author.query.all()
            return jsonify({
                'success': True,
                'authors': [author.format() for author in authors]
            })
        except:
            abort(404)

    @app.route('/authors', methods=['POST'])
    @requires_auth('post:authors')
    def add_author(jwt):

        body = request.json
        if 'firstname' not in body or 'lastname' not in body:
            abort(422)

        firstname = body.get('firstname')
        lastname = body.get('lastname')

        try:
            author = Author(firstname=firstname, lastname=lastname)
            author.insert()
            return jsonify({
                'success': True,
                'author': [author.format()]
            })
        except:
            abort(422)

    @app.route('/authors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:authors')
    def update_author(jwt, id):
        author = Author.query.get(id)

        if author:
            try:
                body = request.json
                author.firstname = body.get(
                    'firstname') if 'firstname' in body else author.firstname
                author.lastname = body.get(
                    'lastname') if 'lastname' in body else author.lastname
                author.update()

                return jsonify({
                    'success': True,
                    'author': [author.format()]
                })
            except:
                abort(422)
        else:
            abort(404)

    @app.route('/authors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:authors')
    def delete_author(jwt, id):
        author = Author.query.get(id)

        if author:
            try:
                author.delete()
                return jsonify({
                    'success': True,
                    'delete': id
                })
            except:
                abort(422)
        else:
            abort(404)

    @app.route('/books')
    def get_books():
        try:
            books = Book.query.all()

            return jsonify({
                'success': True,
                'books': [book.format() for book in books]
            })
        except:
            abort(422)

    @app.route('/books', methods=['POST'])
    @requires_auth('post:books')
    def add_book(jwt):

        body = request.json
        if 'title' not in body or 'year' not in body:
            abort(422)
        title = body.get('title')
        year = body.get('year')
        category = body.get('category') if 'category' in body else None

        try:
            book = Book(title=title, year=year, category=category)
            book.insert()

            return jsonify({
                'success': True,
                'book': [book.format()],
            })
        except:
            abort(422)

    @app.route('/books/<int:id>', methods=['PATCH'])
    @requires_auth('patch:books')
    def update_book(self, id):
        book = Book.query.get(id)

        if book:
            try:
                body = request.json
                book.title = body['title'] if 'title' in body else book.title
                book.year = body['year'] if 'year' in body else book.year
                book.category = body['category'] if 'category' in body else book.category
                book.update()
                return jsonify({
                    'success': True,
                    'book': [book.format()]
                })
            except:
                abort(422)
        else:
            abort(404)

    @app.route('/books/<int:id>', methods=['DELETE'])
    @requires_auth('delete:books')
    def delete_book(jwt, id):
        book = Book.query.get(id)
        if book:
            try:
                book.delete()
                return jsonify({
                    'success': True,
                    'delete': id
                })
            except:
                abort(422)
        else:
            abort(422)

    # Error Handling
    '''
    Example error handling for unprocessable entity
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            'success': False,
            'message': error.error
        }), error.status_code

    return app


application = create_app()


# if __name__ == '__main__':
#     application.run(debug=True)
