# Generated by Django 4.2.4 on 2023-09-14 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0005_delete_oldpasswords"),
    ]

    operations = [
        migrations.AddField(
            model_name="usermodel",
            name="about",
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name="usermodel",
            name="address",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="usermodel",
            name="city",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="usermodel",
            name="country",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="usermodel",
            name="name",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="usermodel",
            name="state/region",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="usermodel",
            name="zip/code",
            field=models.IntegerField(max_length=20, null=True),
        ),
    ]
