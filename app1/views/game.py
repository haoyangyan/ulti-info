from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from django import forms
from app01.utils.pagination import Pagination


def game_new(request,nid):
    if "info" not in request.session.keys():
        return HttpResponse('请先登录 / Please Register First')
    if (request.session["info"]['name'] != models.Tnmt.objects.filter(id=nid).values().get()['host_name']) and (request.session["info"]['name'] != 'admin'):
        return HttpResponse('你不是主办 / You are not the holder')

    if request.method == "GET":
        choices = {'type_choice':models.Game.type_choice}
        return render(request,'game_new.html',choices)
    else:
        if not models.Game.objects.filter(tnmt_id=nid).exists():
            sch_n = 0
        else:
            sch_n = max(list(models.Game.objects.filter(tnmt_id=nid).values_list('sch_id',flat=True)))
        
        date = models.Tnmt.objects.filter(id=nid).values().get()['s_date']
        tnmt_name = models.Tnmt.objects.filter(id=nid).values().get()['tnmtname']
        sch_type = request.POST.get('sch_type') 
        sch_name = request.POST.get('sch_name') 

        for j in [2,3,4,5,6,8,9,10,12,16]:
            if (sch_type=='b'+str(j)) or (sch_type=='i'+str(j)):
                for i in range(j-1):
                    models.Game.objects.create(tnmt_id=nid, sch_type=sch_type, sch_id=sch_n+1, sch_name=sch_name, game_id=i+1, date=date, tnmt_name=tnmt_name)
                return redirect('/tnmt/'+str(nid)+'/edit/')
        for j in [1,2,3,4]:
            for i in [3,4,5,6]:
                if sch_type == str(j)+'p'+str(i):
                    for k in range(int(j*i*(i-1)/2)):
                        models.Game.objects.create(tnmt_id=nid, sch_type=sch_type, sch_id=sch_n+1, sch_name=sch_name, game_id=k+1, date=date, tnmt_name=tnmt_name)
                    for jj in range(j):
                        for ii in range(i):
                            models.Pool.objects.create(tnmt_id=nid, sch_id=sch_n+1, pool_id=jj+1, team_id=ii+1)
                    return redirect('/tnmt/'+str(nid)+'/edit/')
        return HttpResponse('error')

def game_nm_show(request,nid,mid):
    select_h = {'homeid':'select id from app01_team where app01_team.teamname=app01_game.home','awayid':'select id from app01_team where app01_team.teamname=app01_game.away'}
    queryset = models.Game.objects.filter(tnmt_id=nid, sch_id=mid).order_by('game_id').extra(select=select_h)
    #print(queryset)
    #raw_qs = Game.objects.raw('select * from app01_game;')
    #.filter(tnmt_id=nid, sch_id=mid).order_by('game_id')
    #print(queryset)
    #team_query = models.Team.objects.all()

    sch_n = max(list(models.Game.objects.filter(tnmt_id=nid).values_list('sch_id',flat=True)))
    sch_type = models.Game.objects.filter(tnmt_id=nid, sch_id=mid).values().first()['sch_type']
    t_n = models.Tnmt.objects.filter(id=nid).values().first()['tnmtname']
    queryset2 = models.Game.objects.filter(tnmt_id=nid).values('sch_id','sch_name').distinct()
    if sch_type[0] == 'b':
        return render(request, sch_type+'.html', {'queryset':queryset, 'sch_n':sch_n, 't_n':t_n, 'queryset2':queryset2})
    elif sch_type[0] == 'i':
        return render(request, 'b2.html', {'queryset':queryset, 'sch_n':sch_n, 't_n':t_n, 'queryset2':queryset2})
    else:
        select_p = {'homeid':'select id from app01_team where app01_team.teamname=app01_pool.team'}
        queryset3 = models.Pool.objects.filter(tnmt_id=nid, sch_id=mid).order_by('pool_id','team_id').extra(select=select_p)
        p_n = int(sch_type[2])
        return render(request, sch_type[0:2]+'.html', {'queryset':queryset, 'sch_n':sch_n, 't_n':t_n, 'queryset2':queryset2, 'queryset3':queryset3, 'p_n':p_n})




class gameform(forms.ModelForm):
    class Meta:
        model = models.Game
        fields = ['game_name','game_info','home','home_s','away_s','away']
        widgets = {
            'game_name':forms.TextInput(attrs={'class':'formcontrol','placeholder':'比赛编号','style': 'width:70px;'}),
            'game_info':forms.TextInput(attrs={'class':'formcontrol','placeholder':'时间&场地','style': 'width:70px;'}),
            'home':forms.TextInput(attrs={'class':'formcontrol','placeholder':'主队','style': 'width:70px;'}),
            'home_s':forms.TextInput(attrs={'class':'formcontrol','placeholder':'主分','style': 'width:70px;'}),
            'away_s':forms.TextInput(attrs={'class':'formcontrol','placeholder':'客分','style': 'width:70px;'}),
            'away':forms.TextInput(attrs={'class':'formcontrol','placeholder':'客队','style': 'width:70px;'}),
        }

class poolform(forms.ModelForm):
    class Meta:
        model = models.Pool
        fields = ['team','result','score_d']
        widgets = {
            'team':forms.TextInput(attrs={'class':'formcontrol','placeholder':'队伍'}),
            'result':forms.TextInput(attrs={'class':'formcontrol','placeholder':'胜-负'}),
            'score_d':forms.TextInput(attrs={'class':'formcontrol','placeholder':'净胜分'}),
        }




