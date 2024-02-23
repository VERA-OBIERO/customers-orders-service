## CUSTOMERS-SERVICE PYTHON SERVICE

This is a python service consisiting of two models, customers and orders. Customers table has the attributes id, firstname, lastname, email, phone while Orders table has the attributes id, item, quantity, amount, timestamp and customer_code.

In the Orders table, customer_code is a foreign key referencing customer.id in the Customers table. Their relationship is one to many where a customer can have many orders.

## Setup

1. Clone this repository to your local environment.
2. Go to it's directory in the terminal and run `pipenv install` to install backend dependencies.
3. After that, set the PORT to 5000 and run `export FLASK_APP=app.py` then `flask run` . This will start your flask application.
 
## Deployment Link

This link will help you interact with the GET endpoints without setting up anything.

 - https://customers-orders-service.onrender.com


## Routes

Some of the endpoints include:

### GET /customers

```json
[
    {
        {
            "id": 1, 
            "firstname": "Regina", 
            "lastname": "Hope", 
            "email": "hope.reg@gmail.com", 
            "phone": "+254726799909", 
            "orders": 
                [
                    {
                        "id": 1, 
                        "item": "Carpet", 
                        "quantity": 2.0, 
                        "amount": 2000.0, 
                        "timestamp": "2024-02-23T12:09:46.459182", 
                        "customer_firstname": "Regina", 
                        "customer_lastname": "Hope"
                    }, 
                    {
                        "id": 6, 
                        "item": "Samosa", 
                        "quantity": 15.0, 
                        "amount": 1000.0, 
                        "timestamp": "2024-02-23T12:09:46.471621", 
                        "customer_firstname": "Regina", 
                        "customer_lastname": "Hope"
                    }
                ]
        }
    }
    
]
```

## Features

1. `Implement authentication and authorization via OpenID Connect.`
   The GET/customers and GET/orders end points require authentication and authorization through the Auth0 platform before accessing them.

2. `SMS alerts.`
   When an order is added through the POST/orders endpoint, an SMS is sent to the user as seen on the Africastalking sandbox simulator. The message referneces the first name of the customer making the order to alert them.

3. `Unit tests (with coverage checking).`
   In the directory tests, there is a file test_app.py that has a few unit tests to check the app. To run the tests, run the command `python -m unittest discover -s tests`. This will run all the test cases in the tests directory which is currently 1.
   You can then verify the code coverage of the tests by running `coverage run -m unittest discover -s tests` followed by `coverage report -m` to display a detailed coverage showing which parts of the code are covered by tests and which ones are not.

4. `CI + automated CD.`
   For this feature I used GitHub Actions to set up a simple pipeline that checks the code, sets up Python, installs dependencies, runs tests and deploys to Render which is the PAAS of choice


## License

This project is licesed under the MIT terms and conditions.