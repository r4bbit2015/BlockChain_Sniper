import json
import random
import string
import datetime
from django.shortcuts import render,HttpResponse
from django.utils import timezone
from django.views.generic import ListView
from monitor.models import MonitorData,ExchangeName

#TypeError: Object of type 'datetime' is not JSON serializable
#这个错误的原因是json.dumps无法对字典中的datetime时间格式数据进行转化，dumps的原功能是将dict转化为str格式，不支持转化时间，所以需要将json类部分内容重新改写，来处理这种特殊日期格式。
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


def index(request):
    return render(request,"index.html")


def all_exchanges(request):
    return render(request,'all_exchanges.html')

def views_all_exchanges(request):
    huobi_data = MonitorData.objects.filter(exchange_name_id=1)  # 取出交易所id为1的数据
    data = []
    #读火币
    for datas in huobi_data:
        datas_dict = {'get_times': datas.get_times,
                      'notice_data': datas.notice_data,
                      'notice_times': datas.notice_times,
                      'notice_coin_name': datas.notice_coin_name,
                      'exchange_name': '火币交易所'}
        data.append(datas_dict);
    #读抹茶
    mx_data = MonitorData.objects.filter(exchange_name_id=4)
    for datas in mx_data:
        datas_dict = {'get_times': datas.get_times,
                      'notice_data': datas.notice_data,
                      'notice_times': datas.notice_times,
                      'notice_coin_name': datas.notice_coin_name,
                      'exchange_name': '抹茶交易所'}
        data.append(datas_dict);
    return_templates = {'code': 0, 'msg': '', 'count': len(data), 'data': data}
    #返回
    return HttpResponse(json.dumps(return_templates, cls=DateEncoder), content_type="application/json,charset=utf-8")

#从orm读取数据到视图层
def views_huobi(request):
    huobi_data = MonitorData.objects.filter(exchange_name_id=1)#取出交易所id为1的数据
    data = []
    for datas in huobi_data:
        datas_dict={'get_times':datas.get_times,
                    'notice_data': datas.notice_data,
                    'notice_times': datas.notice_times,
                    'notice_coin_name': datas.notice_coin_name,
                    'exchange_name': '火币交易所'}
        data.append(datas_dict);
    return_templates = {'code': 0, 'msg': '', 'count': len(data), 'data': data}
    return HttpResponse(json.dumps(return_templates,cls=DateEncoder), content_type="application/json,charset=utf-8")

def huobi(request):
    return render(request,'huobi.html')

def views_mx(request):
    mx_data = MonitorData.objects.filter(exchange_name_id=4)
    data = []
    for datas in mx_data:
        datas_dict = {'get_times': datas.get_times,
                      'notice_data': datas.notice_data,
                      'notice_times': datas.notice_times,
                      'notice_coin_name': datas.notice_coin_name,
                      'exchange_name': '抹茶交易所'}
        data.append(datas_dict);
    return_templates = {'code': 0, 'msg': '', 'count': len(data), 'data': data}
    return HttpResponse(json.dumps(return_templates, cls=DateEncoder), content_type="application/json,charset=utf-8")

def mx(request):
    return render(request,'mx.html')

#测试

''' monitor_monitordata Table Struct
+------------------+---------------+------+-----+---------+----------------+
| Field            | Type          | Null | Key | Default | Extra          |
+------------------+---------------+------+-----+---------+----------------+
| id               | int           | NO   | PRI | NULL    | auto_increment |
| get_times        | datetime(6)   | NO   |     | NULL    |                |
| notice_data      | varchar(1024) | NO   |     | NULL    |                |
| notice_times     | datetime(6)   | NO   |     | NULL    |                |
| notice_coin_name | varchar(128)  | NO   |     | NULL    |                |
| exchange_name_id | int           | NO   | MUL | NULL    |                |
+------------------+---------------+------+-----+---------+----------------+
        moitor_moitordata ORM Model
    get_times = models.DateTimeField(auto_now_add=True)#默认为模型创建时间
    exchange_name = models.ForeignKey(ExchangeName,on_delete=models.CASCADE)
    notice_data = models.CharField(max_length=1024,default=0)
    notice_times = models.DateTimeField()
    notice_coin_name =  models.CharField(max_length=128,default=0)
'''
def test_fakedata(reques):
    item = 50 #生成随机数据条数
    #生成随机数据
    #结果集
    # insert_log = {'获取时间': exchange_name, '交易所名称': exchange_name, '公告数据': notice_data, '上线时间': notice_times,
    #           '币名': notice_coin_name}
    result_set =[]
    i = 1;
    while(i<=item):
        get_times = timezone.now()
        exchange_name_id =  random.randint(1,4)
        notice_data = "".join(random.sample(string.ascii_letters + string.digits, 50))
        notice_times = timezone.now()
        notice_coin_name = "".join(random.sample('zyxwvutsrqponmlkjihgfedcba',4))
        insert_log = {'获取时间': get_times, '交易所编号': exchange_name_id, '公告数据': notice_data, '上线时间': notice_times,
                      '币名': notice_coin_name,'status':'插入失败'}
        # print(get_times)
        # print(exchange_name_id)
        # print(notice_data)
        # print(notice_times)
        # print(notice_coin_name)
        #插入数据
        insert_status = MonitorData.objects.create(get_times=get_times,exchange_name_id=exchange_name_id,notice_data=notice_data,notice_times=notice_times,notice_coin_name=notice_coin_name)
        if insert_status!=0:
            insert_log['status']='插入成功'
        i += 1
        result_set.append(insert_log)

    return HttpResponse(str(result_set));