from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path('sign_up/', views.UserSignUpApiView.as_view(), name = 'sign_up'),
    #path('verify/', views.PhoneTokenVerifyApiView.as_view(), name = 'verify'),
    #path('resend_phone_number/', views.ResendPhoneNumberApiView.as_view(), name = 'resend_phonenumber'),
    path('profile/<str:pk>/', views.ProfileRetrieveEditApiView.as_view(), name = 'profile'),
]