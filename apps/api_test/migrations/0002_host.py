# Generated by Django 3.2.12 on 2022-03-31 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_test', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('host', models.CharField(max_length=1024, verbose_name='Host地址')),
                ('description', models.CharField(blank=True, max_length=1024, null=True, verbose_name='描述')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hosts', to='api_test.project', verbose_name='所属项目')),
            ],
        ),
    ]
