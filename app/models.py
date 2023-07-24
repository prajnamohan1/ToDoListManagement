from app import db

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(200))
    complete = db.Column(db.Boolean)
  
    def __repr__(self):
        return self.title

class Deleted(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(200))
  
    def __repr__(self):
        return self.title

        