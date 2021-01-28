from django.urls import path
from . import views
urlpatterns = [
    path('index/', views.index),

    path('all_exchanges', views.views_all_exchanges),
    path('all_exchanges.html',views.all_exchanges),

    path('huobi/',views.views_huobi),
    path('huobi.html',views.huobi),

    path('mx/', views.views_mx),
    path('mx.html', views.mx),


    #测试接口
    path('fakedata/',views.test_fakedata)
]