# Generated by Django 3.2.21 on 2023-12-05 10:01

import django.db.models.deletion
from django.db import migrations, models

import baserow.core.formula.field


class Migration(migrations.Migration):
    dependencies = [
        ("builder", "0030_dropdownelement"),
    ]

    operations = [
        migrations.AddField(
            model_name="dropdownelement",
            name="default_value",
            field=baserow.core.formula.field.FormulaField(
                default="", help_text="This dropdowns input's default value."
            ),
        ),
        migrations.AddField(
            model_name="dropdownelement",
            name="label",
            field=baserow.core.formula.field.FormulaField(
                default="", help_text="The text label for this dropdown"
            ),
        ),
        migrations.AddField(
            model_name="dropdownelement",
            name="placeholder",
            field=baserow.core.formula.field.FormulaField(
                default="",
                help_text="The placeholder text which should be applied to the element.",
            ),
        ),
        migrations.AddField(
            model_name="dropdownelement",
            name="required",
            field=models.BooleanField(
                default=False, help_text="Whether this drodpown is a required field."
            ),
        ),
        migrations.CreateModel(
            name="DropdownElementOption",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "value",
                    baserow.core.formula.field.FormulaField(
                        default="", help_text="The value of the option"
                    ),
                ),
                (
                    "name",
                    baserow.core.formula.field.FormulaField(
                        default="", help_text="The display name of the option"
                    ),
                ),
                (
                    "dropdown",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="builder.dropdownelement",
                    ),
                ),
            ],
        ),
    ]
