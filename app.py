"""Flask app for Cupcakes"""
import os

from flask import Flask, jsonify, request, render_template

from models import connect_db, Cupcake, db, DEFAULT_URL

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///flask_cupcakes")

connect_db(app)


@app.get("/api/cupcakes")
def get_all_cupcakes_data():
    """Shows all of the cupcakes
    Returns JSON {'cupcakes': [{id, flavor, size, rating, image_url}, ...]}
    """

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
    Returns JSON {cupcake: {id, flavor, size, rating, image_url}}
    """

    current_cupcake = Cupcake.query.get_or_404(id)

    current_cupcake.flavor = request.json.get(
        "flavor", current_cupcake.flavor)

    current_cupcake.size = request.json.get(
        "size", current_cupcake.size)

    current_cupcake.rating = request.json.get(
        "rating", current_cupcake.rating)

    current_cupcake.image_url = request.json.get(
        "image_url", current_cupcake.image_url) or DEFAULT_URL

    db.session.commit()

    serialized = current_cupcake.serialize()

    return (jsonify(cupcake=serialized), 200)


@app.delete("/api/cupcakes/<int:id>")
def delete_cupcake(id):
    """Deletes a cupcake
     Returns JSON {"deleted": id}
    """

    current_cupcake = Cupcake.query.get_or_404(id)

    db.session.delete(current_cupcake)
    db.session.commit()

    return (jsonify({"deleted": id}), 200)


@app.get("/")
def render_homepage():
    """Shows a form to add a cupcake and list of cupcakes at the homepage"""

    return render_template('home.html')