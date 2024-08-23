from backend.api.v1.viewsets.utils import remove_image
from backend.restaurant.models import Address, Feedback, Media, Restaurant
from rest_framework import serializers


class MediaSerializer(serializers.ModelSerializer):
    """
        Restaurant Media Images Serializer ok :)
    """
    class Meta:
        model = Media
        fields = ("id", "image", "alt_text", "is_feature")



class RestaurantSerializer(serializers.ModelSerializer):
    """
        Restaurant Serializer :)
    """
    qr_code = serializers.SerializerMethodField()
    restaurant_images = MediaSerializer(many = True, read_only = True)
    class Meta:
        model = Restaurant
        fields = ("name", "slug", "about_us", "phone_number1", "phone_number2", "telegram_link", "instagram_link", "facebook_link", "domain_name", "qr_code", "created_at", "updated_at", "restaurant_images")
        extra_kwargs = {
            "qr_code": {'read_only': True},
            "slug": {'read_only': True},
            "domain_name": {'write_only': True, 'required': False},
        }

    
    def create(self, validated_data):
        restaurant = Restaurant.objects.exists()
        if restaurant:
            raise serializers.ValidationError("Sorry, you can't save again.")
        return super().create(validated_data)

    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.about_us = validated_data.get("about_us", instance.about_us)
        instance.phone_number1 = validated_data.get("phone_number1", instance.phone_number1)
        instance.phone_number2 = validated_data.get("phone_number2", instance.phone_number2)
        instance.telegram_link = validated_data.get("telegram_link", instance.telegram_link)
        instance.instagram_link = validated_data.get("instagram_link", instance.instagram_link)
        instance.facebook_link = validated_data.get("facebook_link", instance.facebook_link)
        new_domain_name = validated_data.get("domain_name")
        if new_domain_name and new_domain_name != instance.domain_name:
            if instance.qr_code:
                remove_image(image=instance.qr_code)
            instance.domain_name = new_domain_name
        instance.save()
        return instance


    def get_qr_code(self, obj) -> str:
        request = self.context.get("request")
        if obj.qr_code:
            return request.build_absolute_uri(obj.qr_code.url)
        return None



class AddressSerializer(serializers.ModelSerializer):
    """
        Address Serializer
    """
    class Meta:
        model = Address
        fields = "__all__"


    def create(self, validated_data):
        """
            Bul jerde bizler taza obiekt jaratilip atirg'an address tin'
            is_defualt = True bolsa onda basqa obiektlerdin' is_default = False
            qilamiz ok :)
        """
        is_default = validated_data.get("is_default") or None
        if is_default is not None:
            if is_default:
                self.__update_address()
        return super().create(validated_data)


    def update(self, instance, validated_data):
        instance.town_city = validated_data.get("town_city", instance.town_city)
        instance.address_line = validated_data.get("address_line", instance.address_line)
        instance.address_line2 = validated_data.get("address_line2", instance.address_line2)
        is_default = validated_data.get("is_default")
        if is_default:
            self.__update_address()
            instance.is_default = is_default
        instance.save()
        return instance


    @classmethod
    def __update_address(cls):
        Address.objects.filter(is_default = True).update(is_default = False)



class FeedBackSerializer(serializers.ModelSerializer):
    restaurant = serializers.SlugRelatedField(
        slug_field="slug",
        queryset = Restaurant.objects.all()
    )
    class Meta:
        model = Feedback
        fields = ("restaurant", "rating", "feedback")


    def validate(self, data):
        user = self.context['request'].user
        restaurant = data.get("restaurant")
        existing_restaurant = Feedback.objects.filter(customer=user, restaurant=restaurant).exists()
        if existing_restaurant:
            raise serializers.ValidationError("You have already submitted a rating for this restaurant.")
        return data
