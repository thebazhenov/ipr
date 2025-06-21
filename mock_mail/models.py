from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    # Входящие письма (user_id — это отправитель, значит user = автор письма)
    letters = db.relationship("Letter", backref="user", lazy=True, foreign_keys="Letter.user_id")

    # Исходящие письма (если понадобится)
    received_letters = db.relationship("Letter", foreign_keys="Letter.receiver_id", lazy=True)

class Letter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # Автор
    receiver_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)  # Получатель

    receiver = db.relationship("User", foreign_keys=[receiver_id])