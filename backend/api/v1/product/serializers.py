from backend.product.models import Category, Ingredient, Product
from django.db import transaction
from rest_framework import serializers


# CATEGORY SERIALIZER
class CategorySerializer(serializers.ModelSerializer):
    """
        THIS CATEGORY LIST API AND ALSO CREATE CATEGORY.
        WHEN ADD NEW CATEGORY WE GONNA VALIDATE SOME FIELD 
        BEFORE SAVING TO DATABASE OK :)
    """
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "image", "is_active")
        read_only_fields = ("slug",)


    def validate_name(self, name):
        self.__validate_category_name(name)
        return name


    @classmethod
    def __validate_category_name(cls, value):
        if value.isdigit():
            raise serializers.ValidationError(f"sorry, your values '{value}' are digits so we can't save")
        
        name = value.capitalize()
        category = Category.objects.filter(name = name).exists()
        if category:
            raise serializers.ValidationError(f'{name} already exists, sorry :)')
# END CATEGORY SERIALIZER


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name")



class ProductSerializer(serializers.ModelSerializer):
    """
        ProductSerializer for List, create and retrieve
    """
    category = serializers.SlugRelatedField(slug_field='name', queryset = Category.objects.all())
    ingredients = IngredientSerializer(many = True)
    class Meta:
        model = Product
        fields = ("category", "name", "slug", "description", "original_price", "image", "is_active", 'ingredients')
        extra_kwargs = {
            "slug": {"read_only": True},
        }


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        ingredients_data = representation.pop("ingredients")
        representation["ingredients"] = [ingredient['name'] for ingredient in ingredients_data]
        return representation


    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients", [])
        image = validated_data.get("image", "product_images/no-food.webp")
  
        with transaction.atomic():
            product = Product.objects.create(image=image, **validated_data)
            for ingredient in ingredients:
                ingredient_name = ingredient.get("name").lower()
                ingredient, _ = Ingredient.objects.get_or_create(name = ingredient_name)
                product.ingredients.add(ingredient)
        return product

