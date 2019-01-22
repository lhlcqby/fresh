from django.shortcuts import render

# Create your views here.
from goods.models import GoodsCategory, Goods


def index(request):
    if request.method == 'GET':
        # 思路：组装结果 【object1 ，object2 ....6】
        # 组装结果的对象object：包含分类，该分类的前四个商品信息
        # 方式1： object ==> [ Goodscategory object, [Goods object1, Goods object2 ...] ]
        # 方法2：            { ‘category_name ':  [Goods objects1,Goods objects2....]}
        categorys = GoodsCategory.objects.all()
        result = []
        for category in categorys:
            goods = category.goods_set.all()[:4]
            data = [category,goods]
            result.append(data)
        print(result)
        category_type = GoodsCategory.CATEGORY_TYPE
        return render(request,'index.html',{'result':result,'category_type':category_type})     #  返回首页渲染


def detail(request,id ):
    if request.method == 'GET':
        goods = Goods.objects.filter(pk=id).first()

        return render(request,'detail.html',{'goods':goods})


def list(request):
    return render(request,'list.html')