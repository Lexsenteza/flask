from flask import Flask, jsonify, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
import random
import requests

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
documentation_url = "https://documenter.getpostman.com/view/23776258/2s83ziP4F1"


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        # Method 1.
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

        # Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        # return {column.name: getattr(self, column.name) for column in self.__table__.columns}


def to_bool(value: str):
    if value.title() == "True":
        return True
    elif value.title() == "False":
        return False
    else:
        return value


@app.route("/")
def home():
    return render_template("index.html", url=documentation_url)


@app.route('/random')
def random_cafe():
    all_cafes = db.session.query(Cafe).all()
    random_choice_cafe = random.choice(all_cafes)

    # jsonify formats the object that you have made from a class into dictionary type of format to be rendered as api
    # get request
    returned_object = jsonify(
        cafe={
            "name": random_choice_cafe.name,
            "map_url": random_choice_cafe.map_url,
            "img_url": random_choice_cafe.img_url,
            "location": random_choice_cafe.location,
            # puts some categories in a subsection
            "amenities": {
                "can_take_calls": random_choice_cafe.can_take_calls,
                "has_sockets": random_choice_cafe.has_sockets,
                "has_wifi": random_choice_cafe.has_wifi,
                "seats": random_choice_cafe.seats,
                "coffee_price": random_choice_cafe.coffee_price
            }
        }
    )
    return returned_object


@app.route('/all')
def all_database_cafes():
    all_cafes = db.session.query(Cafe).all()
    cafes = []
    for cafe in all_cafes:
        dict_to_send = cafe.to_dict()
        cafes.append(dict_to_send)
    return jsonify(cafes=cafes)


@app.route('/search')
def search():
    location = request.args.get("loc")
    if location is None:  # this means that the person never filled in the api parameters in the get request
        return abort(404)
    elif location != "":
        # when stating parameters for your api. use the args.get.("key") because your getting it directly from the
        # url and it is visible this why using the args.get
        all_cafes = db.session.query(Cafe).all()
        cafes_in_location = []
        for cafe in all_cafes:
            if location.lower() in cafe.location.lower():
                cafes_in_location.append(cafe)
        data_to_send = []
        if not cafes_in_location:  # this means if there is nothing in the cafes_in_location
            error = {
                "Not Found": "Sorry We dont have that cafe at the moment"
            }
            return jsonify(error=error)
        else:
            for matching_cafe in cafes_in_location:
                data_to_send.append(matching_cafe.to_dict())
            return jsonify(cafe=data_to_send)
    else:
        return jsonify(error={
                "Not Found": "Sorry We dont have that cafe at the moment"
            })
    # cafes_in_location = Cafe.query.filter_by(location=search_location).first()


@app.route('/add', methods=['POST'])
def add_cafe():
    cafe = Cafe()
    cafe.name = request.form.get("name")
    cafe.map_url = request.form.get("map_url")
    cafe.img_url = request.form.get("img_url")
    cafe.location = request.form.get("location")
    cafe.seats = request.form.get("seats")
    cafe.coffee_price = request.form.get("coffee_price")

    # the rest are booleans so i created a function to turn them into booleans
    # because the request.form.get brings them back as strings. and yet we had specified in the making of the
    # database that they are booleans
    cafe.has_toilet = to_bool(request.form.get("has_toilet"))
    cafe.has_wifi = to_bool(request.form.get("has_wifi"))
    cafe.has_sockets = to_bool(request.form.get("has_sockets"))
    cafe.can_take_calls = to_bool(request.form.get("can_take_calls"))

    db.session.add(cafe)
    db.session.commit()

    return jsonify(response={
        "success": "Successfully added the new cafe"
    })


@app.route('/update-price/<cafe_id>', methods=['PATCH'])
def update_price(cafe_id):
    cafe_to_update = Cafe.query.get(cafe_id)
    new_price = request.args.get("price")
    if cafe_to_update:
        cafe_to_update.coffee_price = new_price
        db.session.commit()
        return jsonify(success="Successfully updated the price")
    else:
        # 404 return a 404 response
        return jsonify(error={"Not found": "Sorry  a Cafe with that id is not available in the database"}), 404


@app.route('/report-closed/<cafe_id>', methods=['DELETE'])
def delete_cafe(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    secret_key = request.args.get("api-key")
    if secret_key != "TopSecretAPIKey" or not secret_key:
        # check to see if they have the right api-key or if they didn't fill in the right information and it is None
        return jsonify(error="sorry, that's not allowed, you need to have the correct api-key to get access"), 403
    elif not cafe_to_delete:
        # check to see if the cafe exists in the database and not an empty list has been returned
        return jsonify(error="sorry the cafe doesn't exist in the database")
    else:
        db.session.delete(cafe_to_delete)
        db.session.commit()
        return jsonify(success="the cafe has been deleted from the database")

# HTTP GET - Read Record

# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
