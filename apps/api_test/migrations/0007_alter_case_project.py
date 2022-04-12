# Generated by Django 3.2.12 on 2022-04-12 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_test', '0006_alter_case_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cases', to='api_test.project', verbose_name='所属项目'),
        ),
    ]