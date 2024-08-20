from flask_wtf import FlaskForm

from wtforms import TextAreaField,StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
import sqlalchemy as sa

from todo_app import db
from todo_app.models import User


class CreateTaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), 
                                             Length(min=1, max=64)])
    description = TextAreaField('Description', validators=[Length(max=256)])
    submit = SubmitField('Create')

class EditTaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), 
                                             Length(min=1, max=64)])
    description = TextAreaField('Description', validators=[Length(max=256)])
    completed = BooleanField('Completed')
    submit = SubmitField('Edit')