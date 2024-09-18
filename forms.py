from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class ComplaintForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    severity = StringField('Severity', validators=[DataRequired()])
    submit = SubmitField('Submit Complaint')
