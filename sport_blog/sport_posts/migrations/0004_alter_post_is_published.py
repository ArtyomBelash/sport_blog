# Generated by Django 4.1.7 on 2023-03-25 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport_posts', '0003_alter_comment_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='Опубликовано'),
        ),
    ]