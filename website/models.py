from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lesson_title = db.Column(db.String(150))
    difficulty = db.Column(db.String(150))
    length = db.Column(db.String(150))
    data = db.Column(db.String(10000))
    task1 = db.Column(db.String(150))
    task2 = db.Column(db.String(150))
    task3 = db.Column(db.String(150))
    completion_message = db.Column(db.String(10000))   
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classroom.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    teacher = db.Column(db.String)
    points = db.Column(db.Integer)
    lessons = db.relationship('Lesson')

class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_code = db.Column(db.String(150), unique=True)
    creator = db.Column(db.String(150))
    lessons = db.relationship('Lesson')
