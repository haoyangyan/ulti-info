"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app01.views import team, user, account, back, tnmt, game

urlpatterns = [
    path('',tnmt.tnmt_list),
    path('admin/', admin.site.urls),

    path('login/', account.login),
    path('logout/', account.logout),

    path('back/',back.back),
    path('team/info/list/', back.team_info_list),
    path('tnmt/info/list/', back.tnmt_info_list),
    path('team/info/delete/', back.team_info_delete),
    path('team/info/edit/', back.team_info_edit),
    path('tnmt/info/delete/', back.tnmt_info_delete),
    path('game/info/list/', back.game_info_list),
    path('game/info/delete/', back.game_info_delete),
    path('info/list/', back.info_list),
    path('info/delete/', back.info_delete),
    path('info/tnmt/edit/', back.info_tnmt_edit),
    path('info/<int:nid>/accept/', back.info_accept), 

    path('user/add/', user.user_add),
    path('page/hist/', user.hist),
    path('page/p_r/', user.p_r),

    path('team/list/', team.team_list),
    path('team/add/', team.team_add),
    path('team/<int:nid>/roster/', team.team_roster),
    path('team/<int:nid>/join/', team.team_join),
    path('team/edit/', team.team_edit),
    path('team/<int:nid>/<int:mid>/accept/', team.team_accept), 
    path('team/<int:nid>/<int:mid>/reject/', team.team_reject), 

    path('tnmt/add/',tnmt.tnmt_add),
    path('tnmt/list/', tnmt.tnmt_list),
    path('tnmt/list/edit/', tnmt.tnmt_list_edit),
    path('tnmt/<int:nid>/edit/', tnmt.tnmt_n_edit),
    path('tnmt/<int:nid>/show/', tnmt.tnmt_n_show),
    path('tnmt/<int:nid>/link_edit/', tnmt.tnmt_n_linkedit),

    path('game/<int:nid>/new/', game.game_new),
    path('game/<int:nid>/<int:mid>/edit/', game.game_nm_edit),
    path('game/<int:nid>/<int:mid>/show/', game.game_nm_show),
    path('game/<int:nid>/<int:mid>/delete/', game.game_nm_delete),


]

