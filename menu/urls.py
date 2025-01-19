from django.urls import path
from .views import ProductsListView, ProductUpdateDeleteView, ProductCreateView, ProductRetriveView

urlpatterns = [
    path('', ProductsListView.as_view(), name='products'),
    path('create/', ProductCreateView.as_view(), name='products-create'),
    path('product/<int:pk>/', ProductRetriveView.as_view(), name='product-detail'),
    path('<int:pk>/', ProductUpdateDeleteView.as_view(), name='product-detail')
]