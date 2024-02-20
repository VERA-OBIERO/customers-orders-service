from flask_marshmallow import Marshmallow
from models import Customer

ma = Marshmallow()

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer

    id = ma.auto_field()
    firstname = ma.auto_field()
    lastname = ma.auto_field()
    email= ma.auto_field()
    phone= ma.auto_field() 