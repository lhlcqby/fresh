from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
from fresh_shop.settings import ORDER_NUMBER
from order.models import OrderInfo
from user.forms import RegisterForm, LoginForm, AddressForm
from user.models import User, UserAddress


def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    if request.method == 'POST':
        #  使用表单 form
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 账号存在数据库，密码一致，邮箱正确
            username = form.cleaned_data['user_name']
            password = make_password( form.cleaned_data['pwd'])
            email = form.cleaned_data['email']
            User.objects.create(username=username,
                                password=password,
                                email=email
                                )
            return HttpResponseRedirect(reverse('user:login'))
        else:
            errors = form.errors
            return  render(request,'register.html',{'errors':errors})


def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('goods:index'))
        else:
            errors = form.errors
            return  render(request,'login.html',{'errors':errors})


def logout(request):
    if request.method == 'GET':
        del request.session['user_id']                   #  删掉session中的键值对
        #  删除商品信息
        if request.session.get('goods'):          # 判断商品是否有这个 key值
            del request.session['goods']
        return HttpResponseRedirect(reverse('goods:index'))


def user_site(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        user_address = UserAddress.objects.filter(user_id=user_id)
        activate = 'site'
        return render(request,'user_center_site.html',{'user_address':user_address,'activate':activate})
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            address = form.cleaned_data['address']
            mobile = form.cleaned_data['mobile']
            postcode = form.cleaned_data['postcode']
            user_id = request.session.get('user_id')
            UserAddress.objects.create(user_id=user_id,
                                       address = address,
                                       signer_name=username,
                                       signer_mobile =mobile,
                                       signer_postcode=postcode)
            return HttpResponseRedirect(reverse('user:user_site'))    # 相当于重新刷新


        else:
            errors = form.errors
            return render(request,'user_center_site.html',{'errors':errors})

#   訂單詳情
def user_list(request):
    if request.method == 'GET':
        # 獲取登錄id
        # 獲取頁數。沒有返回 1
        page = int(request.GET.get('page',1))
        user_id = request.session.get('user_id')
        # 當前用戶的訂單信息
        orders = OrderInfo.objects.filter(user_id=user_id)
        #  分頁
        pg = Paginator(orders,ORDER_NUMBER)
        # 獲取到那一頁
        orders = pg.page(page)
        status = OrderInfo.ORDER_STATUS
        activate = 'list'   # 為了做一個切換標記用的（include ’function.html ' ）
        return render(request,'user_center_order.html',{'orders':orders,'status':status,'activate':activate})

#  用戶中心：
def user_center(request):
    user = request.session.get('user_id')
    activate = 'center'
    return render(request,'user_center_info.html',{'user_id':user,'activate':activate})   # 这里的user是给前端用的东西