# Generated by Django 2.1.5 on 2019-03-04 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('major', '0010_majors_is_net'),
    ]

    operations = [
        migrations.AlterField(
            model_name='majors',
            name='major_image',
            field=models.CharField(max_length=255, null=True, verbose_name='专业封面图'),
        ),
    ]
