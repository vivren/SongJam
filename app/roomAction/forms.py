from flask_wtf import FlaskForm
from wtforms.fields import StringField, RadioField, SubmitField, HiddenField
from wtforms.validators import DataRequired, InputRequired

class CreateForm(FlaskForm):
    name = StringField(validators=[DataRequired()], render_kw={'placeholder': 'Nickname', 'class': 'form-control', 'style': 'width: 75%; margin: auto;'})
    roomName = StringField(validators=[DataRequired()], render_kw={'placeholder': 'Room Name', 'class': 'form-control', 'style': 'width: 75%; margin: auto;'})
    roomType = RadioField(validators=[InputRequired()], choices=['Public Room', 'Private Room'], default='Public Room', render_kw={'style': 'margin: auto;'})
    roomPassword = StringField(render_kw={'placeholder': 'Room Password', 'class': 'form-control', 'style': 'width: 75%; margin: auto; visibility: hidden;'})
    submit = SubmitField('Create', render_kw={'class': 'btn', 'style': 'background-color: rgba(76, 201, 240, 1); color: white;'})

class JoinForm(FlaskForm):
    name = StringField(validators=[DataRequired()], render_kw={'placeholder': 'Nickname', 'class': 'form-control', 'style': 'width: 75%; margin: auto;'})
    roomName = StringField(validators=[DataRequired()], render_kw={'placeholder': 'Room Name', 'class': 'form-control', 'style': 'width: 75%; margin: auto;'})
    submit = SubmitField('Join', render_kw={'class': 'btn btn-light'})
