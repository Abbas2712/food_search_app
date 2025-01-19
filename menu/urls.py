from django.urls import path
from .views import ProductsView, ProductRetrieveUpdateDeleteView

urlpatterns = [
    path('', ProductsView.as_view(), name='products'),
    path('<int:pk>/', ProductRetrieveUpdateDeleteView.as_view(), name='product-detail')
]