def game_nm_edit(request,nid,mid):
    if "info" not in request.session.keys():
        return HttpResponse('请先登录 / Please Register First')
    if (request.session["info"]['name'] != models.Tnmt.objects.filter(id=nid).values().get()['host_name']) and (request.session["info"]['name'] != 'admin'):
        return HttpResponse('你不是主办 / You are not the holder')
    queryset = models.Game.objects.filter(tnmt_id=nid, sch_id=mid).order_by('game_id')
    sch_n = max(list(models.Game.objects.filter(tnmt_id=nid).values_list('sch_id',flat=True)))
    sch_type = models.Game.objects.filter(tnmt_id=nid, sch_id=mid).values().first()['sch_type']
    t_n = models.Tnmt.objects.filter(id=nid).values().first()['tnmtname']
    queryset2 = models.Game.objects.filter(tnmt_id=nid).values('sch_id','sch_name').distinct()
    
    rows = models.Game.objects.filter(tnmt_id=nid, sch_id=mid)
    if request.method == "GET":
        for j in [2,3,4,5,6,8,9,10,12,16]:
            if (sch_type=='b'+str(j)) or (sch_type=='i'+str(j)):
                form_l = [0]*(j-1)
                for i in range(j-1):
                    rowi = rows.filter(game_id=i+1).first()
                    form_l[i] = gameform(instance=rowi)
                if sch_type[0] == 'b':
                    return render(request, sch_type+'_e.html', {'queryset':queryset, 'sch_n':sch_n, 't_n':t_n, 'queryset2':queryset2, 'nid':nid, 'mid':mid, 'form_l':form_l})
                else:
                    return render(request, 'b2_e.html', {'queryset':queryset, 'sch_n':sch_n, 't_n':t_n, 'queryset2':queryset2, 'nid':nid, 'mid':mid, 'form_l':form_l})
        for j in [1,2,3,4]:
            for i in [3,4,5,6]:
                if sch_type == str(j)+'p'+str(i):
                    rows_p = models.Pool.objects.filter(tnmt_id=nid, sch_id=mid)
                    form_l = [0]*int(j*i*(i-1)/2)
                    for k in range(int(j*i*(i-1)/2)):
                        rowk = rows.filter(game_id=k+1).first()
                        form_l[k] = gameform(instance=rowk)
                    form_l2 = [0]*(i*j)
                    for jj in range(j):
                        for ii in range(i):
                            rowk = rows_p.filter(pool_id=jj+1,team_id=ii+1).first()
                            form_l2[i*jj+ii] = poolform(instance=rowk)
                    return render(request, sch_type[0:2]+'_e.html', {'queryset':queryset, 'sch_n':sch_n, 't_n':t_n, 'queryset2':queryset2, 'nid':nid, 'mid':mid, 'form_l':form_l, 'form_l2':form_l2})


    else:
        for j in [2,3,4,5,6,8,9,10,12,16]:
            if sch_type=='b'+str(j):
                for i in range(j-1):
                    if str(i) in request.POST:
                        rowi = rows.filter(game_id=i+1).first()
                        form_i = gameform(data=request.POST, instance=rowi)
                        if form_i.is_valid():
                            form_i.save()
                            return redirect('/game/'+str(nid)+'/'+str(mid)+'/edit/')
                        return HttpResponse('数据不符合规范 / Data not valid')
            if sch_type=='i'+str(j):
                for i in range(j-1):
                    if str(i+1) in request.POST:
                        rowi = rows.filter(game_id=i+1).first()
                        form_i = gameform(data=request.POST, instance=rowi)
                        if form_i.is_valid():
                            form_i.save()
                            return redirect('/game/'+str(nid)+'/'+str(mid)+'/edit/')
                        return HttpResponse('数据不符合规范 / Data not valid')
        for j in [1,2,3,4]:
            for i in [3,4,5,6]:
                if sch_type == str(j)+'p'+str(i):
                    rows_p = models.Pool.objects.filter(tnmt_id=nid, sch_id=mid)
                    for k in range(int(j*i*(i-1)/2)):
                        if 'g'+str(k+1) in request.POST:
                            rowk = rows.filter(game_id=k+1).first()
                            form_k = gameform(data=request.POST, instance=rowk)
                            if form_k.is_valid():
                                form_k.save()
                                return redirect('/game/'+str(nid)+'/'+str(mid)+'/edit/')
                            return HttpResponse('数据不符合规范 / Data not valid')
                    for jj in range(j):
                        for ii in range(i):
                            if 'p'+str(jj+1)+'_'+str(ii+1) in request.POST:
                                rowk = rows_p.filter(pool_id=jj+1,team_id=ii+1).first()
                                form_k = poolform(data=request.POST, instance=rowk)
                                if form_k.is_valid():
                                    form_k.save()
                                    return redirect('/game/'+str(nid)+'/'+str(mid)+'/edit/')
                                return HttpResponse('数据不符合规范 / Data not valid')      




def game_nm_delete(request,nid,mid):
    if "info" not in request.session.keys():
        return HttpResponse('请先登录 / Please Register First')
    if request.session["info"]['name'] != (models.Tnmt.objects.filter(id=nid).values().get()['host_name']) and (request.session["info"]['name'] !='admin'):
        return HttpResponse('你不是主办 / You are not the holder')
    models.Game.objects.filter(tnmt_id=nid, sch_id=mid).delete()
    return HttpResponse('已删除 / Deleted')

