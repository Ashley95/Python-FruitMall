from django.conf.urls import url

from app import views

urlpatterns = [
    # 首页
    url(r'^home/', views.home, name='home'),
    # 个人中心
    url(r'^mine/', views.mine, name='mine'),
    # 闪购超市
    url(r'^market/$', views.market, name='market'),
    url(r'^market/(\d+)/(\d+)/(\d+)/', views.user_market, name='market_params'),
    # 添加购物车
    url(r'^addCart/', views.addCart, name='addCart'),
    url(r'^subCart/', views.subCart, name='subCart'),
    url(r'^cart/', views.cart, name='cart'),
    # 修改购物车中商品的选择情况
    url(r'^changeSelectStatus/', views.changeSelectStatus, name='changeSelectStatus'),
    # 下单
    url(r'^generate_order/', views.generate_order, name='generate_order'),
    # 修改订单状态
    url(r'^changeOrderStatus/', views.changeOrderStatus, name='changeOrderStatus'),
    # 待付款订单
    url(r'^orderWaitPay/', views.orderWaitPay, name='orderWaitPay'),
    # 待收货
    url(r'^orderpayed/', views.orderpayed, name='orderpayed'),
    # 待付款订单支付
    url(r'^waitPayToPayed/', views.waitPayToPayed, name='waitPayToPayed'),
    # 全选
    url(r'^changeCartAllSelect/', views.changeCartAllSelect, name='changeCartAllSelect'),
    # 总价
    url(r'^countPrice/', views.countPrice, name='countPrice'),
]