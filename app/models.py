from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from sqlalchemy import event
from flask_sqlalchemy import SQLAlchemy
from app import login

@login.user_loader
def load_user(id):
    return db.session.get(Users, int(id))

class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), unique=True, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Users {self.username}>'

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercise'
    id = db.Column(db.Integer, primary_key=True)
    workoutplan_id = db.Column(db.Integer, db.ForeignKey('workoutplan.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)

    # Relationships for convenience
    workoutplan = db.relationship("Workoutplan", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

# workoutplan_exercise= db.Table('workoutplan_exercise',
#     db.Column('workout_id', db.Integer, db.ForeignKey('workoutplan.id')),
#     db.Column('exercise_id', db.Integer, db.ForeignKey('exercise.id'))
# )

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(400), unique=False, nullable=True)
    workoutplans = db.relationship('Workoutplan', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'
    
class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<Status {self.name}>'

class Workoutplan(db.Model):
    __tablename__ = 'workoutplan'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(400), unique=False, nullable=True)
    # exercises = db.relationship('Exercise', backref='exercise in workoutplan', lazy=True)
    # sets = db.Column(db.Integer, unique=True, nullable=False)
    # plan = db.relationship('WorkoutExercise', secondary=workoutplan_exercise, backref='plan')
    # Relationship to the association table
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workoutplan', cascade='all, delete-orphan')

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)

    def __repr__(self):
        return f'<Workoutplan {self.name}>'


class Exercise(db.Model):
    __tablename__ = 'exercise'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(400), unique=False, nullable=True)
    # Relationship to the association table
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')
    # workoutplan_id = db.Column(db.Integer, db.ForeignKey('workoutplan.id'), nullable=False)
    # sets = db.Column(db.Integer, unique=True, nullable=False)


    def __repr__(self):
        return f'<Excercise {self.name}>'
    

class Date(db.Model):
    __tablename__ = 'date'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    workoutplan_id = db.Column(db.Integer, db.ForeignKey('workoutplan.id'), nullable=False)
    exercises_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)

    # Relationship with WorkoutDateExercises
    # exercises = db.relationship('Exercise', back_populates='date')
    workoutplan = db.relationship('Workoutplan', backref='dates')


