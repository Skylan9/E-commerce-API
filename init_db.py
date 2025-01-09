from sqlalchemy.sql import text
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from config import Config

# result = subprocess.run(['python', '__init__.py'], capture_output=True, text=True, check=True)

# print(result.stdout)
# app = Flask(__name__)
# # app.config.from_object(Config)
# app.config['SECRET_KEY'] = 'b1f23c5db3b209eb359fe27810405d'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/workout_tracker'
# # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# from app.models import Workoutplan,Exercise,Status,WorkoutExercise,Date,Category,Users
print('test')
def reset_database(db):
    try:
        print("Existing tables before drop_all():", inspect(db.engine).get_table_names())
        db.drop_all()
        db.create_all()
        print("Existing tables after create_all():", inspect(db.engine).get_table_names())
        db.session.execute(
            text("""INSERT INTO exercise(id, name, description) VALUES 
                (1, 'Bench Press', 'Performing a bench press with a barbell'), 
                (2, 'Dumbell Press', 'Performing a bench press with dumbells'),
                (3, 'Squat', 'Performing a squat with a barbell'),
                (4, 'Deadlift', 'Performing a deadlift with a barbell')
                ON CONFLICT (id) DO UPDATE SET name = excluded.name, description= excluded.description"""
                )
        )
        db.session.execute(
            text("""INSERT INTO status(id, name) VALUES 
                (1, 'Not started'), 
                (2, 'In progress'),
                (3, 'Finished')
                ON CONFLICT (id) DO UPDATE SET name = excluded.name"""
                )
        )
    except:
        print("Error while creating the database")
    db.session.commit()
    return 'exercise data successfully inserted into the database'