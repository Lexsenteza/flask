from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config["SECRET_KEY"] = "key"
admin = "admin@email.com"
secure = "12345678"
Bootstrap(app)


class MyForm(FlaskForm):
    email = EmailField(label="email", validators=[DataRequired(), Email()])
    password = PasswordField(label="password", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label="Login")


@app.route('/')
def home_page():  # put application's code here
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    made_form = MyForm(request.form)

    if made_form.validate_on_submit():
        if str(made_form.email.data) == admin and str(made_form.password.data) == secure:
            return render_template('success.html')
        else:
            return render_template('denied.html')

    return render_template('login.html', form=made_form)


if __name__ == '__main__':
    app.run()
#
# from email_validator import validate_email, EmailNotValidError
# email = "lexsenteza@outlook.com"
# validation = validate_email(email=email)
#

