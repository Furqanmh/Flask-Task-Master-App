#imports
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#my application
app = Flask(__name__)
Scss(app)

#Configure Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my_database.db"
app.config["SQLAlchemy_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

#Data Class
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String[100], nullable = False)
    created = db.Column(db.DateTime, default = datetime.now)
    complete = db.Column(db.Integer, default = 0)

    def __repr__(self):
        return f"Task: {self.id}"

#Create Database
with app.app_context():
    db.create_all()

#Routes to the webpages
@app.route("/", methods = ["GET", "POST"])
def index():
    #Add a task
    if request.method == "POST":
        current_task = request.form['content']
        new_task = MyTask(content = current_task)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error: {e}"

    #Show all tasks
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html", tasks = tasks)



#Delete a task
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"Error: {e}"


#Edit a task
@app.route("/edit/<int:id>", methods = ["GET", "POST"])
def edit(id:int):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error: {e}"

    else:
        return render_template("edit.html", task = task)





#Runs and debugs app
if __name__ == "__main__":
    app.run()