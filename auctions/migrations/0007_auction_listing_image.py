# Generated by Django 5.1.1 on 2024-10-10 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0006_rename_closing_date_auction_listing_closing_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="auction_listing",
            name="image",
            field=models.FileField(
                default="auctions/media/placeholder.jpg", upload_to="auction_images/"
            ),
            preserve_default=False,
        ),
    ]
