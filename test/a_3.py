import re
# s = """
# 修炼总和≥ <input id="expt_total" type="text" size="6" class="txt1">
# 攻击修炼≥ <input id="expt_gongji" type="text" size="6" class="txt1">&nbsp;&nbsp;&nbsp;
# 防御修炼≥ <input id="expt_fangyu" type="text" size="6" class="txt1">&nbsp;&nbsp;&nbsp;
# 法术修炼≥ <input id="expt_fashu" type="text" size="6" class="txt1">&nbsp;&nbsp;&nbsp;
# 抗法修炼≥ <input id="expt_kangfa" type="text" size="6" class="txt1">&nbsp;&nbsp;
# 攻击上限≥ <input id="max_expt_gongji" type="text" size="6" class="txt1">&nbsp;&nbsp;&nbsp;
# 防御上限≥ <input id="max_expt_fangyu" type="text" size="6" class="txt1">&nbsp;&nbsp;&nbsp;
# 法术上限≥ <input id="max_expt_fashu" type="text" size="6" class="txt1">&nbsp;&nbsp;&nbsp;
# 抗法上限≥ <input id="max_expt_kangfa" type="text" size="6" class="txt1">&nbsp;&nbsp;&nbsp;
# 猎术修炼≥ <input id="expt_lieshu" type="text" size="6" class="txt1">
# """
# d = {}
# for line in s.splitlines():
#     if not line:
#         continue
#     k = line[:4]
#     v = re.match(r'.*?id="(.*?)".*', line)
#     d[v.group(1)] = k
# print(d)
# for k in d.values():
#     print('%s:""' % k, ',')

# s = """
# 攻击控制≥ <input id="bb_expt_gongji" type="text" size="6" class="txt1">&nbsp;&nbsp;&nbsp;
# 防御控制≥ <input id="bb_expt_fangyu" type="text" size="6" class="txt1">&nbsp;&nbsp;&nbsp;
# 法术控制≥ <input id="bb_expt_fashu" type="text" size="6" class="txt1">&nbsp;&nbsp;&nbsp;
# 抗法修炼≥ <input id="bb_expt_kangfa" type="text" size="6" class="txt1">&nbsp;&nbsp;
# 宠修总和≥ <input id="bb_expt_total" type="text" size="6" class="txt1">
# """
# d = {}
# for line in s.splitlines():
#     if not line:
#         continue
#     k = line[:4]
#     v = re.match(r'.*?id="(.*?)".*', line)
#     print(v.group(1))
#     d[v.group(1)] = k
# for k in d.keys():
#     print('%s:"",' % k, )
# s = """
# 强身术≥ <input id="skill_qiang_shen" type="text" size="6" class="txt1">&nbsp;&nbsp;&nbsp;　　
# 强壮≥ <input id="skill_qiang_zhuang" type="text" size="6" class="txt1">&nbsp;&nbsp;&nbsp;　　
# 神速≥ <input id="skill_shensu" type="text" size="6" class="txt1">&nbsp;&nbsp;&nbsp;　　
# 冥想≥ <input id="skill_ming_xiang" type="text" size="6" class="txt1">&nbsp;&nbsp;&nbsp;
# 暗器技巧≥ <input id="skill_anqi" type="text" size="6" class="txt1">
# 打造技巧≥ <input id="skill_dazao" type="text" size="6" class="txt1">&nbsp;&nbsp;&nbsp;
# 裁缝技巧≥ <input id="skill_caifeng" type="text" size="6" class="txt1">&nbsp;&nbsp;&nbsp;
# 巧匠之术≥ <input id="skill_qiaojiang" type="text" size="6" class="txt1">&nbsp;&nbsp;&nbsp;　
# 炼金术≥ <input id="skill_lianjin" type="text" size="6" class="txt1">&nbsp;&nbsp;&nbsp;
# 养生之道≥ <input id="skill_yangsheng" type="text" size="6" class="txt1">
# 烹饪技巧≥ <input id="skill_pengren" type="text" size="6" class="txt1">&nbsp;&nbsp;&nbsp;
# 中药医理≥ <input id="skill_zhongyao" type="text" size="6" class="txt1">&nbsp;&nbsp;&nbsp;
# 灵石技巧≥ <input id="skill_lingshi" type="text" size="6" class="txt1">&nbsp;&nbsp;&nbsp;　
# 健身术≥ <input id="skill_jianshen" type="text" size="6" class="txt1">
# 逃离技巧≥ <input id="skill_taoli" type="text" size="6" class="txt1">&nbsp;&nbsp;&nbsp;
# 追捕技巧≥ <input id="skill_zhuibu" type="text" size="6" class="txt1">&nbsp;&nbsp;&nbsp;
# 熔炼技巧≥ <input id="skill_ronglian" type="text" size="6" class="txt1">&nbsp;&nbsp;&nbsp;
# 淬灵之术≥ <input id="skill_cuiling" type="text" size="6" class="txt1">
# """
# d = {}
# for line in s.splitlines():
#     if not line:
#         continue
#     k = re.match(r'(.*?)≥', line).group(1)
#     v = re.match(r'.*?id="(.*?)".*', line)
#     d[v.group(1)] = k
# print(d)
# for k in d.keys():
#     print('%s:"",' % k, )

s ="""
<li data_value="1"><span>逍遥生</span></li>
<li data_value="2"><span>剑侠客</span></li>
<li data_value="3"><span>飞燕女</span></li>
<li data_value="4"><span>英女侠</span></li>
<li data_value="5"><span>巨魔王</span></li>
<li data_value="6"><span>虎头怪</span></li>
<li data_value="7"><span>狐美人</span></li>
<li data_value="8"><span>骨精灵</span></li>
<li data_value="9"><span>神天兵</span></li>
<li data_value="10"><span>龙太子</span></li>
<li data_value="11"><span>舞天姬</span></li>
<li data_value="12"><span>玄彩娥</span></li>
<li data_value="203"><span>巫蛮儿</span></li>
<li data_value="205"><span>杀破狼</span></li>
<li data_value="209"><span>羽灵神</span></li>
<li data_value="201"><span>偃无师</span></li>
<li data_value="207"><span>鬼潇潇</span></li>
<li data_value="211"><span>桃夭夭</span></li>
"""
d = {}
for line in s.splitlines():
    if not line:
        continue
    k = re.match(r'.*?data_value="(\d+)"',line).group(1)
    v = re.match(r'.*?<span>(.*?)</span>', line).group(1)
    d[k] = v
print(d)

