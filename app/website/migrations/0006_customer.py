# Generated by Django 5.1.1 on 2024-10-21 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_vat_payer_setting'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NAZOV', models.CharField(max_length=100)),
                ('ICO', models.CharField(blank=True, max_length=8, null=True)),
                ('DIC', models.CharField(blank=True, max_length=10, null=True)),
                ('IC_DPH', models.CharField(blank=True, max_length=12, null=True)),
            ],
        ),
    ]