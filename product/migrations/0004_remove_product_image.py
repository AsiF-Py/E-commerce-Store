# Generated by Django 4.2.6 on 2023-12-06 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
    ]