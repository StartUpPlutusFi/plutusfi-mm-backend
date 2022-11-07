# Generated by Django 4.0.7 on 2022-11-01 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autotrade', '0002_alter_marketmakerbot_pair_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='marketmakerbotorderhistory',
            name='spreed',
        ),
        migrations.RemoveField(
            model_name='marketmakerbotorderhistory',
            name='trade_qty_high',
        ),
        migrations.RemoveField(
            model_name='marketmakerbotorderhistory',
            name='trade_qty_low',
        ),
        migrations.AddField(
            model_name='marketmakerbotautotradequeue',
            name='exec_ref_price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='marketmakerbotorderhistory',
            name='exec_ref_price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='marketmakerbotorderhistory',
            name='user_ref_price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='marketmakerbotorderhistory',
            name='pair_token',
            field=models.CharField(default='DUMMY', max_length=64),
        ),
        migrations.AlterField(
            model_name='marketmakerbotorderhistory',
            name='side',
            field=models.CharField(default='FILL', max_length=64),
        ),
        migrations.AlterField(
            model_name='marketmakerbotorderhistory',
            name='status',
            field=models.CharField(default='FINISHED', max_length=64),
        ),
    ]
