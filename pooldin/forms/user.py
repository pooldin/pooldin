from flask.ext.wtf import Form, PasswordField, TextField, Required


class FormUserLogin(Form):
    login = TextField('Login', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
