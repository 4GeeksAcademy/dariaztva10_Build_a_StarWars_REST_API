import os
from admin import setup_admin
from flask_cors import CORS
from utils import APIException, generate_sitemap
from flask import Flask, request, jsonify
from models import db, User, Character, Planet, Vehicle, Favorite
from flask_migrate import Migrate

app = Flask(__name__)
app.url_map.strict_slashes = False

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de la base de datos y las migraciones
db.init_app(app)
migrate = Migrate(app, db)

# Habilitar CORS
CORS(app)

# Configuración del panel de administración
setup_admin(app)

# Manejador de errores personalizados
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Ruta raíz para el mapa del sitio
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Endpoint para manejar usuarios
@app.route('/user', methods=['GET', "POST"])
def handle_user():
    if request.method == 'GET':
        # Listar todos los usuarios
        users = User.query.all()
        users = list(map(lambda user: user.to_dict(), users))
        return jsonify({"data": users}), 200
    elif request.method == 'POST':
        # Crear un nuevo usuario
        user = User()
        data = request.get_json()
        user.name = data["name"]
        user.username = data["username"]
        user.password = data["password"]

        db.session.add(user)
        db.session.commit()

        return jsonify({"msg": "user created"}), 200

# Endpoint para manejar un usuario específico por id
@app.route("/user/<int:id>", methods=["GET", "PUT", "DELETE"])
def update_user(id):
    if request.method == 'GET':
        # Obtener detalles de un usuario
        user = User.query.get(id)
        if user:
            return jsonify(user.to_dict()), 200
        return jsonify({"msg": "user not found"}), 404
    elif request.method == 'PUT':
        # Actualizar datos de un usuario
        user = User.query.get(id)
        if user:
            data = request.get_json()
            user.name = data["name"]
            user.username = data["username"]
            db.session.commit()
            return jsonify({"msg": "user updated"}), 200
        return jsonify({"msg": "user not found"}), 404
    elif request.method == 'DELETE':
        # Eliminar un usuario
        user = User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"msg": "user deleted"}), 202
        return jsonify({"msg": "user not found"}), 404

# Endpoint para manejar personajes
@app.route('/character', methods=['GET', "POST"])
def handle_character():
    if request.method == 'GET':
        # Listar todos los personajes
        characters = Character.query.all()
        characters = list(map(lambda character: character.to_dict(), characters))
        return jsonify({"data": characters}), 200
    elif request.method == 'POST':
        # Crear un nuevo personaje
        character = Character()
        data = request.get_json()
        character.name = data["name"]
        db.session.add(character)
        db.session.commit()
        return jsonify({"msg": "character created"}), 200

# Endpoint para manejar un personaje específico por id
@app.route("/character/<int:id>", methods=["PUT", "DELETE"])
def update_character(id):
    if request.method == 'PUT':
        # Actualizar datos de un personaje
        character = Character.query.get(id)
        if character:
            data = request.get_json()
            character.name = data["name"]
            db.session.commit()
            return jsonify({"msg": "character updated"}), 200
        return jsonify({"msg": "character not found"}), 404
    elif request.method == 'DELETE':
        # Eliminar un personaje
        character = Character.query.get(id)
        if character:
            db.session.delete(character)
            db.session.commit()
            return jsonify({"msg": "character deleted"}), 202
        return jsonify({"msg": "character not found"}), 404

# Endpoint para manejar planetas
@app.route('/planet', methods=['GET', "POST"])
def handle_planet():
    if request.method == 'GET':
        # Listar todos los planetas
        planets = Planet.query.all()
        planets = list(map(lambda planet: planet.to_dict(), planets))
        return jsonify({"data": planets}), 200
    elif request.method == 'POST':
        # Crear un nuevo planeta
        planet = Planet()
        data = request.get_json()
        planet.name = data["name"]
        db.session.add(planet)
        db.session.commit()
        return jsonify({"msg": "planet created"}), 200

