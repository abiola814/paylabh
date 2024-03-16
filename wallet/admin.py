from django.contrib import admin
from .models import Wallet,Transaction,Duration
# Register your models here.
admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(Duration)