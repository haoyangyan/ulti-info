# Generated by Django 4.1.4 on 2023-01-17 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_remove_userinfo_team2_remove_userinfo_team3_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='intro',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='简介/Intro'),
        ),
    ]
