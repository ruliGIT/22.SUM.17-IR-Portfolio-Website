import os
#from tkinter import N
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict 
import re

load_dotenv()
app = Flask(__name__)

#connect to MySQL db
if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306)

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

class Proj:
    def __init__(self, name, stack, descrip, git, demo) -> None:
        self.name = name
        self.stack = stack
        self.descrip = descrip
        self.git = git
        self.demo = demo

class Polaroid:
    def __init__(self, caption, pic):
        self.caption = caption
        self.pic = pic

class Exp:
    def __init__(self, name, descrip) -> None:
        self.name = name
        self.descrip = descrip

class Post:
    def __init__(self, name, email, content) -> None:
        self.name = name
        self.email = email
        self.content = content

@app.route('/')
def index():

    projs = [
        Proj(
            "Cryptocurrency Details and News", 
            "Tech Stack: JavaScript, React, Redux Toolkit, Chart.js, and Node.js", 
            "Built a React application that displays present data and news of the top 100 crypto currencies",
            "https://github.com/ruliGIT/Top100crypto", "https://sage-100-cryptos-ir.netlify.app/"),
        Proj(
            "Diabetes Predictor", 
            "Tech Stack: Python, Pandas, Numpy, Scikit-Learn, Streamlit", 
            "Built a machine learning model that predicts a users diabetes diagnosis",
            "https://github.com/ruliGIT/diabetes-prediction", "https://share.streamlit.io/ruligit/diabetes-prediction/main/streamlitApp.py"),
        Proj(
            "Queen’s University CISC 226: Game Design Course Project", 
            "Tech Stack: Unity, C#", 
            "Developed a PacMan inspired rogue-like game using the Unity Game Engine",
            "https://github.com/CISC-226-22W/gpd-gdp-23/tree/VideoSceneIsaac", "https://creative.caslab.queensu.ca/~GDP23/"),
        Proj(
            "This Portfolio Website!", 
            "Tech Stack:  Python, Flask, Jinja, MySQL, Docker", 
            "Portfolio website template using Python, Flask, Jinja, MySQL, Nginx, and unittest",
            "https://github.com/ruliGIT/pe-portfolio", "https://ishami-ru.duckdns.org/")
    ]

    exps = [
        Exp("Production Engineering Fellow (Meta)", 
        ["Major League Hacking", "Completed 12-weeks of structured curriculum-based learning covering core Production Engineering topics and built this website!", "Jun 2022 – Aug 2022"]),
        Exp("Research Volunteer ", 
        ["Queen’s MIB Laboratory", "Working towards finding more advanced computational methods to analyze cancer mutation data by exploring different machine learning techniques", "Jun 2022 – present"]),
        Exp("General Member", 
        ["Queen’s Web Development Club", "Learned fundamentals of web development and modern web development tools (React.js, Node.js, Figma) and worked on team project using Google Maps JavaScript API", "Sept 2021 – Apr 2022"])
    ]

    pols = [
        Polaroid("Queen's University", 
        "static\img\Image-Queens-University.jpg"),
    ]

    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"), projects=projs, polaroids=pols, experiences=exps)

# create timeline post page
@app.route('/timeline')
def timeline():
    posts = [model_to_dict(p) for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())]
    return render_template('timeline.html', title="Timeline", url=os.getenv("URL"), posts=posts)

# create db timeline_post
@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name, content, email = None, None, None
    try: 
        name = request.form['name']
        if name =="":
            return "<html>Invalid name</html>", 400
    except:
        if not name:
            return "<html>Invalid name</html>", 400
    try:
        email = request.form['email']
        pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        if email == "" or not re.match(pat, email):
            return "<html>Invalid email</html>", 400
    except:
        if not email:
            return "<html>Invalid email</html>", 400
    try:
        content = request.form['content']
        if content == "":
            return "<html>Invalid content</html>", 400
    except:
        if not content:
            return "<html>Invalid content</html>", 400
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)

# create a GET endpoint that retrieves all timeline posts ordered by created_at descending 
# so the newest timeline posts are returned at the top
@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {'timeline_posts': [
            model_to_dict(p) for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }