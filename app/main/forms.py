from flask_wtf import FlaskForm
from wtforms import StringField,TextField,SubmitField,TextAreaField
from wtforms.validators import Required,DataRequired,Email,EqualTo

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')