from rest_framework.generics import ListCreateAPIView 
from .models import Products
from .serializers import ProductSerializer
# Create your views here.

class ProductsView(ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer