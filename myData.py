# -*- coding: utf-8 -*- 

HELP_INFO = \
u"""
欢迎关注程序猿int64Ago的试验品^_^ 目前功能包括：
【成都公交】【成都天气】[【快递智能查询】【河畔最新热帖】【校车时刻表】【电科院新闻公告】【清水河/沙河后禽各部门电话】

发送gj+线路/站点名称(gj不区分大小写，下同)，即可查询公交路线或站点信息
eg:'Gj34a'查询34A路公交线路，'gj一环路东一段'查询经过此站点公交

发送tq，即可查询最近几天成都天气

发送kd+订单号，可自动在[申通/圆通/韵达/顺丰/中通/国通]中选择查询结果，抱歉其它不常用快递无法查
eg:'kd028435956303'自动返回正确的快递公司及追踪结果

发送hp，可查询河畔首页热帖

发送xc，可查校车学生班车发车时刻表（非节假日）

发送qsh，可查询清水河后禽各集团电话

发送sh，可查询沙河后禽各集团电话

发送dk，可获取电科院最新新闻和通告

"""

SORRY_MSG = \
u"""
查询失败，请回复"?"查看帮助'
"""

XC_DATA = \
u"""
一．周一至周五：
清水河校区—沙河校区：
上午8:10、10:30、中午13:00、下午16:30、晚上18:30
沙河校区—清水河校区：
中午13:00、下午16:00—17:20、晚上19:30
二．星期六、星期日
沙河校区—清水河校区：
上午7:40—10:00、下午13:00—17:00
清水河校区—沙河校区：
上午8:00—11:00、下午14:00—18:00
"""
TEXT_MSG_TPL = \
u"""
<xml> 
  <ToUserName><![CDATA[%s]]></ToUserName>  
  <FromUserName><![CDATA[%s]]></FromUserName>  
  <CreateTime>%s</CreateTime>  
  <MsgType><![CDATA[text]]></MsgType>  
  <Content><![CDATA[%s]]></Content>  
  <FuncFlag>0</FuncFlag> 
</xml>
"""

PIC_MSG_TPL = \
u"""
<xml> 
  <ToUserName><![CDATA[%s]]></ToUserName>  
  <FromUserName><![CDATA[%s]]></FromUserName>  
  <CreateTime>%s</CreateTime>  
  <MsgType><![CDATA[news]]></MsgType>  
  <ArticleCount>1</ArticleCount>  
  <Articles> 
    <item> 
      <Title><![CDATA[点击看大图信息]]></Title>  
      <Description><![CDATA[%s]]></Description>  
      <PicUrl><![CDATA[%s]]></PicUrl>  
      <Url><![CDATA[%s]]></Url> 
    </item> 
  </Articles> 
</xml>
"""

NUMBER_QSH = \
u"""
【清水河校区】
维修工程部61830183
服务质量管理科61830826
后勤集团办61831234
后勤财务办61830018
网运综合办61830789
电话故障申告61830112
网络故障申告61830222
电信营业厅61830255
多媒体办公室61830027
一卡通维护61830123
商贸文印中心61830505
水站61830777
银桦餐厅61830302
紫荆餐厅61830181
芙蓉餐厅61830590
清真餐厅61830781
学子餐厅61830568
思源餐厅61830445
物管服务中心收发室61830207
物业管理中心公寓管理部61830374
主楼物管61830160
品学楼物管61830114
科研楼物管61830201
研究院物管61830506
活动中心物管61830103
图书馆物管61830788
综合楼物管61830691
硕士1栋组团61830124
硕士2栋组团61830257
硕士3栋组团61830166
硕士4栋组团61830393
硕士5栋组团61830692
硕士6栋组团61831215
本科2值班室61830384
本科3值班室61830364
本科4值班室61830274
本科5值班室61830314
本科6值班室61830247
本科7值班室61830085
本科8值班室61830162
本科10值班室61831871
本科11值班室61830324
本科12值班室61830214
本科13值班室61830107
本科14值班室61830194
本科15值班室61830184
本科16值班室61830281
本科17值班室61830282
本科19值班室61830296
本科20值班室61830632
本科22值班室61830637
本科24值班室61831526
本科25值班室61831633
本科26值班室61831531
硕士6值班室61830094
硕士8值班室61830097
硕士9值班室61830391
硕士10值班室61830392
硕士13值班室61830394
硕士14值班室61830681
硕士15值班室61830395
硕士16值班室61830651
硕士17值班室61830639
硕士18值班室61830679
硕士19值班室61830689
硕士21值班室61831013
交通运输服务公司61831596
驾校61830333
校医院办公室61830575
医保办61830541
急诊室61830120
防疫办61830545
财务室61830548
校园治安室61831111
户证室61830014
消防科61830012
监控室61830110
"""

NUMBER_SH = \
u"""
【沙河校区】
保卫处值班室83202241
户证室83206692
校内110	83200110
消防科83200119
社区居委会83202259
东院一区门卫83201044
东院二区门卫83201248
东院三区门卫83201225
后勤管理处住宅管理科83202473
东院物业管理办公室83207668
成电花园物业管理办公室83205868
华东云庭物业管理办公室83200678
圣地名苑物业管理办公室83208930
校医院办公室83204355
校医院财务室83207421
急诊室83202481
防疫办83202406
住院部83202495
计生办83200228
后勤集团办公室83202458
后勤集团财务室83202437
打卡机房83202483
面包房8328059
教授餐厅83208062
万友餐厅83202274
风华餐厅83202492
阳光餐厅83202441
星海图片社83208988
复印室83207808
商贸酒业83207979
校园超市83205050
新村校园超市83205353
送水部83207777
楼宇物业管理服务中心83203144
物管服务公司校园管理部83202279
水电交费处83202431
高压配电房83202464
收发室83202363
主楼物管83208313
211楼管办83202467
一教值班室83201321
三教值班室83202434
新村1栋值班室83201441
新村2栋值班室83201442
新村3栋值班室83203359
新村4栋值班室83205763
新村5栋值班室83205762
新村6栋值班室83204034
学生11栋值班室83202417
学生12栋值班室83202418
学生13栋值班室83202416
学生14栋值班室83202420
学生15栋值班室83202422
学生16栋值班室83201144
学生17栋值班室83201154
学生18栋值班室83201244
网运中心营业厅83202112
查号台83201114
电话故障申告83200112
网络故障申告83205114
外线室83201219
现代教育技术中心83202157
交通运输服务中心调度室83202429
驾校83206868
宾馆总台83206666
总机83208888
商务中心（订票）83203510
客房部83207316
餐饮部83203066
茶楼83205200
"""