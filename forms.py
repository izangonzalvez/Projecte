# from flask_wtf import FlaskForm
# from wtforms import StringField, IntegerField, SubmitField, SelectField, FloatField
# from wtforms.validators import DataRequired, NumberRange, InputRequired, Length

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, NumberRange, InputRequired
from flask_wtf.file import FileField, FileAllowed

class ItemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    photo = FileField('Photo', validators=[DataRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    price = FloatField('Price', validators=[DataRequired()])
    submit = SubmitField('Update')

class DeleteForm(FlaskForm):
    submit = SubmitField()

# class ItemForm(FlaskForm):
#     titulo = StringField(
#         validators = [Length(max="255"),DataRequired()]
#     )
#     description = StringField(
#         validators = [DataRequired()]
#     )
#     foto = StringField(
#         validators = [DataRequired()]
#     )
#     price = FloatField(
#         validators = [InputRequired()]
#     )
#     submit = SubmitField()

# class DeleteForm(FlaskForm):
#     submit = SubmitField()