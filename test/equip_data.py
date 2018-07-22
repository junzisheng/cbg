#encoding=utf-8
import re
# EquipKinds = [[10, '扇'], [6, '剑'], [14, '刀'], [5, '斧'], [15, '锤'], [4, '枪'], [13, '双环'], [7, '双剑'], [12, '鞭子'], [9, '爪刺'], [11, '魔棒'], [8, '飘带'], [52, '宝珠'], [53, '弓箭'], [54, '法杖'], [18, '男衣'], [59, '女衣'], [17, '男头'], [58, '女头'], [20, '腰带'], [19, '鞋子'], [21, '饰品'], [72, '灯笼'], [73, '巨剑'], [74, '伞']]
# SpecialSkills = [[1027, "罗汉金钟"], [1015, "晶清诀"], [1018, "笑里藏刀"], [1036, "破血狂攻"], [1042, "破碎无双"], [1011, "慈航普度"], [1008, "四海升平"], [1014, "玉清诀"], [1030, "放下屠刀"], [1020, "野兽之力"], [1024, "流云诀"], [1034, "凝滞术"], [1022, "光辉之甲"], [1032, "破甲术"], [1012, "水清诀"], [1037, "弱点击破"], [2002, "聚精会神"], [2004, "燃烧之光"], [1010, "起死回生"], [1009, "回魂咒"], [1023, "圣灵之甲"], [1033, "碎甲术"], [1031, "河东狮吼"], [1021, "魔兽之印"], [1025, "啸风诀"], [1035, "停陷术"], [2003, "先发制人"], [2007, "菩提心佑"], [1038, "吸血"], [1039, "残月"], [1007, "命归术"], [1045, "虚空之刃"], [1001, "气疗术"], [1002, "心疗术"], [1003, "命疗术"], [1004, "凝气诀"], [1005, "凝神决"], [1006, "气归术"], [1013, "冰清诀"], [1016, "诅咒之伤"], [1017, "诅咒之亡"], [1019, "绝幻魔音"], [1026, "太极护法"], [1028, "修罗咒"], [1029, "天衣无缝"], [1040, "冥王暴杀"], ["2041,1041", "乾坤斩"], [1043, "帝释无双"], [1044, "伽罗无双"], [1046, "亡灵之刃"], [1047, "死亡之音"], [1048, "身似菩提"], [1049, "心如明镜"], [1050, "移形换影"], [2001, "凝心决"], [2005, "毁灭之光"], [2006, "金刚不坏"]]
# SpecialEffects = [[1, "无级别"], [2, "简易"], [3, "愤怒"], [4, "暴怒"], [5, "永不磨损"], [6, "神农"], [7, "神佑"], [8, "精致"], [9, "坚固"], [10, "狩猎"], [11, "绝杀"], [12, "专注"], [13, "伪装"], [14, "易修理"], [15, "再生"], [16, "必中"], [17, "迷踪"], [18, "珍宝"]]
# d = {}
# for k, v in SpecialEffects:
#     d[k] = v
# print(d)
# s = """
# 初伤（包含命中）≥ <input type="text" size="6" class="txt1" id="txt_init_damage">&nbsp;&nbsp;&nbsp;
# 初伤（不含命中）≥ <input type="text" size="6" class="txt1" id="txt_init_damage_raw">&nbsp;&nbsp;&nbsp;
# 初防≥ <input type="text" size="6" class="txt1" id="txt_init_defense">&nbsp;&nbsp;&nbsp;
# 初血≥ <input type="text" size="6" class="txt1" id="txt_init_hp">&nbsp;&nbsp;&nbsp;
# 初敏≥ <input type="text" size="6" class="txt1" id="txt_init_dex">&nbsp;&nbsp;&nbsp;
# 初灵≥ <input type="text" size="6" class="txt1" id="txt_init_wakan">
# 总伤≥ <input type="text" size="6" class="txt1" id="txt_all_damage">&nbsp;&nbsp;&nbsp;
# 伤害≥ <input type="text" size="6" class="txt1" id="txt_damage">
# """
# d = {}
# for line in s.splitlines():
#     if not line:
#         continue
#     k = re.match(r'(.*?)≥ ', line).group(1)
#     v = re.match(r'.*?id="(.*?)"', line).group(1)
#     d[v] = k
# print(d)
SumAtrs = [['physique', '体质'], ['endurance', '耐力'], ['dex', '敏捷'], ['magic', '魔力'], ['power', '力量']]
Gems = [[1, '红玛瑙'], [2, '太阳石'], [3, '舍利子'], [4, '光芒石'], [5, '月亮石'], [6, '黑宝石'], [7, '神秘石'], [12, '翡翠石']]
EquipAttrs160 = [[1, '物理暴击几率'], [2, '法术暴击几率'], [3, '物理暴击伤害'], [4, '法术暴击伤害'], [5, '治疗能力'], [6, '封印命中率'], [7, '抵抗封印命中率'], [8, '穿刺效果'], [9, '格挡物理伤害'], [10, '魔法回复'], [11, '法术伤害减免效果']]

d = {}
for k, v in EquipAttrs160:
    d[k] = v
print(d)





