from django.contrib import admin
from django.urls import path,include
from .views import *
from .coralpay import coralpay_webhook
urlpatterns = [

    path('wallet/', WalletView.as_view()),
    path('transaction/', TransactionsView.as_view()),
    path('vault/', VaultView.as_view()),
    path('Account/', AccountView.as_view()),
    path('webhook/',coralpay_webhook,name="bankhook"),
    path("labtransfer/",LabTransferView.as_view()),
     path("duration/",DurationView.as_view()),
    path('payback/', PaybackView.as_view()),
    path('checkbank/',  CheckUserBankDetails.as_view()),
    path('transfer/', BankTransfer.as_view()),

        path('bank-list/', BankListView.as_view()),


]