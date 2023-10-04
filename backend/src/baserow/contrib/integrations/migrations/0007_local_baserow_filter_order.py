# Generated by Django 3.2.21 on 2023-10-04 11:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("integrations", "0006_localbaserowtableservice_filter_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="localbaserowtableservicefilter",
            name="order",
            field=models.DecimalField(
                decimal_places=20,
                default=1,
                editable=False,
                help_text="Lowest first.",
                max_digits=40,
            ),
        ),
    ]
