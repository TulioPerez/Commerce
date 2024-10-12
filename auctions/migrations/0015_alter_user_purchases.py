# Generated by Django 5.1.1 on 2024-10-12 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0014_remove_user_purchases_user_purchases"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="purchases",
            field=models.ManyToManyField(
                blank=True, related_name="purchased_by", to="auctions.auction_listing"
            ),
        ),
    ]
