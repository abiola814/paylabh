from django.db import models
from user.models import User
from datetime import datetime, timedelta
# Create your models here.


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency_code = models.CharField(max_length=3)
    account_number = models.CharField(max_length=30,blank=True,null=True)
    bank_name = models.CharField(max_length=30,blank=True,null=True)
    account_name = models.CharField(max_length=80,blank=True,null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    limit = models.DecimalField(max_digits=10, decimal_places=2, default=200000)
    created = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.get_full_name}'s {self.currency_code} wallet"

class Transaction(models.Model):
    Success_status = 'Success'
    Failed_status = 'Failed'
    Pending_status = 'Pending'
    Reverse_status = "Reverse"

    STATUSES = [
        (Failed_status, 'Failed'),
        (Pending_status, "Pending"),
        (Success_status, "Success"),
        (Reverse_status,"Reverse")
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    transaction_type = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=20)
    reference_id = models.CharField(max_length=20)
    description = models.CharField(max_length=20,blank=True,null=True)
    currency_code = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    remainbalance = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_LabTransfer = models.BooleanField(default=False)
    is_Bills = models.BooleanField(default=False)
    is_Transfer = models.BooleanField(default=False)
    reference = models.JSONField(null=True,blank=True)
    DestinationAccountNumber= models.CharField(max_length=20,null=True,blank=True)
    DestinationAccountName = models.CharField(max_length=20,null=True,blank=True)
    DestinationBankName = models.CharField(max_length=20,null=True,blank=True)
    SourceAccountNumber= models.CharField(max_length=20,null=True,blank=True)
    SourceAccountName = models.CharField(max_length=20,null=True,blank=True)
    SourceBankName = models.CharField(max_length=20,null=True,blank=True)
    settlementId = models.CharField(max_length=20,null=True,blank=True)
    status = models.CharField(max_length=255, choices=STATUSES, default=Pending_status)
    response= models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_type} transaction for {self.user.first_name}"


class NameofSaving(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.name}"

# class Vault(models.Model):
#     name = models.CharField(max_length=120)
#     amount = models.DecimalField(("amount to save"), max_digits=10, decimal_places=2)
#     timestamp = models.DateTimeField(("date created"), auto_now=False, auto_now_add=True)
#     deadline = models.DateField()
#     fundedAmount = models.DecimalField(("funded amount"), max_digits=10, decimal_places=2,default=0)
#     withdrawAmount = models.DecimalField(("withdraw amount"), max_digits=10, decimal_places=2,default=0)
#     balance = models.DecimalField(("balance"), max_digits=10, decimal_places=2,blank=True, null=True)
#     percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
#     currency_code = models.CharField(max_length=3)

#     def save(self, *args, **kwargs):
#         self.balance = self.fundedAmount - self.withdrawAmount
#         if self.amount and self.balance:
#             self.percentage = (self.balance / self.amount) * 100
#         else:
#             self.percentage = None
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.name}"


class Duration(models.Model):
    percentage = models.PositiveIntegerField()
    start = models.PositiveIntegerField()
    end = models.PositiveIntegerField()

    def generate_date_range_with_increasing_percentage(self):
        # Calculate the start and end dates
        current_date = datetime.now().date()
        start_date = current_date + timedelta(days=self.start - 1)  # Subtract 1 to start from the current day
        end_date = current_date + timedelta(days=self.end)

        # Generate the date range between start and end dates
        date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

        # Calculate the increasing percentage for each date
        num_days = len(date_range)
        if num_days == 0:
            return []

        max_percentage = self.percentage
        percentage_increment = max_percentage / num_days
        percentages = [ (i + 1) * percentage_increment for i in range(num_days)]

        # Serialize the result into a JSON-serializable format
        result = [{'date': date.strftime('%Y-%m-%d'), 'percentage': percentage} for date, percentage in zip(date_range, percentages)]

        return result
class Vault(models.Model):
    VAULT_TYPES = [
        ('safe', 'Safe Lock'),
        ('target', 'Target Lock'),
    ]

    name = models.CharField(max_length=20,null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, blank=True)

    vault_type = models.CharField(max_length=10, choices=VAULT_TYPES,null=True, blank=True)
    saved_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    percentage = models.PositiveIntegerField(default=0)
    duration = models.ForeignKey(Duration, on_delete=models.SET_NULL, null=True, blank=True)
    payback_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    frequency = models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], max_length=10, null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True,blank=True,null=True)


# Chargefee model
class Chargefee(models.Model):
    ispercentage = models.BooleanField(default=True, help_text="Flag indicating if the charge is a percentage")
    chargeTitle = models.CharField(max_length=50, help_text="Title of the charge")
    value = models.FloatField(default=0, help_text="Value of the charge")

    def __str__(self):
        return str(self.chargeTitle)