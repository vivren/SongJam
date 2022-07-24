from flask_wtf import FlaskForm
from wtforms.fields import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired

class CreateForm(FlaskForm):
    name = StringField(validators=[DataRequired()], render_kw={'placeholder': 'Nickname', 'class': 'form-control', 'style': 'width: 75%; margin: auto;'})
    roomName = StringField(validators=[DataRequired()], render_kw={'placeholder': 'Room Name', 'class': 'form-control', 'style': 'width: 75%; margin: auto;'})
    roomType = RadioField('Room Type', choices=['Public', 'Private'], validators=[DataRequired()])
    submit = SubmitField('Create', render_kw={'class': 'btn btn-light'})

class JoinForm(FlaskForm):
    name = StringField(validators=[DataRequired()], render_kw={'placeholder': 'Nickname', 'class': 'form-control', 'style': 'width: 75%; margin: auto;'})
    roomName = StringField(validators=[DataRequired()], render_kw={'placeholder': 'Room Name', 'class': 'form-control', 'style': 'width: 75%; margin: auto;'})
    submit = SubmitField('Join', render_kw={'class': 'btn btn-light'})