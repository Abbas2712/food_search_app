from rest_framework import serializers
from .models import Products, Toppings, Ratings

class RatingSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    product_rating = RatingSerialzier(many=True, read_only=True)
    class Meta:
        model = Products
        fields = '__all__'

class ToppingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Toppings
        fields = '__all__'

