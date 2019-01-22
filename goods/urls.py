from django.urls import path

from goods import views

urlpatterns = [
    #  首页
    path('index/',views.index,name='index'),
    # path('detail/',views.detail,name='detail'),    #  商品详情  自己写的 没有考虑到页数
    path('detail/<int:id>',views.detail,name='detail'),    #  商品详情
    path('list/',views.list,name='list'),    #  商品列表


]