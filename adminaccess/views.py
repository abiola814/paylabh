# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.models import User, EmailVerifyTable, PhoneVerifyTable, bvnVerifyTable, BeneficiaryTable
from .serializers import UserSerializer, EmailVerifyTableSerializer, PhoneVerifyTableSerializer, bvnVerifyTableSerializer, BeneficiaryTableSerializer

class UserListAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EmailVerifyTableListAPIView(APIView):
    def get(self, request):
        email_verifications = EmailVerifyTable.objects.all()
        serializer = EmailVerifyTableSerializer(email_verifications, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmailVerifyTableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmailVerifyTableDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return EmailVerifyTable.objects.get(pk=pk)
        except EmailVerifyTable.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        email_verification = self.get_object(pk)
        serializer = EmailVerifyTableSerializer(email_verification)
        return Response(serializer.data)

    def put(self, request, pk):
        email_verification = self.get_object(pk)
        serializer = EmailVerifyTableSerializer(email_verification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        email_verification = self.get_object(pk)
        email_verification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PhoneVerifyTableListAPIView(APIView):
    def get(self, request):
        phone_verifications = PhoneVerifyTable.objects.all()
        serializer = PhoneVerifyTableSerializer(phone_verifications, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PhoneVerifyTableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PhoneVerifyTableDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return PhoneVerifyTable.objects.get(pk=pk)
        except PhoneVerifyTable.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        phone_verification = self.get_object(pk)
        serializer = PhoneVerifyTableSerializer(phone_verification)
        return Response(serializer.data)

    def put(self, request, pk):
        phone_verification = self.get_object(pk)
        serializer = PhoneVerifyTableSerializer(phone_verification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        phone_verification = self.get_object(pk)
        phone_verification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class bvnVerifyTableListAPIView(APIView):
    def get(self, request):
        bvn_verifications = bvnVerifyTable.objects.all()
        serializer = bvnVerifyTableSerializer(bvn_verifications, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = bvnVerifyTableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class bvnVerifyTableDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return bvnVerifyTable.objects.get(pk=pk)
        except bvnVerifyTable.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        bvn_verification = self.get_object(pk)
        serializer = bvnVerifyTableSerializer(bvn_verification)
        return Response(serializer.data)

    def put(self, request, pk):
        bvn_verification = self.get_object(pk)
        serializer = bvnVerifyTableSerializer(bvn_verification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        bvn_verification = self.get_object(pk)
        bvn_verification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BeneficiaryTableListAPIView(APIView):
    def get(self, request):
        beneficiaries = BeneficiaryTable.objects.all()
        serializer = BeneficiaryTableSerializer(beneficiaries, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BeneficiaryTableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BeneficiaryTableDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return BeneficiaryTable.objects.get(pk=pk)
        except BeneficiaryTable.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        beneficiary = self.get_object(pk)
        serializer = BeneficiaryTableSerializer(beneficiary)
        return Response(serializer.data)

    def put(self, request, pk):
        beneficiary = self.get_object(pk)
        serializer = BeneficiaryTableSerializer(beneficiary, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        beneficiary = self.get_object(pk)
        beneficiary.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
