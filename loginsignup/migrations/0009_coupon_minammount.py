# Generated by Django 5.1.2 on 2024-10-19 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginsignup', '0008_rename_discriptiion_coupon_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='minammount',
            field=models.TextField(default='100'),
            preserve_default=False,
        ),
    ]
