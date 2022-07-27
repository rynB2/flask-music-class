from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
from flask_login import login_required, current_user
from .models import User, Lesson, Classroom
from sqlalchemy.sql import insert
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
   
    return render_template("home.html", user=current_user)


@views.route('/leaderboards', methods=['GET', 'POST'])
@login_required
def leaderboards():
    y = User.query.all()
    
    x = session.get('my_var', None)
    
    return render_template("leaderboards.html", user=current_user, x=x, y=y)

@views.route('/classroom', methods=['GET', 'POST'])
@login_required
def classroom():
    if request.method == 'POST':
        room_code = request.form.get('room_code', type=str)
        room = Classroom.query.filter_by(room_code=room_code).first()
        if room:    
            flash('Room entered!', category='success')
            session['my_var'] = room_code
            return redirect(url_for('views.classroom_1'))
        else:
            flash('Room not found', category='error')
    
    
    return render_template("/classroom.html", user=current_user)

@views.route('/classroom/classroom_1', methods=['GET', 'POST'])
@login_required
def classroom_1():    
    room = session.get('my_var', None)
    room2 = int(room)
    x = Lesson.query.all()
    if request.method == 'POST':
        test = User.query.filter_by(id=current_user.id).first()
        if test.points is None:
            test.points = 10
        else: 
            test.points = test.points + 10
        db.session.commit()
    return render_template("/classroom/classroom_1.html", user=current_user, room=room, room2=room2, x=x)

@views.route('/class_lessons', methods=['GET', 'POST'])
@login_required
def class_lessons():
    if request.method == 'POST':
        lesson = request.form.get('lesson') 
        classroom = request.form.get('classroom')
        lesson_title = request.form.get('lesson_title')
        difficulty = request.form.get('difficulty')
        length = request.form.get('length')
        task1 = request.form.get('task1')
        task2 = request.form.get('task2')
        task3 = request.form.get('task3')
        completion_message = request.form.get('completion_message')

        room = Classroom.query.filter_by(room_code=classroom).first()
        if room:
            if len(lesson) < 1:
                flash('Lesson is too short!', category='error')
            elif len(length) < 1:
                flash("Length must not be blank!", category='error')
            elif len(task1) < 1:
                flash("Task 1 must not be blank!", category='error')
            elif len(task2) < 1:
                flash("Task 2 must not be blank!", category='error')
            elif len(task3) < 1:
                flash("Task 3 must not be blank!", category='error')
            elif len(completion_message) < 1:
                flash("Completion message must not be blank!", category='error')    
            else:
                new_lesson = Lesson(data = lesson, lesson_title=lesson_title, difficulty=difficulty, length=length, task1=task1, task2=task2, task3=task3, 
                           completion_message=completion_message, user_id = current_user.id, class_id = classroom)
                db.session.add(new_lesson)
                db.session.commit()
                flash('Lesson added!', category='success')
        else:
            flash('Room not found!', category='error')
    return render_template("class_lessons.html", user=current_user)


