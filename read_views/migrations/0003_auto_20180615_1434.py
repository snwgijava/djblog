# Generated by Django 2.0.1 on 2018-06-15 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('read_views', '0002_readdetail'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='readdetail',
            options={'verbose_name': '阅读记录', 'verbose_name_plural': '阅读记录'},
        ),
        migrations.AlterModelOptions(
            name='readnum',
            options={'verbose_name': '阅读数', 'verbose_name_plural': '阅读数'},
        ),
    ]