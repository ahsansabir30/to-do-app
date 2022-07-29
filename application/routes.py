from flask import request, redirect, url_for, render_template
from application import app, db
from datetime import date
from application.models import Task
from application.forms import ToDoForm

@app.route('/')
def home():
    tasks = Task.query.all()
    return render_template('view.html', tasks=tasks)

@app.route('/add-task/', methods=['GET', 'POST'])
def new_task():
    form = ToDoForm()

    if form.validate_on_submit():
        new_task = Task(name=form.name.data, description=form.description.data, due_date=form.due_date.data, status=form.status.data)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))
    
    errors = form.due_date.errors
    errors += form.name.errors
    return render_template('form.html', form=form, errors=errors)
    
@app.route('/update-task/<int:id>/', methods=['GET', 'POST'])
def update_task(id):
    task = Task.query.get(id)
    
    form = ToDoForm(obj=task)
    if form.validate_on_submit():
        form.populate_obj(task)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('home'))

    errors = form.due_date.errors
    errors += form.name.errors
    return render_template('form.html', form=form, errors=errors)

@app.route('/delete-task/<int:id>/')
def delete_task(id):
    task_to_delete = Task.query.get(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))