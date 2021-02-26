from django.db import models

# Create your models here.
# Create your models here.

#存储交易所名称
class ExchangeName(models.Model):
    '''存储交易所名称'''
    name = models.CharField(max_length=128, default=0)
#监控爬取数据
'''核心数据
1.获取时间
2.从什么交易所来的-》名称
数据结构:
上线时间
公告名

'''
class MonitorData(models.Model):
    '''
    1.监控抓取时间
    2.监控的交易所名称
    3.公告数据
    4.公告中新币上线时间
    5.上线币名
                '''

    get_times = models.DateTimeField(auto_now_add=True)#默认为模型创建时间
    exchange_name = models.ForeignKey(ExchangeName,on_delete=models.CASCADE)
    notice_data = models.CharField(max_length=1024,default=0)
    notice_times = models.DateTimeField()
    notice_coin_name =  models.CharField(max_length=128,default=0)


class PriceMonitorData(models.Model):
    ''' 价格监控
    1.创建时间
    2.交易所
    3.币名
    4.当前价格
    5.设定价格
    6.当前状态 是否触发
    '''
    create_times = models.DateTimeField(auto_now_add=True)#默认为模型创建时间
    exchange_name = models.CharField(max_length=1024,default=0)
    coin_name = models.CharField(max_length=1024,default=0)
    #要存储的数字最大长度为100位，而带有4个小数位
    current_price = models.DecimalField(max_digits=10, decimal_places=4)
    monitor_price = models.DecimalField(max_digits=10, decimal_places=4)
    monitor_statue = models.BooleanField(default=True)#默认为正在监控

