# Generated by Django 5.1.1 on 2024-10-10 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0011_alter_auction_listing_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="auction_listing",
            name="image",
            field=models.FileField(default="media/placeholder.jpg", upload_to="media/"),
        ),
    ]
