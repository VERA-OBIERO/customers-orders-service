from flask_marshmallow import Marshmallow
from models import Customer, Order

ma = Marshmallow()

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer

    id = ma.auto_field()
    firstname = ma.auto_field()
    lastname = ma.auto_field()
    email= ma.auto_field()
    phone= ma.auto_field() 

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order

    id = ma.auto_field()
    item = ma.auto_field()
    quantity = ma.auto_field()
    amount= ma.auto_field()
    timestamp= ma.auto_field()
    customer_code= ma.auto_field()