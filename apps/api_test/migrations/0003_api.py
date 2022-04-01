# Generated by Django 3.2.12 on 2022-04-01 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_test', '0002_host'),
    ]

    operations = [
        migrations.CreateModel(
            name='Api',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='接口名字')),
                ('http_method', models.CharField(choices=[('POST', 'POST'), ('GET', 'GET'), ('PUT', 'PUT'), ('DELETE', 'DELETE')], max_length=50, verbose_name='请求方式')),
                ('path', models.CharField(max_length=1024, verbose_name='接口地址')),
                ('headers', models.TextField(blank=True, null=True, verbose_name='请求头')),
                ('data', models.TextField(blank=True, null=True, verbose_name='请求的数据')),
                ('description', models.CharField(blank=True, max_length=1024, null=True, verbose_name='描述')),
                ('expect_code', models.CharField(choices=[('200', '200'), ('201', '201'), ('202', '202'), ('203', '203'), ('204', '204'), ('301', '301'), ('302', '302'), ('400', '400'), ('401', '401'), ('403', '403'), ('404', '404'), ('405', '405'), ('406', '406'), ('407', '407'), ('408', '408'), ('500', '500'), ('502', '502')], default=200, max_length=10, verbose_name='期望返回的code')),
                ('expect_content', models.CharField(blank=True, max_length=255, null=True, verbose_name='期望返回的内容')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_test.host', verbose_name='host')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='apis', to='api_test.project', verbose_name='项目')),
            ],
        ),
    ]
