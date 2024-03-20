import unittest
from unittest.mock import patch
from app import app, db
from models import Order, Customer
from order import post_args, patch_args, Orders, OrderById
from datetime import datetime
from flask import json

class TestOrderEndpoints(unittest.TestCase):
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

    def test_create_order(self):
        order_data = {
            'item': 'Test Item',
            'quantity': 2,
            'amount': 50.0,
            'customer_code': 1  # Assuming customer with ID 1 exists
        }
        response = self.app.post('/orders', json=order_data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(Order.query.filter_by(item='Test Item').first())

    def test_create_order_missing_fields(self):
        order_data = {
            # Missing 'item' field intentionally
            'quantity': 2,
            'amount': 50.0,
            'customer_code': 1
        }
        response = self.app.post('/orders', json=order_data)
        self.assertEqual(response.status_code, 400)

    def test_get_order_by_id(self):
        order = Order(item='Test Item', quantity=2, amount=50.0, customer_code=1)
        db.session.add(order)
        db.session.commit()

        response = self.app.get('/orders/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['item'], 'Test Item')

    def test_get_order_by_invalid_id(self):
        response = self.app.get('/orders/999')  # Assuming order with ID 999 does not exist
        self.assertEqual(response.status_code, 404)

    def test_patch_order_by_id(self):
        order = Order(item='Test Item', quantity=2, amount=50.0, customer_code=1)
        db.session.add(order)
        db.session.commit()

        update_data = {'item': 'Updated Item'}
        response = self.app.patch('/orders/1', json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_order = Order.query.get(1)
        self.assertEqual(updated_order.item, 'Updated Item')

    def test_patch_order_with_invalid_id(self):
        update_data = {'item': 'Updated Item'}
        response = self.app.patch('/orders/999', json=update_data)  # Assuming order with ID 999 does not exist
        self.assertEqual(response.status_code, 404)

    def test_delete_order_by_id(self):
        order = Order(item='Test Item', quantity=2, amount=50.0, customer_code=1)
        db.session.add(order)
        db.session.commit()

        response = self.app.delete('/orders/1')
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(Order.query.get(1))

    def test_delete_order_with_invalid_id(self):
        response = self.app.delete('/orders/999')  # Assuming order with ID 999 does not exist
        self.assertEqual(response.status_code, 404)


class TestSMSNotifications(unittest.TestCase):
    @patch('order.send_sms')
    def test_send_sms_on_order_placement(self, mock_send_sms):
        order_data = {
            'item': 'Test Item',
            'quantity': 2,
            'amount': 50.0,
            'customer_code': 1  # Assuming customer with ID 1 exists
        }
        with app.app_context():
            response = Orders().post()
            self.assertEqual(response.status_code, 200)
            mock_send_sms.assert_called_once()


if __name__ == '__main__':
    unittest.main()

