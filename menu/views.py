from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView 
from .models import Products
from .serializers import ProductSerializer
# Create your views here.

class ProductsView(ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

class ProductRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer