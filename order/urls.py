from django.urls import path

from order import views

urlpatterns = [
    #  结算
    path('place_order/',views.place_order,name= 'place_order'),
    #  创建订单。（place_order)
    path('order/',views.order,name= 'order'),

]