# Generated by Django 2.0 on 2019-05-10 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateTimeField(auto_now=True, verbose_name='发表日期'),
        ),
    ]
