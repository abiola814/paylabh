from rest_framework.permissions import BasePermission
from wallet.models import Wallet


class IsWallet(BasePermission):
    def has_permission(self, request, view):
        try:
            walletUser = Wallet.objects.get(user=request.user,currency_code="NGN")
        except walletUser.DoesNotExist:
            return False
  
        return True




