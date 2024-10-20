E-Commerce API Project Overview

Introduction

The E-Commerce API project is designed to provide a robust backend solution for an online shopping platform. Built using Django and Django REST Framework, this API allows for seamless product management, order processing, user authentication, and user-generated content like reviews and ratings.

Features

Key Endpoints

- Product Management
  - `GET /api/products/`: List all products.
  - `POST /api/products/`: Create a new product.
  - `GET /api/products/{id}/`: Retrieve a specific product.
  - `PUT /api/products/{id}/`: Update a specific product.
  - `DELETE /api/products/{id}/`: Delete a specific product.

- Order Management**
  - `POST /api/orders/{product_id}/create-order/`: Create an order for a specific product.
  - `GET /api/orders/`: List user orders.
  - `GET /api/orders/{id}/`: Retrieve a specific order.
  - `PUT /api/orders/{id}/`: Update an order.
  - `DELETE /api/orders/{id}/`: Delete an order.

- User Authentication**
  - `POST /users/register/`: Register a new user.
  - `POST /users/login/`: Login an existing user.
  - `POST /users/logout/`: Logout the current user.
  - `GET /users/profile/`: Retrieve user profile information.
  - `DELETE /users/delete_account/`: Delete a user account.

- Reviews and Ratings
  - `GET /api/reviews/`: List all reviews.
  - `POST /api/reviews/`: Create a new review.
  - `PUT /api/reviews/{id}/`: Update a specific review.
  - `DELETE /api/reviews/{id}/`: Delete a specific review.
  - `GET /api/ratings/`: List all ratings.
  - `POST /api/ratings/`: Create a new rating.

Technology Stack

- Framework: Django
- Library: Django REST Framework
- Database: PostgreSQL (or SQLite for development)

 Project Goals

The main goals of this project include:

- Developing a fully functional REST API for product and order management.
- Implementing user authentication and permissions for secure operations.
- Allowing users to leave reviews and ratings for products.

Challenges and Learnings

Throughout the project, several challenges were faced, including complex data relationships, authentication setup, and time management. Key learnings involved the importance of thorough planning, the need for early and continuous testing, and the value of user feedback in shaping the API.

Conclusion

The E-Commerce API project provides a solid foundation for future e-commerce applications, enabling further integrations with mobile apps or third-party services. With a focus on security and user experience, this API aims to enhance the online shopping experience for users.
