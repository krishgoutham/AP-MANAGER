# Generated by Django 2.2.3 on 2019-08-10 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usrhome', '0004_auto_20190806_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='order_id',
            field=models.DateField(max_length=20),
        ),
    ]