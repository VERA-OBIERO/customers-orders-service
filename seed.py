from models import db, Customer, Order
from datetime import datetime
from app import app

with app.app_context():

    # Delete all existing data from tables
    db.session.query(Customer).delete()
    db.session.query(Order).delete()
    db.session.commit()

    # Create customers
    customer1 = Customer(firstname='Regina', lastname='Hope', email='hope.reg@gmail.com', phone='+254726799909')
    customer2 = Customer(firstname='Tracy', lastname='Morgan', email='morg.tracy@gmail.com', phone='+254722346098')
    customer3 = Customer(firstname='Lucy', lastname='Smith', email='smith.lucy@gmail.com', phone='+254725670098')
    customer4 = Customer(firstname='Fidel', lastname='Castro', email='fidcastro@gmail.com', phone='+254720020098')
    customer5 = Customer(firstname='Vera', lastname='Shelly', email='vera.shelly@gmail.com', phone='+254729735014')
    
    # Add customers to session
    print("Seeding customers data")
    db.session.add_all([customer1, customer2, customer3, customer4, customer5])
    db.session.commit()

    # Create orders
    order1 = Order(item='Carpet', quantity=2, amount=2000.00, timestamp=datetime.now(), customer_code=customer1.id)
    order2 = Order(item='Sufuria', quantity=1, amount=1500.00, timestamp=datetime.now(), customer_code=customer2.id)
    order3 = Order(item='Cupcakes', quantity=10, amount=100.00, timestamp=datetime.now(), customer_code=customer3.id)
    order4 = Order(item='Towels', quantity=3, amount=1800.00, timestamp=datetime.now(), customer_code=customer4.id)
    order5 = Order(item='Fries', quantity=5, amount=500.00, timestamp=datetime.now(), customer_code=customer5.id)
    order6 = Order(item='Samosa', quantity=15, amount=1000.00, timestamp=datetime.now(), customer_code=customer1.id)
    order7 = Order(item='Brooms', quantity=4, amount=1750.00, timestamp=datetime.now(), customer_code=customer3.id)
    order8 = Order(item='Sunglasses', quantity=1, amount=2500.00, timestamp=datetime.now(), customer_code=customer5.id)
    
    # Add orders to session
    print("Seeding orders data")
    db.session.add_all([order1, order2, order3, order4, order5, order6, order7, order8])
    db.session.commit()

    print("Done!")

