from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float(), nullable=False)

    def __repr__(self):
        return '<Books %r>' % self.title


# with app.app_context():
#     book = Book()
#     db.create_all()
#     db.session.add(book)
#     db.session.commit()


@app.route('/', methods=['GET'])
def home():
    all_books = db.session.query(Book).all()
    # all_books is now a list item which you can loop through and find the rows.
    return render_template('index.html', books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    book = Book()
    if request.method == "POST":
        book.title = request.form["book"]
        book.rating = request.form["rating"]
        book.author = request.form["author"]
        # db.create_all()
        # the instance of the database was created on the first run of the app.
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route('/edit/<book_id>', methods=['GET', 'POST'])
def edit_rating(book_id):
    book_to_change = Book.query.get(book_id)
    if request.method == "POST":
        book_to_change.rating = request.form['changeRating']
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit.html', book=book_to_change)


@app.route('/delete')
def delete_rating():
    # the request helped me get the book_id from the template which i had passed as a key word argument
    book_id = request.args.get('book_id')
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

