# Generated by Django 5.1.1 on 2024-10-21 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='NAZOV',
            field=models.CharField(max_length=200),
        ),
    ]
