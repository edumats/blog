# Generated by Django 3.1.4 on 2020-12-15 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_post_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='comment',
        ),
    ]