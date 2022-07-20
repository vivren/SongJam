from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    name = StringField(validators=[DataRequired()], render_kw={'placeholder': 'Nickname', 'class': 'form-control', 'style': 'width: 75%; margin: auto;'})
    room = StringField(validators=[DataRequired()], render_kw={'placeholder': 'Room Name', 'class': 'form-control', 'style': 'width: 75%; margin: auto;'})
    submit = SubmitField('Join', render_kw={'class': 'btn btn-light'})
