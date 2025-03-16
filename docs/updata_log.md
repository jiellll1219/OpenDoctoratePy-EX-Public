# 更新日志

- 2025 年 3 月 16 日

    修复：  
    charBuildSetDefaultSkill函数无法对新角色技能进行修改的问题

    修改：  
    尝试优化syncdata函数Tamper Skins部分，并添加注释

- 2025 年 3 月 13 日

    修复：  
    1、accountSyncData函数未正确调用已有角色数据  
    2、accountSyncData函数全部皮肤获取异常问题  
    3、accountSyncData函数角全部色最新皮肤未覆盖问题  
    4、config的funcVer版本问题
    
    添加：  
    exConfig添加是否使用已有角色数据的开关 

    更新：  
    新gacha文件添加

- 2025 年 3 月 8 日

    修改：  
    1、基建数据更新会客室DIY内容，尝试优化基建sync函数  
    2、修复getOtherPlayerNameCard函数错误  
    3、恢复social被删除的路由，添加新功能  
    4、更新config的游戏版本信息，更新README

- 20255 年 3 月 7 日

    贡献者：  
    [Ali-Ericpu](https://github.com/Ali-Ericpu)

    修改：更新商店数据

- 2025 年 3 月 2 日

    添加：  
    user.json补充mission的内容

    修改：  
    1、gacha模块与user.json删除gachaCountn相关内容  
    2、尝试优化accountSyncData函数  
    3、更新gacha文件和游戏版本信息  
    4、更改README中模糊的描述  
    5、修复 [79be343](https://github.com/jiellll1219/OpenDoctoratePy-EX-Public/commit/79be3430f3676ea23da3472f6c1d9949926c3893) 中遗漏的crisisV2商店返回逻辑

- 2025 年 2 月 25 日

    贡献者：  
    [Ali-Ericpu](https://github.com/Ali-Ericpu)

    修改：  
    删除pay、shop、constants模块的冗余代码

- 2025 年 2 月 24 日

    贡献者：  
    [Ali-Ericpu](https://github.com/Ali-Ericpu)

    修改：  
    优化商店访问逻辑，更新商店数据

- 2025 年 2 月 15 日

    修复：  
    updatePreset函数对部分情况的处理失败

    添加：  
    1、building模块添加部分未完成的功能以防止404  
    2、危机合约路由与商店内容  
    3、为gacha系统增加防御措施，当不存在卡池文件时，返回默认卡池文件  
    4、尝试修复助战系统

    修改：  
    1、对app.py的路由表进行整理  
    2、syncdata函数删除测试用代码内容

- 2025 年 2 月 6 日

    临时更新

    修复：  
    1、user.json内容错误  
    2、building模块sync函数get_memory参数错误，导致未开启“载入到内存”时无法正确读取building_data.json

    添加：危机合约第三赛季文件

    修改：config文件修改危机合约为第三赛季；user.json添加危机合约第三赛季内容

- 2025 年 1 月 28 日

    修复：  
    syncData对界面方案系统不生效的问题

    添加：  
    为excel文件夹的文件添加‘载入到内存’方法以更快地读取table数据，感谢同一位好心的开发者提供灵感

    修改：  
    1、尝试为syncData提升效率  
    2、为读取table类文件的代码改为使用新的'get_memory'方法

    不出意外的话，在春节期间我不会有更新

- 2025 年 1 月 25 日

    大幅降低使用本仓库代码的门槛  
    修复众多错误与匪夷所思的代码（仍有众多匪夷所思的地方）  
    已进行常用功能测试（商店浏览、抽卡、基建浏览）

    修复：修复Gacha函数未正确更新保底次数

- 2025 年 1 月 23 日

    修复：  
    对charrotation.py中一处错误的import进行修正

    添加：  
    1、对2.4.41版本邮件夹功能支持，感谢同一位好心的开发者对此功能开发的帮助  
    2、为不同类型的卡池添加独立保底功能  
    3、在app.py中添加基建队列功能的路由（未完成功能，但进行使用不会报错）

    修改：  
    1、尝试对accountSyncData函数进行优化
    2、删除exConfig.json中不需要的内容

    更新：新gacha文件添加

- 2025 年 1 月 2 日

    修复：  
    对updatePreset函数返回会导致游戏错误的问题进行修复，进行并通过了简单测试

    添加：  
    ~~半机器半人工翻译的英文版本README~~纯机器翻译的英文版本的README

- 2024 年 12 月 31 日

    修复：  
    尝试对updatePreset函数进行修复；添加gachaHistory.json空文件

    更新：  
    新gacha文件添加

- 2024 年 12 月 17 日

    修复：  
    修复对界面方案系统的支持，已进行简单测试

- 2024 年 12 月 16 日

    添加：  
    为2.4.21版本的界面方案系统添加支持

    修改：  
    building部分：初步改进基建的日报报文内容  
    account部分：为2.4.21版本的界面方案系统添加支持

- 2024 年 12 月 3 日

    修改：  
    修复抽卡功能实现代码，兼容至游戏版本2.4.01，基建支持房间升降级，统一constants中部分函数的命名，修复部分bug

    添加：  
    抽卡记录查询功能，gacha文件更新

    感谢某位好心的开发者提供的gacha文件

- 2024 年 10 月 28 日

    修改：  
    对rlv2和pay的部分代码进行优化和bug修复

- 2024 年 10 月 11 日

    添加：  
    充值系统基本功能

    由于我完全不充钱，导致充值成功的数据无法抓取，充值成功的实现方法从逆向代码中推测而来

- 2024 年 8 月 27 日

    修复：来自issues [关于商店购买东西出错 #2](https://github.com/jiellll1219/OpenDoctoratePy-EX-Public/issues/2) 关于shop购买部分的报告

- 2024 年 8 月 15 日

    添加：  
    sandbox框架搭建

    修改：   
    游戏日志上报处理代码简化

- 2024 年 8 月 10 日

    添加：  
    游戏日志上报处理，卡池文件更新

- 2024 年 8 月 3 日

    添加：  
    自定义时间戳功能支持输入更易读的时间格式

- 2024年 7 月 20日

    添加：  
    卡池消耗资源与保存抽取信息开关，活动商店获取数据与购买相关代码的初始化

    修改：  
    优化pay模块导入，mail模块添加注释

- 2024 年 7 月 15 日

    添加：  
    gacha寻访功能完善，全部卡池信息文件

    修改：  
    virtualtime移至exConfig.json中保存

- 2024 年 5 月 25 日

    添加：  
    virtualtime功能，social模块，building部分功能

    修改：  
    全部time函数从virtualtime获取

- 2024 年 4 月 8 日

    修改：  
    building基建副手功能完善

- 2024 年 4 月 7 日

    添加：  
    building部分功能（别问为什么水，我自己看得也迷糊）

- 2024 年 3 月 22 日

    添加：  
    pay充值功能，GiveItem函数

-  2024 年 3 月 4 日

    添加：  
    助理更换保存功能
    
    修改：  
    从config设置全角色语音语言

- 2024 年 3 月 2 日

    添加：  
    背景修改保存功能

- 2024 年 2 月 28 日

    添加：  
    shop家具商店购买功能

- 2024 年 2 月 26 日

    添加：  
    shop皮肤商店购买、资质凭证商店购买、高级凭证商店购买、通用凭证功商店能

- 2024 年 2 月 25 日

    初始化：  
    building相关内容  
    shop相关内容

- 2024 年 2 月 23 日

    初始化仓库、上传源代码
    
    增加env与README

