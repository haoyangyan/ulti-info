from django.shortcuts import render, HttpResponse, redirect
from app01 import models
from django import forms
from app01.utils.pagination import Pagination
from django.db.models import Q


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

def back(request):
    if "info" in request.session.keys():
        if request.session["info"]['name'] == 'admin':
            return render(request,'back.html')
    return HttpResponse('你不是管理员')

def team_info_list(request):
    if "info" in request.session.keys():
        if request.session["info"]['name'] == 'admin':
            data_list = models.Team.objects.all()
            return render(request, "info_team_list.html", {"data_list": data_list})
def tnmt_info_list(request):
    if "info" in request.session.keys():
        if request.session["info"]['name'] == 'admin':
            data_list = models.Tnmt.objects.all()
            return render(request, "info_tnmt_list.html", {"data_list": data_list})
def team_info_delete(request):
    if "info" in request.session.keys():
        if request.session["info"]['name'] == 'admin':
            nid = request.GET.get('nid')
            models.Team.objects.filter(id=nid).delete()
            return redirect("/team/info/list/")
def tnmt_info_delete(request):
    if "info" in request.session.keys():
        if request.session["info"]['name'] == 'admin':
            nid = request.GET.get('nid')
            models.Tnmt.objects.filter(id=nid).delete()
            return redirect("/tnmt/info/list/")
def team_info_edit(request):
    if "info" in request.session.keys():
        if request.session["info"]['name'] == 'admin':
            nid = request.GET.get('nid')
            if request.method == "GET":
                rowi = models.Team.objects.filter(id=nid).first()
                formi = TeamModelForm(instance=rowi)
                return render(request, 'team_add.html', {"form": formi})
            else:
                rowi = models.Team.objects.filter(id=nid).first()
                formi = TeamModelForm(data=request.POST, instance=rowi)
                if formi.is_valid():
                    formi.save()
                    return redirect("/team/info/list/")



def game_info_list(request):
    if "info" in request.session.keys():
        if request.session["info"]['name'] == 'admin':
            data_list = models.Game.objects.all()
            return render(request, "info_game_list.html", {"data_list": data_list})
def game_info_delete(request):
    if "info" in request.session.keys():
        if request.session["info"]['name'] == 'admin':
            nid = request.GET.get('nid')
            models.Game.objects.filter(id=nid).delete()
            return redirect("/game/info/list/")


def info_list(request):
    if "info" in request.session.keys():
        if request.session["info"]['name'] == 'admin':
            # 1.获取数据库中所有的用户信息
            data_list = models.UserInfo.objects.all()

            # 2.渲染，返回给用户
            return render(request, "info_list.html", {"data_list": data_list})

def info_delete(request):
    if "info" in request.session.keys():
        if request.session["info"]['name'] == 'admin':
            nid = request.GET.get('nid')
            models.UserInfo.objects.filter(id=nid).delete()
            return redirect("/info/list/")



def info_tnmt_edit(request):
    if "info" not in request.session.keys():
        return HttpResponse('请先登录')
    elif request.session["info"]['name'] != 'admin':
        return HttpResponse('你不是管理员')
    else:
        queryset = models.Tnmt.objects.filter(~Q(appro='Y'))
        return render(request, 'tnmt_edit.html', {'queryset': queryset})    

def info_accept(request,nid):
    models.Tnmt.objects.filter(id=nid).update(appro='Y')

    queryset = models.Tnmt.objects.all()
    return render(request, 'tnmt_edit.html', {'queryset': queryset})  