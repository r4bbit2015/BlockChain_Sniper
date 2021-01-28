layui.use('table',
function() {
    var table = layui.table;
    //
    //定时渲染页面
    table.render({
        async: false,
        elem: '#huobi-table',
        height: 'full-200' //高度自适应
        ,
        url: '/huobi' //数据接口
        ,
        cellMinWidth: 90,
        limit: 100 //一页显示条数
        ,
        loading: true,
        first: false //不显示首页
        ,
        last: false //不显示尾页
        ,
        page: true //开启分页
        ,
        cols: [[ //表头
        {
            field: 'id',
            type: 'numbers',
            title: 'ID',
            width: 80,
            sort: true,
            fixed: 'left'
        },
        {
            field: 'notice_times',
            title: '上线时间',
            align: 'center',
            sort: true
        },
        {
            field: 'exchange_name',
            title: '交易所',
            align: 'center'
        },
        {
            field: 'notice_coin_name',
            title: '币名',
            align: 'center'
        },
        {
            field: 'notice_data',
            title: '详情公告',
            align: 'center'
        },
        {
            field: 'get_times',
            title: '触发狙击',
            align: 'center'
        }]]
    });

});