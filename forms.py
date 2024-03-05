"""Forms for playlist app."""

from wtforms import StringField, IntegerField, URLField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, URL, Optional



class CupcakeForm(FlaskForm):
    """Form for adding cupcakes."""

    flavor = StringField(
        "Cupcake Flavor",
        validators=[InputRequired()]
    )

    size = StringField(
        "Cupcake Size",
        validators=[InputRequired()]
    )

    rating = IntegerField(
        "Cupcake Rating",
        validators=[InputRequired()]
    )

    image_url = URLField(
        "Cupcake Image Address",
        validators=[Optional(), URL()]
    )

