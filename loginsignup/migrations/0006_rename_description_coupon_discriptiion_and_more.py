# Generated by Django 5.1.2 on 2024-10-18 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginsignup', '0005_rename_discriptiion_coupon_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupon',
            old_name='description',
            new_name='discriptiion',
        ),
        migrations.AddField(
            model_name='user',
            name='conformpassword',
            field=models.CharField(default='password', max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(default='password', max_length=100),
        ),
    ]
