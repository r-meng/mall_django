import re

from django import forms

# from accounts.models import User
from django.contrib.auth import authenticate, login

from accounts.models import User, UserAddress
from utils.verify import VerifyCode


class UserLoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=64)
    password = forms.CharField(label='密码',
                               max_length=64,
                               widget=forms.PasswordInput,
                               error_messages={
                                   'required': '请输入密码'
                               })
    verify_code = forms.CharField(label='验证码',
                                  max_length=4,
                                  error_messages={
                                      'required': '请输入验证码'
                                  })

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     print(username)
    #     pattern = r'^0{0,1}1[0-9]{10}$'
    #     if not re.search(pattern, username):
    #         raise forms.ValidationError('请输入正确的手机号码')
    #     return username

    def clean_verify_code(self):
        verify_code = self.cleaned_data['verify_code']
        if not verify_code:
            raise forms.ValidationError('请输入验证码')
        client = VerifyCode(self.request)
        if not client.validate_code(verify_code):
            raise forms.ValidationError('您输入的验证码不正确')
        return verify_code


    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username', None)
        password = cleaned_data.get('password', None)
        if username and password:
            user_list = User.objects.filter(username=username)
            if user_list.count() == 0:
                raise forms.ValidationError('用户名不存在')
            # if not user_list.filter(password=password).exists():
            #     raise forms.ValidationError('密码错误')

            if not authenticate(username=username, password=password):
                raise forms.ValidationError('密码错误')
        return cleaned_data




class UserRegistForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=64)
    # nickname = forms.CharField(label='昵称', max_length=64)
    password = forms.CharField(label='密码', max_length=64, widget=forms.PasswordInput)
    password_repeat = forms.CharField(label='密码', max_length=64, widget=forms.PasswordInput)
    verify_code = forms.CharField(label='验证码', max_length=4)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('用户名已存在')
        return data

    def clean_verify_code(self):
        verify_code = self.cleaned_data['verify_code']
        if not verify_code:
            raise forms.ValidationError('请输入验证码')
        client = VerifyCode(self.request)
        if not client.validate_code(verify_code):
            raise forms.ValidationError('您输入的验证码不正确')
        return verify_code

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password', None)
        password_repeat = cleaned_data.get('password_repeat', None)
        if password and password_repeat:
            if password != password_repeat:
                raise forms.ValidationError('两次密码输入不一致')
        return cleaned_data

    def register(self):
        data = self.cleaned_data
        # 1. 创建用户
        User.objects.create_user(username=data['username'], password=data['password'], level=0, nickname='nickname')
        # 2. 自动登录
        user = authenticate(username=data['username'], password=data['password'])
        login(self.request, user)
        return user


class UserAddressForm(forms.ModelForm):

    region = forms.CharField(label='大区域选项', max_length=64, required=True,
                             error_messages={
                                 'required': '请选择地址'
                             })

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    class Meta:
        model = UserAddress
        fields = ['address', 'username', 'phone', 'is_default']
        widgets = {
            'is_default': forms.CheckboxInput(attrs={
                'class': 'weui-switch'
            })
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        pattern = r'^0{0,1}1[0-9]{10}$'
        if not re.search(pattern, phone):
            raise forms.ValidationError('请输入正确的手机号码')
        return phone

    def clean(self):
        cleaned_data = super().clean()
        addr_list = UserAddress.objects.filter(is_valid=True, user=self.request.user)
        if addr_list.count() >= 20:
            raise forms.ValidationError('最多只能添加20个地址')
        return cleaned_data

    def save(self, commit=True):
        obj = super().save(commit=False)
        region = self.cleaned_data['region']
        (province, city, area) = region.split(' ')
        obj.province = province
        obj.city = city
        obj.area = area
        obj.user = self.request.user

        # 修改时，如果已经有默认地址，当前也勾选了默认地址选项，需要把之前的地址都改为非默认地址
        if self.cleaned_data['is_default']:
            UserAddress.objects.filter(is_valid=True, user=self.request.user, is_default=True).update(is_default=False)
        obj.save()




