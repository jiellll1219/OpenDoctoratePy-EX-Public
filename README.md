# DoctoratePy-EX-Public

[简中](https://github.com/jiellll1219/OpenDoctoratePy-EX-Public/tree/main/README.md) | [EN](https://github.com/jiellll1219/OpenDoctoratePy-EX-Public/blob/main/docs/README_EN.md)

[更新日志（CN Only）](https://github.com/jiellll1219/OpenDoctoratePy-EX-Public/tree/main/docs/updata_log.md)

本项目旨在作为OpenDoctoratePy的分支，拓展与完善功能。短期目标为尽可能防止因404或未知错误被踹回登录界面，长期目标为实现类似SPT-AKI项目的单人游玩本地服务

此仓库部分功能实现的代码与数据结构参考了[LocalArknight](https://github.com/jiellll1219/LocalArknight)

开发仅为个人兴趣，鄙人技术有限，随缘更新，如有问题请提issue，但不保证可以第一时间修复bug（学生党只有假期期间和课余时间才有空~~堆屎山~~写代码）

这个仓库欢迎各位开发者提出pr，共同开发DoctoratePy是我创建这个仓库的初衷

如果需要联系我，请提出issue或向我的邮箱发送邮件：jiege0019@gmail.com

此项目无任何交流群，且禁止任何以盈利为目的的分发、二次开发等行为

如果您希望为此仓库贡献代码，但苦于没有数据，可以在 [此处](https://tptpmmpc.ap-southeast-1.clawcloudrun.com/) 下载il2cpp文件，我会不定时上传每个版本的il2cpp文件

## 拓展进度

| 目标功能 | 进度 | 完成情况 | 备注 |
|:---:|:---:|:---:|:---:|
| 公开招募 | 暂停 | 神秘BUG |  |
| 定向寻访 | 完成 | 完成 | 已测试 |
| 基建 | 需要完善 | 需要完善 |  |
| 商店 | 完成 | 基本完成 | 无法购买 |
| 充值 | 完成 | 完成 |  |
| 界面方案 | 完成 | 完成 | 已测试 |
| 签到 | 完成 | 完成 | 已测试 |
| 签到活动 | 持续更新 | 基本完成 |  |
| 限时活动 | 持续更新 |  |  |
| 肉鸽 | 正在编写 | 仅限能玩 |  |
| 任务 | 正在编写 |  |  |
| 生息演算 | 暂停 |  |  |
| 好友助战 | 暂停 |  |  |

## 充值系统实现代码声明

# **本仓库的充值系统在正式支付环境中完全不可用，请不要尝试将此部分的代码移植到你的私有仓库中使用，我不会把这部分实现代码上传到公开仓库中，我并不希望该仓库被DMCA TakeDown**

## 使用教程

请确保你使用的python版本大于等于3.11.0，低于3.11.0可能会出现python自带的datetime模块缺失函数

1、自行寻找GameData或dump游戏资源以获取`excel`文件夹以及内容，并把`excel`文件夹放到 `data` 目录下  
2、（可选）使用pip命令安装需要的模块 `pip install -r requirements.txt`  
3、运行 `start_local_server.bat` 启动服务端  
4、自行寻找办法使游戏路由指向服务端，本仓库不提供解决办法

~~如果您觉得这很麻烦，也可以连接到我的公共服务器上进行体验，服务器地址为`http://8.138.148.178:8443/`，我的功能开发进度也会~~实时~~间歇性同步到此服务器中。注意！此服务器的版本仍为单人游玩版本，不支持多用户游玩，此服务器位于中国境内，服务器所使用的代码结构与此仓库的代码不完全一致，但功能基本相同~~

## data数据结构说明

本项目部分数据的存放结构参考了 [LocalArknight](https://github.com/jiellll1219/LocalArknight)

详细的文件结构与相关文件请查看此仓库 [LocalArknight-res](https://github.com/jiellll1219/LocalArknight-res)

此仓库提供的 user.json 的游戏版本为CN2.4.41

## EX_Config参数说明

### virtualtime

供开启旧卡池使用，值小于0时为返回实时时间

可能导致基建出现问题，确定后勿随意减小该值

兼容更多时间类型，可直接输入时间戳，亦可输入如“2024/02/02 12:12:12”、“2024-02-02 12:12:12”的时间格式。请注意，在输入此类时间时请使用英文双引号""，在日期与时间之间需要一个空格，请确保填写的时间完整且合理

### useMemoryCache

控制是否使用内存缓存功能，默认为false（关闭），启用（设定为true）此功能时，启动服务端后会占用至少0.4GB内存，同时会略微降低 CPU使用率 和 syncdata函数的耗时 以及其它读取table类文件的函数的耗时。不启用此功能时，启动后内存占用为80MB左右，最大内存消耗在0.2GB左右，请酌情开启。

优化后的syncdata函数实测耗时已经控制在一个比较好的范围内，不启用内存缓存时，CPU频率3.1Ghz的syncData耗时1.667709秒，CPU频率1.5Ghz的syncData耗时3.695747秒（测试使用的版本为2.4.61）

### useExistingCharData

控制在同步数据（SyncData）时，默认为false（关闭），是否使用user.json保存的角色数据，用于个性化角色设置。在有角色数据的情况下，启用（设定为true）时，该功能可以加快函数运行速度

## user.json的全部键

在这个文件中的user字典中，存在的项如下

```json
"dungeon": {},
"activity": {},
"status": {},
"troop": {},
"npcAudio": {},
"pushFlags": {},
"equipment": {},
"skin": {},
"shop": {},
"mission": {},
"social": {},
"building": {},
"dexNav": {},
"crisis": {},
"crisisV2": {},
"nameCardStyle": {},
"tshop": {},
"gacha": {},
"backflow": {},
"mainline": {},
"avatar": {},
"background": {},
"homeTheme": {},
"rlv2": {},
"deepSea": {},
"tower": {},
"siracusaMap": {},
"sandboxPerm": {},
"openServer": {},
"trainingGround": {},
"storyreview": {},
"medal": {},
"inventory": {},
"limitedBuff": {},
"carousel": {},
"car": {},
"collectionReward": {},
"consumable": {},
"ticket": {},
"aprilFool": {},
"retro": {},
"campaignsV2": {},
"recruit": {},
"checkIn": {},
"share": {},
"charRotation": {},
"charm": {},
"firework": {},
"event": {}
```
