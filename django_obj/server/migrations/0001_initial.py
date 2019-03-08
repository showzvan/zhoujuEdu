# Generated by Django 2.1.5 on 2019-01-28 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Centers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='中心名称')),
                ('num', models.PositiveIntegerField(verbose_name='编号')),
                ('address', models.CharField(max_length=255, verbose_name='地址')),
                ('phone', models.CharField(max_length=255, verbose_name='电话')),
                ('is_direct', models.BooleanField(default=False, verbose_name='是否直属')),
                ('is_status', models.BooleanField(default=True, verbose_name='状态')),
            ],
            options={
                'verbose_name': '学习中心',
                'verbose_name_plural': '学习中心',
                'db_table': 'zhouju_centers',
            },
        ),
        migrations.CreateModel(
            name='ServerCategorys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('catename', models.CharField(max_length=255, verbose_name='分类名')),
                ('is_status', models.BooleanField(default=True, verbose_name='状态')),
            ],
            options={
                'verbose_name': '服务大厅文章分类',
                'verbose_name_plural': '服务大厅文章分类',
                'db_table': 'zhouju_server_categorys',
            },
        ),
        migrations.CreateModel(
            name='ServerPosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_title', models.CharField(max_length=255, verbose_name='文章标题')),
                ('source', models.CharField(default='舟炬教育', max_length=255, verbose_name='文章来源')),
                ('source_link', models.URLField(default='http://www.zhoujuedu.com', verbose_name='来源链接')),
                ('post_content', models.TextField(verbose_name='文章内容')),
                ('edit_time', models.DateTimeField(auto_now=True, verbose_name='编辑时间')),
                ('views', models.IntegerField(default=0, verbose_name='阅读人数')),
                ('keywords', models.CharField(max_length=255, verbose_name='关键字')),
                ('is_status', models.BooleanField(default=True, verbose_name='状态')),
                ('cateid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.ServerCategorys', verbose_name='分类id')),
            ],
            options={
                'verbose_name': '服务大厅文章',
                'verbose_name_plural': '服务大厅文章',
                'db_table': 'zhouju_server_posts',
            },
        ),
    ]
