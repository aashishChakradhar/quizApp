# Generated by Django 5.0.2 on 2024-04-11 14:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0012_alter_records_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='records',
            name='score',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=6, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100.0)]),
        ),
    ]
