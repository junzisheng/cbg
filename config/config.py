# encoding=utf-8
# 爬取人物的基础url
import redis
ROLE_BASE_URL = 'http://xyq.cbg.163.com/cgi-bin/xyq_overall_search.py'
ROLE_BASE_URL_SEARCH = 'http://xyq.cbg.163.com/cgi-bin/xyq_overall_search.py' + '?'
# 爬取人物的act
ROLE_ACT = 'overall_search_role'
XIANG_RUI_LIST = """
神行小驴,七彩小驴,粉红小驴,天使猪猪,甜蜜猪猪,九尾冰狐,冰晶魅灵,玉瓷葫芦,战火穷奇,铃儿叮当,萌动猪猪,
甜蜜泡泡,飞天猪猪,猪猪小侠,月影天马,星华飞马,九幽灵虎,如意宝狮,妙缘暖犀,玄火神驹,玄冰灵虎,鹤雪锦犀,
青霄天麟,莽林猛犸,九霄冰凤,九霄幽凰,暗影战豹,逐日天辇,魔骨战熊,翠灵锦篮,金鳞仙子,碧海云舟,玄霜玉兔,
翠云宝扇,沉星寒犀,浣碧石犀,璇彩灵仙,浑火魔精,紫霞云麒,瑞彩祥云,琉璃宝象,彩翎羽轿,穿云飞辇,踏雪灵熊,
炫彩飞篮,叠彩仙蜗,太白仙骑,嬉闹灵狮,开明天兽,腾云仙牛,沙漠驼铃,落英纷飞,沐月灵猫,轻云羊驼,怒雷狂狮,
赤瞳妖猫,御风灵貂,霓羽锦鹊,雪域圣灵,炫影魔蝎,蝠翼冥骑,灵尾松鼠,机关木鸢,灯笼锦鱼,碧海鳐鱼,玉脂福羊,
雷霆战豹,烈焰斗猪,幽骨战龙,齐天小轿,竹林熊猫,跃动精灵,七彩祥云,冰晶雪魄,冰晶小雪魄
"""


# 配置服务器
REDIS_1 = redis.StrictRedis(host='localhost', db=2, password='Xj3.14164')

