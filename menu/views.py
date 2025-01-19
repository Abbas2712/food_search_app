from django.db.models import Avg
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.filters import BaseFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from .models import Products
from .serializers import ProductSerializer
# Create your views here.

class ProductPagination(PageNumberPagination):
    """
    Custom pagination class for listing products.
    
    This class handles pagination for the list of products in the API. 
    It provides the following features:
    
    - Limits the number of products returned per page (default is 10).
    - Allows clients to specify a custom page size via the 'page_size' query parameter.
    - Restricts the maximum page size to 100 products per page.

    Attributes:
        page_size (int): The default number of products to return per page. Default is set to 10.
        page_size_query_param (str): The name of the query parameter that allows clients to specify a custom page size. Default is 'page_size'.
        max_page_size (int): The maximum limit on the number of products that can be requested per page. Default is set to 100.
    """
    page_size = 10  # Number of products per page
    page_size_query_param = 'page_size'  # Allow clients to specify page size
    max_page_size = 100  # Maximum page size limit

class ProductFilterBackend(BaseFilterBackend):
    """
    Custom filter backend for filtering products based on various attributes such as price, 
    rating, category, toppings, and product type.
    
    This backend processes incoming requests and applies filters to the queryset based on 
    the provided query parameters.

    Methods:
        filter_queryset(request, queryset, view):
            Filters the queryset based on the following query parameters:
                - min_price: Filters products by minimum price.
                - max_price: Filters products by maximum price.
                - min_rating: Filters products by minimum average rating.
                - category: Filters products by category name.
                - toppings: Filters products by a list of toppings.
                - product_type: Filters products by exact match of product type.

    Attributes:
        None
    """

    def filter_queryset(self, request, queryset, view):
        # Filter by price range
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        if min_price and max_price:
            queryset = queryset.filter(product_price__gte=min_price, product_price__lte=max_price)

        # Filter by average rating
        min_rating = request.query_params.get('min_rating')
        if min_rating:
            queryset = queryset.annotate(avg_rating=Avg('ratings__rating_value')).filter(avg_rating__gte=min_rating)

        # Filter by category
        category = request.query_params.get('category')
        if category:
            queryset = queryset.filter(product_category__icontains=category)

        # Filter by toppings
        toppings = request.query_params.getlist('toppings')
        if toppings:
            queryset = queryset.filter(producttoppings__topping__topping_name__in=toppings).distinct()

        # Filter by product type
        product_type = request.query_params.get('product_type')
        if product_type:
            queryset = queryset.filter(product_type__iexact=product_type)

        return queryset
class ProductsListView(generics.ListAPIView):
    """
    ProductsView handles listing all products with filtering functionality.

    Methods:
    - GET: Retrieves all products.
      - Returns a 404 status if no products are available.
    """
    queryset = Products.objects.all()
    # serializer class
    serializer_class = ProductSerializer
    # pagination class
    pagination_class = ProductPagination
    # Filter backends
    filter_backends = [ProductFilterBackend]

    def list(self, request, *args, **kwargs):
        """
        List all products.

        - If products exist, returns a 200 status with the list of products.
        - If no products exist, returns a 404 status with a message.
        """
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response({"message": "No products found"}, status=status.HTTP_404_NOT_FOUND)
            
        # Pagination is automatically handled by DRF, but you can customize it here
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ProductCreateView(generics.CreateAPIView):
    """
    View for creating a new product.

    Methods:
    - POST: Creates a new product based on the provided data.
      - Request Body: JSON containing product details (e.g., name, description, price, etc.)
      - Response 201: Returns the created product's data.
      - Response 400: Returns validation errors if the provided data is invalid.
    """
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Handle the creation of a new product.

        Validates the input data and saves the new product to the database.
        Returns the created product's data or validation errors.

        Example Request Body:
        {
            "name": "Chicken Shawarma",
            "description": "The Standard Chicken Shawarma",
            "price": 70.00,
            "average_rating": 4.5,
            "category": "Shawarma",
            "type": "Non-Veg"
        }
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductRetriveView(generics.RetrieveAPIView):
    """
    View for retrieving a product by ID.

    Methods:
    - GET: Retrieves a specific product by its ID.
      - Path Parameter: `pk` (primary key of the product).
      - Response 200: Returns the product's data.
      - Response 404: Returns an error if the product does not exist.
      
    """
    serializer_class = ProductSerializer

    def get_object(self):
        """
        Retrieve a product by its primary key (pk).

        Raises:
        - NotFound: If the product does not exist.

        Example:
        URL: /products/1/
        """
        try:
            queryset = Products.objects.get(product_id=self.kwargs['pk'])
        except Products.DoesNotExist:
            # Custom error for when the product is not found
            raise NotFound(detail="Product not found.", code=status.HTTP_404_NOT_FOUND)
        return queryset

class ProductUpdateDeleteView(generics.UpdateAPIView,generics.DestroyAPIView):
    """
    View for updating, or deleting a product by ID.

    Methods:
    - PUT/PATCH: Updates a specific product by its ID.
      - Request Body: JSON containing fields to update (full or partial).
      - Response 200: Returns the updated product's data.
      - Response 400: Returns validation errors for invalid data.
      - Response 404: Returns an error if the product does not exist.

    - DELETE: Deletes a specific product by its ID.
      - Response 204: Returns a success message upon successful deletion.
      - Response 404: Returns an error if the product does not exist.
      - Response 500: Returns an error if the deletion process fails.
    """
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Retrieve a product by its primary key (pk).

        Raises:
        - NotFound: If the product does not exist.

        Example:
        URL: /products/1/
        """
        try:
            queryset = Products.objects.get(product_id=self.kwargs['pk'])
        except Products.DoesNotExist:
            # Custom error for when the product is not found
            raise NotFound(detail="Product not found.", code=status.HTTP_404_NOT_FOUND)
        return queryset
        
    def update(self, request, *args, **kwargs):
        """
        Update a product's details by its primary key (pk).

        Validates the input data and updates the product.
        Supports partial updates.

        Raises:
        - ValidationError: If the provided data is invalid.

        Example Request Body:
        {
            "price": 24.99
        }
        """
        try:
            product = self.get_object()
            serializer = self.get_serializer(product, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except ValidationError as e:
            # Custom error handling for invalid data
            return Response(
                {"detail": "Invalid data", "errors": e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a product by its primary key (pk).

        Deletes the product from the database and returns a success message.

        Raises:
        - Exception: If the deletion process fails.

        Example:
        URL: /products/1/
        """
        try:
            product = self.get_object()
            self.perform_destroy(product)
        except Exception as e:
            return Response(
                {"detail": "Failed to delete the product.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response({"detail": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)