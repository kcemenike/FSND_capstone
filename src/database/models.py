import os
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import json
from dotenv import load_dotenv

# Get environment variables
load_dotenv()


# Connect to database
srv = os.getenv("server")
port = os.getenv("port")
dbuser = os.getenv("database_user")
pw = os.getenv("database_password")
dbname = os.getenv("production_db")

database_path = f'''postgresql://{dbuser}:{pw}@{srv}:{port}/{dbname}'''
database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.drop_all()
    db.create_all()
    return db


'''
Author
a persistent author entity, extends the base SQLAlchemy Model
'''


class Author(db.Model):
    __tablename__ = 'authors'
    # Autoincrementing, unique primary key
    id = Column(Integer(), primary_key=True)
    # String Title
    firstname = Column(String())
    lastname = Column(String())

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname
        }


class Book(db.Model):
    __tablename__ = 'books'
    id = Column(Integer(), primary_key=True)
    # String Title
    title = Column(String())
    year = Column(Integer)
    category = Column(String())

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'category': self.category
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
