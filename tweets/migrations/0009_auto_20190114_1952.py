# Generated by Django 2.0.5 on 2019-01-14 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0008_auto_20190112_2026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='tags_helper',
        ),
        migrations.AddField(
            model_name='tag',
            name='num_of_tweets',
            field=models.PositiveIntegerField(default=0),
        ),
    ]