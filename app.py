
import re

from datetime import datetime

from flask import Flask

from flask import render_template

app = Flask(__name__)

print ("http://127.0.0.1:5000//hello//Regev")


def decorator_function(func):
    def inner_function():
        print("Before the function is called.")
        func()
        print("After the function is called.")
    return inner_function

@decorator_function
def args_funtion():
    print("In the middle we are!")

args_funtion()  
    
@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")


@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template("hello_there.html", name=name, date=datetime.now())
    

# Replace the existing home function with the one below
@app.route("/")
def home():
    return render_template("home.html")

# New functions
@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")



'''
@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content
'''