from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required

import sqlalchemy as sa

from todo_app import db
from todo_app.main import main_bp
from todo_app.main.forms import CreateTaskForm, EditTaskForm
from todo_app.models import Task


@main_bp.route('/')
@main_bp.route('/index')
def index():
    return render_template('main/index.html')


@main_bp.route('/todolist')
@login_required
def todolist():
    tasks = db.session.scalars(
        current_user.tasks.select().order_by(Task.completed)
    ).all()
    return render_template('main/todolist.html', tasks=tasks)

@main_bp.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    form = CreateTaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, description=form.description.data, 
                    author=current_user)
        db.session.add(task)
        db.session.commit()
        flash("You have successfully create the task")

        return redirect(url_for('main.todolist'))

    return render_template('main/create_task.html', form=form)

@main_bp.route('/edit_task/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    task = db.session.get(Task, id)

    if task is not None and task.author == current_user:
        # Reuse CreateTaskForm for editing task
        form = EditTaskForm()
        if form.validate_on_submit():
            task.title = form.title.data
            task.description = form.description.data
            task.completed = form.completed.data
            db.session.commit()
            flash("You have successfully edit the task")

            return redirect(url_for('main.todolist'))
        elif request.method == 'GET':
            form.title.data = task.title
            form.description.data = task.description
    else:
        flash("You don't have a permission")
        return redirect(url_for('main.todolist'))

    return render_template('main/edit_task.html', form=form)

@main_bp.route('/delete_task/<int:id>', methods=("POST", ))
@login_required
def delete_task(id):
    task = db.session.get(Task, id)
    if task is not None and task.author == current_user:
        db.session.delete(task)
        db.session.commit()
        flash("You have successfully deleted the task")
    else:
        flash("You don't have a permission")
    return redirect(url_for('main.todolist'))

@main_bp.route("/edit_task_status/<int:id>", methods=("POST", ))
@login_required
def edit_task_status(id):
    task = db.session.get(Task, id)
    if task is not None and task.author == current_user:
        task.completed = not task.completed
        db.session.commit()
    else:
        flash("You don't have a permission")
    return redirect(url_for("main.todolist"))