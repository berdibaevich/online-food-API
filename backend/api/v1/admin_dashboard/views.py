from backend.account.models import UserBase
from backend.api.v1.product.serializers import (CategorySerializer,
                                                ProductSerializer)
from backend.api.v1.restaurant.serializers import (AddressSerializer,
                                                   RestaurantSerializer)
from backend.api.v1.viewsets.permissions import (AdminDashboardPermission,
                                                 IsOwnerOfProfile)
from backend.api.v1.viewsets.utils import remove_image
from backend.product.models import Category, Ingredient, Product
from backend.restaurant.models import Address, Feedback, Media, Restaurant
from rest_framework import (filters, generics, permissions, response, status,
                            viewsets)
from rest_framework.decorators import action

from .serializers import (CategoryUpdateSerializer, CompanyMediaSerializer,
                          PasswordResetSerializer, ProductUpdateSerializer,
                          ReviewSerializer)


# CATEGORY API VIEW SIDE
class CategoryViewSet(viewsets.ModelViewSet):
    """
        CATEGORYVIEWSET INCLUDED METHODS LIST, RETRIEVE, CREATE,
        UPDATE, DELETE.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminDashboardPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = "slug"


    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return CategoryUpdateSerializer
        return CategorySerializer


    @action(detail=True, methods=['delete'])
    def perform_destroy(self, instance):
        """
            This is help us to remove image from MEDIA, when category object will be deleted
        """
        if instance.image:
            remove_image(image=instance.image)
        instance.delete()
        return response.Response(
            {'message': 'Object successfully deleted.'},
            status=status.HTTP_204_NO_CONTENT
        )
# END CATEGORY API VIEW SIDE


# PRODUCT & INGREDIENTS API VIEW
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related("category").prefetch_related('ingredients')
    serializer_class = ProductSerializer
    permission_classes = [AdminDashboardPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['category__name', 'ingredients__name', 'name']
    lookup_field = "slug"


    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ProductUpdateSerializer
        return ProductSerializer


    @action(detail=True, methods=['delete'])
    def perform_destroy(self, instance):
        """
            This is help us to remove image from MEDIA, when product object will be deleted
        """
        if instance.image:
            if instance.image.name != "product_images/no-food.webp":
                remove_image(image=instance.image)
        instance.delete()
        return response.Response(
            {'message': 'Object successfully deleted.'},
            status=status.HTTP_204_NO_CONTENT
        )
# END PRODUCT & INGREDIENTS API VIEW


# REVIEW API VIEWS
class ReviewAPiView(viewsets.ReadOnlyModelViewSet):
    """
        Review API View
    """
    queryset = Feedback.objects.all().select_related('customer')
    serializer_class = ReviewSerializer
    permission_classes = [AdminDashboardPermission]
# END REVIEW API VIEWS


# ADDRESS API VIEWS
class AddressAPIViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [AdminDashboardPermission]

    def destroy(self, request, *args, **kwargs):
        """
            Bellow we gonna prevent to removing address
            if the is_default field is set to True
        """
        instance = self.get_object()
        if instance.is_default:
            return response.Response(
                {"message": "You can't remove the default address. So set default to another address."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
# END ADDRESS API VIEWS


# RESTAURANT API VIEWS
class RestaurantApiViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [AdminDashboardPermission]
    lookup_field = "slug"
    

    @action(detail=True, methods='GET')
    def restaurant(self, request):
        try:
            restaurant = self.queryset.get()
        except Restaurant.DoesNotExist:
            return response.Response(
            {"error": "no restaurant found"},
            status=status.HTTP_404_NOT_FOUND
        ) 
        serializer = self.get_serializer(restaurant)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        """
            Bellow we gonna delete Restaurant & Media files
        """
        instance = self.get_object()
        if instance.qr_code:
            remove_image(instance.qr_code) # Remove qr_code images from Media
        restaurant_images = instance.restaurant_images.all()
        if restaurant_images:
            for restaurant_media in restaurant_images:
                if restaurant_media.image:
                    # Remove media images which is referenced with restaurant
                    remove_image(restaurant_media.image)
        instance.delete()
        response_data = {"detail": "Successfully deleted."}
        return response.Response(response_data, status= status.HTTP_204_NO_CONTENT)
# END RESTAURANT API VIEWS


# RESTAURANT MEDIA API VIEW
class RestaurantMediaApiViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = CompanyMediaSerializer
    permission_classes = [AdminDashboardPermission]
    http_method_names = ['post', 'put', 'delete']


    def destroy(self, request, *args, **kwargs):
        """
            Bellow we gonna delete media of restaurant
        """
        instance = self.get_object()
        media = Media.objects.get(pk = instance.pk)
        media.delete()
        if instance.image:
            remove_image(image=instance.image)
        response_data = {"detail": "Successfully deleted."}
        return response.Response(response_data, status= status.HTTP_204_NO_CONTENT)
# END RESTAURANT MEDIA API 


# PASSWORD RESET API VIEW
class PasswordResetViewSet(viewsets.ViewSet):
    serializer_class = PasswordResetSerializer
    permission_classes = [IsOwnerOfProfile]

    @action(detail=False, methods=['put'])
    def reset_password(self, request, *args, **kwargs):
        user = request.user
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data.get("new_password")
        if new_password:
            user.set_password(new_password)
            user.save()
        return response.Response({'status': 'success'}, status=status.HTTP_200_OK)
# END PASSWORD RESET API VIEW