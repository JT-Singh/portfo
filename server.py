from flask import Flask, render_template, url_for, request, redirect
from markupsafe import escape
import csv

app = Flask(__name__)


@app.route("/")
def my_home():
    return render_template("index.html")


@app.route("/<page_name>")
def my_works(page_name):
    return render_template(page_name)


def write_to_file(data):
    with open("db.txt", mode="a") as db:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        file = db.write(f"\n {email},{subject},{message}")


def write_to_csv(data):
    with open("db.csv", newline="", mode="a") as db_csv:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(db_csv, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])


@app.route("/submit_form", methods=["POST", "GET"])
def submit_form():
    if request.method == "POST":
        try:
            data = request.form.to_dict()
            write_to_file(data)
            write_to_csv(data)
            return redirect("/thankyou.html")
        except:
            return "Did not save to database"
    else:
        return "Error - try again!"
