from django.urls import path

from . import views

urlpatterns = [
    path('', views.RestaurantReadOnlyViewSet.as_view({'get': 'restaurant'}), name = 'restaurant'),
    path('addresses/', views.AddressReadOnlyViewSet.as_view({'get': 'addresses'}), name = 'addresses'),
    path('post_feedback/', views.FeedBackModelViewSetForClient.as_view({'post': 'post_feedback'}), name = 'post_feedback'),
]