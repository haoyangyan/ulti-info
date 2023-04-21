from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from django import forms
from app01.utils.pagination import Pagination
from django.db.models import Q
import datetime

def tnmt_list(request):

    queryset = models.Tnmt.objects.filter(appro='Y', e_date__gte = datetime.date.today()).order_by('s_date')
    queryset2 = models.Tnmt.objects.filter(appro='Y', e_date__lt = datetime.date.today()).order_by('-s_date')

    return render(request, 'tnmt_list.html', {'queryset': queryset, 'queryset2': queryset2})


class TnmtModelForm(forms.ModelForm):
    tnmtname = forms.CharField(min_length=2, label="赛事/Tournament name")

    class Meta:
        model = models.Tnmt
        fields = ["tnmtname","divi","host_name","host","prov","city","s_date","e_date","o_link"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加了class="form-control"
        for tnmtname, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def tnmt_add(request):
    if request.method == "GET":
        if "info" not in request.session.keys():
            return HttpResponse('请先登录 / Please Register First')
        else:
            form = TnmtModelForm(initial={'host_name':request.session["info"]['name']})
            return render(request, 'tnmt_add.html', {"form": form})

    # 用户POST提交数据，数据校验。
    form = TnmtModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        if models.Tnmt.objects.filter(tnmtname=form.data['tnmtname'], s_date=form.data['s_date']).exists():
            return HttpResponse('该赛事已存在 / This tournament already exists')
        elif not models.UserInfo.objects.filter(name=form.data['host_name']).exists():
            return HttpResponse('主办人不存在 / The host name does not exist')
        form.save()
        return HttpResponse('您的赛事发布申请已提交，如一周内未通过，可按联系方式联系网站运营 / Your application of tournament publishing has sent. If it does not accepted in a week, you can connect the operation by the contact information')

    # 校验失败（在页面上显示错误信息）
    return render(request, 'tnmt_add.html', {"form": form})


def tnmt_list_edit(request):
    if "info" not in request.session.keys():
        return HttpResponse('请先登录 / Please Register First')
    else:
        queryset = models.Tnmt.objects.filter(host_name=request.session["info"]['name'])
        if request.session["info"]['name'] == 'admin':
            queryset = models.Tnmt.objects.all()
        return render(request, 'tnmt_list_edit.html', {'queryset': queryset})


def tnmt_n_edit(request,nid):
    if not models.Game.objects.filter(tnmt_id=nid).exists():
        return redirect('/game/'+str(nid)+'/new/')
    else:
        sch_n = max(list(models.Game.objects.filter(tnmt_id=nid).values_list('sch_id',flat=True)))
        return redirect('/game/'+str(nid)+'/'+str(sch_n)+'/edit/')

def tnmt_n_show(request,nid):
    if not models.Game.objects.filter(tnmt_id=nid).exists():
        return HttpResponse('赛程不存在 / The schedule does not exsit')
    else:
        sch_n = max(list(models.Game.objects.filter(tnmt_id=nid).values_list('sch_id',flat=True)))
        sch_min = min(list(models.Game.objects.filter(tnmt_id=nid).values_list('sch_id',flat=True)))
        return redirect('/game/'+str(nid)+'/'+str(sch_min)+'/show/')


class linkform(forms.ModelForm):
    class Meta:
        model = models.Tnmt
        fields = ['o_link']

def tnmt_n_linkedit(request,nid):
    if request.method == "GET":
        rowi = models.Tnmt.objects.filter(id=nid).first()
        linki = linkform(instance=rowi)
        return render(request, 'o_link.html', {'linki':linki})
    else:
        rowi = models.Tnmt.objects.filter(id=nid).first()
        linki = linkform(data=request.POST, instance=rowi)
        if linki.is_valid():
            linki.save()
            return redirect('/tnmt/list/edit/')
        return HttpResponse('数据不符合规范 / Data not valid')
