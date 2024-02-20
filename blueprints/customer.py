from flask import Blueprint
from flask_restful import Resource, Api, abort
from models import Customer
from serializers import CustomerSchema

customer_bp = Blueprint('customer', __name__)
api = Api(customer_bp)


customer_schema = CustomerSchema()

class Customers(Resource):

    def get(self):
        customers = Customer.query.all()
        return customer_schema.dump(customers, many=True)

class CustomerById(Resource):
   
   def get(self,id):
        customer = Customer.query.get(id)
        if not customer:
            abort(404, detail=f'customer with {id=} does not exist')
        return customer_schema.dump(customer)
    
api.add_resource(Customers, '/customers')
api.add_resource(CustomerById, '/customers/<int:id>')