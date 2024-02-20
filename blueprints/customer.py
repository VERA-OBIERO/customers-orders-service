from flask import Blueprint
from flask_restful import Resource, Api, abort, reqparse
from models import Customer, db
from serializers import CustomerSchema

customer_bp = Blueprint('customer', __name__)
api = Api(customer_bp)

patch_args = reqparse.RequestParser()
patch_args.add_argument('firstname', type=str)
patch_args.add_argument('lastname', type=str)
patch_args.add_argument('email', type=str)
patch_args.add_argument('phone', type=str)

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
   
    def patch(self,id):
        customer = Customer.query.get(id)
        if not customer:
            abort(404, detail=f'customer with {id=} does not exist')
        data = patch_args.parse_args()
        print(data)
        for key,value in data.items():
            if value is None:
                continue
            setattr(customer, key, value)
        db.session.commit()

        return customer_schema.dump(customer)
    
api.add_resource(Customers, '/customers')
api.add_resource(CustomerById, '/customers/<int:id>')