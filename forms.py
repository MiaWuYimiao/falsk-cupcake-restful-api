from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import InputRequired, Optional, URL

class CupcakeForm(FlaskForm):
    flavor = StringField("Flavor", validators=[InputRequired(message="Flavor can't be blank")])
    size = SelectField("Size", choices=[('mini', 'mini'),('small', 'small'),('median', 'median'),('large', 'large')])
    rating = SelectField("Rate", choices=[(i,i) for i in range(10)]);
    image = StringField("Image URL", validators=[InputRequired(), URL()])