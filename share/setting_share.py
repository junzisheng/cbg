import redis
import os
import logging


env = os.getenv('CBG_ENV', 'LOCALHOST').lower()
setting_name = 'localhost' if env == 'localhost' else 'ecs'


HOST_TEST_SEREVER = '127.0.0.1'
ALI1_IP = '47.104.193.247'
ALI2_IP = '47.98.229.132'
BB_BASE_URL_SEARCH = 'http://xyq-android2.cbg.163.com/app2-cgi-bin/app_search.py?act=super_query&search_type=overall_pet_search&order_by=selling_time+DESC&'

# paypayzhu 第三方支付的认证信息
PPZ = {
	'api_user': '12123',
	'api_key': 'adjfkljldfjklsjdflajsdlf',
}


G_MYSQL = {
	'localhost': { 'default':   {    'ENGINE'    :   'django.db.backends.mysql',
                                     'NAME'      :   'cbg',
                                     'USER'      :   'wordpress',
                                     'PASSWORD'  :   'Xj3.14164',
                                     'HOST'      :   HOST_TEST_SEREVER,
                                     'PORT'      :   '3306',
                                },
					},
	'ali_1': { 'default':   {       'ENGINE'    :   'django.db.backends.mysql',
									'NAME'      :   'cbg',
									'USER'      :   'root',
									'PASSWORD'  :   'gwj527910351',
									'HOST'      :   'gz-cdb-ff2fjjs1.sql.tencentcdb.com',
									'PORT'      :   '62332',
									},
				   },
}
G_MYSQL['ali_2'] = G_MYSQL['ali_1']

G_REDIS = {
	'localhost': {
		'host': HOST_TEST_SEREVER,
        'password': 'Xj3.14164',
	},
	'ali_1': {
		'host': ALI1_IP,
		'password': 'Xj3.14164'
	}
}

G_REDIS['ali_2'] = G_REDIS['ali_1']

# mysql数据库配置
DATABASES = G_MYSQL[env]

# redis数据库配置
redis1 = redis.StrictRedis(db=1, **G_REDIS[env])
redis2 = redis.StrictRedis(db=2, **G_REDIS[env])
redis3 = redis.StrictRedis(db=3, **G_REDIS[env])

if env in ('localhost',):
	DOMAIN = HOST_TEST_SEREVER
elif env in ('ali_1', 'ali_2'):
	DOMAIN = ALI1_IP

# payapis的认证信息
PAYS_API = {
	'uid': 'eedadd48a90c4cfb90c901ad',
	'token': '5a56dab0016464c5e44b730627e1f731',
}

# ali短信服务的参数
ALI_SMS = {
	'ACCESS_KEY_ID':"LTAIMshZrufl5aa7",
	'ACCESS_KEY_SECRET' : "HhMNbXOzTVtq46QmmGn0aCHvgYFEmw",
	# 验证码通知
	'Verification': {
		'template_code': 'SMS_137200009',  # 模板
		'sign_name': '藏宝阁助手',
		'content': '您的校验码：${code}，您正在注册成为会员，感谢您的支持！',
	},
	# 爬取通知
    'Push': {
		'template_code': 'SMS_136856176',
		'sign_name': '藏宝阁助手',
        'content': '订单:${memo}，有新的${push}通知，点击http://47.104.193.247/d/${oid}查看。',
	},
}

qiniu = {
	'AK': 'ADJfGuGpD_WsbWYVzJ55SrZestVkU02GvlnI4kZ4',
	'SK': 'DbQO9ms27VY21UwLY68MPvL4HfxaD0I59-SkX64y',
	'ImageBucket': 'cangbaoge',
	'Domain': 'pba761gcy.bkt.clouddn.com',
}


# 初始化日志对象
log_error = logging.getLogger('django')
log_django = log_error
log_paysapi = logging.getLogger('paysapi')






























XIANG_RUI_LIST = """
神行小驴,七彩小驴,粉红小驴,天使猪猪,甜蜜猪猪,九尾冰狐,冰晶魅灵,玉瓷葫芦,战火穷奇,铃儿叮当,萌动猪猪,
甜蜜泡泡,飞天猪猪,猪猪小侠,月影天马,星华飞马,九幽灵虎,如意宝狮,妙缘暖犀,玄火神驹,玄冰灵虎,鹤雪锦犀,
青霄天麟,莽林猛犸,九霄冰凤,九霄幽凰,暗影战豹,逐日天辇,魔骨战熊,翠灵锦篮,金鳞仙子,碧海云舟,玄霜玉兔,
翠云宝扇,沉星寒犀,浣碧石犀,璇彩灵仙,浑火魔精,紫霞云麒,瑞彩祥云,琉璃宝象,彩翎羽轿,穿云飞辇,踏雪灵熊,
炫彩飞篮,叠彩仙蜗,太白仙骑,嬉闹灵狮,开明天兽,腾云仙牛,沙漠驼铃,落英纷飞,沐月灵猫,轻云羊驼,怒雷狂狮,
赤瞳妖猫,御风灵貂,霓羽锦鹊,雪域圣灵,炫影魔蝎,蝠翼冥骑,灵尾松鼠,机关木鸢,灯笼锦鱼,碧海鳐鱼,玉脂福羊,
雷霆战豹,烈焰斗猪,幽骨战龙,齐天小轿,竹林熊猫,跃动精灵,七彩祥云,冰晶雪魄,冰晶小雪魄
"""
