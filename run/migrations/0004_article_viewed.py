# Generated by Django 4.1.5 on 2023-01-28 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('run', '0003_article_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='viewed',
            field=models.PositiveIntegerField(default=0, verbose_name='Views'),
        ),
    ]
