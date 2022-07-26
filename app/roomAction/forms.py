from flask_wtf import FlaskForm
from wtforms.fields import StringField, RadioField, SubmitField, PasswordField
from wtforms.validators import DataRequired, InputRequired, ValidationError
import redis

class CreateForm(FlaskForm):
    name = StringField(validators=[DataRequired()], render_kw={'placeholder': 'Nickname', 'class': 'form-control', 'style': 'width: 75%; margin: auto;'})
    roomName = StringField(validators=[DataRequired()], render_kw={'placeholder': 'Room Name', 'class': 'form-control', 'style': 'width: 75%; margin: auto;'})
    roomType = RadioField(validators=[InputRequired()], choices=['Public Room', 'Private Room'], default='Public Room', render_kw={'style': 'margin: auto;'})
    roomPassword = PasswordField(render_kw={'placeholder': 'Room Password', 'class': 'form-control', 'style': 'width: 75%; margin: auto; visibility: hidden;'})
    submit = SubmitField('Create', render_kw={'class': 'btn', 'style': 'background-color: rgba(76, 201, 240, 1); color: white;'})

def validateRoom(form, roomId):
    rooms = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True, db=1)
    if rooms.exists(roomId.data) == 0:
        raise ValidationError("Room Doesn't Exist")

def validatePassword(form, roomId, roomPassword):
    rooms = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True, db=1)
    if roomPassword.data != rooms.hget(roomId.data, "password"):
        raise ValidationError('Incorrect Room Password')

#https://stackoverflow.com/questions/52435660/how-to-get-data-of-another-field-in-wtform-validate


class JoinForm(FlaskForm):
    name = StringField(validators=[DataRequired()], render_kw={'placeholder': 'Nickname', 'class': 'form-control', 'style': 'width: 75%; margin: auto;'})
    roomId = StringField(validators=[validateRoom, DataRequired()], render_kw={'placeholder': 'Room ID', 'class': 'form-control', 'style': 'width: 75%; margin: auto;'})
    roomPassword = PasswordField(validators=[validatePassword], render_kw={'placeholder': 'Room Password', 'class': 'form-control', 'style': 'width: 75%; margin: auto;'})
    submit = SubmitField('Join', render_kw={'class': 'btn btn-light'})
