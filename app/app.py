#!/usr/bin/env python3

from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/pius/Downloads/python-code-challenge-pizzas/code-challenge/app/db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Add your models here (Restaurant, Pizza, RestaurantPizza)

# Validation function for RestaurantPizza
def validate_restaurant_pizza_data(data):
    errors = []

    # Validate price
    price = data.get('price')
    if price is None or not (1 <= price <= 30):
        errors.append("Price must be between 1 and 30")

    return errors

# Routes

# GET /restaurants
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    restaurant_list = []
    for restaurant in restaurants:
        restaurant_list.append({
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address
        })
    return jsonify(restaurant_list)

# GET /restaurants/:id
@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        pizza_list = []
        for restaurant_pizza in restaurant.restaurant_pizzas:
            pizza = Pizza.query.get(restaurant_pizza.pizza_id)
            if pizza:
                pizza_list.append({
                    "id": pizza.id,
                    "name": pizza.name,
                    "ingredients": pizza.ingredients
                })
        return jsonify({
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address,
            "pizzas": pizza_list
        })
    else:
        return jsonify({"error": "Restaurant not found"}), 404

# DELETE /restaurants/:id
@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        # Check if there are associated RestaurantPizzas and delete them
        for restaurant_pizza in restaurant.restaurant_pizzas:
            db.session.delete(restaurant_pizza)

        # Delete the restaurant itself
        db.session.delete(restaurant)
        db.session.commit()
        return "", 204
    else:
        return jsonify({"error": "Restaurant not found"}), 404

# GET /pizzas
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    pizza_list = []
    for pizza in pizzas:
        pizza_list.append({
            "id": pizza.id,
            "name": pizza.name,
            "ingredients": pizza.ingredients
        })
    return jsonify(pizza_list)

# POST /restaurant_pizzas
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.json
    errors = validate_restaurant_pizza_data(data)

    if errors:
        return jsonify({"errors": errors}), 400

    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')
    price = data.get('price')

    # Check if both Pizza and Restaurant exist
    pizza = Pizza.query.get(pizza_id)
    restaurant = Restaurant.query.get(restaurant_id)

    if not pizza or not restaurant:
        return jsonify({"error": "Pizza or Restaurant not found"}), 404

    # Create RestaurantPizza
    restaurant_pizza = RestaurantPizza(
        pizza_id=pizza_id,
        restaurant_id=restaurant_id,
        price=price
    )

    db.session.add(restaurant_pizza)
    db.session.commit()
    
    return jsonify({
        "id": pizza.id,
        "name": pizza.name,
        "ingredients": pizza.ingredients
    }), 201

if __name__ == '__main__':
    app.run(port=5555)


