from flask import Flask, render_template
import requests
from post import Post


app = Flask(__name__)
blog_url = "https://api.npoint.io/fd02134904d7ee52f82a"
response = requests.get(url=blog_url).json()


@app.route('/')
def home():
    all_posts = response
    return render_template("index.html", posts=all_posts)


@app.route('/post/<int:number>')
def posts_page(number):
    num = int(number)
    poster = Post(response, num)
    data = poster.get_body()
    return render_template('post.html', page_data=data)


if __name__ == "__main__":
    app.run(debug=True)
