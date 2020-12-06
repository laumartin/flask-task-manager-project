import os
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_pymongo import PyMongo 
# MongoDB stores its data in a JSON-like format called BSON. To find documents
# from MongoDB, we need to be able to render the ObjectId
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
    #As well as rendering of the template, we'll pass that tasks variable through to the template. 
    # The first 'tasks' is what the template will use, and that's equal to the
    # second 'tasks', which is our variable defined above.
    return render_template("tasks.html", tasks=tasks)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Check if username already exist in db and store that in a variable
        # set it to look for a user with find_one() method in users collection
        existing_user = mongo.db.users.find_one(
            # Look for the key username in db,the value will be the form data
            # username input(Python looks name="" attribute from html form)
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            # redirect the user back to the url_for()'register' function
            # to try again with another username.
            return redirect(url_for("register"))

        # if no existing user,take data from form into the register dictionary
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        # call the users collection on MongoDB and use the insert_one() method
        # which requires a dictionary
        mongo.db.users.insert_one(register)

        # put the new user into a 'sesion' temporary cookie, using the sesion
        # function imported from flask at the top
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            # Werkzeug helper to 'check_password_hash'takes 2 arguments
            # The first is existing_user's hashed password on the database in
            # [] since is part or our exisitng_user variable above, we found
            # the user, and to target his password in the db,we append the key
            # that we need inside[].Second argument is the password form input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                # we can now log the user in using session variables
                # that we have called user.
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome,{}".format(request.form.get("username")))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # Username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
