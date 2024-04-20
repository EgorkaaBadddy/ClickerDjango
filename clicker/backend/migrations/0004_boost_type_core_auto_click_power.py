# Generated by Django 5.0.3 on 2024-04-20 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_alter_boost_lvl_alter_core_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='boost',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'auto'), (0, 'casual')], default=0),
        ),
        migrations.AddField(
            model_name='core',
            name='auto_click_power',
            field=models.IntegerField(default=0),
        ),
    ]
