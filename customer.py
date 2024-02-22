from flask import Blueprint
from flask_restful import Resource, Api, abort, reqparse
from models import Customer, db
from serializers import CustomerSchema
from auth import oidc

customer_bp = Blueprint('customer', __name__)
api = Api(customer_bp)

post_args = reqparse.RequestParser()
post_args.add_argument('firstname', type=str, required=True)
post_args.add_argument('lastname', type=str, required=True)
post_args.add_argument('email', type=str, required=True)
post_args.add_argument('phone', type=str, required=True)

patch_args = reqparse.RequestParser()
patch_args.add_argument('firstname', type=str)
patch_args.add_argument('lastname', type=str)
patch_args.add_argument('email', type=str)
patch_args.add_argument('phone', type=str)

customer_schema = CustomerSchema()

class Customers(Resource):

    @oidc.require_login
    def get(self):
        customers = Customer.query.all()
        return customer_schema.dump(customers, many=True)
    
    def post(self):
        data = post_args.parse_args()

        new_customer = Customer(firstname=data['firstname'], lastname=data['lastname'], email=data['email'], phone=data['phone'])
        db.session.add(new_customer)
        db.session.commit()
        return customer_schema.dump(new_customer)

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
    
    def delete(self,id):
        customer = Customer.query.filter_by(id=id).first()
        if not customer:
            abort(404, detail=f'customer with {id=} does not exist')
        
        db.session.delete(customer)
        db.session.commit()
        return{"detail": f"customer with {id=} has been deleted successfully"}
    
api.add_resource(Customers, '/customers')
api.add_resource(CustomerById, '/customers/<int:id>')