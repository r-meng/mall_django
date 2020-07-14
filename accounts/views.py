from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from accounts.forms import UserLoginForm, UserRegistForm
from accounts.models import User, UserAddress
from utils import constants
from utils.verify import VerifyCode


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request=request, data=request.POST)
        client = VerifyCode(request)
        code = request.POST.get('vcode', None)
        rest = client.validate_code(code)
        print('验证结果:', rest)

        if form.is_valid():
            data = form.cleaned_data
            # 使用自定义的方式实现登录
            # user = User.objects.get(username=data['username'], password=data['password'])
            # request.session[constants.LOGIN_SESSION_ID] = user.id
            # return redirect('index')

            # 使用django-auth实现登录
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                return redirect('index')
        else:
            print(form.errors)
    else:
        form = UserLoginForm(request)
    return render(request, 'login.html', {
        'form': form
    })


def user_logout(request):
    logout(request)
    return redirect('index')


def user_register(request):
    if request.method == 'POST':
        form = UserRegistForm(request=request, data=request.POST)
        if form.is_valid():
            form.register()
            return redirect('index')
    else:
        form = UserRegistForm(request=request)
    return render(request, 'register.html', {
        'form': form
    })


def address_list(request):
    my_addr_list = UserAddress.objects.all()
    return render(request, 'address_list.html', {
        'my_addr_list': my_addr_list
    })


def address_edit(request, pk):
    return render(request, 'address_edit.html', {

    })




