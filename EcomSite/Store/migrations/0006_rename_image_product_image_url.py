# Generated by Django 4.2 on 2023-06-14 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0005_alter_category_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='image',
            new_name='image_url',
        ),
    ]
