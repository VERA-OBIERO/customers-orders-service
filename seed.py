from models import db, Customer, Order
from datetime import datetime
from app import app

with app.app_context():

    # Delete all existing data from tables
    db.session.query(Customer).delete()
    db.session.query(Order).delete()
    db.session.commit()

    # Create customers
    customer1 = Customer(firstname='Regina', lastname='Hope', email='hope@example.com', phone='0723456789')
    customer2 = Customer(firstname='Jacob', lastname='Smith', email='smith@example.com', phone='0798765432')
    
    # Add customers to session
    print("Seeding customers data")
    db.session.add_all([customer1, customer2])
    db.session.commit()

    # Create orders
    order1 = Order(item='Carpet', quantity=2, amount=2000.00, timestamp=datetime.now(), customer_code=customer1.id)
    order2 = Order(item='Sufuria', quantity=1, amount=150.00, timestamp=datetime.now(), customer_code=customer2.id)
    order3 = Order(item='Cupcakes', quantity=1, amount=10.00, timestamp=datetime.now(), customer_code=customer1.id)
    
    # Add orders to session
    print("Seeding orders data")
    db.session.add_all([order1, order2, order3])
    db.session.commit()

    print("Done!")

