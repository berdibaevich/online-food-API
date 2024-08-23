from backend.account.models import UserBase
from backend.api.v1.viewsets.permissions import IsOwnerOfProfile
from backend.restaurant.models import Feedback
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (MyAccountSerializer, PhoneTokenVerifySerializer,
                          ResendPhoneNumberSerializer, UserSerializer)
from .utils import generate_token, verify_token


# USER SIGN UP API VIEW
class UserSignUpApiView(generics.CreateAPIView):
    """
        REGISTER USHIN API VIEW OK :)
    """
    queryset = UserBase.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
       serializer = self.get_serializer(data = request.data)
       serializer.is_valid(raise_exception = True)
       user = serializer.save()
       refresh = RefreshToken.for_user(user)
       return Response(
        {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
       )
# END USER SIGN UP API VIEW


# PHONE TOKEN VERIFY API VIEW
class PhoneTokenVerifyApiView(views.APIView):
    """
    VERIFY PHONE TOKEN API VIEW :)
    """
    serializer_class = PhoneTokenVerifySerializer

    def put(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get("phone_number")
        phone_token = serializer.validated_data.get("token")
        account = verify_token(token=phone_token, phone_number=phone_number)
        if account:
            refresh = RefreshToken.for_user(account)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }
            )
        return Response(
            {'status': 'Invalid or expired token.'},
            status=status.HTTP_400_BAD_REQUEST
        )
# END PHONE TOKEN VERIFY API VIEW


# RESEND AGAIN API VIEW
class ResendPhoneNumberApiView(views.APIView):
    def post(self, request):
        serializer = ResendPhoneNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get("phone_number")
        account = UserBase.objects.filter(phone_number=phone_number).last()
        token, expires_at = generate_token()
        account.phone_token = token
        account.expires_at = expires_at
        account.save()
        return Response(
            {
            'status': 200,
            'message': 'Resend successfully. Please verify your account.',
            'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
# END RESEND AGAIN API VIEW


# PROFILE API VIEW FOR SPECIFIC USER & Edit
class ProfileRetrieveEditApiView(generics.RetrieveUpdateAPIView):
    """
        Customer's Profile
    """
    queryset = UserBase.objects.all().defer("last_name", "password", "last_login", "is_staff", "phone_token", "expires_at")
    serializer_class = MyAccountSerializer
    permission_classes = [IsOwnerOfProfile]
# END PROFILE API VIEW FOR SPECIFIC USER & Edit



# OUR CUSTOM TOKENOBTAINPAIRSERIALIZER
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
        WE ADD EXTRA FIELD FOR FEEDBACK 
        AND ALSO IN SETTINGS CHANGE DEFAULT CHECK OUT
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        is_feedback = Feedback.objects.filter(customer = user).exists()
        token['is_feedback'] = is_feedback
        return token
# END OUR CUSTOM TOKENOBTAINPAIRSERIALIZER
