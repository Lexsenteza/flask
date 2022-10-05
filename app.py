from flask import Flask, render_template, request
import requests
from posts import Post
from datetime import datetime
import smtplib

app = Flask(__name__)
blog_end_point = "https://api.npoint.io/1200c3014dfc28a6e47a"
response = requests.get(url=blog_end_point)
data = response.json()
date = datetime.now().date()
my_email = "badeoye415@outlook.com"
my_password = "bamilede145#"


@app.route('/')
def home_page():  # put application's code here
    return render_template('index.html', page_data=data)


@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/contact', methods=['POST', 'GET'])
def contact_page():
    if request.method == "POST":
        heading = "Success your message was successfully sent."
        name = request.form["userName"]
        user_email = request.form["userEmail"]
        phone = request.form["userPhone"]
        body = request.form["userMessage"]
        email_message = f"Name: {name}\nEmail: {user_email}\nPhone Number: {phone}\nMessage: {body}"
        with smtplib.SMTP("smtp.office365.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_password)
            connection.sendmail(from_addr=my_email, to_addrs="ngobokaemmanuel1@gmail.com", msg=f"Subject: New Message\n\n{email_message}")
    else:
        heading = "Contact Me"
    return render_template('contact.html', big_heading=heading)


@app.route('/post/<int:number>')
def posts_page(number):
    post_data = Post(data=data, page_number=number)
    post_info = post_data.get_body()
    return render_template('post.html', posting=post_info)


if __name__ == '__main__':
    app.run()
