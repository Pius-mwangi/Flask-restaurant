from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates

app = Flask(__name__)
db = SQLAlchemy()

class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String, nullable=False)
    # Relationship definition
    pizzas = db.relationship('RestaurantPizza', back_populates='restaurant')

    @validates('name')
    def validate_name(self, key, name):
        # Rule 2: Validation for name length (less than 50 characters)
        if len(name) >= 50:
            raise ValueError("Name must be less than 50 characters")
        return name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'pizzas': [pizza.serialize() for pizza in self.pizzas]
        }

class Pizza(db.Model):
    __tablename__ = 'pizzas'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    # Relationship definition 
    restaurants = db.relationship('RestaurantPizza', back_populates='pizza')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients,
        }

class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.String, db.ForeignKey('pizzas.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)

    price = db.Column(db.Float, nullable=False)
    __table_args__ = (
        # Rule 1: CheckConstraint for price between 1 and 30
        CheckConstraint('price >= 1 and price <= 30', name='check_price_range'),
    )

    @validates('price')
    def validate_price(self, key, price):
        # Rule 1: Validation for price between 1 and 30
        if price < 1 or price > 30:
            raise ValueError("Price must be between 1 and 30")
        return price

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    pizza = db.relationship('Pizza', back_populates='restaurants')
    restaurant = db.relationship('Restaurant', back_populates='pizzas')

