from django.urls import path
from . import views
urlpatterns = [

    path('mx.html', views.mx),
    path('all_exchanges.html', views.all_exchanges),
    path('huobi.html', views.huobi),
    path('settings.html', views.settings),
    path('coin_price_monitor.html', views.coin_price_monitor),
    path('timing_futures.html', views.timing_futures),


    path('all_exchanges', views.views_all_exchanges),
    path('huobi/',views.views_huobi),
    path('mx/', views.views_mx),
    #设置邮箱
    path('client/set_mail',views.views_set_mail),
    #监听币价格
    path('client/monitor_price',views.views_monitor_price),
    #实时获取币的价格
    #测试接口
    path('fakedata/',views.test_fakedata)
]