from .models import Transaction,Wallet,Vault,Duration
from rest_framework import serializers
from rest_framework.validators import ValidationError
from random import randrange


class TransactionSerializer(serializers.ModelSerializer):
    class Meta(object):
        model=Transaction
        fields = ("id","user","name","transaction_type","transaction_id","reference_id","status","description","currency_code","amount","remainbalance","timestamp","sourceAccountNumber","sourceAccountName","sourceBankName","settlementId")

class WalletSerializer(serializers.ModelSerializer):
    class Meta(object):
        model=Wallet
        fields = '__all__'

class VaultaSerializer(serializers.ModelSerializer):
    class Meta(object):
        model= Vault
        fields = '__all__'
    def validate(self, data):
        amount = data.get('amount')
        currency_code = data.get('currency_code')
        user = self.context['request'].user

        # Retrieve the user's wallet based on the currency_code and user information
        try:
            user_wallet = Wallet.objects.get(user=user, currency_code=currency_code)
        except Wallet.DoesNotExist:
            raise serializers.ValidationError("Wallet not found for the specified currency code.")

        # Check if the wallet's balance is sufficient
        if user_wallet.balance < amount:
            raise serializers.ValidationError("Insufficient funds in the wallet.")

        return data

    def update(self, instance, validated_data):
        user = self.context['request'].user
        currency_code = instance.currency_code
        # # Proceed with updating the instance using the validated_data
        instance.name = validated_data.get('name', instance.name)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.deadline = validated_data.get('deadline', instance.deadline)
        fundedAmount = validated_data.get('fundedAmount', instance.fundedAmount)
        instance.withdrawAmount = validated_data.get('withdrawAmount', instance.withdrawAmount)
        # Retrieve the user's wallet based on the currency_code and user information
        try:
            wallet_balance = Wallet.objects.get(user=user, currency_code=currency_code)
        except Wallet.DoesNotExist:
            raise serializers.ValidationError("Wallet not found for the specified currency code.")
        print(wallet_balance.balance)
        # Perform your custom validation check for the update
        if fundedAmount != None:
            self.validate_amount_for_update(fundedAmount, wallet_balance.balance)
            instance.fundedAmount += fundedAmount
            wallet_balance.balance -= fundedAmount
            wallet_balance.save()

        # Update the balance and percentage fields
        instance.balance = instance.fundedAmount - instance.withdrawAmount
        if instance.amount and instance.balance:
            instance.percentage = (instance.balance / instance.amount) * 100
        else:
            instance.percentage = None

        instance.save()
        return instance

    def validate_amount_for_update(self, amount, wallet_balance):
        # Your custom validation logic here
        print("pass successfull")
        if int(amount) >= int(wallet_balance):
            raise serializers.ValidationError("Insufficient funds in the wallet for this update.")



class VaultSerializer(serializers.ModelSerializer):

    id = serializers.CharField(max_length=100,required=False)
    class Meta:
        model= Vault
        fields = '__all__'
    def create(self, validated_data):
        vault_type = validated_data['vault_type']
        
        name =  validated_data["name"]
        user = validated_data['user']


        if vault_type == 'safe':
            id = validated_data['id']
            duration = Duration.objects.get(id=id)  # You might need to adjust this based on your Duration model structure
            total_amount = validated_data['total_amount']
            #check if user have enough amount
            
            vault_data = {
                'vault_type': vault_type,
                'saved_amount': total_amount,
                'percentage': duration.percentage,
                'duration': duration,
                'total_amount': total_amount,
                "name":name,
                "payback_date": validated_data["payback_date"],
                "user":user

            }

        elif vault_type == 'target':
            start_date = validated_data['start_date']
            end_date = validated_data['end_date']
            total_amount = validated_data['total_amount']
            frequency = validated_data['frequency']
            name =  validated_data["name"]
            saved_amount = validated_data["saved_amount"]
            percentage = float(saved_amount / total_amount) * 100

            vault_data = {
                'vault_type': vault_type,
                'saved_amount': saved_amount,
                'percentage': percentage,
                'start_date': start_date,
                'end_date': end_date,
                'total_amount': total_amount,
                'frequency': frequency,
                'name': name,
                "user":user
            }

        return Vault.objects.create(**vault_data)
    
    
    def update(self, instance, validated_data):
        user = self.context['request'].user
        currency_code = instance.currency_code
        # # Proceed with updating the instance using the validated_data
        amount = validated_data.get('amount')
        # Retrieve the user's wallet based on the currency_code and user information
        try:
            wallet_balance = Wallet.objects.get(user=user, currency_code=currency_code)
        except Wallet.DoesNotExist:
            raise serializers.ValidationError("Wallet not found for the specified currency code.")
        print(wallet_balance.balance)
        # Perform your custom validation check for the update
        if amount != None:
            self.validate_amount_for_update(amount, wallet_balance.balance)
            instance.savedamount += amount
            wallet_balance.balance -= amount
            wallet_balance.save()

        # Update the balance and percentage fields
        instance.percentage = (instance.totalamount / instance.savedamount) * 100
        instance.save()
        return instance

    def validate_amount_for_update(self, amount, wallet_balance):
        # Your custom validation logic here
        print("pass successfull")
        if int(amount) >= int(wallet_balance):
            raise serializers.ValidationError("Insufficient funds in the wallet for this update.")



class DurationSerializer(serializers.ModelSerializer):
    class Meta(object):
        model=Duration
        fields = '__all__'