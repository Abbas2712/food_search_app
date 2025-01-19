from rest_framework import serializers
from .models import Products, Toppings, Ratings, ProductToppings

class RatingSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    product_rating = serializers.SerializerMethodField()
    product_toppings = serializers.SerializerMethodField()
    class Meta:
        model = Products
        fields = ['product_id', 'product_name', 'product_description', 'product_price', 
                  'product_category','product_toppings','product_rating', 'product_type']

    def get_product_rating(self, obj):
        # Fetch ratings for the current product
        ratings = Ratings.objects.filter(product=obj.product_id)
        # Return the rating values or an average
        return [product_rating.rating_value for product_rating in ratings]

    def get_product_toppings(self, obj):
        """
        Fetch related toppings for a product using raw SQL.

        This method retrieves the names of all toppings associated with a product.
        It uses raw SQL to query the `product_toppings` and `toppings` tables directly
        since the `ProductToppings` model is unmanaged (`managed = False`).

        Args:
            obj: The current product object being serialized.

        Returns:
            A list of topping names (strings) associated with the given product.
        """
        # Fetch related toppings using raw SQL for unmanaged models
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT t.topping_name 
                FROM product_toppings pt
                JOIN toppings t ON pt.topping_id = t.topping_id
                WHERE pt.product_id = %s
                """,
                [obj.product_id]
            )
            toppings = [row[0] for row in cursor.fetchall()]
        return toppings
    
class ToppingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Toppings
        fields = '__all__'

class ProductToppingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductToppings
        fields = '__all__'