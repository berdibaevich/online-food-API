from django.urls import path

from . import views

urlpatterns = [
    path('categories/', views.CategoryListApiView.as_view(), name = "category_list"),
    path('menu/', views.ProductListApiView.as_view(), name = 'menu'),
]