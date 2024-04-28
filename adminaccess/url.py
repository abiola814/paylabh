# urls.py
from django.urls import path
from .views import (
    UserListAPIView, UserDetailAPIView,
    EmailVerifyTableListAPIView, EmailVerifyTableDetailAPIView,
    PhoneVerifyTableListAPIView, PhoneVerifyTableDetailAPIView,
    bvnVerifyTableListAPIView, bvnVerifyTableDetailAPIView,
    BeneficiaryTableListAPIView, BeneficiaryTableDetailAPIView,
)

urlpatterns = [
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
    
    path('email-verify/', EmailVerifyTableListAPIView.as_view(), name='email-verify-list'),
    path('email-verify/<int:pk>/', EmailVerifyTableDetailAPIView.as_view(), name='email-verify-detail'),
    
    path('phone-verify/', PhoneVerifyTableListAPIView.as_view(), name='phone-verify-list'),
    path('phone-verify/<int:pk>/', PhoneVerifyTableDetailAPIView.as_view(), name='phone-verify-detail'),
    
    path('bvn-verify/', bvnVerifyTableListAPIView.as_view(), name='bvn-verify-list'),
    path('bvn-verify/<int:pk>/', bvnVerifyTableDetailAPIView.as_view(), name='bvn-verify-detail'),
    
    path('beneficiary/', BeneficiaryTableListAPIView.as_view(), name='beneficiary-list'),
    path('beneficiary/<int:pk>/', BeneficiaryTableDetailAPIView.as_view(), name='beneficiary-detail'),
]
