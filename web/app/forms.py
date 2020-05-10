from flask_wtf import FlaskForm
from wtforms import SubmitField


class StartForm(FlaskForm):
    start = SubmitField('Choose city')

