# Generated by Django 2.2.3 on 2019-08-10 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usrhome', '0007_auto_20190810_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='paid_on',
            field=models.DateTimeField(max_length=20, null=True),
        ),
    ]