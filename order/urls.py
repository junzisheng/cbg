# encoding: utf-8
from django.conf.urls import url
from order.views import order, currency, data
from order import public_views


urlpatterns = [
    # 公共接口
    url('^test/?$', public_views.test),
    # 订单
    url('^main/?$', order.order_main, {'need_login': True}),  # 订单主页面
    url('^pay_page/(?P<order_id>\d+)/?$', order.pay_page, {'need_login': True}),  # 订单支付页面
    url('^order_paysapi_notify/?$', order.order_paysapi_notify),  # 订单第三方回调接口
    url('^order_pay_success/?$', order.order_pay_success, {'need_login': True}),  # 订单第三方支付成功返回得页面
    url('^order_detail/(?P<order_id>\d+)/?$', order.order_detail, {'need_login': True}),
    url('^pull_order_data/?$', order.pull_order_data, {'need_login': True, 'ajax': True}),   # 获取订单数据的api
    url('^delete_order/(?P<order_id>\d+)/?$', order.delete_order, {'need_login': True, 'ajax': True}),  # 删除订单api
    # 盒币
    url('^currency_recharge_page/?$', currency.currency_recharge_page, {'need_login': True}),  # 充值货币的页面
    url('^build_currency_order_api/(?P<istype>1|2)/(?P<currency>10|50|100|200|300|500)/?$', currency.build_curency_order_api, {'need_login': True}),  # 生成货币充值记录的api
    url('^currency_paysapi_notify/?$', currency.currency_paysapi_notify),  # 货币第三方回调接口
    url('^currency_pay_success/?$', currency.currency_pay_success, {'need_login': True}),  # 货币第三方支付成功返回得页面
    url('^currency_log_page/?$', currency.currency_log_page, {'need_login': True}),  # 货币充值使用记录页面
    url('^pull_currency_recharge_log/?$', currency.currency_recharge_log_api, {'need_login': True, 'ajax': True}),  # ajax获取货币充值记录
    url('^pull_currency_conssume_log/?$', currency.currency_consume_log_api, {'need_login': True, 'ajax': True}),  # ajax获取货币消费记录
    url('^currency_pay_page/?', currency.currency_pay_page, {'need_login': True}),
    url('^currency_pay_api/(?P<captcha>\d{4})/(?P<order_id>\d+)/?$', currency.currency_pay_api, {'need_login': True, 'ajax': True}),
    # 爬取的数据
    url('^crawl_data_page/(?P<order_id>\d+)/?$', data.crawl_data_page, {'need_login': True}),  # 爬取数据的页面
    url('^crawl_data_api/?$', data.crawl_data_api, {'need_login': True}),  # 获取爬取数据的api
    url('^delete_crawl_data_api/?$', data.delete_crawl_data_api, {'need_login': True, 'ajax': True}),  # 删除爬取到的数据api
]
