from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from utils.email_send import send_register_email


# 自定义authenticate
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')

        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        registerform = RegisterForm()
        return render(request, 'register.html', {'registerform': registerform})

    def post(self, request):
        registerform = RegisterForm(request.POST)
        if registerform.is_valid():
            username = request.POST.get('email', '')
            if UserProfile.objects.filter(email=username):
                return render(request, 'register.html', {'registerform': registerform, 'msg': '用户已经存在'})
            password = request.POST.get('password', '')
            userprifile = UserProfile()
            userprifile.is_active = False  # 表明用户未激活
            userprifile.username = username
            userprifile.email = username
            userprifile.password = make_password(password)
            userprifile.save()

            send_register_email(username, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'registerform': registerform})


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)  # 验证用户名密码是否正确
            if user is not None:
                if user.is_active:
                    login(request, user)  # 完成登陆
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': '用户未激活！'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误！'})
        else:
            return render(request, 'login.html', {'loginform': loginform})


class ForgetPwdView(View):
    def get(self, request):
        forgetform = ForgetForm()
        return render(request, 'forgetpwd.html', {'forgetform': forgetform})

    def post(self, request):
        forgetform = ForgetForm(request.POST)
        if forgetform.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forgetform': forgetform})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})

        else:
            return render(request, 'active_fail.html')

        return render(request, 'login.html')


class ModifyPwdView(View):
    def post(self, request):
        modifypwdform = ModifyPwdForm(request.POST)
        if modifypwdform.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': '两次密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modifypwdform': modifypwdform})

#  第一版 使用函数实现的login
# # Create your views here.
# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#         user = authenticate(username=username, password=password)  # 验证用户名密码是否正确
#         if user is not None:
#             login(request, user)  # 完成登陆
#             return render(request, 'index.html')
#         else:
#             return render(request, 'login.html', {'msg':'用户名或密码错误！'})
#
#     elif request.method == 'GET':
#         return render(request, 'login.html', {})
