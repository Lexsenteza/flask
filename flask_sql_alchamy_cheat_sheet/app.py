from flask import Flask
import sqlite3
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app=app)
# db = sqlite3.connect('books-collection.db')
# cursor = db.cursor()
# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
# cursor.execute("INSERT INTO books VALUES (1, 'Harry Potter', 'J. K. Rowling', '9.3')")
# db.commit()


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float(), nullable=False)

    def __repr__(self):
        return '<Books %r>' % self.title


with app.app_context():
    # Create a new Record
    db.create_all()
    # book = Books()
    # book.id = 1
    # YOU DONT ALWAYS NEED TO SPECIFY THE PRIMARY KEY FOR IT WILL ALWAYS BE AUTO GENERATED
    # book.title = 'Harry Potter'
    # book.author = 'J.K Rowling'
    # book.rating = 9.3
    # db.session.add(book)
    # db.session.commit()

    # read all records
    # all_books = db.session.query(Books).all()
    # print(all_books)

    # Another way i found in the documentation online
    # book = db.session.execute(db.select(Books).filter_by(title="Harry Potter")).one()
    # print(book)
    # this method is for all the items by a particular heading in a column
    # book = db.session.execute(db.select(Books).order_by(Books.title)).scalars()
    # < sqlalchemy.engine.result.ScalarResult object at 0x7f031942f010 >
    # this is the result then you loop through to get want you want.
    # for i in book:
    #     print(i.author)

    # read a particular record by query
    # book = Books.query.filter_by(title="Harry Potter").first()
    # print(book)

    # Update a particular record by query
    # book_to_update = Books.query.filter_by(title="Harry Potter").first()
    # book_to_update.title = "Harry Potter and the Chamber of Secrets"
    # db.session.commit()

    # Update a Record by Primary Key
    # book_id = 1
    # book_to_update = Books.query.get(book_id)
    # book_to_update.title = "Harry Potter and the Goblet of Fire"
    # db.session.commit()

    # Delete a particular Record By PRIMARY KEY
    # book_id = 1
    # book_to_delete = Books.query.get(book_id)
    # db.session.delete(book_to_delete)
    # db.session.commit()


@app.route('/')
def hello_world():  # put application's code here
    # db.create_all()


    #
    # db.session.add(book)

    return "hello"


if __name__ == '__main__':
    app.run()
