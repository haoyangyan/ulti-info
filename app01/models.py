from django.db import models

# Create your models here.


class Team(models.Model):
    """ 队伍表 """
    teamname = models.CharField(verbose_name='队伍/Team', max_length=32,unique=True)
    divi_choices = (
        ("混合/Mixed", "混合/Mixed"),
        ("公开/Open", "公开/Open"),
        ("女子/Women", "女子/Women"),
    )
    divi = models.CharField(verbose_name="组别/Division", choices=divi_choices, max_length=32)
    captain = models.CharField(verbose_name='队长/Captain', max_length=32)
    prov = models.CharField(verbose_name='省/Province', max_length=32,null=True,blank=True)
    city = models.CharField(verbose_name='市/City', max_length=32,null=True,blank=True)
    intro = models.CharField(verbose_name='简介/Intro', max_length=512,null=True,blank=True)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """ 会员表 """
    name = models.CharField(verbose_name="姓名/Name", max_length=16)
    pwd = models.CharField(verbose_name="密码/password", max_length=32)
    gender_choices = (
        ("男/Male", "男/Male"),
        ("女/Female", "女/Female"),
    )
    gender = models.CharField(verbose_name="性别/Gender", choices=gender_choices,max_length=32)
    DOB= models.DateField(verbose_name="生日/DoB (YYYY-MM-DD)")

    team1 = models.CharField(max_length=32,null=True,blank=True)
    teamapply = models.CharField(max_length=32,null=True,blank=True)
    confirm_pwd = models.CharField(verbose_name="确认密码/confirm_password", max_length=32,null=True,blank=True)
    # 在django中做的约束


class Tnmt(models.Model):
    """ 赛事表 """
    tnmtname = models.CharField(verbose_name='赛事/Tournament', max_length=32)
    divi_choices = (
        ("混合/Mixed", "混合/Mixed"),
        ("公开/Open", "公开/Open"),
        ("女子/Women", "女子/Women"),
    )
    divi = models.CharField(verbose_name="性别组别/Division", choices=divi_choices, max_length=32)
    host_name = models.CharField(verbose_name='主办姓名/Host name', max_length=32,null=True,blank=True)
    host = models.CharField(verbose_name='主办方/Host', max_length=32,null=True,blank=True)
    prov = models.CharField(verbose_name='省/Province', max_length=32,null=True,blank=True)
    city = models.CharField(verbose_name='市/City', max_length=32,null=True,blank=True)
    s_date = models.DateField(verbose_name="开始日期/Start date (YYYY-MM-DD)")
    e_date = models.DateField(verbose_name="结束日期/End date (YYYY-MM-DD)")

    #intro = models.CharField(verbose_name='简介/Intro', max_length=512,null=True,blank=True)
    o_link = models.CharField(verbose_name='外链/Link', max_length=512,null=True,blank=True)

    appro = models.CharField(verbose_name='通过', max_length=32)

    def __str__(self):
        return self.title

class Game(models.Model):
    """比赛表"""
    tnmt = models.ForeignKey(to='Tnmt',to_field='id',on_delete=models.CASCADE)
    type_choice = (
        ('i2','单场比赛'),
        ('i3','两场比赛'),
        ('i5','四场比赛'),
        ('i9','八场比赛'),
        ('b4','4队淘汰赛'),
        ('b6','6队淘汰赛'),
        ('b8','8队淘汰赛'),
        ('b12','12队淘汰赛'),
        ('b16','16队淘汰赛'),
        ('1p3','1组3队小组赛'),
        ('1p4','1组4队小组赛'),
        ('1p5','1组5队小组赛'),
        ('1p6','1组6队小组赛'),
        ('2p3','2组6队小组赛'),
        ('2p4','2组8队小组赛'),
        ('2p5','2组10队小组赛'),
        ('2p6','2组12队小组赛'),
        ('3p3','3组9队小组赛'),
        ('3p4','3组12队小组赛'),
        ('4p3','4组12队小组赛'),
        ('4p4','4组16队小组赛'),
        ('4p5','4组20队小组赛'),
    )
    sch_type = models.CharField(max_length=32,choices=type_choice)
    sch_id = models.IntegerField()
    sch_name = models.CharField(max_length=32)
    game_id = models.IntegerField()
    game_name = models.CharField(verbose_name='比赛编号', max_length=32,null=True,blank=True)
    game_info = models.CharField(verbose_name='时间&场地', max_length=32,null=True,blank=True)
    home = models.CharField(max_length=32,null=True,blank=True)
    away = models.CharField(max_length=32,null=True,blank=True)
    home_s = models.IntegerField(default=0)
    away_s = models.IntegerField(default=0)
    tnmt_name = models.CharField(max_length=32,null=True,blank=True)
    date = models.DateField(null=True,blank=True)


    def __str__(self):
        return self.title


class Pool(models.Model):
    tnmt = models.ForeignKey(to='Tnmt',to_field='id',on_delete=models.CASCADE)
    sch_id = models.IntegerField()
    pool_id = models.IntegerField()
    team_id = models.IntegerField()
    team = models.CharField(max_length=32,null=True,blank=True)
    result = models.CharField(max_length=32,null=True,blank=True,default='0-0')
    score_d = models.CharField(max_length=32,null=True,blank=True)

    def __str__(self):
        return self.title


