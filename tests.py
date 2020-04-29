import os
import unittest
import json
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from src.api import application
from src.database.models import setup_db, Author, Book


# load env
load_dotenv()


class LibraryTestCase(unittest.TestCase):
    """This class represents the CastingAgency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = application
        self.testing = True
        self.client = self.app.test_client

        # self.svr = os.getenv("server")
        # self.port = os.getenv("port")
        # self.dbname = os.getenv("test_db")
        # self.dbusr = os.getenv("database_user")
        # self.dbpass = os.getenv("database_password")
        # self.dbpath = \
        #     f"postgresql://{self.dbusr}:{self.dbpass}@{self.svr}/{self.dbname}"
        # self.db = setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_author = Author(
            firstname="New",
            lastname="Author"
        )
        self.new_book = Book(title="New Title", year=1990)

        self.new_author.insert()
        self.new_book.insert()

        # Get auth tokens
        self.student_token = os.getenv('STUDENT_TOKEN')
        self.publisher_token = os.getenv('PUBLISHER_TOKEN')

        self.author = {
            "firstname": "Kelechi",
            "lastname": "EMENIKE"
        }
        self.book = {
            "title": "Python for Accounting Professionals",
            "year": 2020,
            "category": "technology"
        }

    def tearDown(self):
        self.new_author.delete()
        self.new_book.delete()

    def test_get_books(self):
        res = self.client().get('/books')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # TEST PUBLIC PERMISSIONS

    def test_get_authors_as_public(self):
        res = self.client().get('/authors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'],
                         "Authorization header is missing. Kindly include")

    def test_post_authors_as_public(self):
        res = self.client().post('/authors', json=self.author)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'],
                         "Authorization header is missing. Kindly include")

    def test_post_books_as_public(self):
        res = self.client().post('/books', json=self.book)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'],
                         "Authorization header is missing. Kindly include")

    def test_patch_authors_as_public(self):
        id = self.new_author.id
        res = self.client().patch(f'/authors/{id}', json=self.author)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'],
                         "Authorization header is missing. Kindly include")

    def test_patch_books_as_public(self):
        id = self.new_book.id
        res = self.client().patch(f'/books/{id}', json=self.author)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'],
                         "Authorization header is missing. Kindly include")

    def test_delete_books_as_public(self):
        id = self.new_book.id
        res = self.client().delete(f'/books/{id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'],
                         "Authorization header is missing. Kindly include")

    def test_delete_books_as_public(self):
        id = self.new_author.id
        res = self.client().delete(f'/authors/{id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'],
                         "Authorization header is missing. Kindly include")

    # # TEST STUDENT PERMISSIONS
    def test_get_authors_as_student(self):
        res = self.client().get(
            '/authors', headers={"Authorization": f"Bearer {self.student_token}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_authors_as_student(self):
        res = self.client().post(
            '/authors', headers={"Authorization": f"Bearer {self.student_token}"}, json=self.author)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'],
                         "You are not authorized to perform this action")

    def test_post_books_as_student(self):
        res = self.client().post(
            '/books', headers={"Authorization": f"Bearer {self.student_token}"}, json=self.book)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'],
                         "You are not authorized to perform this action")

    def test_patch_authors_as_student(self):
        id = self.new_author.id
        res = self.client().patch(
            f'/authors/{id}', headers={"Authorization": f"Bearer {self.student_token}"}, json=self.author)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'],
                         "You are not authorized to perform this action")

    def test_patch_books_as_student(self):
        id = self.new_book.id
        res = self.client().patch(
            f'/books/{id}', headers={"Authorization": f"Bearer {self.student_token}"}, json=self.book)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'],
                         "You are not authorized to perform this action")

    def test_delete_books_as_student(self):
        id = self.new_book.id
        res = self.client().delete(
            f'/books/{id}', headers={"Authorization": f"Bearer {self.student_token}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'],
                         "You are not authorized to perform this action")

    def test_delete_authors_as_student(self):
        id = self.new_author.id
        res = self.client().delete(
            f'/authors/{id}', headers={"Authorization": f"Bearer {self.student_token}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'],
                         "You are not authorized to perform this action")

    # TEST PUBLISHER PERMISSIONS

    def test_get_authors_as_publisher(self):
        res = self.client().get(
            '/authors', headers={"Authorization": f"Bearer {self.publisher_token}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_authors_as_publisher(self):
        res = self.client().post(
            '/authors', headers={"Authorization": f"Bearer {self.publisher_token}"}, json=self.author)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['author'])

    def test_patch_authors_as_publisher(self):
        id = self.new_author.id
        res = self.client().patch(
            f'/authors/{id}', headers={"Authorization": f"Bearer {self.publisher_token}"}, json=self.author)
        data = json.loads(res.data)
        # print(data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['author'])

    def test_delete_authors_as_publisher(self):
        id = self.new_author.id
        res = self.client().delete(
            f'/authors/{id}', headers={"Authorization": f"Bearer {self.publisher_token}"})
        data = json.loads(res.data)
        # print(data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], id)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
