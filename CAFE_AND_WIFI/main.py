from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField(label="Cafe Location on Google Maps(URL)", validators=[DataRequired(), URL()])
    opening_time = StringField(label='Opening Time e.g.8AM', validators=[DataRequired()])
    closing = StringField(label='Closing Time e.g.5.50PM', validators=[DataRequired()])
    rating = SelectField(label="Coffee Rating", validators=[DataRequired()], choices=[])
    wifi = SelectField(label="Wifi Strength Rating", validators=[DataRequired()])
    power = SelectField(label="Power Strength Rating", validators=[DataRequired()])
    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    form.power.choices = ['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌']
    form.rating.choices = ['✘', '☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕']
    form.wifi.choices = ['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪']

    if form.validate_on_submit():
        cafe_name = form.cafe.data
        location = form.location.data
        opening_time = form.opening_time.data
        closing_time = form.closing.data
        coffee_rating = form.rating.data
        wifi_rating = form.wifi.data
        power_rating = form.power.data
        new_cafe_place = [cafe_name, location, opening_time, closing_time, coffee_rating, wifi_rating, power_rating]
        with open('cafe-data.csv', mode="a", newline='') as csv_file:
            data = csv.writer(csv_file, delimiter=',')
            data.writerow(new_cafe_place)
        return redirect(url_for('cafes'))

    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
