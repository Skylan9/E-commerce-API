from flask import render_template, flash, redirect, url_for,request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
from app import app, db
import sqlalchemy as sa
from app.forms import LoginForm, RegistrationForm, WorkoutForm
from app.models import Users, Workoutplan, WorkoutExercise, Exercise, Category, Status

@app.route('/')
@login_required
def home():
    #The current user can only see their own workoutplans
    workoutplan = Workoutplan.query.filter(Workoutplan.users_id == current_user.id)
    print(workoutplan)
    return render_template('home.html', workoutplan=workoutplan)
# Create functionality - CRUD -------------------------------------
@app.route('/create-workout', methods=['GET', 'POST'])
@login_required
def create():
    form = WorkoutForm()
    form.exercises.choices = [(exercise.id, exercise.name) for exercise in Exercise.query.all()]
    form.status.choices = [(item.id, item.name) for item in Status.query.all()]
    
    if form.validate_on_submit():
        try:
            # Create a new workout plan
            status_name = form.status.data.strip()
            status = Status.query.filter_by(id=status_name).first()
            category_name = form.category.data.strip()
            category = Category.query.filter_by(name=category_name).first()

            
            # If category doesn't exist, create it
            if not category:
                category = Category(name=category_name)
                db.session.add(category)
                db.session.commit()
                
            # test = Category.query.filter_by(name= form.category.data)
            # for category in test:
            #     print(f"ID: {category.id}, Name: {category.name}")
            #     category_id = category.id
        
            # Create workout plan
            
            workoutplan = Workoutplan(name=form.name.data, description=form.description.data, category_id = category.id, users_id=current_user.id, status_id=status.id)

            # Add selected exercises to the workout plan
            selected_exercises = Exercise.query.filter(Exercise.id.in_(form.exercises.data)).all()
            print(selected_exercises)
            for item in selected_exercises:
                db.session.add(WorkoutExercise(workoutplan=workoutplan, exercise=item, sets=0, reps=0))
            
            # workoutplan.plan.extend(selected_exercises)
            # workoutplan.workout_exercises.extend(selected_exercises)
            db.session.add(workoutplan)
            db.session.commit()
            flash('You created a workoutplan!')
            return redirect(url_for('home'))
        except Exception as e:
            print(e)
            print('error test')
            db.session.rollback()
            
    return render_template('create_workout.html', title='create workout', form=form)
# END Create functionality - CRUD -----------------------------------
# Read functionality - CRUD -----------------------------------------
@app.route('/wp_page/<id>')
@login_required
def wp_page(id):
    workoutplan = Workoutplan.query.filter_by(id=id).first_or_404()
    exercises = Exercise.query.all()
    exercises_plan = db.session.query(WorkoutExercise, Exercise).join(Exercise, WorkoutExercise.exercise_id == Exercise.id).filter(WorkoutExercise.workoutplan_id == workoutplan.id).all()
    return render_template('wp_page.html', workoutplan=workoutplan, exercises=exercises, exercises_plan = exercises_plan)
# END Read functionality - CRUD -------------------------------------
# Update functionality - CRUD ---------------------------------------
@app.route('/workoutplan/<int:plan_id>/add_exercise', methods=['POST'])
def add_exercise(plan_id):
    print("test")
    data = request.json
    exercise_id = data.get('exercise_id')
    new_exercise = data.get('new_exercise')
    workoutplan = Workoutplan.query.get_or_404(plan_id)
    workoutExercise = WorkoutExercise.query.all()
    workoutexercises = [(item.exercise_id) for item in WorkoutExercise.query.all()]
    print(workoutexercises)
    if exercise_id:
        # Add existing exercise
        exercise = Exercise.query.get_or_404(exercise_id)
        # for item in workoutExercise:
        #     if item.
        db.session.add(WorkoutExercise(workoutplan=workoutplan, exercise=exercise, sets=0, reps=0))
    elif new_exercise:
        # Create new exercise and add it to the workout plan
        exercise = Exercise(id=db.session.query(Exercise).count()+1, name=new_exercise)
        db.session.add(exercise)
        db.session.add(WorkoutExercise(workoutplan=workoutplan, exercise=exercise, sets=0, reps=0))
        
        

    db.session.commit()
    return jsonify({'success': True})

@app.route('/wp_edit/<id>', methods=['GET', 'POST'])
@login_required
def wp_edit(id):
    workoutplan = Workoutplan.query.filter_by(id=id).first_or_404()
    form = WorkoutForm(obj=workoutplan)
    form.status.choices = [(item.id, item.name) for item in Status.query.all()]
    form.exercises.choices = [(exercise.id, exercise.name) for exercise in Exercise.query.all()]
    # form.exercises.default = workoutplan.plan
    
    if request.method == 'GET':
        form.name.data = workoutplan.name
        form.description.data = workoutplan.description
        form.category.data = workoutplan.category.name
        # form.exercises.data = [exercise.id for exercise in workoutplan.plan]
    if request.method == 'POST':
        if form.btn_cancel.data:
            return redirect(url_for('wp_page', id=id))
    if form.validate_on_submit():
        category_name = form.category.data.strip()
        category = Category.query.filter_by(name=category_name).first()
        # If category doesn't exist, create it
        if not category:
            category = Category(name=category_name)
            db.session.add(category)
            db.session.commit()
        #Add data to the workoutplan
        workoutplan.name = form.name.data
        workoutplan.description = form.description.data
        workoutplan.status_id = form.status.data
        workoutplan.category_id = category.id
        
        selected_exercises = Exercise.query.filter(Exercise.id.in_(form.exercises.data)).all()
        # workoutplan.plan.extend(selected_exercises)
        #commit data
        db.session.add(workoutplan)
        db.session.commit()
        return redirect(url_for("wp_page", id=id))
    
    
    return render_template('wp_edit.html', form=form, workoutplan=workoutplan)
# END Update functionality - CRUD -------------------------------------
# Delete functionality - CRUD -----------------------------------------
@app.route('/wp_delete/<id>', methods=['POST'])
@login_required
def wp_delete(id):
    workoutplan = Workoutplan.query.filter_by(id=id).first_or_404()
    # workoutplan.plan = []
    db.session.delete(workoutplan)
    db.session.commit()
    return redirect(url_for('home'))
# END Delete functionality - CRUD -------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(Users).where(Users.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
