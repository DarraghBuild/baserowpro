# Generated by Django 3.2.21 on 2023-10-31 10:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("builder", "0029_inputtextelement_label"),
    ]

    operations = [
        migrations.AddField(
            model_name="builderworkflowaction",
            name="order",
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]