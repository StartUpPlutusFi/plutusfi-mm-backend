# Generated by Django 4.0.6 on 2022-07-22 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketmakerbotorderhistory',
            name='side',
            field=models.CharField(max_length=4),
        ),
    ]
