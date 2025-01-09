from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from init_db import reset_database

app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Reset the database
# from app.models import Workoutplan,Exercise,Status,WorkoutExercise,Date,Category,Users
# with app.app_context():
#     reset_database(db)


from app import routes, models

# #Resetting the database
# app.app_context().push()
# create(db)


