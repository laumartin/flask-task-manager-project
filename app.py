import os
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_pymongo import PyMongo 
# MongoDB stores its data in a JSON-like format called BSON. To find documents from MongoDB, we need to be able to render the ObjectId,
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)
# first configuration will be used to grab the database name
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
# we need to configure the actual connection string
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
#grab our SECRET_KEY, which is a requirement when using some of the functions from Flask
app.secret_key = os.environ.get("SECRET_KEY")
# This is the Flask 'app' object defined above, to ensure  Flask app is communicating with the Mongo database.
mongo = PyMongo(app)


@app.route("/")
# creating a function with a decorator that includes a route to that function. The routing is a string that, 
# when we attach it to a URL, will redirect to a particular function in our Flask app. 
# added directly beneath our existing default root, so that either URL will direct the user to the same page.
@app.route("/get_tasks")
def get_tasks():
    # On this tasks template, we want to generate data from our tasks collection on MongoDB, visible to our users.
    # This will find all documents from the tasks collection, and assign them to our new 'tasks' variable.
    tasks = mongo.db.tasks.find()
    #Along with the rendering of the template, we'll pass that tasks variable through to the template. 
    # The first 'tasks' is what the template will use, and that's equal to the second 'tasks', which is our variable defined above.
    return render_template("tasks.html", tasks=tasks)


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
