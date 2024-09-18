from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# Crear una instancia de SQLAlchemy
db = SQLAlchemy()

# Modelo User
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username
        }

# Modelo Character
class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

# Modelo Planet
class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

# Modelo Vehicle
class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

# Modelo Favorite
class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=True)

    user = db.relationship('User', backref=db.backref('favorites', lazy=True))
    character = db.relationship('Character', backref=db.backref('favorites', lazy=True))
    planet = db.relationship('Planet', backref=db.backref('favorites', lazy=True))
    vehicle = db.relationship('Vehicle', backref=db.backref('favorites', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "vehicle_id": self.vehicle_id
        }
