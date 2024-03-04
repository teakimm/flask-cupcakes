"""Flask app for Cupcakes"""
import os

from flask import Flask, jsonify, request

from models import connect_db, Cupcake, db, DEFAULT_URL

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///flask_cupcakes")

connect_db(app)


@app.get("/api/cupcakes")
def get_all_cupcakes_data():
    """Shows all of the cupcakes
    Returns JSON {'cupcakes': [{id, flavor, size, rating, image_url}, ...]}"""

    cupcakes = Cupcake.query.all()

    serialized = [c.serialize() for c in cupcakes]

    return (jsonify(cupcakes=serialized), 200)


@app.get("/api/cupcakes/<int:id>")
def get_cupcake_data(id):
    """Shows data about a specific cupcake
    Returns JSON {'cupcake': {id, flavor, size, rating, image_url}}
    """

    cupcake = Cupcake.query.get_or_404(id)

    serialized = cupcake.serialize()

    return (jsonify(cupcake=serialized), 200)


@app.post("/api/cupcakes")
def create_cupcake():
    """Create a cupcake
    Sends {
            "flavor": "strawberry",
            "size": "2",
            "rating": "10"
        }
    Returns JSON {'cupcake': {id, flavor, size, rating, image_url}}
    """
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image_url = request.json.get("image_url") or None

    new_cupcake = Cupcake(flavor=flavor, size=size,
                          rating=rating, image_url=image_url)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)

@app.patch("/api/cupcakes/<int:id>")
def update_cupcake(id):
    """Updates a cupcake
    Returns JSON {cupcake: {id, flavor, size, rating, image_url}}"""

    current_cupcake = Cupcake.query.get_or_404(id)

    current_cupcake.flavor = request.json["flavor"]
    current_cupcake.size = request.json["size"]
    current_cupcake.rating = request.json["rating"]
    current_cupcake.image_url = request.json.get("image_url") or DEFAULT_URL

    db.session.commit()

    serialized = current_cupcake.serialize()

    return (jsonify(cupcake=serialized), 200)

