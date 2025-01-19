# Product API

## Overview
The Product API is built using Django and Django REST Framework (DRF). It allows for managing products in a system with full support for CRUD operations, filtering, pagination, and authentication.

The API provides functionality to:
- List products with pagination and filtering.
- Create, retrieve, update, and delete products.
- Filter products based on price, rating, category, and type.

## Features
- **List Products**: Retrieve products with support for filtering and pagination.
- **Create Product**: Add new products to the system.
- **Retrieve Product**: Get product details by ID.
- **Update Product**: Modify product details (full or partial).
- **Delete Product**: Remove a product from the system.
- **Filter Products**: Filter by price, rating, category, toppings, and product type.
- **Pagination**: Limit the number of products returned per page.

## Setup

### Prerequisites
Ensure that you have the following installed:
- Python 3.x (preferably 3.8+)
- Django 3.x+
- Django REST Framework
- PostgreSQL/MySQL/SQLite (any DB of choice)

### Installation
Clone the repository:
```bash
git clone <repository-url>
cd <repository-folder>
```

## Install dependencies
pip install -r requirements.txt

## Migrate the database
python manage.py migrate

## Create a superuser (optional, for accessing Django admin):
python manage.py createsuperuser

## Run the server
python manage.py runserver

## Authentication
This API uses JWT-based authentication. You can obtain a token by logging in via the /api/token/ endpoint and passing it in the Authorization header as Bearer <token> for protected endpoints.

## Custom Pagination
The ProductPagination class provides a custom pagination scheme with:

- Default page size: 10 items per page.
- Maximum page size: 100 items per page.
- Page size query: You can change the page size via the page_size query parameter.

## Custom Filtering
The ProductFilterBackend class supports filtering by:

- **Price**: min_price, max_price
- **Rating**: min_rating
- **Category**: category
- **Toppings**: toppings (can be a list of values)
- **Product Type**: product_type
