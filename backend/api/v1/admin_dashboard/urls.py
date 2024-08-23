from backend.api.v1.account.views import ProfileRetrieveEditApiView
from django.urls import path

from . import views

urlpatterns = [
    # CATEGORIES
    path('categories/', views.CategoryViewSet.as_view({'get': 'list'}), name = "list"),
    path('category/add/', views.CategoryViewSet.as_view({'post': 'create'}), name = "add"),
    path('category/edit_and_detail/<str:slug>/', views.CategoryViewSet.as_view({'put': 'update', 'get': 'retrieve'}), name = "edit_detail"),
    path('category/destroy/<str:slug>/', views.CategoryViewSet.as_view({'delete': 'destroy'}), name = "destroy"),
    # END CATEGORIES
    # PRODUCT
    path('products/', views.ProductViewSet.as_view({'get': 'list'}), name = 'product_list'),
    path('product/add/', views.ProductViewSet.as_view({'post': 'create'}), name = 'product_add'),
    path('product/edit_and_detail/<str:slug>/', views.ProductViewSet.as_view({'put': 'update', 'get': 'retrieve'}), name = 'product_edit_detail'),
    path('product/destroy/<str:slug>/', views.ProductViewSet.as_view({'delete': 'destroy'}), name = 'product_destroy'),
    # END PRODUCT
    # REVIEWS
    path('reviews/', views.ReviewAPiView.as_view({'get': 'list'}), name = "review_list"),
    # END REVIEWS
    # ADDRESS
    path('addresses/', views.AddressAPIViewSet.as_view({'get': 'list'}), name = "address_list"),
    path('address/add/', views.AddressAPIViewSet.as_view({'post': 'create'}), name = "address_add"),
    path('address/edit_and_detail/<str:pk>/', views.AddressAPIViewSet.as_view({'put': 'update', 'get': 'retrieve'}), name = "address_edit_detail"),
    path('address/destroy/<str:pk>/', views.AddressAPIViewSet.as_view({'delete': 'destroy'}), name = "address_destroy"),
    # END ADDRESS
    # RESTAURANT & media
    path('restaurant/', views.RestaurantApiViewSet.as_view({'get': 'restaurant'}), name = 'admin_restaurant'),
    path('restaurant/add/', views.RestaurantApiViewSet.as_view({'post': 'create'}), name = 'add_restaurant'),
    path('restaurant/edit/<str:slug>/', views.RestaurantApiViewSet.as_view({'put': 'update'}), name = 'edit_restaurant'),
    path('restaurant/destroy/<str:slug>/', views.RestaurantApiViewSet.as_view({'delete': 'destroy'}), name = 'delete_restaurant'),
    path('restaurant/media/add/', views.RestaurantMediaApiViewSet.as_view({'post': 'create'}), name = 'add_media_to_restaurant'),
    path('restaurant/media/edit/<str:pk>/', views.RestaurantMediaApiViewSet.as_view({'put': 'update'}), name = 'edit_media_from_restaurant'),
    path('restaurant/media/delete/<str:pk>/', views.RestaurantMediaApiViewSet.as_view({'delete': 'destroy'}), name = 'delete_media_from_restaurant'),
    # END RESTAURANT & media
    # ADMIN PROFILE & EDIT
    path('profile/detail_edit/<str:pk>/', ProfileRetrieveEditApiView.as_view(), name = 'admin_detail_edit'),
    path('profile/reset_password/', views.PasswordResetViewSet.as_view({"put": "reset_password"}), name = 'reset_password'),
    # END ADMIN PROFILE & EDIT 
]