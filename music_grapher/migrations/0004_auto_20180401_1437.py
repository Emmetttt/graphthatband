# Generated by Django 2.0 on 2018-04-01 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_grapher', '0003_auto_20180328_1407'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='album_id',
        ),
        migrations.RemoveField(
            model_name='album',
            name='score_avg',
        ),
        migrations.AddField(
            model_name='album',
            name='album_link',
            field=models.CharField(default='x', max_length=200),
        ),
        migrations.AddField(
            model_name='album',
            name='critic_score_avg',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='album',
            name='user_score_avg',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='album',
            name='album_name',
            field=models.CharField(default='x', max_length=50),
        ),
        migrations.AlterField(
            model_name='album',
            name='review_summary',
            field=models.CharField(default='x', max_length=5000),
        ),
    ]