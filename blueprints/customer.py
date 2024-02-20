from flask import Blueprint
from flask_restful import Resource, Api
from models import Customer
from serializers import CustomerSchema

customer_bp = Blueprint('customer', __name__)
api = Api(customer_bp)


customer_schema = CustomerSchema()

class Customers(Resource):

    def get(self):
        customers = Customer.query.all()
        return customer_schema.dump(customers, many=True)
    
api.add_resource(Customers, '/customers') 