"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Vehicle, Species, Favorite, Gender
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    #app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route ('/character', methods = ['GET'])
def get_all_characters ():
   characters = Character.query.all()
   return jsonify ([character.serialize() for character in characters]), 200

@app.route ('/character/<int:character_id>', methods = ['GET'])
def get_character (character_id):
    character = Character.query.get (character_id)
    if character is None:
        raise APIException ("Character is not found", status_code = 404)
    return jsonify (character.serialize ()), 200

@app.route ('/character', methods = ['POST'])
def add_character ():
    body = request.get_json()

    planet = Planet.query.get(body["planet_id"])
    if planet is None:
        raise APIException("Planet not found", status_code=404)

    species = Species.query.get(body["species_id"])
    if species is None:
        raise APIException("Species not found", status_code=404)

    new_character = Character(
        name=body["name"],
        description=body["description"],
        planet_id=body["planet_id"],
        species_id=body["species_id"],
        gender=Gender(body["gender"])
    )

    try:
        db.session.add (new_character)
        db.session.commit ()
    
    except Exception as e:
        raise APIException (f"Failed to create character", status_code = 500) from e

    return jsonify ({
        "msg": "Character was added succesfully",
        "character": new_character.serialize ()
    }), 201

@app.route ('/planet', methods = ['GET'])
def get_all_planets ():
    planets = Planet.query.all ()
    return jsonify ([planet.serialize () for planet in planets]), 200

@app.route ('/planet/<int:planet_id>', methods = ['GET'])
def get_planet (planet_id):
    planet = Planet.query.get (planet_id)
    if planet is None:
        raise APIException ("Planet is not found", status_code = 404)
    return jsonify (planet.serialize()), 200

@app.route('/species', methods=['GET'])
def get_all_species():
    species = Species.query.all()
    return jsonify([specie.serialize() for specie in species]), 200

@app.route ('/user', methods = ['GET'])
def get_all_users ():
    users = User.query.all ()
    return jsonify ([user.serialize () for user in users]), 200

@app.route ('/user/<int:user_id>/favorite', methods = ['GET'])
def get_all_favorites (user_id):
    favorites = Favorite.query.filter_by (user_id = user_id).all ()
    return jsonify ([favorite.serialize () for favorite in favorites]), 200

@app.route ('/favorite/planet/<int:planet_id>', methods = ['POST'])
def add_favorite_planet (planet_id):
    planet = Planet.query.get (planet_id)

    if planet is None:
        raise APIException ('Planet not found', status_code = 404)

    new_favorite = Favorite (user_id = 1, planet_id = planet_id)

    try:
        db.session.add (new_favorite)
        db.session.commit ()
    
    except Exception as e:
        raise APIException (f"Failed to add planet to favorites", status_code = 500) from e

    return jsonify ({
        "msg": "Planet was added succesfully",
        "favorite": new_favorite.serialize ()
    }), 201

@app.route ('/favorite/character/<int:character_id>', methods = ['POST'])
def add_favorite_character (character_id):
    character = Character.query.get (character_id)

    if character is None:
        raise APIException ('Character not found', status_code = 404)

    new_favorite = Favorite (user_id = 1, character_id = character_id)

    try:
        db.session.add (new_favorite)
        db.session.commit ()
    
    except Exception as e:
        raise APIException (f"Failed to add character to favorites", status_code = 500) from e

    return jsonify ({
        "msg": "Character was added succesfully",
        "favorite": new_favorite.serialize ()
    }), 201

@app.route ('/favorite/planet/<int:planet_id>', methods = ['DELETE'])
def delete_favorite_planet (planet_id):
    searched_favorite_planet = Favorite.query.filter_by (planet_id = planet_id, user_id = 1).first()

    if not searched_favorite_planet:
        raise APIException (f"Favorite planet is not found", status_code = 404)
    
    try:
        db.session.delete (searched_favorite_planet)
        db.session.commit ()
    
    except Exception as e:
        raise APIException (f"Something wrong happened", status_code = 500) from e

    return jsonify({
        "msg": "Favorite planet deleted"
    }), 200

@app.route ('/favorite/character/<int:character_id>', methods = ['DELETE'])
def delete_favorite_character (character_id):
    searched_favorite_character = Favorite.query.filter_by (character_id = character_id, user_id = 1).first()

    if not searched_favorite_character:
        raise APIException (f"Favorite character not found", status_code = 404)
    
    try:
        db.session.delete (searched_favorite_character)
        db.session.commit ()
    
    except Exception as e:
        raise APIException (f"Something wrong happened", status_code = 500) from e

    return jsonify({
        "msg": "Favorite character deleted"
    }), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    #app.run(host='0.0.0.0', port=PORT, debug=False)
    app.run(host='0.0.0.0', port=PORT, debug=True)