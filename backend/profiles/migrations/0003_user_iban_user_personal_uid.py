# Generated by Django 5.1.3 on 2024-12-09 13:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "profiles",
            "0002_user_bank_statement_image_user_identity_card_image_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="iban",
            field=models.CharField(blank=True, max_length=34, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="personal_uid",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
