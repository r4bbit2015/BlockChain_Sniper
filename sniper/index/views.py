import json
import random
import string
import datetime
import requests
from django.shortcuts import render,HttpResponse
from django.utils import timezone
from django.views.generic import ListView
from monitor.models import MonitorData,ExchangeName
from django.http import JsonResponse
from django.core.mail import send_mail   # 导入邮箱模块

# #TypeError: Object of type 'datetime' is not JSON serializable
#这个错误的原因是json.dumps无法对字典中的datetime时间格式数据进行转化，dumps的原功能是将dict转化为str格式，不支持转化时间，所以需要将json类部分内容重新改写，来处理这种特殊日期格式。

from dwebsocket.decorators import accept_websocket #添加websocket

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
def timing_futures(request):
    return render(request,'timing_futures.html')

def huobi(request):
    return render(request,'huobi.html')

def mx(request):
    return render(request,'mx.html')



def settings(request):
    return render(request,'settings.html')

def coin_price_monitor(request):
    return render(request,'coin_price_monitor.html')
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


def views_set_mail(request):
    #设置邮箱
    #code 返回值 200 发送成功，404 后端未接受到数据  301 发送邮件失败
    res = {"code": 200}

    if request.method == 'POST':
        email = request.POST.get('email')#邮箱号
        email_content = request.POST.get('email_content')#邮件内容
        #验证是否正常接受到数据
        if(email== None or email_content == None or email_content == None):
            print("未接受到数据")
            res['code'] = 404
        print("邮箱账户", email)
        print("邮件内容", email_content)

        #发送邮件
        #标题，邮件内容，发送人，接受人，是否使用ssl
        try:
            send_mail('沉船资本', email_content, '2912285367@qq.com',[email], fail_silently=False)
        except Exception as e:
            print(e)
            res['code'] =301
        # 验证邮箱密码是否正确

    elif request.method == 'GET':
        return redirect("/login")  # 如果是get 就返回登录界面
    # In order to allow non-dict objects to be serialized set the safe parameter to False. 添加safe=False
    # return JsonResponse(res, safe=False)
    return JsonResponse(res,safe=False)
#传入交易所ID 返回当前价格

# dwebsocket有两种装饰器：require_websocket和accept_websocekt，使用require_websocket装饰器会导致视图函数无法接收导致正常的http请求，一般情况使用accept_websocket方式就可以了，
# dwebsocket的一些内置方法：
# request.is_websocket（）：判断请求是否是websocket方式，是返回true，否则返回false
# request.websocket： 当请求为websocket的时候，会在request中增加一个websocket属性，
# WebSocket.wait（） 返回客户端发送的一条消息，没有收到消息则会导致阻塞
# WebSocket.read（） 和wait一样可以接受返回的消息，只是这种是非阻塞的，没有消息返回None
# WebSocket.count_messages（）返回消息的数量
# WebSocket.has_messages（）返回是否有新的消息过来
# WebSocket.send（message）像客户端发送消息，message为byte类型


def views_monitor_price(request):
    res = {"code": 200,"current_price":0};

    # code 返回值 200 发送成功，301 后端未接受到数据  404 不识别的交易对
    if request.method == 'POST':
        exchange_id = int(request.POST.get('exchange'))  # 交易所ID 1-火币 2-币安 3-抹茶 4-OKex
        monitor_price = request.POST.get('monitor_price') #监控价格
        coin_name = request.POST.get('coin_name')
        #获取当前价格返回
        #
        # 验证是否正常接受到数据
        if (exchange_id == None or monitor_price == None or coin_name == None):
            print("未接受到数据")
            res['code'] = 301
            return JsonResponse(res,safe=False)
        res['current_price'] = get_current_price(exchange_id,coin_name)

        print("交易所ID:", exchange_id)
        print("监控币名:", coin_name)
        print("当前价格:",res['current_price'])
        print("监控价格:", monitor_price)


    elif request.method == 'GET':
        return redirect("/login")  # 如果是get 就返回登录界面


    return JsonResponse(res,safe=False)

def get_current_price(exchange_id,coin_name):
    res = {"code": 200};

    current_price = 0;
    if exchange_id == 1:
        print("火币交易所")
        huobi_api = f"https://api.huobi.be/market/history/kline?period=1day&size=1&symbol={coin_name}usdt"
        print(huobi_api)
        r = requests.get(huobi_api)
        price = r.json();
        #如果是无效交易对 比如火币不存在的交易对 就直接返回404
        current_price = price['data'][0]['close']

    elif exchange_id == 2:
        pass
    elif exchange_id == 3:
        pass
    elif exchange_id == 4:
        pass

    return current_price;
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