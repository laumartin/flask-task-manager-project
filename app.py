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
# creating a function with a decorator that includes a route to that function.
# The routing is a string that,when we attach it to a URL, will redirect to a
# particular function in our Flask app,added directly beneath our existing
# default root, so that either URL will direct the user to the same page.
@app.route("/get_tasks")
def get_tasks():
    # On this tasks template, we want to generate data from our tasks collection on MongoDB, visible to our users.
    # This will find all documents from the tasks collection, and assign them
    #  to our new 'tasks' variable.
    # We convert the mongo cursor object into a list.
    tasks = list(mongo.db.tasks.find())
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
        return redirect(url_for("profile", username=session["user"]))

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
                    return redirect(url_for(
                        "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # Username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # create new username variable that is the user found from db
    # the session variable in [] must be called 'user' to be consistent.
    # to avoid retreive the entire record from db,and just get the username
    # stored, include more []to only grab the 'username' key field from record
    username = mongo.db.users.find_one({"username": session["user"]})["username"]
    # the first username is what the template expect to retrieve in html file
    # the sedond username is what has been defined in the line above
    if session["user"]:
        return render_template("profile.html", username=username)
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    # session.clear will remove all session cookies applicable to our app
    # session.pop specify which session cookie
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        # since this is a styled checkbox,we add a ternary operator and
        # create a new variable, which will also be called 'is_urgent'
        is_urgent = "on" if request.form.get("is_urgent") else "off"
        # If the HTTP method requested is POST,we insert our form to the db.
        # Normally use insert_one() method on our tasks collection, and inside,
        # convert entire form into a dictionary with 'request.form.to_dict()'
        # that would take all of our name attributes from the form, and build
        # a dictionary that gets inserted into the db.However, we also want to
        # include some additional fields,mwhich aren't listed on our form, such
        # as the username of the person adding the task. So above we create our
        # own dictionary of items from the form, stored in a variable 'task'.
        task = {
            # Python uses the name attributes from the form to grab data, and
            # that's what gets stored into our db in these pair key-values.
            "category_name": request.form.get("category_name"),
            "task_name": request.form.get("task_name"),
            "task_description": request.form.get("task_description"),
            "is_urgent": is_urgent,
            "due_date": request.form.get("due_date"),
            "created_by": session["user"]  
            }
        # use the task variable into our tasks collection
        mongo.db.tasks.insert_one(task)
        flash("Task Successfully Added")
        return redirect(url_for("get_tasks"))

    # Perform find() method on categories collection.The categories will
    # display in the same order we added them to the db,so sort them by
    # category_name key, using 1 for ascending, or alphabetical.
    categories = mongo.db.categories.find().sort("category_name", 1)
    # we need to pass this new 'categories' variable over to our HTML
    # template, so 'categories=categories'
    return render_template("add_task.html", categories=categories)

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
