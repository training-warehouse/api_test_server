# Generated by Django 3.2.12 on 2022-04-10 14:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_test', '0004_apirunrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='用例名称')),
                ('description', models.CharField(blank=True, max_length=1024, null=True, verbose_name='描述')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('apis', models.ManyToManyField(related_name='cases', to='api_test.Api')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cases', to='api_test.project', verbose_name='所属项目')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
            ],
        ),
        migrations.CreateModel(
            name='CaseArgument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='参数名称')),
                ('value', models.CharField(max_length=100, verbose_name='参数值')),
                ('case', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arguments', to='api_test.case', verbose_name='用例')),
            ],
        ),
        migrations.CreateModel(
            name='ApiArgument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='参数名字')),
                ('origin', models.CharField(choices=[('HEADER', 'HEADER'), ('BODY', 'BODY'), ('COOKIE', 'COOKIE')], max_length=20, verbose_name='参数来源')),
                ('format', models.CharField(max_length=100, verbose_name='参数获取格式')),
                ('api', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arguments', to='api_test.api', verbose_name='用例API')),
            ],
        ),
    ]
