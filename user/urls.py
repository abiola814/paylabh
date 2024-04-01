from django.contrib import admin
from django.urls import path,include
from .views import *
urlpatterns = [

    path('signup/', SignupView.as_view()),
    path('tag/', TagView.as_view()),
    path('validatephone/', verifyPhone.as_view()),
    path('validateemail/',verifyMail.as_view()),
    path('activatemail/', activateMail.as_view()),
    path('activatephone/', activatePhone.as_view()),
    path('verifyemailcode/', EmailVerifycode.as_view()),
    path('verifyphonecode/', PhoneVerifycode.as_view()),
    path('login/', LoginView.as_view()),
     path('passcodelogin/', PasscodeLoginView.as_view()),
    path('forgotpassword/',ForgotPasswordView.as_view()),
    path('passcode/',CreatePasscodeView.as_view()),
    path('transactionpin/',TransactionPinView.as_view()),
    path("profileimage/",ProfileImage.as_view()),
    path("profile/",Profile.as_view()),
    path("changepassword/",Changepassword.as_view()),
    path("country/",CountryView.as_view()),
    path("reason/",JoinreasonView.as_view()),
    path("Beneficairy/",Beneficairy.as_view()),
    path('referral-link/', ReferralLinkView.as_view(), name='referral_link'),



]
