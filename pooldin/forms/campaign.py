from flask.ext.wtf import (Form,
                           DateField, IntegerField, TextField,
                           Length, Required)


class FormCampaignCreate(Form):
    name = TextField('name', validators=[Required()])
    description = TextField('description')
    active_end = DateField('active_end', format='%m/%d/%Y')
    active_days = IntegerField('active_days', validators=[Length(min=1)])


class FormCampaignUpdate(Form):
    pass
