# Generated by Django 2.0.5 on 2019-01-12 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20190112_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='followers_count',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
    ]