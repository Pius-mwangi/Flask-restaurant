#!/usr/bin/env python3

from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/pius/Downloads/python-code-challenge-pizzas/code-challenge/app/db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)



def validate_restaurant_pizza_data(data):
    errors = []
   
    # Example: Check if 'pizza_id', 'restaurant_id', and 'price' are present and valid
    if 'pizza_id' not in data or 'restaurant_id' not in data or 'price' not in data:
        errors.append("Missing required fields: pizza_id, restaurant_id, price")
    # Additional validation checks can be added
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

    # Create a custom response with JSON data and a 200 (OK) status code
    response = make_response(jsonify(restaurant_list), 200)
    return response


# GET /restaurants/:id
@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        pizza_list = []
        for restaurant_pizza in restaurant.pizzas: 
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
        # Log restaurant and associated pizza IDs
        print(f"Deleting Restaurant ID: {restaurant.id}")
        for restaurant_pizza in restaurant.restaurant_pizzas:
            print(f"Deleting RestaurantPizza ID: {restaurant_pizza.id}")

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

    # Validate the JSON data
    errors = validate_restaurant_pizza_data(data)
    if errors:
        return jsonify({"errors": errors}), 400

    # Extract data from the JSON
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')
    price = data.get('price')

    # Check if both Pizza and Restaurant exist
    pizza = Pizza.query.get(pizza_id)
    restaurant = Restaurant.query.get(restaurant_id)

    if not pizza:
        return jsonify({"error": "Pizza not found"}), 404
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    # Create RestaurantPizza
    restaurant_pizza = RestaurantPizza(
        pizza_id=pizza_id,
        restaurant_id=restaurant_id,
        price=price
    )

    db.session.add(restaurant_pizza)
    db.session.commit()

    # Return a response with the newly created RestaurantPizza's details
    return jsonify({
        "id": restaurant_pizza.id,
        "pizza_id": pizza.id,
        "restaurant_id": restaurant.id,
        "price": restaurant_pizza.price
    }), 201

if __name__ == '__main__':
    app.run(debug=True, port=5555)


