from app import app, db
from models import Restaurant, Pizza, RestaurantPizza
import uuid 
# Check if the restaurants already exist in the database
with app.app_context():
    restaurant1 = Restaurant.query.filter_by(name="Dominion Pizza").first()
    restaurant2 = Restaurant.query.filter_by(name="Pizza Hut").first()

    # If the restaurants don't exist, create them
    if not restaurant1:
        restaurant1 = Restaurant(name="Dominion Pizza", address="Good Italian, Ngong Road, 5th Avenue")
        db.session.add(restaurant1)

    if not restaurant2:
        restaurant2 = Restaurant(name="Pizza Hut", address="Westgate Mall, Mwanzi Road, Nrb 100")
        db.session.add(restaurant2)

    # Create some sample pizzas with manually generated UUIDs
    pizza1 = Pizza(id=str(uuid.uuid4()), name="Cheese", ingredients="Dough, Tomato Sauce, Cheese")
    pizza2 = Pizza(id=str(uuid.uuid4()), name="Pepperoni", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")

    db.session.add(pizza1)
    db.session.add(pizza2)

    # Create some sample RestaurantPizzas (associations between restaurants and pizzas)
    restaurant_pizza1 = RestaurantPizza(restaurant=restaurant1, pizza=pizza1, price=10)
    restaurant_pizza2 = RestaurantPizza(restaurant=restaurant1, pizza=pizza2, price=12)
    restaurant_pizza3 = RestaurantPizza(restaurant=restaurant2, pizza=pizza1, price=11)

    db.session.add(restaurant_pizza1)
    db.session.add(restaurant_pizza2)
    db.session.add(restaurant_pizza3)

    # Commit the changes to the database
    db.session.commit()

print("Sample data seeded successfully.")

print("Sample data seeded successfully.")

