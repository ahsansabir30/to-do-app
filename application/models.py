from application import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(30), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    
    def __str__(self):
        return self.name
