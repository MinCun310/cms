# Generated by Django 4.2.4 on 2023-09-12 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0004_oldpasswords"),
    ]

    operations = [
        migrations.DeleteModel(name="OldPasswords",),
    ]