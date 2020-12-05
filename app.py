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
# grab our SECRET_KEY, which is a requirement when using some of the functions from Flask
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
<<<<<<< HEAD
    if request.method == "POST":
        # Check if username already exist in db assigning a new variable, using find_one() method
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            # redirect the user back to the url_for()'register' function, to try again with another username.
            return redirect(url_for("register")) 

        # if no existing user, gather the data from the form into the register dictionary below
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        # call the users collection on MongoDB and use the insert_one() method which requires a dictionary
        mongo.db.users.insert_one(register)

        # put the new user into a 'sesion' temporary cookie, using the sesion function imported from flask at the top
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
=======
>>>>>>> da33813108138eb721f879e599698e148261b4da
    return render_template("register.html")

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
