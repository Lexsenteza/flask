from flask import Flask, request, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import pprint

db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app=app)
Bootstrap(app)


# api keys from themoviedb.org
api_key = "295d351d0173cb9ee61c74576a28e654"
api_read_access = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyOTVkMzUxZDAxNzNjYjllZTYxYzc0NTc2YTI4ZTY1NCIsInN1YiI6IjYzNDEz" \
                  "ZTc5NzFmZmRmMDA3YTI0N2IyMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.SMc2ElnTIVQJUfgR9nyz" \
                  "uexlQ-nfZz8UCnPcBEI3qGM"
search_movie_url = "https://api.themoviedb.org/3/search/movie"
get_movie_information_url = "https://api.themoviedb.org/3/movie/"
headers = {
            "Authorization": f"Bearer {api_read_access}"
        }


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(200), nullable=False)

# first time creating the database.
# with app.app_context():
#     new_movie = Movie(title="Phone Booth",
#                       year=2002,
#                       description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an"
#                                   "extortionist's sniper rifle. Unable to leave or receive outside help, "
#                                   "Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#                       rating=7.3,
#                       ranking=10,
#                       review="My favourite character was the caller.",
#                       img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg")
#     db.create_all()
#     db.session.add(new_movie)
#     db.session.commit()


class Edit(FlaskForm):
    change_rating = StringField(label="Your Rating Out of 10 e.g 7.5", validators=[DataRequired()])
    change_review = StringField(label="Your Review", validators=[DataRequired()])
    submit = SubmitField(label="Done")


class Add(FlaskForm):
    movie = StringField(label="Movie Title", validators=[DataRequired()])
    movie_submit = SubmitField(label="Add Movie")





@app.route('/')
def home_page():  # put application's code here
    # at first this was the way i got hold of the data from the database
    #  all_movies = db.session.query(Movie).all()
    # but i had to change because i wanted them ordered by rating. and that returned the query in an ordered way by
    # ranking of highest to lowest in the ratings' column. because on defining it in the class. it was an integer.
    # also the read the docs on query in this link. that's where flask sqlalchemy gets its methods and functions
    # https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.order_by

    all_movies = db.session.query(Movie).order_by("rating")
    list_of_movies = list(all_movies)
    current_ranking = 1

    # another way which returns a list item is:
    # all_movies = Movie.query.order_by(Movie.rating).all()

    # i turned the all movies into a list because a "query object" has no length attribute and comes back as a whole
    # wording type of thing. so that is the best way to get the length and be able to loop through as well.

    for number in range(len(list_of_movies), 0, -1):
        # this is a range function in this manner range(start, stop, number_limit or range) in order to start from top
        list_of_movies[number - 1].ranking = current_ranking
        current_ranking += 1

    db.session.commit()
    return render_template('index.html', movies=all_movies)


@app.route('/edit/<movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    form = Edit()
    movie_to_edit = Movie.query.get(movie_id)
    if form.validate_on_submit():
        # new_rating = request.args.get("change_rating")
        # you use the request.args.get when your getting a key from a url that has passed down from another index.
        # but if its a form. use the request.form.get("key")
        # new_review = request.args.get("change_review")
        new_rating = request.form.get("change_rating")
        new_review = request.form.get("change_review")
        movie_to_edit.rating = new_rating
        movie_to_edit.review = new_review
        db.session.commit()
        return redirect(url_for('home_page'))
    return render_template('edit.html', form=form, movie=movie_to_edit)


@app.route('/delete')
def delete_movie():
    movie_id = request.args.get("movie_id")
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home_page"))


@app.route('/add', methods=['GET', 'POST'])
def add_movie():
    movie_form = Add()

    if movie_form.validate_on_submit():
        # if this is a post request and all the validations have been passed.
        movie_title = request.form.get("movie")

        parameters = {
            "api_key": api_key,
            "query": movie_title
        }
        response = requests.get(url=search_movie_url, headers=headers, params=parameters)
        response.raise_for_status()
        search_results = response.json()["results"]
        return render_template('select.html', results=search_results)
    return render_template('add.html', form=movie_form)


@app.route('/select')
def select_movie():
    movie_to_be_added = Movie()
    movie_selected_id = request.args.get("movie_id")
    movie_parameters = {
        "api_key": api_key,
        "append_to_response": "images"
    }
    response = requests.get(url=f"{get_movie_information_url}{movie_selected_id}", headers=headers,
                            params=movie_parameters)
    response.raise_for_status()
    data = response.json()
    poster_path = data["images"]["posters"][0]["file_path"]
    title = data["original_title"]
    movie_to_be_added.title = title
    movie_to_be_added.year = data["release_date"].split("-")[0]
    movie_to_be_added.img_url = f"https://image.tmdb.org/t/p/original/{poster_path}"
    movie_to_be_added.description = data["overview"]
    # i added these fields as zero because i put them as "nullable" when i was naming the class so an error would be
    # raised if i left them blank. but will edit them later on.
    movie_to_be_added.rating = 0.0
    movie_to_be_added.ranking = 0
    movie_to_be_added.review = "Yet to be Reviewed"

    db.session.add(movie_to_be_added)
    db.session.commit()

    # after this commitment user will be redirected to the edit page where they can edit the rating and review.
    # that is why we need to get the id of the movie to be edited from the database.
    # and because the title is unique when i added the column to the database meaning they can only be one title. i can
    # easily identify the movie using the title MAKE SURE TO ADD THE "first()" AT THE END
    movie_to_be_edited = Movie.query.filter_by(title=title).first()
    # now we go ahead and get the movies' id. because we need to pass that as a parameter in the redirect
    id_of_movie = movie_to_be_edited.id
    return redirect(url_for('edit', movie_id=id_of_movie))


if __name__ == '__main__':
    app.run()

