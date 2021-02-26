from django.urls import path
from . import views
urlpatterns = [

    path('mx.html', views.mx),
    path('all_exchanges.html', views.all_exchanges),
    path('huobi.html', views.huobi),
    path('settings.html', views.settings),
    path('coin_price_monitor.html', views.coin_price_monitor),
    path('timing_futures.html', views.timing_futures),


    path('all_exchanges/', views.show_all_exchanges),
    path('huobi/',views.show_huobi),
    path('mx/', views.show_mx),
    #设置邮箱
    path('client/add_mail',views.add_mail),
    #添加监听 币价格
    path('client/add_monitor_price',views.add_monitor_price),
    #显示监听内容
    path('client/show_monitor_price',views.show_monitor_price),
    #删除监听币
    path('client/del_all_monitor_price', views.del_all_monitor_price),

    #实时获取币的价格
    #测试接口
    path('fakedata/',views.test_fakedata)
]