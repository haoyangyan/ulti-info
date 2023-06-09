# Generated by Django 4.1.4 on 2023-01-13 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teamname', models.CharField(max_length=32, verbose_name='队伍/Team')),
                ('divi', models.CharField(choices=[('混合/Mixed', '混合/Mixed'), ('公开/Open', '公开/Open'), ('女子/Women', '女子/Women')], max_length=32, verbose_name='组别/Division')),
                ('captain', models.CharField(max_length=32, verbose_name='队长/Captain')),
                ('prov', models.CharField(blank=True, max_length=32, null=True, verbose_name='省/Province')),
                ('city', models.CharField(blank=True, max_length=32, null=True, verbose_name='市/City')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='真实姓名/Legal Name')),
                ('pwd', models.CharField(max_length=32, verbose_name='密码/password')),
                ('gender', models.CharField(choices=[('男/Male', '男/Male'), ('女/Female', '女/Female')], max_length=32, verbose_name='性别/Gender')),
                ('DOB', models.DateTimeField(verbose_name='生日/DoB')),
                ('team1', models.CharField(blank=True, max_length=32, null=True)),
                ('team2', models.CharField(blank=True, max_length=32, null=True)),
                ('team3', models.CharField(blank=True, max_length=32, null=True)),
                ('team4', models.CharField(blank=True, max_length=32, null=True)),
                ('team5', models.CharField(blank=True, max_length=32, null=True)),
                ('teamapply', models.CharField(blank=True, max_length=32, null=True)),
            ],
        ),
    ]
