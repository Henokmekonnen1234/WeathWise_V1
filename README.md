# WealthWise API

## Overview
WealthWise API is a backend service for the WealthWise application, designed to manage user registration, login, profile management, transaction handling, and more. The API is built using Flask, Flask-JWT-Extended for authentication, and MongoDB for database storage. It also includes utilities for password encryption and validation.

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
  - [User Endpoints](#user-endpoints)
  - [Transaction Endpoints](#transaction-endpoints)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites
- Python 3.7 or higher
- MongoDB
- Pipenv (optional but recommended for virtual environment management)

### Steps
1. Clone the repository:
    ```sh
    git clone https://github.com/Henokmekonnen1234/WeathWise_V1
    cd WeathWise_V1 
    ```
2. Create and activate a virtual environment:
    ```sh
    .\winenv\Scripts\Activate
    ```
3. Install the dependencies:
    ```sh
    .\winenv\Scripts\Activate
    ```
4. Set up environment variables:
    All env variables are setuped but if you want create a `.env` file in the project root and add the following variables:
    ```makefile
    MONGO_HOST=localhost
    MONGO_PORT=27017
    MONGO_DB=wealthwise
    ```

5. Run the application:
    ```sh
        Python -m api.v1.app
    ```

## Configuration
The application uses environment variables for configuration. You can set these in a `.env` file in the project root:

- `MONGO_HOST`: MongoDB host (default: localhost)
- `MONGO_PORT`: MongoDB port (default: 27017)
- `MONGO_DB`: MongoDB database name (default: wealthwise)

## Usage

### Running the Server
```sh
Python -m api.v1.app
```
# API Endpoints

## User Endpoints

### Register a User
- **URL**: `/register`
- **Method**: `POST`
- **Description**: Register a new user.
- **Request**:
    ```json
    {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "username": "johndoe",
        "password": "securepassword"
    }
    ```
- **Response**:
    ```json
    {
        "_id": "user_id",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "username": "johndoe",
        "created_date": "2024-07-01T00:00:00.000000",
        "updated_date": "2024-07-01T00:00:00.000000"
    }
    ```

### Login
- **URL**: `/login`
- **Method**: `POST`
- **Description**: Authenticate a user and return a JWT token.
- **Request**:
    ```json
    {
        "username": "johndoe",
        "password": "securepassword"
    }
    ```
- **Response**:
    ```json
    {
        "token": "jwt_token"
    }
    ```

### Get User Profile
- **URL**: `/user`
- **Method**: `GET`
- **Description**: Retrieve the user profile information.
- **Headers**:
    - `Authorization`: Bearer `<JWT_TOKEN>`
- **Response**:
    ```json
    {
        "_id": "user_id",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "username": "johndoe",
        "created_date": "2024-07-01T00:00:00.000000",
        "updated_date": "2024-07-01T00:00:00.000000"
    }
    ```

### Update User Profile
- **URL**: `/user`
- **Method**: `PUT`
- **Description**: Update the user profile information.
- **Headers**:
    - `Authorization`: Bearer `<JWT_TOKEN>`
- **Request**:
    ```json
    {
        "first_name": "John",
        "last_name": "Doe"
    }
    ```
- **Response**:
    ```json
    {
        "_id": "user_id",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "username": "johndoe",
        "created_date": "2024-07-01T00:00:00.000000",
        "updated_date": "2024-07-01T00:00:00.000000"
    }
    ```

### Delete User
- **URL**: `/user`
- **Method**: `DELETE`
- **Description**: Delete the user account.
- **Headers**:
    - `Authorization`: Bearer `<JWT_TOKEN>`
- **Response**:
    ```json
    {
        "message": "User deleted successfully."
    }
    ```

## Transaction Endpoints

### Create Transaction
- **URL**: `/transactions`
- **Method**: `POST`
- **Description**: Create a new transaction.
- **Headers**:
    - `Authorization`: Bearer `<JWT_TOKEN>`
- **Request**:
    ```json
    {
        "user_id": "user_id",
        "amount": 100.0,
        "type": "expense",
        "category": "food",
        "description": "Dinner at restaurant"
    }
    ```
- **Response**:
    ```json
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
    ```

### Get Transactions
- **URL**: `/transactions`
- **Method**: `GET`
- **Description**: Retrieve all transactions for a user.
- **Headers**:
    - `Authorization`: Bearer `<JWT_TOKEN>`
- **Response**:
    ```json
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
        }
    ]
    ```

### Update Transaction
- **URL**: `/transactions/<transaction_id>`
- **Method**: `PUT`
- **Description**: Update a transaction.
- **Headers**:
    - `Authorization`: Bearer `<JWT_TOKEN>`
- **Request**:
    ```json
    {
        "amount": 120.0,
        "description": "Updated description"
    }
    ```
- **Response**:
    ```json
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
    ```

### Delete Transaction
- **URL**: `/transactions/<transaction_id>`
- **Method**: `DELETE`
- **Description**: Delete a transaction.
- **Headers**:
    - `Authorization`: Bearer `<JWT_TOKEN>`
- **Response**:
    ```json
    {
        "message": "Transaction deleted successfully."
    }
    ```

### Get Transaction Summary
- **URL**: `/transactions/summary`
- **Method**: `POST`
- **Description**: Retrieve a summary of transactions for a specific year or month. Provides aggregate values for expenses and income along with detailed transaction records.

#### Request

- **Headers**:
  - `Authorization`: Bearer `<JWT_TOKEN>`

- **Body**:
  - **Example 1: Yearly Summary**:
    ```json
    {
        "year": 2024
    }
    ```
  - **Example 2: Monthly Summary**:
    ```json
    {
        "year": 2024,
        "month": 7
    }
    ```

#### Response
- **Status Code**: `200 OK`
- **Body**:
    ```json
    {
        "page": 1,
        "page_size": 10,
        "summary": {
            "expense": 253.77,
            "income": 200
        },
        "total_documents": 4,
        "total_pages": 1,
        "transactions": [
            {
                "__class__": "Transaction",
                "_id": "28e76830-2734-41bc-81d5-4c0f1e58605d",
                "amount": 125.45,
                "category": "entertainment",
                "created_date": "2024-07-08T10:30:30.023526",
                "description": "Expense for entertainment",
                "type": "expense",
                "updated_date": "2024-07-08T10:30:30.023526"
            },
            {
                "__class__": "Transaction",
                "_id": "5b78d2d2-a064-449a-a365-c08757cc10f5",
                "amount": 200,
                "category": "work",
                "created_date": "2024-07-08T10:28:21.785968",
                "description": "Income for work",
                "type": "income",
                "updated_date": "2024-07-08T12:00:10.610362"
            },
            {
                "__class__": "Transaction",
                "_id": "66063865-e0dd-44ab-af97-e285123c8cd9",
                "amount": 87.92,
                "category": "food",
                "created_date": "2024-07-08T10:29:04.389542",
                "description": "Expense for food",
                "type": "expense",
                "updated_date": "2024-07-08T10:29:04.389542"
            },
            {
                "__class__": "Transaction",
                "_id": "fa5707a2-692a-4ad9-a45f-32fb01d6b454",
                "amount": 40.4,
                "category": "food",
                "created_date": "2024-06-26T10:24:19.076715",
                "description": "For coffee",
                "type": "expense",
                "updated_date": "2024-06-26T10:24:19.076715"
            }
        ]
    }
    ```

## Documentation
Swagger documentation is available for all API endpoints. You can access it by navigating to [http://localhost:5000/apidocs](http://localhost:5000/apidocs) after starting the server.

You can also access individual Swagger YAML files directly via URLs like [http://localhost:5000/documentation/user/register.yml](http://localhost:5000/documentation/user/register.yml).

## Contributing
We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License
This project is free anyone can use it.
