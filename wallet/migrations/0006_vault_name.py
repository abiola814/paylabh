# Generated by Django 4.2.2 on 2023-12-24 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0005_duration_remove_vault_amount_remove_vault_balance_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vault',
            name='name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
