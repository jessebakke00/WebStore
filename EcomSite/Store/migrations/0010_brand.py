# Generated by Django 4.2 on 2023-07-11 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0009_customer_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=100)),
            ],
        ),
    ]
