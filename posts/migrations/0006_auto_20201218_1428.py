# Generated by Django 3.1.4 on 2020-12-18 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_remove_post_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='overview',
            field=models.CharField(help_text='Description of your post', max_length=160),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(help_text='Try placing important keywords first', max_length=60),
        ),
    ]