# Endpoint para manejar un planeta específico por id
@app.route("/planet/<int:id>", methods=["PUT", "DELETE"])
def update_planet(id):
    if request.method == 'PUT':
        # Actualizar datos de un planeta
        planet = Planet.query.get(id)
        if planet:
            data = request.get_json()
            planet.name = data["name"]
            db.session.commit()
            return jsonify({"msg": "planet updated"}), 200
        return jsonify({"msg": "planet not found"}), 404
    elif request.method == 'DELETE':
        # Eliminar un planeta
        planet = Planet.query.get(id)
        if planet:
            db.session.delete(planet)
            db.session.commit()
            return jsonify({"msg": "planet deleted"}), 202
        return jsonify({"msg": "planet not found"}), 404

# Endpoint para manejar vehículos
@app.route('/vehicle', methods=['GET', "POST"])
def handle_vehicle():
    if request.method == 'GET':
        # Listar todos los vehículos
        vehicles = Vehicle.query.all()
        vehicles = list(map(lambda vehicle: vehicle.to_dict(), vehicles))
        return jsonify({"data": vehicles}), 200
    elif request.method == 'POST':
        # Crear un nuevo vehículo
        vehicle = Vehicle()
        data = request.get_json()
        vehicle.name = data["name"]
        db.session.add(vehicle)
        db.session.commit()
        return jsonify({"msg": "vehicle created"}), 200

# Endpoint para manejar un vehículo específico por id
@app.route("/vehicle/<int:id>", methods=["PUT", "DELETE"])
def update_vehicle(id):
    if request.method == 'PUT':
        # Actualizar datos de un vehículo
        vehicle = Vehicle.query.get(id)
        if vehicle:
            data = request.get_json()
            vehicle.name = data["name"]
            db.session.commit()
            return jsonify({"msg": "vehicle updated"}), 200
        return jsonify({"msg": "vehicle not found"}), 404
    elif request.method == 'DELETE':
        # Eliminar un vehículo
        vehicle = Vehicle.query.get(id)
        if vehicle:
            db.session.delete(vehicle)
            db.session.commit()
            return jsonify({"msg": "vehicle deleted"}), 202
        return jsonify({"msg": "vehicle not found"}), 404

# Endpoint para manejar los favoritos de un usuario
@app.route('/user/<int:id>/favorite', methods=['GET'])
def handle_favorite(id):
    # Listar todos los favoritos de un usuario
    favorites = Favorite.query.filter_by(user_id=id).all()
    favorites = list(map(lambda favorite: favorite.to_dict(), favorites))
    return jsonify({"data": favorites}), 200

# Endpoint para crear un nuevo favorito
@app.route('/favorite', methods=["POST"])
def create_favorite():
    data = request.get_json()
    favorite = Favorite()
    user_id = data["user_id"]
    character_id = data.get("character_id")
    planet_id = data.get("planet_id")
    vehicle_id = data.get("vehicle_id")
    
    # Verificar existencia del usuario
    user_exists = User.query.get(user_id)
    if not user_exists:
        return jsonify({"msg": "user not found"}), 404

    # Verificar existencia del personaje, planeta o vehículo
    if character_id:
        character_exists = Character.query.get(character_id)
        if not character_exists:
            return jsonify({"msg": "character not found"}), 404
        favorite.user_character = character_id
    if planet_id:
        planet_exists = Planet.query.get(planet_id)
        if not planet_exists:
            return jsonify({"msg": "planet not found"}), 404
        favorite.user_planet = planet_id
    if vehicle_id:
        vehicle_exists = Vehicle.query.get(vehicle_id)
        if not vehicle_exists:
            return jsonify({"msg": "vehicle not found"}), 404
        favorite.user_vehicle = vehicle_id

    favorite.user_id = user_id
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"msg": "favorite created"}), 200

# Endpoint para eliminar un favorito
@app.route('/favorite/<int:id>', methods=["DELETE"])
def delete_favorite(id):
    favorite = Favorite.query.get(id)
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"msg": "favorite deleted"}), 202
    return jsonify({"msg": "favorite not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
