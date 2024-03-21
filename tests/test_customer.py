import unittest
from unittest.mock import patch
from app import app, db
from models import Customer
from customer import post_args, patch_args, Customers, CustomerById
from flask import json

class TestCustomerEndpoints(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_customer(self):
        with app.app_context():
            customer_data = {
                'firstname': 'John',
                'lastname': 'Doe',
                'email': 'john@example.com',
                'phone': '123456789'
            }
            response = self.app.post('/customers', json=customer_data)
            self.assertEqual(response.status_code, 200)
            self.assertIsNotNone(Customer.query.filter_by(firstname='John').first())

    def test_create_customer_missing_fields(self):
        customer_data = {
            # Missing 'firstname' intentionally
            'lastname': 'Doe',
            'email': 'john@example.com',
            'phone': '123456789'
        }
        response = self.app.post('/customers', json=customer_data)
        self.assertEqual(response.status_code, 400)

    def test_get_customer_by_id(self):
        with app.app_context():
            customer = Customer(firstname='John', lastname='Doe', email='john@example.com', phone='123456789')
            db.session.add(customer)
            db.session.commit()

            response = self.app.get('/customers/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['firstname'], 'John')

    def test_get_customer_by_invalid_id(self):
        response = self.app.get('/customers/999')  # Assuming customer with ID 999 does not exist
        self.assertEqual(response.status_code, 404)

    def test_patch_customer_by_id(self):
        with app.app_context():
            customer = Customer(firstname='John', lastname='Doe', email='john@example.com', phone='123456789')
            db.session.add(customer)
            db.session.commit()

            update_data = {'firstname': 'Jane'}
            response = self.app.patch('/customers/1', json=update_data)
            self.assertEqual(response.status_code, 200)
            updated_customer = Customer.query.get(1)
            self.assertEqual(updated_customer.firstname, 'Jane')

    def test_patch_customer_with_invalid_id(self):
        update_data = {'firstname': 'Jane'}
        response = self.app.patch('/customers/999', json=update_data)  # Assuming customer with ID 999 does not exist
        self.assertEqual(response.status_code, 404)

    def test_delete_customer_by_id(self):
        with app.app_context():
            customer = Customer(firstname='John', lastname='Doe', email='john@example.com', phone='123456789')
            db.session.add(customer)
            db.session.commit()

            response = self.app.delete('/customers/1')
            self.assertEqual(response.status_code, 200)
            self.assertIsNone(Customer.query.get(1))

    def test_delete_customer_with_invalid_id(self):
        response = self.app.delete('/customers/999')  # Assuming customer with ID 999 does not exist
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
