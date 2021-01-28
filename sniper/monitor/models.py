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