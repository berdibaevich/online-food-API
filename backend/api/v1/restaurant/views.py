from backend.restaurant.models import Address, Feedback, Media, Restaurant
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response

from .serializers import (AddressSerializer, FeedBackSerializer,
                          RestaurantSerializer)


class RestaurantReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):  
    """
    Restaurant API view for Client APP
    """  
    serializer_class = RestaurantSerializer
    
    @action(detail=False, methods=['get'])
    def restaurant(self, request, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get()
            serializer = RestaurantSerializer(restaurant, many = False, context = {'request': request})
            return Response(
            {'restaurant': serializer.data},
            status=status.HTTP_200_OK
        )
        except Restaurant.DoesNotExist:
            return Response(
                {"error": "no restaurant found"},
                status=status.HTTP_404_NOT_FOUND
            )


class AddressReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Addresses of Restaurant for Client APP
    """    
    serializer_class = AddressSerializer

    @action(detail=False, methods=['get'])
    def addresses(self, request, *args, **kwargs):
        addresses = Address.objects.filter(is_default = True)
        if not addresses:
            return Response({"error": "no addresses found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AddressSerializer(addresses, many = True)
        return Response(
            {'addresses': serializer.data},
            status=status.HTTP_200_OK
        )



class FeedBackModelViewSetForClient(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedBackSerializer
    http_method_names = ['post']

    @action(detail=False, methods=['post'])
    def post_feedback(self, request, *args, **kwargs):
        serializer = FeedBackSerializer(data=request.data, context = {'request': request})
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(customer = request.user)
        return Response("Feedback submitted successfully", status=status.HTTP_201_CREATED)
        