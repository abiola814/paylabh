# Generated by Django 4.2.2 on 2023-06-14 18:20

import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone', models.CharField(max_length=17, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.", regex='^\\+?1?\\d{9,14}$')])),
                ('first_name', models.CharField(blank=True, max_length=20, null=True)),
                ('last_name', models.CharField(blank=True, max_length=80, null=True)),
                ('country_origin', models.CharField(blank=True, max_length=80, null=True)),
                ('recoveryCode', models.CharField(blank=True, max_length=10, null=True)),
                ('avatar', models.ImageField(blank=True, default=None, null=True, upload_to='profileImage/')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_login', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_bvn', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='bvnVerifyTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bvn', user.models.EncryptedField()),
                ('is_verified', models.CharField(default=False, max_length=50, verbose_name='isVerified')),
            ],
        ),
        migrations.CreateModel(
            name='EmailVerifyTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=50, verbose_name='email')),
                ('is_verified', models.CharField(default=False, max_length=50, verbose_name='isVerified')),
                ('code', models.CharField(max_length=50, verbose_name='code')),
            ],
        ),
        migrations.CreateModel(
            name='PhoneVerifyTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=50, verbose_name='phone')),
                ('is_verified', models.CharField(default=False, max_length=50, verbose_name='isVerified')),
                ('code', models.CharField(max_length=50, verbose_name='code')),
            ],
        ),
    ]
