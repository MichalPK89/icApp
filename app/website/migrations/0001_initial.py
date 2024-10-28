# Generated by Django 5.1.1 on 2024-10-28 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer_VAT_check',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('NAZOV', models.CharField(max_length=200)),
                ('ICO', models.CharField(blank=True, max_length=20, null=True)),
                ('IC_DPH_customer', models.CharField(blank=True, max_length=20, null=True)),
                ('IC_DPH_fin', models.CharField(blank=True, max_length=20, null=True)),
                ('DRUH_REG_DPH', models.CharField(blank=True, max_length=10, null=True)),
                ('DESCRIPTION', models.CharField(blank=True, max_length=40, null=True)),
            ],
            options={
                'db_table': 'customer_vat_check',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NAZOV', models.CharField(max_length=200)),
                ('ICO', models.CharField(blank=True, max_length=20, null=True)),
                ('DIC', models.CharField(blank=True, max_length=20, null=True)),
                ('IC_DPH', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vat_payer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DatumAktualizacieZoznamu', models.DateField()),
                ('IC_DPH', models.CharField(blank=True, max_length=20, null=True)),
                ('ICO', models.CharField(blank=True, max_length=20, null=True)),
                ('NAZOV_DS', models.CharField(blank=True, max_length=200, null=True)),
                ('OBEC', models.CharField(blank=True, max_length=100, null=True)),
                ('PSC', models.CharField(blank=True, max_length=10, null=True)),
                ('ULICA_CISLO', models.CharField(blank=True, max_length=100, null=True)),
                ('STAT', models.CharField(blank=True, max_length=50, null=True)),
                ('DRUH_REG_DPH', models.CharField(blank=True, max_length=5, null=True)),
                ('DATUM_REG', models.DateField(blank=True, null=True)),
                ('DATUM_ZMENY_DRUHU_REG', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vat_payer_setting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('DRUH_REG_DPH', models.CharField(max_length=5, unique=True)),
                ('PLATNY_DRUH_REG', models.BooleanField()),
            ],
        ),
    ]
