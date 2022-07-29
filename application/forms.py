from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import date

class checkDate():
    def __init__(self, message):
        self.message = message
    
    def __call__(self, form, field):
        if field.data < date.today():
            raise ValidationError(self.message)

class ToDoForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2,max=15)])
    description = TextAreaField('Description')
    due_date = DateField('Date due', validators=[DataRequired(), checkDate("Invalid Date, Enter a date in the future")])
    status = BooleanField('Complete')
    submit = SubmitField('Submit')

