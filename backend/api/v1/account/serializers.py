
import re

from backend.account.models import UserBase
from backend.account.validators import validate_uzb_phone_number
from backend.api.v1.viewsets.utils import remove_image
from backend.api.v1.viewsets.validators import validate_username
from rest_framework import serializers

from .utils import generate_token


# SIGN UP SERIALIZER
class UserSerializer(serializers.ModelSerializer):
    """
        FOR USER SIGN UP SERIALIZERS

        EDIT
            - FIELDS ISHINDE "expires_at" ALIP TASLADIQ
            - EXTRA_KWARGS ISHINE "expires_at" USHIN READ_ONLY = TRUE EDI ONIDA ALIP TASLADI.
    """
    first_name = serializers.CharField(validators = [validate_username])
    class Meta:
        model = UserBase
        fields = ("first_name", "phone_number", "password")
        extra_kwargs = {
            'password': {'write_only': True},
        }

    # --- TOMENDEGIDE HAZIRSHE MUZDA (MUZDA MEANS WAQTINSHA ISLEMEY TURADI.)
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     time_diff = instance.expires_at - instance.created_at
    #     minutes = int(time_diff.total_seconds() // 60)
    #     representation['expires_at'] = f"The token will expire in {minutes} minutes"
    #     return representation

    

    def create(self, validated_data):
        first_name = validated_data.get("first_name").capitalize()
        user = UserBase.objects.create(
            first_name = first_name,
            phone_number = validated_data.get("phone_number")
        )
        user.set_password(validated_data['password'])
        # TOMENDEGI HAZIRSHE MUZDA
        # token, expires_at = generate_token()
        # user.phone_token = token
        # user.expires_at = expires_at

        # USI JERDE IS_ACTIVE TRUE BELGILEP KETEMIZ
        user.is_active = True
        user.save()
        return user
        


    def validate_password(self, password):
        """
            Check password
            Bul jerde password uzinlig'i 8 den to'men bolsa
            ham keminde bir san bolmasa error beredi.
        """
        password_regex = r"^(?=.*\d).{8,}$"
        if not re.match(password_regex, password):
            raise serializers.ValidationError("Kiritilgen password keminde 8 den to'men bolmawi, ja'ne sannan 1 san boliwi kerek.")
        return password
# END SIGN UP SERIALIZER


# MY PROFILE AND EDIT API VIEW SERIALIZER
class MyAccountSerializer(serializers.ModelSerializer):
    """
        PROFILE & EDIT USHIN SERIALIZER OK :)
    """
    first_name = serializers.CharField(validators = [validate_username])
    class Meta:
        model = UserBase
        fields = ("first_name", "phone_number", "avatar", "created_at", "updated_at")
    
    
    def update(self, instance, validated_data):
        old_image = instance.avatar
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.avatar = validated_data.get("avatar", instance.avatar)
        
        if validated_data.get("avatar"):
            # HELP US TO REMOVE OLD IMAGE FROM MEDIA IF OLD IMAGE IS DEFAULT 
            # SO IT WILL NOT BE REMOVE
            if old_image and old_image.name != "avatars/no_photo.png":
                remove_image(image=old_image)

        instance.save()
        return instance
# END MY PROFILE AND EDIT API VIEW SERIALIZER


# PHONE TOKEN VERIFY SERIALIZER
class PhoneTokenVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators = [validate_uzb_phone_number], required = True)
    token = serializers.CharField()

    def validate_phone_number(self, phone_number):
        account = UserBase.objects.filter(phone_number = phone_number).exists()
        if not account:
            raise serializers.ValidationError(f"{phone_number} doesn't exists.")
        return phone_number
    

    def validate_token(self, token):
        self.__verify_token(token)
        return token


    @classmethod
    def __verify_token(self, token: str):
        if len(token) != 6:
            raise serializers.ValidationError("Kiritilgen mag'liwmat toliq emes!")

        if not token.isdigit():
            raise serializers.ValidationError("Kiritiliwi kerek bolg'an mag'liwmat sannan ibarat boliwi kerek.")
# END PHONE TOKEN VERIFY SERIALIZER


# RESEND AGAIN TO VERIFY ACCOUNT
class ResendPhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators = [validate_uzb_phone_number], required = True)

    def validate_phone_number(self, phone_number):
        account_exists = UserBase.objects.filter(phone_number=phone_number).exists()
        if not account_exists:
            raise serializers.ValidationError(f"{phone_number} doesn't exist.")
        return phone_number
# END RESEND AGAIN TO VERIFY ACCOUNT