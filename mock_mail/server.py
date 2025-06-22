import os
from flask import Flask, request, render_template, redirect, url_for, jsonify, session
from .models import db, User, Letter
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv("TEST_USER_EMAIL")
PASSWORD = os.getenv("TEST_USER_PASSWORD")

app = Flask(__name__, template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mail.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "super_secret_key"

db.init_app(app)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(email=EMAIL).first():
        user = User(email=EMAIL, password=PASSWORD)
        db.session.add(user)
        db.session.commit()

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    email = request.form.get("email")
    password = request.form.get("password")
    if User.query.filter_by(email=email).first():
        return "<h3>User already exists</h3>"
    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/inbox", methods=["POST"])
def inbox():
    email = request.form.get("email")
    password = request.form.get("password")
    user = User.query.filter_by(email=email, password=password).first()
    if not user:
        return "<h3>Invalid credentials</h3>"
    session["user_id"] = user.id
    return redirect(url_for("inbox_via_get"))

@app.route("/inbox", methods=["GET"])
def inbox_via_get():
    user_id = session.get("user_id")
    if not user_id:
        return "<h3>Unauthorized</h3>"
    user = User.query.get(user_id)
    letters = Letter.query.filter_by(user_id=user.id).all()
    return render_template("inbox.html", messages=letters)

@app.route("/send", methods=["POST"])
def send_message():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    if not user:
        return "<h3>Unauthorized</h3>"
    message = request.form.get("message")
    if message:
        letter = Letter(message=message, user=user)
        db.session.add(letter)
        db.session.commit()
    return redirect(url_for("inbox_via_get"))

@app.route("/send_to", methods=["POST"])
def send_to_user():
    sender_id = session.get("user_id")
    if not sender_id:
        return "Unauthorized", 401
    receiver_email = request.form.get("receiver_email")
    message = request.form.get("message")
    receiver = User.query.filter_by(email=receiver_email).first()
    sender = User.query.get(sender_id)
    if receiver and message:
        letter = Letter(message=message, user=sender, receiver=receiver)
        db.session.add(letter)
        db.session.commit()
    return redirect(url_for("inbox_via_get"))

@app.route("/delete/<int:letter_id>", methods=["POST"])
def delete_one(letter_id):
    user_id = session.get("user_id")
    letter = Letter.query.filter_by(id=letter_id, user_id=user_id).first()
    if letter:
        db.session.delete(letter)
        db.session.commit()
    return redirect(url_for("inbox_via_get"))

@app.route("/delete_all", methods=["POST"])
def delete_all():
    user_id = session.get("user_id")
    Letter.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return redirect(url_for("inbox_via_get"))

@app.route("/search")
def search():
    user_id = session.get("user_id")
    query = request.args.get("q", "")
    results = Letter.query.filter(Letter.user_id == user_id, Letter.message.contains(query)).all()
    return render_template("inbox.html", messages=results)

@app.route("/api/letters")
def get_letters():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    user = User.query.get(user_id)
    return jsonify(letters=[letter.message for letter in user.letters])

if __name__ == "__main__":
    app.run(port=8088)