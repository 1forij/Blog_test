from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired

class CreatePost(FlaskForm):
    title = StringField('博客标题',validators=[DataRequired()])
    body = TextAreaField('博客内容',validators=[DataRequired()])
    # categories = SelectMultipleField('Categories', coerce=int)
    submit = SubmitField("发布")

    # def __init__(self):
    #     super(CreatePost, self).__init__()
    #     self.categories.choices = [(c.id, c.title) for c in Category.query.order_by('id')]