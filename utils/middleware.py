import re

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from cart.models import ShoppingCart
from user.models import User


class FreshMiddleware(MiddlewareMixin):              #  2.0 版本以上都要继承父类
    def process_request(self,request):               # 拦截请求之前调用的函数
        # 1.给requesr.user  赋值
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.filter(pk=user_id).first()
            request.user = user                # 把匿名用户改成 我们的名字
        #  登录校验哦：分为需要检验。不需要的
        path = request.path
        # 訪問首頁時單獨搞的訪問 ：：
        if path == '/':
            return None

        # 不需要登录校验单 地址
        not_need_check = ['/user/register/','/user/login/','/goods/index/',
                          '/goods/detail/.*/','/cart/.*/' ]
        for check_path in not_need_check:
            if re.match(check_path,path):
                #  不需要登录校验的路由
                return None
        # path 为需要做登录校验的路由是，没有登录就跳转到登录
        if not user_id:
            return HttpResponseRedirect(reverse('user:login'))

  # 结算时要进行同步操作
class SessionToDbMiddleware(MiddlewareMixin):
    def process_response(self,request,response):
        # 同步session中商品信息和数据库中购物车表达商品信息
        # 1，判读用户是否登录。登录才同步
        user_id = request.session.get('user_id')
        if user_id:
            # 2. 同步
            # a.判读session 中的商品是否存在。存在则更新
            # b.如果不存在。则创建
            #  c.同步数据库的数据到session中
            session_goods = request.session.get('goods')
            if session_goods:
                for se_goods in session_goods:
                    # se_goods :结构 ：【goods_id ,num ,is_select]
                    cart = ShoppingCart.objects.filter(user_id = user_id,goods_id = se_goods[0]).first()
                    if cart:
                        #  更新商品信息
                        if cart.nums != se_goods[1] or cart.is_select != se_goods[2]:
                            cart.nums = se_goods[1]
                            cart.is_select = se_goods[2]
                            cart.save()
                    else:
                        # 创建
                        ShoppingCart.objects.create(user_id= user_id,
                                                goods_id = se_goods[0],
                                                nums = se_goods[1],
                                                is_select = se_goods[2])

            # 同步数据库中的数据到session中
            db_carts = ShoppingCart.objects.filter(user_id=user_id)
            #  组成商品结构 [[],[],[]]
            if db_carts:
                new_session_goods = [[cart.goods_id,cart.nums,cart.is_select] for cart in db_carts]
                request.session['goods'] = new_session_goods
                # 下面一眼的
                # result = []
                # for cart in db_carts:
                #     data = [cart.goods_id,cart.nums.cart.is_select]
                #     result.append(data)
                # request.session['goods'] = new_session_goods
        return response
















'''
            #  自己写的  有问题
        path = request.path
        if path in ['/goods/index/','/goods/register/']:
            return None
        try:
            user_id = request.session['user_id']
            user = User.objects.get(pk = user_id)
            request.user = user
            return None
        except :
            return HttpResponseRedirect(reverse('user:login'))

    def process_response(self,request,response):
        return response

'''