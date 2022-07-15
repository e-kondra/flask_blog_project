from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Attach photo', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    comment = StringField('Comment', validators=[DataRequired()])