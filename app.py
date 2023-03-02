"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template, redirect
from models import db, connect_db, Cupcake
from forms import CupcakeForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "secretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.app_context().push()

connect_db(app)

@app.route('/')
def index_page():
    """Renders html template that includes some JS - NOT PART OF JSON API"""
    #cupcakes = Cupcake.query.all()
    form = CupcakeForm()

    return render_template('index.html', form=form)


# *****************************
# RESTFUL CUPCAKES JSON API
# *****************************

@app.route('/api/cupcakes')
def list_all_cupcakes():
    """Return JSON {'cupcakes':[{id, flavor, size,...},...]}"""

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.route('/api/cupcakes/<int:cupcake_id>')
def list_single_cupcake(cupcake_id):
    """Return JSON {'cupcake':{id, flavor, size, ...}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/search')
def list_searched_cupcakes():
    """Return JSON {'cupcakes':[{id, flavor, size,...},...]}"""

    search = request.args.get("search")
    cupcakes = Cupcake.query.filter(Cupcake.flavor.ilike(search))
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Create cupcake from json data & return it
    
    Return JSON {'cupcake':{id,flavor,size,...}}
    """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    # Return w/status code 201 --- return tuple (json, status)
    return ( jsonify(cupcake=new_cupcake.serialize()), 201 )


@app.route('/api/cupcakes/<int:cupcake_id>/edit', methods=["PATCH"])
def edit_cupcake(cupcake_id):

    # import pdb
    # set.pdb()
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    form = CupcakeForm(obj=cupcake)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())



@app.route('/api/cupcakes/<int:cupcake_id>/edit', methods=["GET"])
def update_cupcake(cupcake_id):
    """
    Show cupcake edit page
    Updates a particular cupcake and responds w/ JSON of that update cupcake
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    form = CupcakeForm(obj=cupcake)

    return render_template("edit_cupcake.html", form=form, id=cupcake_id)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete a particular cupcake."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")

