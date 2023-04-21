from django.shortcuts import render, HttpResponse, redirect
from app01 import models
from app01.utils.bootstrap import BootStrapForm
from app01.utils.encrypt import md5
from django import forms

class LoginForm(BootStrapForm):
    name = forms.CharField(
        label="姓名/Name",
        widget=forms.TextInput,
        required=True
    )
    pwd = forms.CharField(
        label="密码/Password",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    def clean_pwd(self):
        password = self.cleaned_data.get("pwd")
        return md5(password)

def login(request):
    """ 登录 """
    if request.method == "GET":
        if "info" in request.session.keys():
            return HttpResponse('您已登录 / You are already Registered')
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():

        # 去数据库校验用户名和密码是否正确，获取用户对象、None
        # admin_object = models.Admin.objects.filter(username=xxx, password=xxx).first()
        user_object = models.UserInfo.objects.filter(**form.cleaned_data).first()
        # print(form.cleaned_data)
        if not user_object:
            form.add_error("pwd", "用户名或密码错误")
            form.add_error("name", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})

        # 用户名和密码正确
        # 网站生成随机字符串; 写到用户浏览器的cookie中；在写入到session中；
        request.session["info"] = {'id': user_object.id, 'name': user_object.name}
        # session可以保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)

        return redirect("/tnmt/list/")

    return render(request, 'login.html', {'form': form})


def logout(request):
    """ 注销 """

    request.session.clear()

    return redirect('/login/')
