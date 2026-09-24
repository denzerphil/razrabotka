#1
import os
from datetime import datetime

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

#2

class Visit(db.Model):
    __tablename__ = "visits"

    id = db.Column(db.Integer, primary_key=True)
    visited_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=False)

#3

with app.app_context():
    db.create_all()

#4

@app.route("/hello")
def hello():
    visit = Visit(
        visited_at=datetime.utcnow(),
        ip_address=request.remote_addr
    )
    db.session.add(visit)
    db.session.commit()
    return "Hello", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)