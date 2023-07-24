from flask import render_template, request, redirect, url_for
from app import app
from app.models import Todo, Deleted
from app import db

@app.route('/')
def index():
    
    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()
    deleted = Deleted.query.all()
  
    return render_template('index.html', incomplete=incomplete, complete=complete, deleted=deleted)
  
  
@app.route('/add', methods=['POST'])
def add():

    todo = Todo(title=request.form['title'], description=request.form['description'], complete=False)
    db.session.add(todo)
    db.session.commit()
  
    return redirect(url_for('index'))
    
@app.route('/complete/<id>')
def complete(id):
  
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()
  
    return redirect(url_for('index'))

@app.route('/delete/<id>')
def delete(id):
  
    todo = Todo.query.filter_by(id=int(id)).first()
    db.session.delete(todo)
    deleted = Deleted(title=todo.title, description=todo.description)
    db.session.add(deleted)
    db.session.commit()
  
    return redirect(url_for('index'))