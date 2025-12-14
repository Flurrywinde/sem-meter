# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, validators
from wtforms.validators import DataRequired, Length

from datetime import date
from wtforms.fields import DateField
from wtforms.validators import ValidationError


class UserDataForm(FlaskForm):
    def validate_end_date(form, field):  # wtforms automatically looks for validate_<fieldname> and adds it to validation
        """Custom validator to ensure end date is not before start date."""
        if field.data < form.start_date.data:
            raise ValidationError("End date must not be earlier than start date.")

    csv_in = FileField('CSV File from Sem-meter', validators=[DataRequired()])
    # Field with validators: data is required and must be between 2 and 60 chars
    #username = StringField('Username', validators=[DataRequired(), Length(min=2, max=60)])
    #duedate = StringField('Due Date', validators=[DataRequired(), Length(min=2, max=60)])
    duedate = DateField(
        'Due Date',
        validators=[validators.DataRequired()],
        format='%Y-%m-%d'
    )
    amtdue = StringField('Amount Due', validators=[DataRequired(), Length(min=2, max=60)])
    kwh = StringField('KWh Billed', validators=[DataRequired(), Length(min=2, max=60)])
    start_date = DateField(
        'Start Date',
        validators=[validators.DataRequired()],
        format='%Y-%m-%d',
        default=date.today
    )
    end_date = DateField(
        'End Date',
        validators=[validators.DataRequired()],
        format='%Y-%m-%d',
        default=date.today
    )
    submit = SubmitField('Generate File')
