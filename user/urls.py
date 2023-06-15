from django.contrib import admin
from django.urls import path,include
from .views import verifyMail,EmailVerifycode,PhoneVerifycode,activateMail,activatePhone,verifyPhone,SignupView
urlpatterns = [

    path('signup/', SignupView.as_view()),
    path('validatephone/', verifyPhone.as_view()),
    path('validateemail/',verifyMail.as_view()),
    path('activatemail/', activateMail.as_view()),
    path('activatephone/', activatePhone.as_view()),
    path('verifyemailcode/', EmailVerifycode.as_view()),
    path('verifyphonecode/', PhoneVerifycode.as_view()),

]