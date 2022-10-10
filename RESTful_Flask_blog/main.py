import datetime

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField


# Delete this code:

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


# WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    # implementing the ckeditor
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    posts = db.session.query(BlogPost).all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    posts = db.session.query(BlogPost).all()
    for blog_post in posts:
        if blog_post.id == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route('/new-post', methods=['GET', 'POST'])
def new_post():
    heading = "New Post"
    blog_form = CreatePostForm()
    if blog_form.validate_on_submit():
        new_blog = BlogPost()
        new_blog.title = request.form.get("title")
        new_blog.author = request.form.get("author")
        new_blog.img_url = request.form.get("img_url")
        new_blog.subtitle = request.form.get("subtitle")
        # to get the text body from the text from the ckeditor
        new_blog.body = request.form.get("body")

        date = datetime.datetime.now()
        today = date.strftime("%B %d,%Y")
        new_blog.date = today

        db.session.add(new_blog)
        db.session.commit()

        posts = db.session.query(BlogPost).all()

        return redirect(url_for('get_all_posts', all_posts=posts))

    return render_template('make-post.html', form=blog_form, h1=heading)


@app.route('/edit-post/<post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    heading = "Edit Post"
    post_to_be_edited = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post_to_be_edited.title,
        subtitle=post_to_be_edited.subtitle,
        author=post_to_be_edited.author,
        img_url=post_to_be_edited.img_url,
    )
    edit_form.body.data = post_to_be_edited.body
    if edit_form.validate_on_submit():
        post_to_be_edited.title = request.form.get("title")
        post_to_be_edited.author = request.form.get("author")
        post_to_be_edited.img_url = request.form.get("img_url")
        post_to_be_edited.subtitle = request.form.get("subtitle")
        # to get the text body from the text from the ckeditor
        post_to_be_edited.body = request.form.get("body")

        db.session.commit()
        return redirect(url_for('show_post', index=post_to_be_edited.id))
    return render_template('make-post.html', form=edit_form, h1=heading)


@app.route('/delete/<post_id>')
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()

    # get the updated blog posts after deleted
    posts = db.session.query(BlogPost).all()

    return redirect(url_for('get_all_posts', all_posts=posts))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
