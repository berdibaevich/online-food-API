from backend.product.models import Category, Ingredient, Product
from django.db.models import Prefetch
from rest_framework import generics, response, status

from .serializers import CategorySerializer, ProductSerializer


# CLIENT WEB API
class CategoryListApiView(generics.ListAPIView):
    """
        CATEGORY LIST API VIEW FOR CLIENT APP 
        RETURN QUERYSET OF CATEGORY IS_ACTIVE = TRUE
    """
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.filter(is_active = True)
        return queryset



class ProductListApiView(generics.ListAPIView):
    """
        Product List Api View for client app
        return queryset of product if is_active = True
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(is_active = True).select_related("category").defer(
            "discount_percent",
            "discounted_price",
            "quantity",
            "category__image",
            "category__is_active",
            "category__slug",
        ).prefetch_related(
            Prefetch("ingredients", queryset=Ingredient.objects.only("name"))
        )
        """JOQARIDA BIZLER OPTIMIZATION QILDIQ TUWRIMA ENDI BUL JERDE
        DEFER() PAYDALANIP KETTIK SEBEBI AYRIM FIELD LAR KEREK EMES
        TOMENDEGI QILIP LOADED BOLADI QASHAN DATABASE QUERY ISKE QOSILGAN
        KEZDE TOMENDEGI ISKE TUSEDI, KORIP TURG'ANDAY KEREK EMES FIELD
        LERDE BAR SONI ALIP TASLADIQ DEFER() ARQALI

        SELECT 
            "product_product"."id", "product_product"."category_id", 
            "product_product"."name", "product_product"."slug", 
            "product_product"."description", "product_product"."original_price", 
            "product_product"."discount_percent", "product_product"."discounted_price", 
            "product_product"."quantity", "product_product"."image", 
            "product_product"."is_active", "product_product"."created_at", 
            "product_product"."updated_at", "product_category"."id", 
            "product_category"."name", "product_category"."slug", 
            "product_category"."image", "product_category"."is_active" 
        FROM 
            "product_product" INNER JOIN "product_category" 
        ON 
            ("product_product"."category_id" = "product_category"."id") 
        WHERE "product_product"."is_active"
        """
        # print(queryset.query)
        # print("____________-")
        return queryset


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        #print(queryset.query)
        category = request.query_params.get("category") or None
        if category is not None:
            queryset = queryset.filter(category__slug = category)

            if not queryset.exists():
                return response.Response(
                    {'message': 'No products found for the specified category.'},
                    status=status.HTTP_404_NOT_FOUND
                )
         
        serializer = self.get_serializer(queryset, many = True)
        return response.Response(serializer.data)