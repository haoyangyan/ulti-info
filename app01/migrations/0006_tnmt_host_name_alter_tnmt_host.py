# Generated by Django 4.1.4 on 2023-01-18 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_tnmt'),
    ]

    operations = [
        migrations.AddField(
            model_name='tnmt',
            name='host_name',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='主办姓名/Host name'),
        ),
        migrations.AlterField(
            model_name='tnmt',
            name='host',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='主办方/Host'),
        ),
    ]