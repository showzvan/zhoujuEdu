# Generated by Django 2.1.5 on 2019-03-04 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_emailverifyrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='nickname',
            field=models.CharField(max_length=255, null=True, unique=True, verbose_name='用户名'),
        ),
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(max_length=255, null=True, verbose_name='密码'),
        ),
    ]
