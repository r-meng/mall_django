from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # username = models.CharField('用户名', max_length=64)
    # password = models.CharField('密码', max_length=255)
    avatar = models.ImageField('用户头像', upload_to='avatar', null=True, blank=True)
    points = models.IntegerField('用户积分', default=0)
    nickname = models.CharField('昵称', max_length=64, null=True, blank=True)
    level = models.SmallIntegerField('用户级别')

    class Meta:
        db_table = 'accounts_user'
        verbose_name = '用户基础信息'
        verbose_name_plural = '用户基础信息'

    @property
    def default_addr(self):
        addr = None
        user_list = self.user_address.filter(is_valid=True)
        # 1.找到默认地址
        try:
            addr = user_list.filter(is_default=True)[0]
        except IndexError:
            try:
                addr = user_list[0]
                # 2.如果没有默认地址，显示所有地址的第一个
            except IndexError:
                pass
        return addr


class UserProfile(models.Model):
    GENDER_CHOICES = (
        (1, '男'),
        (0, '女'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    real_name = models.CharField('姓名', max_length=32)
    email = models.CharField('邮箱', max_length=128, null=True, blank=True)
    is_email_valid = models.BooleanField('邮箱是否已经验证', default=False)
    phone_no = models.CharField('手机号码', max_length=20, null=True, blank=True)
    is_phone_valid = models.BooleanField('手机是否已经验证', default=False)
    gender = models.SmallIntegerField('性别', default=1, choices=GENDER_CHOICES)
    age = models.SmallIntegerField('年龄', default=0)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('最后修改时间', auto_now=True)

    class Meta:
        db_table = 'accounts_user_profile'
        verbose_name = '用户详细信息'
        verbose_name_plural = '用户详细信息'


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_address')
    province = models.CharField('省份', max_length=32)
    city = models.CharField('市区', max_length=32)
    area = models.CharField('区域', max_length=32)
    town = models.CharField('街道', max_length=32, null=True, blank=True)

    address = models.CharField('详细地址', max_length=64)
    username = models.CharField('收件人', max_length=32)
    phone = models.CharField('收件人电话', max_length=32)

    is_default = models.BooleanField('是否为默认地址', default=False)
    is_valid = models.BooleanField('是否有效', default=True)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('最后修改时间', auto_now=True)

    class Meta:
        db_table = 'accounts_user_address'
        verbose_name = '用户地址'
        verbose_name_plural = '用户地址'
        ordering = ['is_default', '-updated_at']

    def get_phone_format(self):
        return self.phone[0:3] + '****' + self.phone[7:]

    def get_region_format(self):
        return '{self.province} {self.city} {self.area}'.format(self=self)

    def __str__(self):
        return self.get_region_format() + self.address


class LoginRecord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField('登录的账号', max_length=32)
    ip = models.CharField('IP', max_length=32)
    address = models.CharField('地址', max_length=32, null=True, blank=True)
    source = models.CharField('登录的来源', max_length=32)

    created_at = models.DateTimeField('登录时间', auto_now_add=True)

    class Meta:
        db_table = 'accounts_login_record'
        verbose_name = '登录历史'
        verbose_name_plural = '登录历史'
