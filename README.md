## CUSTOMERS-SERVICE PYTHON SERVICE

This is a python service consisiting of two models, customers and orders. Customers table has the attributes id, firstname, lastname, email, phone while Orders table has the attributes id, item, quantity, amount, timestamp and customer_code.

In the Orders table, customer_code is a foreign key referencing customer.id in the Customers table. Their relationship is one to many where a customer can have many orders.

## Setup

1. Clone this repository to your local environment.
2. Go to it's directory in the terminal and run `pipenv install` to install backend dependencies.
3. After that, set the PORT to 5000 and run `export FLASK_APP=app.py` then `flask run` . This will start your flask application.
 
## Deployment Link

 - https://customers-orders-service.onrender.com


## Routes

Some of the endpoints include:

### GET /customers

```json
[
    {
    "description": "Guy law door watch conference owner. Play analysis theory.",
    "location": "St. Lucia",
    "isAvailable": false,
    "property_type": "Cottage",
    "price": 910520.0,
    "id": 1,
    "title": "7757 Obrien Radial\nLake Philip, NJ 13431",
    "image": "http://tinyurl.com/4adswm53"
  }
    
]
```

## License

This project is licesed under the MIT terms and conditions.