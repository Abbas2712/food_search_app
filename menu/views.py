from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from .models import Products
from .serializers import ProductSerializer
# Create your views here.

class ProductsListView(generics.ListAPIView):
    """
    ProductsView handles listing all products.

    Methods:
    - GET: Retrieves all products.
      - Returns a 404 status if no products are available.
    """
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        """
        List all products.

        - If products exist, returns a 200 status with the list of products.
        - If no products exist, returns a 404 status with a message.
        """
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response({"message": "No products found"}, status=status.HTTP_404_NOT_FOUND)
            
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

class ProductRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, or deleting a product by ID.

    Methods:
    - GET: Retrieves a specific product by its ID.
      - Path Parameter: `pk` (primary key of the product).
      - Response 200: Returns the product's data.
      - Response 404: Returns an error if the product does not exist.

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