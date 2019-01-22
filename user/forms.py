import re

from django import forms
from django.contrib.auth.hashers import check_password

from user.models import User


class RegisterForm(forms.Form):

    user_name = forms.CharField(max_length=20,min_length=5,required=True,
                                error_messages={
                                    'required': '用户名必填',
                                    'max_length': '长度20',
                                    'min_length':'不能小于5'
                                })
    pwd = forms.CharField(max_length=20,min_length=8,required=True,
                                error_messages={
                                    'required': '密码必填',
                                    'max_length': '长度20',
                                    'min_length':'不能小于5'
                                })
    cpwd = forms.CharField(max_length=20,min_length=8,required=True,
                                error_messages={
                                    'required': '密码必填',
                                    'max_length': '长度20',
                                    'min_length':'不能小于5'
                                })
    allow = forms.BooleanField(required=True,error_messages={
                            'required': '协议必同意'
    })
    email = forms.CharField(required=True,error_messages={
                            'required': '邮箱必填'
    })
    def clean_user_name(self):
        #  校验注册账号是否存在
        username = self.cleaned_data['user_name']
        user = User.objects.filter(username = username).first()
        if user :
            raise forms.ValidationError('账号存在。更换')
        return self.cleaned_data['user_name']
    def clean(self):
        # 密码时候一致
        pwd = self.cleaned_data.get('pwd')
        cpwd = self.cleaned_data.get('cpwd')
        if pwd != cpwd:
            raise forms.ValidationError({'cpwd':'两次密码不一致'})
        return self.cleaned_data
    def clean_email(self):
        # 校验邮箱格式
        email_rel =  '^[a-z0-9A-Z]+[- | a-z0-9A-Z . _]+@([a-z0-9A-Z]+(-[a-z0-9A-Z]+)?\\.)+[a-z]{2,}$'
        email = self.cleaned_data['email']
        if not re.match(email_rel,email):
            raise forms.ValidationError('邮箱格式错误')
        #  主意：  这里的ValidationError 中不要写{'email':'XXX'}  !!!  因为这里已经针对email 。
        return self.cleaned_data['email']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20,min_length=5,required=True,
                                error_messages={
                                    'required': '用户名必填',
                                    'max_length': '长度20',
                                    'min_length':'不能小于5'
                                })
    pwd = forms.CharField(max_length=20, min_length=8, required=True,
                          error_messages={
                              'required': '密码必填',
                              'max_length': '长度20',
                              'min_length': '不能小于5'
                          })
    def clean(self):
        # 校验用户名是否注册
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username= username).first()
        if not user:
            raise forms.ValidationError({'username':'该账号不存在'})
        password = self.cleaned_data.get('pwd')
        if not check_password(password,user.password):
            raise forms.ValidationError({'pwd':'密码错误'})
        return self.cleaned_data

class AddressForm(forms.Form):
    username = forms.CharField(max_length=5,required=True,
                               error_messages={
                                   'required':'收件必填',
                                   'max_length': '名字不能超过5',
                               })
    address = forms.CharField( required=True,
                               error_messages={
                                   'required':'收货地址必填',

                               })
    postcode = forms.CharField( required=True,
                               error_messages={
                                   'required':'邮编必填',

                               })
    mobile = forms.CharField( required=True,
                              max_length=11,
                               error_messages={
                                   'required':'手机号必填',
                                   'max_length': '名字不能超过11',
                               })
    def clean(self):
        pass
