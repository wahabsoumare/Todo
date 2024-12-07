from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import func

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model) :
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    created_at = db.Column(db.DateTime, default = func.now())

    def __repr__(self) -> str :
        return f'({self.id}, {self.name}, {self.created_at})'

@app.route('/', methods = ['GET', 'POST'])
def index() :
    title = 'To Do List'
    if request.method == 'POST' :
        name = request.form['task']
        new_task = Task(name = name)
        try :
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except :
            return 'There was an issue adding your task'
    else :
        tasks = Task.query.order_by(Task.created_at).all()
    return render_template('index.html', title = title, tasks = tasks)

@app.route('/delete/<int:id>/')
def delete(id) :
    task_to_delete = Task.query.get_or_404(id)
    try :
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except :
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>/', methods = ['GET', 'POST'])
def update(id) :
    task = Task.query.get_or_404(id)
    if request.method == 'POST' :
        task.name = request.form['task']
        try :
            db.session.commit()
            return redirect('/')
        except :
            return 'There was an issue updating your task'
    else :
        title = 'Update Task'
        return render_template('update.html', title = title, task = task)

@app.route('/about')
def about() :
    title = 'About'
    return render_template('about.html', title = title)


if __name__ == '__main__' :
    app.run(debug = True)