from application import db
from application.models import Task

db.drop_all()
db.create_all()