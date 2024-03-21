import unittest
from app import app, db
from unittest.mock import patch, MagicMock
from africastalking_helper import send_sms
from models import Order, Customer

class TestApp(unittest.TestCase):
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

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Hello, World!')

# class TestAfricaTalkingHelper(unittest.TestCase):

#     @patch('africastalking.SMS')
#     def test_send_sms_success(self, mock_sms):
#         mock_response = {'SMSMessageData': {'Message': 'Sent to 1/1 Total Cost: KES 0.8000 Message parts: 1', 'Recipients': [{'cost': 'KES 0.8000', 'messageId': 'ATXid_6bbc999c9658bcc504f22abea1c5164b', 'number': '+254723456789', 'status': 'Success', 'statusCode': 101}]}}
#        # {'SMSMessageData': {'Recipients': [{'number': '+254723456789', 'status': 'Success'}]}}
#         mock_sms.send.return_value = mock_response

#         message = "Test message"
#         recipients = ["+254723456789"]

#         response = send_sms(message, recipients)

#         self.assertIsNotNone(response)
#         self.assertEqual(response, mock_response)

#     @patch('africastalking.SMS')
#     def test_send_sms_failure(self, mock_sms):
#         mock_sms.send.side_effect = Exception("Test exception")

#         message = "Test message"
#         recipients = ["+254723456789"]

#         response = None
#         #send_sms(message, recipients)

#         self.assertIsNone(response)


if __name__ == '__main__':
    unittest.main()
