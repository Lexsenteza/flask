from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app=app)


# CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
# Line below only required once, when creating DB.
#
# with app.app_context():
    # user = User()
    # db.create_all()


@login_manager.user_loader
def load_user(user_id):
    # this is how the login_manager will get hold user_objects inorder to login them in or out. using their ids.
    # your User class should have a UserMixin, this allows for multiple inheritance of a from different class. like
    # using the super when you initialize a class
    # the UserMixin has the functions of is_active, is_authenticated and is_anonymous which the login_manager changes
    # once the login_user function is called. changing the current_user's status and giving them access to restricted
    # parts of the website. those that have the login_required decorator.
    return User.query.get(int(user_id))

# CHECK THE flask-login DOCS FOR MORE INFORMATION.


@app.route('/')
def home():
    # print(current_user.is_active, current_user.is_authenticated)
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        check_email = User.query.filter_by(email=request.form.get("email")).first()
        if check_email:
            flash("This email already exists, please try logging in")
            return redirect(url_for('register'))
        else:
            new_user = User()
            user_name = request.form.get("name")

            new_user.name = user_name
            new_user.email = request.form.get("email")

            password = request.form.get("password")
            # generate the password hash from werkzeug.security, password is the password, the method of hashing the
            # password and then the length of the random word to which the password will be added inorder to hash it.
            # for more information of hashing check my notes on Agenda. about password hashing.
            hashed_password = generate_password_hash(password=password, method='pbkdf2:sha256', salt_length=8)
            new_user.password = hashed_password

            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # you can also create a flask wtf form and check the validate on submit function.
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if not user:
            # if there is no user with that email. and it is None
            flash('The email does not exist')
            redirect(url_for('login'))
        elif not check_password_hash(pwhash=user.password, password=password):
            # if the password doesn't match the one in the database
            flash('Wrong Password')
            return redirect(url_for('login'))
        else:
            # else means that the email does exist and the password do match so you can log them in
            # a user becomes authenticated once you log them in. otherwise. they are anonymous users
            login_user(user)
            flash('You were successfully logged in')
            return redirect(url_for('secrets'))

    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():

    return render_template("secrets.html", name=current_user.name)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    # this logouts the user by changing the current_user is_active from True to False. the current_user is an object
    # from the class created at the top.
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():
    # this returns the file in its format
    # the as_attachment automatically downloads the file.
    return send_from_directory(directory='static/files', path='cheat_sheet.pdf', as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
