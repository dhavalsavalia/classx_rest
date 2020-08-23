from django.urls import path
from .views import ImageDetail, ImageList, ItemDetail, ItemList

urlpatterns = [
    path('items/', ItemList.as_view(), name='item-list'),
    path('items/<int:pk>/', ItemDetail.as_view(), name='item-detail'),
    path('images/', ImageList.as_view(), name='image-list'),
    path('images/<int:pk>/', ImageDetail.as_view(), name='image-detail'),
]
