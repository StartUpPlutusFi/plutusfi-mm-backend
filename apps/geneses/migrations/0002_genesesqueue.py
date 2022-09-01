# Generated by Django 4.0.7 on 2022-09-01 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geneses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenesesQueue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cancel_code', models.CharField(max_length=128)),
                ('status', models.CharField(max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('geneses_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='geneses.geneses')),
            ],
        ),
    ]