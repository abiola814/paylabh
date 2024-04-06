# from rest_framework.permissions import BasePermission
# from wallet.models import Wallet
# from user.utils import log_request,send_password_reset_mail,send_activation_mail,send_activation_phone,validatingPassword,checkRequest,errorResponse,successResponse
# from rest_framework.response import Response
# from rest_framework import status


from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status
from wallet.models import Wallet

class IsWallet(BasePermission):
    message = "You do not have a wallet with the required currency."

    def has_permission(self, request, view):
        try:
            wallet = Wallet.objects.get(user=request.user, currency_code="NGN")
        except Wallet.DoesNotExist:
            return self.handle_no_wallet(request)

        return True

    def handle_no_wallet(self, request):
        return Response({"error": self.message}, status=status.HTTP_403_FORBIDDEN)




