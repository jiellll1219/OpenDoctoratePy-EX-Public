# DoctoratePy-EX-Public

本项目旨在作为OpenDoctoratePy的分支，拓展与完善功能。短期目标为尽可能防止因404或未知错误被踹回登录界面，长期目标为实现类似SPT-AKI项目的单人游玩本地服务

公开版仓库不提供任何游戏数据或与客户端修改相关的内容

开发仅为个人兴趣，鄙人技术有限，随缘更新，如有问题请提issue，但不保证可以第一时间修复bug（学生党只有假期期间和课余时间才有空~~堆屎山~~写代码）

此项目无任何交流群，且禁止任何以盈利为目的的分发、二次开发等行为

## 拓展进度

| 目标功能 | 进度 | 完成情况 | 备注 |
|:---:|:---:|:---:|:---:|
| 公开招募 | 编写完成 | 基本完成 | 需要测试 |
| 定向寻访 | 编写完成 | 基本完成 | 需要测试 |
| 基建 | 编写完成 | 基本完成 | 需要测试 |
| 商店 | 编写完成 | 基本完成 | 需要测试 |
| 充值 | 编写完成 | 基本完成 | 尚未测试 |
| 生息演算 | 正在研究 |  |  |
| 好友 | 正在研究 |  |  |

## 充值系统实现代码声明

# **本仓库的充值系统在正式支付环境中完全不可用，请不要尝试将此部分的代码移植到你的私有仓库中使用，我不会把这部分实现代码上传到公开仓库中，我并不希望该仓库被DMCA Take Down**

## data数据结构说明

本项目部分数据的存放结构参考了 [LocalArknight](https://github.com/jiellll1219/LocalArknight)

详细的文件结构与相关文件请查看此仓库 [LocalArknight-res](https://github.com/jiellll1219/LocalArknight-res)

Tips：如果你的user.json数据缺失，可参考 [LocalArknight](https://github.com/jiellll1219/LocalArknight) 项目的user数据，例如shop、skin等

## EX_Config参数说明

### virtualtime

供开启旧卡池使用，值小于0时为返回实时时间

可能导致基建出现问题，确定后勿随意减小该值

兼容更多时间类型，可直接输入时间戳，亦可输入如“2024/02/02 12:12:12”、“2024-02-02 12:12:12”的时间格式。请注意，在输入此类时间时请使用英文双引号""，在日期与时间之间需要一个空格，请确保填写的时间完整且合理

### Gacha

isFree控制抽卡是否消耗资源，但抽卡时仍需拥有足够资源才能进行

saveCharacter控制是否保存抽取角色

## 更新日志

- 2024 年 10 月 11 日

    添加：充值系统基本功能

    由于我完全不充钱，导致充值成功的数据无法抓取，充值成功的实现方法从逆向代码中推测而来

- 2024 年 8 月 27 日

    修复：来自issues [关于商店购买东西出错 #2](https://github.com/jiellll1219/OpenDoctoratePy-EX-Public/issues/2) 关于shop购买部分的报告

- 2024 年 8 月 15 日

    添加：sandbox框架搭建

    修改： 游戏日志上报处理代码简化

- 2024 年 8 月 10 日

    添加：游戏日志上报处理，卡池文件更新

- 2024 年 8 月 3 日

    添加：自定义时间戳功能支持输入更易读的时间格式

- 2024年 7 月 20日

    添加：卡池消耗资源与保存抽取信息开关，活动商店获取数据与购买相关代码的初始化

    修改：优化pay模块导入，mail模块添加注释

- 2024 年 7 月 15 日

    添加：gacha寻访功能完善，全部卡池信息文件

    修改：virtualtime移至exConfig.json中保存

- 2024 年 5 月 25 日

    添加：virtualtime功能，social模块，building部分功能

    修改：全部time函数从virtualtime获取

- 2024 年 4 月 8 日

    修改：building基建副手功能完善

- 2024 年 4 月 7 日

    添加：building部分功能（别问为什么水，我自己看得也迷糊）

- 2024 年 3 月 22 日

    添加：pay充值功能，GiveItem函数

-  2024 年 3 月 4 日

    添加：助理更换保存功能
    
    修改：从config设置全角色语音语言

- 2024 年 3 月 2 日

    添加：背景修改保存功能

- 2024 年 2 月 28 日

    添加：shop家具商店购买功能

- 2024 年 2 月 26 日

    添加：shop皮肤商店购买、资质凭证商店购买、高级凭证商店购买、通用凭证功商店能

- 2024 年 2 月 25 日

    初始化：building相关内容

    初始化：shop相关内容

- 2024 年 2 月 23 日

    初始化仓库、上传源代码
    
    增加env与README

