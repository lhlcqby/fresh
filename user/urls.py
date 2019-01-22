from django.urls import path

from user import views

urlpatterns = [
    path('register/',views.register,name = 'register'),
    path('login/',views.login,name = 'login'),
    path('logout/',views.logout,name = 'logout'),
    # 收货地址
    path('user_site/',views.user_site,name = 'user_site'),
    # 订单详情
    path('user_list/',views.user_list,name = 'user_list'),
    #  用户中心
    path('user_center/',views.user_center,name = 'user_center'),

]