# Generated by Django 2.0 on 2018-04-01 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_grapher', '0007_auto_20180401_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review_link',
            field=models.CharField(max_length=100),
        ),
    ]
