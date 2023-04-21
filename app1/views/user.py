from django.shortcuts import render, HttpResponse, redirect
from app01 import models
from django import forms
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.encrypt import md5
from django.core.exceptions import ValidationError

class UserForm(BootStrapModelForm):

    class Meta:
        model = models.UserInfo
        fields = ["name", "gender", "DOB", "pwd","confirm_pwd"]
        widgets = {
            "pwd": forms.PasswordInput(render_value=True),
            "confirm_pwd": forms.PasswordInput(render_value=True),
        } 

    def clean_pwd(self):
        password = self.cleaned_data.get("pwd")
        return md5(password)

    def clean_confirm_pwd(self):
        password = self.cleaned_data.get("pwd")
        confirm = md5(self.cleaned_data.get("confirm_pwd"))
        if confirm != password:
            raise ValidationError("密码不一致")
        # 返回什么，此字段以后保存到数据库就是什么。
        return confirm

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # 循环找到所有的插件，添加了class="form-control"
    #     for field in self.fields.items():
    #         #### ？？？？？？ ####
    #         field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def user_add(request):
    """ 添加用户（ModelForm版本）"""
    if request.method == "GET":
        if "info" in request.session.keys():
            return HttpResponse('您已登录 / You are already Registered')
        form = UserForm()
        return render(request, 'user_add.html', {"form": form})

    # 用户POST提交数据，数据校验。
    form = UserForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        # {'name': '123', 'password': '123', 'age': 11, 'account': Decimal('0'), 'create_time': datetime.datetime(2011, 11, 11, 0, 0, tzinfo=<UTC>), 'gender': 1, 'depart': <Department: IT运维部门>}
        # print(form.cleaned_data['name'])
        # models.UserInfo.objects.create(..)
        exist_user =  models.UserInfo.objects.filter(name=form.cleaned_data['name'],DOB=form.cleaned_data['DOB']).exists()
        if not exist_user:
            form.save()
            return redirect('/login')
        else:
            form.add_error("name", "用户已存在")
            return render(request, 'user_add.html', {'form': form})

    # 校验失败（在页面上显示错误信息）
    return render(request, 'user_add.html', {"form": form})


def hist(request):
    return render(request, "his_c.html")

def p_r(request):
    return render(request, "p_r.html")