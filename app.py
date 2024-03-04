"""Flask app for Cupcakes"""
import os

from flask import Flask, jsonify

from models import connect_db, Cupcake, db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///cupcakes")

connect_db(app)

@app.get("/api/cupcakes")
def get_all_cupcakes_data():

    cupcakes = Cupcake.query.all()

    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes = serialized)

