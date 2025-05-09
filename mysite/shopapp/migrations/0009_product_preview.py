# Generated by Django 5.1.6 on 2025-04-24 19:03

import shopapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shopapp", "0008_order_receipt"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="preview",
            field=models.ImageField(
                blank=True, null=True, upload_to=shopapp.models.product_preview_path
            ),
        ),
    ]
