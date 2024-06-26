# Generated by Django 4.2.2 on 2023-07-17 23:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wallet', '0002_transaction_reference'),
    ]

    operations = [
        migrations.CreateModel(
            name='NameofSaving',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Vault',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='amount to save')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('deadline', models.DateField()),
                ('fundedAmount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='funded amount')),
                ('withdrawAmount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='withdraw amount')),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='balance')),
                ('percentage', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('currency_code', models.CharField(max_length=3)),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='settlementId',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sourceAccountName',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sourceAccountNumber',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sourceBankName',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='wallet',
            name='account_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='wallet',
            name='account_number',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
