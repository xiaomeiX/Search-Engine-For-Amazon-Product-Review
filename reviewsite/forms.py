from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, SelectField

class ReviewSearchForm(FlaskForm):
	query, facetValue = StringField('Review Keywords', validators=[validators.DataRequired()]),  'overall'
	submit = SubmitField('Submit')
