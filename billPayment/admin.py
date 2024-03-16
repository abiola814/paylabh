from django.contrib import admin
from .models import NetworkType,DataBundle,Bills,Exam,Cable
# Register your models here.
admin.site.register(NetworkType)
admin.site.register(DataBundle)
admin.site.register(Cable)
admin.site.register(Bills)
admin.site.register(Exam)