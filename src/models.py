from enum import Enum as pyEnum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped [str] = mapped_column (String (20), nullable = False)
    surname: Mapped [str] = mapped_column (String (20), nullable = False)
    username: Mapped [str] = mapped_column (String (10), unique = True, nullable = False)
    email: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String (20), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "username": self.username,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planet (db.Model):
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped [str] = mapped_column (String (20), nullable = False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class Gender (pyEnum):
    Female = 1
    Male = 2

class Species (db.Model):
    __tablename__ = "species"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped [str] = mapped_column (String (20), nullable = False)
    language: Mapped [str] = mapped_column (String(20), nullable = True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "language": self.language
        }

class Character (db.Model):
    __tablename__ = "character"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped [str] = mapped_column (String (20), nullable = False)
    description: Mapped [str] = mapped_column (String (100), nullable=True)

    planet_id: Mapped [int]= mapped_column (ForeignKey ("planet.id"))
    planet: Mapped [Planet] = relationship ("Planet")

    species_id: Mapped [int]= mapped_column (ForeignKey ("species.id"))
    species: Mapped [Species] = relationship ("Species")

    gender: Mapped [Gender] = mapped_column (Enum (Gender))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "descripcion": self.description,
            "planet": {
                "id": self.planet.id,
                "name": self.planet.name,
            } if self.planet else None,
            "species": {
                "id": self.species.id,
                "name": self.species.name
            } if self.species else None,
            "gender": self.gender.value if self.gender else None
        }

class Vehicle (db.Model):
    __tablename__ = "vehicle"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped [str] = mapped_column (String (20), nullable = False)
    description: Mapped [str] = mapped_column (String (100), nullable = True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

class Favorite (db.Model):
    __tablename__ = "favorite"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped [int]= mapped_column (ForeignKey ("user.id"))
    user: Mapped [User] = relationship ()

    character_id: Mapped [int] = mapped_column (ForeignKey ("character.id"), nullable=True)
    character: Mapped [Character] = relationship ()

    planet_id: Mapped [int] = mapped_column (ForeignKey ("planet.id"), nullable=True)
    planet: Mapped [Planet] = relationship ()

    vehicle_id: Mapped [int] = mapped_column (ForeignKey ("vehicle.id"), nullable=True)
    vehicle: Mapped [Vehicle] = relationship ()

    def serialize(self):
        return {
            "id": self.id,
            "user": {
                "id":self.user.id,
                "name": self.user.name,
            } if self.user else None,
            "character": {
                "id": self.character.id,
                "name": self.character.name
            } if self.character else None,
            "planet": {
                "id": self.planet.id,
                "name": self.planet.name
            } if self.planet else None,
            "vehicle": {
                "id": self.vehicle.id,
                "name": self.vehicle.name
            } if self.vehicle else None,
        }