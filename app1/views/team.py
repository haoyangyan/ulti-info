from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from django import forms
from app01.utils.pagination import Pagination
from django.db.models import Q



def team_list(request):
    """ 部门列表 """

    # 去数据库中获取所有的部门列表
    #  [对象,对象,对象]
    queryset = models.Team.objects.all()
    # print(request.session.keys())
    # print(models.Team.objects.get(captain='p1'))
    # print(str(models.UserInfo.objects.filter(id=8).values().get()['team1'])+'-')

    return render(request, 'team_list.html', {'queryset': queryset})




class TeamModelForm(forms.ModelForm):
    teamname = forms.CharField(min_length=2, label="队名/Teamname")

    class Meta:
        model = models.Team
        fields = ["teamname", "divi", "captain","prov","city","intro"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加了class="form-control"
        for teamname, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def team_add(request):
    """ 添加用户（ModelForm版本）"""
    if request.method == "GET":
        if "info" not in request.session.keys():
            return HttpResponse('请先登录 / Please Register First')
        else:
            form = TeamModelForm(initial={'captain':request.session["info"]['name']})
            return render(request, 'team_add.html', {"form": form})

    # 用户POST提交数据，数据校验。
    form = TeamModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        # {'name': '123', 'password': '123', 'age': 11, 'account': Decimal('0'), 'create_time': datetime.datetime(2011, 11, 11, 0, 0, tzinfo=<UTC>), 'gender': 1, 'depart': <Department: IT运维部门>}
        # print(form.cleaned_data)
        # models.UserInfo.objects.create(..)
        if models.Team.objects.filter(teamname=form.data['teamname']).exists():
            return HttpResponse('该队伍已存在 / This team already exists')
        elif not models.UserInfo.objects.filter(name=form.data['captain']).exists():
            return HttpResponse('队长不存在 / The captain does not exist')
        form.save()
        return redirect('/team/list')

    # 校验失败（在页面上显示错误信息）
    return render(request, 'team_add.html', {"form": form})







#############
def team_roster(request,nid):
    row_object = models.Team.objects.filter(id=nid).first()

    queryset = models.UserInfo.objects.filter(team1__contains=(row_object.teamname+'-'))

    queryset2 = models.Game.objects.filter(Q(home=row_object.teamname) | Q(away=row_object.teamname))

    return render(request, 'team_roster.html', {'queryset': queryset, 'teamid1':nid,'teamname1':row_object.teamname, 'intro1':row_object.intro, 'queryset2': queryset2} )



def team_join(request,nid):
    row_object = models.Team.objects.filter(id=nid).first()
    if "info" not in request.session.keys():
        return HttpResponse('请先登录 / Please Login First')
    elif models.UserInfo.objects.filter(id=request.session["info"]['id'],team1__contains=row_object.teamname+'-').exists():
        return HttpResponse('您已在该队伍中/ You are already in this team')
    else:
        models.UserInfo.objects.filter(id=request.session["info"]['id']).update(teamapply=row_object.id)

        return HttpResponse('申请成功，您过往未完成的申请将被覆盖 / Application sent, your previous unaccepted application will be covered')

def team_edit(request):
    if "info" not in request.session.keys():
        return HttpResponse('请先登录 / Please Register First')
    elif not models.Team.objects.filter(captain=request.session["info"]['name']).exists():
        return HttpResponse('你不是队长 / You are not a captain')
    else:
        team_cap = models.Team.objects.filter(captain=request.session["info"]['name']).values_list('id')
        #team_cap1 = (list(team_cap))
        #print(team_cap)
        #return HttpResponse('你不是队长1 / You are not a captain')
        select_i = {'applyname':'select teamname from app01_team where app01_team.id=app01_userinfo.teamapply'}
        queryset = models.UserInfo.objects.filter(teamapply__in = team_cap).extra(select=select_i)
        return render(request, 'team_edit.html', {'queryset': queryset})

def team_accept(request,nid,mid):
    temp = str(models.UserInfo.objects.filter(id=nid).values().get()['team1'])
    row_object = models.Team.objects.filter(id=mid).first()
    models.UserInfo.objects.filter(id=nid).update(team1=temp+row_object.teamname+'-')
    models.UserInfo.objects.filter(id=nid).update(teamapply=None)
    return redirect('/team/edit')

def team_reject(request,nid,mid):
    models.UserInfo.objects.filter(id=nid).update(teamapply=None)
    return redirect('/team/edit')
