# Generated by Django 2.2.4 on 2021-06-23 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_dashboard_app', '0003_auto_20210622_0311'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
