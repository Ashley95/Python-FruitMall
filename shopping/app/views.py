from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse

from app.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, UserModel, FoodType, Goods, CartModel, \
    OrderModel, OrderGoodsModel
from utils.functions import get_ticket


def home(request):
    """
    首页视图函数
    """
    if request.method == 'GET':
        mainwheels = MainWheel.objects.all()
        mainnavs = MainNav.objects.all()
        mainbuy = MainMustBuy.objects.all()
        mainshop = MainShop.objects.all()
        mainshow = MainShow.objects.all()
        data = {
            'title': '首页',
            'mainwheels': mainwheels,
            'mainnavs': mainnavs,
            'mainbuy': mainbuy,
            'mainshop': mainshop,
            'mainshow': mainshow,

        }
        return render(request, 'home/home.html', data)


def mine(request):
    """
    个人中心
    """
    if request.method == 'GET':
        user = request.user
        orders = OrderModel.objects.filter(user=user)
        payed, wait_pay = 0, 0
        for order in orders:
            if order.o_status == 0:
                wait_pay += 1
            if order.o_status == 1:
                payed += 1
        data = {
            'wait_pay': wait_pay,
            'payed': payed
        }
        return render(request, 'mine/mine.html', data)


def market(request):
    if request.method == 'GET':

        return HttpResponseRedirect(reverse('shopping:market_params', args=('104749', '0', '0')))


def user_market(request, typeid, cid, sid):
    """
    :param typeid:分类id
    :param cid: 子分类id
    :param sid: 排序id
    """
    if request.method == 'GET':
        foodtypes = FoodType.objects.all()
        # 获取某分类下的商品
        if cid == '0':
            goods = Goods.objects.filter(categoryid=typeid)
        else:
            goods = Goods.objects.filter(categoryid=typeid,
                                         childcid=cid)
        # 重新组装全部分类的参数
        # 组装结果为[['全部分类','0'], ['酒类':13550], ['饮用水':15431]]
        foodtypes_current = foodtypes.filter(typeid=typeid).first()
        if foodtypes_current:
            childtypes = foodtypes_current.childtypenames
            childtypenames = childtypes.split('#')
            child_list = []
            for childtypename in childtypenames:
                child_type_info = childtypename.split(':')
                child_list.append(child_type_info)

        # 排序
        if sid == '0':
            pass
        if sid == '1':
            goods = goods.order_by('productnum')
        if sid == '2':
            goods = goods.order_by('-price')
        if sid == '3':
            goods = goods.order_by('price')

        data = {
            'foodtypes': foodtypes,
            'goods': goods,
            'typeid': typeid,
            'child_list': child_list,
            'cid': cid,
        }
        return render(request, 'market/market.html', data)


def addCart(request):
    if request.method == 'POST':
        user = request.user
        goods_id = request.POST.get('goods_id')
        data = {
            'code': 200,
            'msg': '请求成功'
        }
        # 判断用户是系统自带的anonymouseuser还是登陆的用户
        if user.id:
            user_carts = CartModel.objects.filter(user=user, goods_id=goods_id).first()
            if user_carts:
                user_carts.c_num += 1
                user_carts.save()
                data['c_num'] = user_carts.c_num
            else:
                CartModel.objects.create(user=user, goods_id=goods_id)
                data['c_num'] = 1
            return JsonResponse(data)
        data['msg'] = '当前用户没有登录'
        return JsonResponse(data)


def subCart(request):
    if request.method == 'POST':
        user = request.user
        goods_id = request.POST.get('goods_id')
        data = {
            'code': 200,
            'msg': '请求成功'
        }
        if user.id:
            user_carts = CartModel.objects.filter(user=user, goods_id=goods_id).first()
            # 如果购物车中已经存在了商品信息
            if user_carts:
                if user_carts.c_num == 1:
                    # 直接删除购物车中的商品信息
                    user_carts.delete()
                    data['c_num'] = 0
                else:
                    user_carts.c_num -= 1
                    user_carts.save()
                    data['c_num'] = user_carts.c_num
                return JsonResponse(data)
            data['c_num'] = 0
            return JsonResponse(data)
        data['msg'] = '当前用户没有登录'
        data['code'] = 403
        return JsonResponse(data)


def cart(request):
    if request.method == 'GET':
        user = request.user
        user_carts = CartModel.objects.filter(user=user)
        data = {
            'user_carts': user_carts
        }
        return render(request, 'cart/cart.html', data)


def changeSelectStatus(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        cart = CartModel.objects.filter(id=cart_id).first()
        if cart.is_select:
            cart.is_select = False
        else:
            cart.is_select = True
        cart.save()
        data = {
            'code': 200,
            'msg': '请求成功',
            'is_select': cart.is_select
        }
        return JsonResponse(data)


def generate_order(request):
    """
    下单
    """
    if request.method == 'GET':
        user = request.user
        # 创建订单
        o_num = get_ticket()
        order = OrderModel.objects.create(user=user, o_num=o_num)
        # 选择勾选的商品进行下单
        user_carts = CartModel.objects.filter(user=user, is_select=True)
        for carts in user_carts:
            # 创建商品和订单之间的关系
            OrderGoodsModel.objects.create(goods=carts.goods,order=order,goods_num=carts.c_num)
        user_carts.delete()
        return render(request, 'order/order_info.html', {'order': order})


def changeOrderStatus(request):
    """
    修改订单状态
    """
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        OrderModel.objects.filter(id=order_id).update(o_status=1)
        return JsonResponse({'code': 200, 'msg': '请求成功'})


def orderWaitPay(request):
    """
    待付款, o_status=1
    """
    if request.method == 'GET':
        user = request.user
        orders = OrderModel.objects.filter(user=user, o_status=0)
        return render(request, 'order/order_list_wait_pay.html', {'orders': orders})


def orderpayed(request):
    """
    待收货
    """
    if request.method == 'GET':
        user = request.user
        orders = OrderModel.objects.filter(user=user, o_status=1)
        return render(request, 'order/order_list_payed.html', {'orders': orders})


def waitPayToPayed(request):
    """
    待付款订单跳转到付款页面
    """
    if request.method == 'GET':
        order_id = request.GET.get('order_id')
        order = OrderModel.objects.filter(id=order_id).first()

        return render(request, 'order/order_info.html', {'order': order})


def changeCartAllSelect(request):
    if request.method == 'POST':
        user = request.user
        is_select = request.POST.get('all_select')
        flag = False
        user_carts = CartModel.objects.filter(user=user)
        if is_select == '1':
            CartModel.objects.filter(user=user).update(is_select=True)
        else:
            flag = True
            CartModel.objects.filter(user=user).update(is_select=True)
        data = {
            'code': 200,
            'ids': [u.id for u in user_carts],
            'flag': flag
        }
        return JsonResponse(data)


def countPrice(request):
    if request.method == 'GET':
        user = request.user
        user_carts = CartModel.objects.filter(user=user, is_select=True)
        price = 0
        for carts in user_carts:
            price += carts.goods.price * carts.c_num
        data = {
            'code': 200,
            'count_price': round(price, 3),
            'msg': '请求成功'
        }
        return JsonResponse(data)
