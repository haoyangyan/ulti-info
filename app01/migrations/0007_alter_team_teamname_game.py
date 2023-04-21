# Generated by Django 4.1.4 on 2023-01-25 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_tnmt_host_name_alter_tnmt_host'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='teamname',
            field=models.CharField(max_length=32, unique=True, verbose_name='队伍/Team'),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sch_type', models.CharField(max_length=32)),
                ('sch_id', models.CharField(max_length=32)),
                ('sch_name', models.CharField(max_length=32)),
                ('game_id', models.CharField(max_length=32)),
                ('game_name', models.CharField(blank=True, max_length=32, null=True, verbose_name='赛事编号')),
                ('game_info', models.CharField(max_length=32, verbose_name='时间&地点')),
                ('home_s', models.IntegerField(default=0)),
                ('away_s', models.IntegerField(default=0)),
                ('away', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='a', to='app01.team', to_field='teamname')),
                ('home', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='h', to='app01.team', to_field='teamname')),
                ('tnmt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.tnmt')),
            ],
        ),
    ]
