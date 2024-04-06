from rest_framework.permissions import BasePermission
from wallet.models import Wallet
from django.
from user.utils import log_request,send_password_reset_mail,send_activation_mail,send_activation_phone,validatingPassword,checkRequest,errorResponse,successResponse
from rest_framework.response import Response

class IsWallet(BasePermission):
    def has_permission(self, request, view):
        try:
            walletUser = Wallet.objects.get(user=request.user,currency_code="NGN")
        except Wallet.DoesNotExist:
            return Response({"error": "Wallet does not exist"}, status=status.HTTP_403_FORBIDDEN)
  
        return True




