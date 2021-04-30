from flask_wtf import FlaskForm
from wtforms import StringField,TextField,SubmitField,TextAreaField
from wtforms.validators import Required,DataRequired,Email,EqualTo

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class NewPost(FlaskForm):
    title = StringField('Title',validators=[Required()])
    content = TextAreaField('Blog Content',validators=[Required()])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment',)
    submit = SubmitField('Submit', validators=[DataRequired()])