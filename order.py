from flask import Blueprint
from flask_restful import Resource, Api, abort, reqparse, fields
from models import Order, db, Customer
from serializers import OrderSchema
from datetime import datetime
from auth import oidc
from africastalking_helper import send_sms

order_bp = Blueprint('order', __name__)
api = Api(order_bp)


post_args = reqparse.RequestParser()
post_args.add_argument('item', type=str, required=True)
post_args.add_argument('quantity', type=float, required=True)
post_args.add_argument('amount', type=float, required=True)
post_args.add_argument('timestamp', type=datetime)
post_args.add_argument('customer_code', type=int, required=True)

patch_args = reqparse.RequestParser()
patch_args.add_argument('item', type=str)
patch_args.add_argument('quantity', type=float)
patch_args.add_argument('amount', type=float)
patch_args.add_argument('customer_code', type=int)

order_schema = OrderSchema()

class Orders(Resource):
    @oidc.require_login
    def get(self):
        orders = Order.query.all()
        return order_schema.dump(orders, many=True)
    
    def post(self):
        data = post_args.parse_args()

        timestamp_str = data.get('timestamp')
        if timestamp_str:
            timestamp = datetime.fromisoformat(timestamp_str)
        else:
            timestamp = datetime.utcnow()

        new_order = Order(
            item=data['item'], 
            quantity=data['quantity'], 
            amount=data['amount'], 
            timestamp=timestamp, 
            customer_code=data['customer_code'])
        
        customer = Customer.query.get(data['customer_code'])
        if customer:
            new_order.customer = customer  # Associate the customer with the order
        
        db.session.add(new_order)
        db.session.commit()

        #customer = Customer.query.get(data['customer_code'])
        if customer:
            message = f"Hello {customer.firstname}, your order has been placed successfully."
            response = send_sms(message, [customer.phone])
            if response and response['SMSMessageData']['Recipients'][0]['status'] == 'Success':
                print("SMS sent successfully!")
            else:
                print("Failed to send SMS!")
        
        return order_schema.dump(new_order)

class OrderById(Resource):
   
    def get(self,id):
        order = Order.query.get(id)
        if not order:
            abort(404, detail=f'order with {id=} does not exist')
        return order_schema.dump(order)
   
    def patch(self,id):
        order = Order.query.get(id)
        if not order:
            abort(404, detail=f'order with {id=} does not exist')
        data = patch_args.parse_args()
        print(data)
        for key,value in data.items():
            if value is None:
                continue
            setattr(order, key, value)
        db.session.commit()

        return order_schema.dump(order)
    
    def delete(self,id):
        order = Order.query.filter_by(id=id).first()
        if not order:
            abort(404, detail=f'order with {id=} does not exist')
        
        db.session.delete(order)
        db.session.commit()
        return{"detail": f"order with {id=} has been deleted successfully"}
    
api.add_resource(Orders, '/orders')
api.add_resource(OrderById, '/orders/<int:id>')