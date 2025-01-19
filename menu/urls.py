from django.urls import path
from .views import ProductsListView, ProductRetrieveUpdateDeleteView, ProductCreateView

urlpatterns = [
    path('', ProductsListView.as_view(), name='products'),
    path('create/', ProductCreateView.as_view(), name='products-create'),
    path('<int:pk>/', ProductRetrieveUpdateDeleteView.as_view(), name='product-detail')
]