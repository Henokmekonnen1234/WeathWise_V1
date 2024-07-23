WealthWise API
Overview
WealthWise API is a backend service for the WealthWise application, designed to manage user registration, login, profile management, transaction handling, and more. The API is built using Flask, Flask-JWT-Extended for authentication, and MongoDB for database storage. It also includes utilities for password encryption and validation.

Table of Contents
Installation
Configuration
Usage
API Endpoints
User Endpoints
Transaction Endpoints
Documentation
Contributing
License
Installation
Prerequisites
Python 3.7 or higher
MongoDB
Pipenv (optional but recommended for virtual environment management)
Steps
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/wealthwise-api.git
cd wealthwise-api
Create and activate a virtual environment:

bash
Copy code
pipenv shell
Install the dependencies:

bash
Copy code
pipenv install
Set up environment variables:
Create a .env file in the project root and add the following variables:

makefile
Copy code
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DB=wealthwise
SECRET_KEY=your_secret_key
Run the application:

bash
Copy code
flask run
Configuration
The application uses environment variables for configuration. You can set these in a .env file in the project root:

MONGO_HOST: MongoDB host (default: localhost)
MONGO_PORT: MongoDB port (default: 27017)
MONGO_DB: MongoDB database name (default: wealthwise)
SECRET_KEY: Secret key for JWT token encryption
Usage
Running the Server
bash
Copy code
flask run
The server will start on http://localhost:5000.

Running Tests
bash
Copy code
pytest
API Endpoints
User Endpoints
Register a User
URL: /register
Method: POST
Description: Register a new user.
Request:
json
Copy code
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "username": "johndoe",
    "password": "securepassword"
}
Response:
json
Copy code
{
    "_id": "user_id",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "username": "johndoe",
    "created_date": "2024-07-01T00:00:00.000000",
    "updated_date": "2024-07-01T00:00:00.000000"
}
Login
URL: /login
Method: POST
Description: Authenticate a user and return a JWT token.
Request:
json
Copy code
{
    "username": "johndoe",
    "password": "securepassword"
}
Response:
json
Copy code
{
    "token": "jwt_token"
}
Get User Profile
URL: /user
Method: GET
Description: Retrieve the user profile information.
Headers:
Authorization: Bearer <JWT_TOKEN>
Response:
json
Copy code
{
    "_id": "user_id",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "username": "johndoe",
    "created_date": "2024-07-01T00:00:00.000000",
    "updated_date": "2024-07-01T00:00:00.000000"
}
Update User Profile
URL: /user
Method: PUT
Description: Update the user profile information.
Headers:
Authorization: Bearer <JWT_TOKEN>
Request:
json
Copy code
{
    "first_name": "John",
    "last_name": "Doe"
}
Response:
json
Copy code
{
    "_id": "user_id",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "username": "johndoe",
    "created_date": "2024-07-01T00:00:00.000000",
    "updated_date": "2024-07-01T00:00:00.000000"
}
Delete User
URL: /user
Method: DELETE
Description: Delete the user account.
Headers:
Authorization: Bearer <JWT_TOKEN>
Response:
json
Copy code
{
    "message": "User deleted successfully."
}
Transaction Endpoints
Create Transaction
URL: /transactions
Method: POST
Description: Create a new transaction.
Headers:
Authorization: Bearer <JWT_TOKEN>
Request:
json
Copy code
{
    "user_id": "user_id",
    "amount": 100.0,
    "type": "expense",
    "category": "food",
    "description": "Dinner at restaurant"
}
Response:
json
Copy code
{
    "_id": "transaction_id",
    "user_id": "user_id",
    "amount": 100.0,
    "type": "expense",
    "category": "food",
    "description": "Dinner at restaurant",
    "created_date": "2024-07-01T00:00:00.000000",
    "updated_date": "2024-07-01T00:00:00.000000"
}
Get Transactions
URL: /transactions
Method: GET
Description: Retrieve all transactions for a user.
Headers:
Authorization: Bearer <JWT_TOKEN>
Response:
json
Copy code
[
    {
        "_id": "transaction_id",
        "user_id": "user_id",
        "amount": 100.0,
        "type": "expense",
        "category": "food",
        "description": "Dinner at restaurant",
        "created_date": "2024-07-01T00:00:00.000000",
        "updated_date": "2024-07-01T00:00:00.000000"
    },
    ...
]
Update Transaction
URL: /transactions/<transaction_id>
Method: PUT
Description: Update a transaction.
Headers:
Authorization: Bearer <JWT_TOKEN>
Request:
json
Copy code
{
    "amount": 120.0,
    "description": "Updated description"
}
Response:
json
Copy code
{
    "_id": "transaction_id",
    "user_id": "user_id",
    "amount": 120.0,
    "type": "expense",
    "category": "food",
    "description": "Updated description",
    "created_date": "2024-07-01T00:00:00.000000",
    "updated_date": "2024-07-01T00:00:00.000000"
}
Delete Transaction
URL: /transactions/<transaction_id>
Method: DELETE
Description: Delete a transaction.
Headers:
Authorization: Bearer <JWT_TOKEN>
Response:
json
Copy code
{
    "message": "Transaction deleted successfully."
}
Documentation
Swagger documentation is available for all API endpoints. You can access it by navigating to http://localhost:5000/apidocs after starting the server.

You can also access individual Swagger YAML files directly via URLs like http://localhost:5000/documentation/user/register.yml.

Contributing
We welcome contributions! Please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes.
Commit your changes (git commit -am 'Add new feature').
Push to the branch (git push origin feature-branch).
Create a new Pull Request.
License
This project is licensed under the MIT License.