# DoctoratePy-EX-Public

[更新日志](https://github.com/jiellll1219/OpenDoctoratePy-EX-Public/tree/main/docs/updata_log.md)

本项目旨在作为OpenDoctoratePy的分支，拓展与完善功能。短期目标为尽可能防止因404或未知错误被踹回登录界面，长期目标为实现类似SPT-AKI项目的单人游玩本地服务

此仓库部分功能实现的代码与数据结构参考了[LocalArknight](https://github.com/jiellll1219/LocalArknight)

开发仅为个人兴趣，鄙人技术有限，随缘更新，如有问题请提issue，但不保证可以第一时间修复bug（学生党只有假期期间和课余时间才有空~~堆屎山~~写代码）

这个仓库欢迎各位开发者提出pr，共同开发DoctoratePy是我创建这个仓库的初衷

如果需要联系我，请提出issue或向我的邮箱发送邮件：jiege0019@gmail.com

此项目无任何交流群，且禁止任何以盈利为目的的分发、二次开发等行为

如果您希望为此仓库贡献代码，但苦于没有数据，可以使用 [这份](https://drive.google.com/file/d/1q7I_cAFzMtyZ2EYqd1IlZLez1uRElgTv/view?usp=sharing) il2cpp文件进行参考

## 拓展进度

| 目标功能 | 进度 | 完成情况 | 备注 |
|:---:|:---:|:---:|:---:|
| 公开招募 | 编写完成 | 基本完成 | 需要测试 |
| 定向寻访 | 编写完成 | 完成 | 基本可用 |
| 基建 | 编写完成 | 基本完成 | 需要测试 |
| 商店 | 编写完成 | 基本完成 | 需要测试 |
| 充值 | 编写完成 | 基本完成 | 尚未测试 |
| 生息演算 | 暂停 |  |  |
| 好友 | 停止 |  | 无作用 |

## 充值系统实现代码声明

# **本仓库的充值系统在正式支付环境中完全不可用，请不要尝试将此部分的代码移植到你的私有仓库中使用，我不会把这部分实现代码上传到公开仓库中，我并不希望该仓库被DMCA TakeDown**

## data数据结构说明

本项目部分数据的存放结构参考了 [LocalArknight](https://github.com/jiellll1219/LocalArknight)

详细的文件结构与相关文件请查看此仓库 [LocalArknight-res](https://github.com/jiellll1219/LocalArknight-res)

Tips：如果你的user.json数据缺失，可参考 [LocalArknight](https://github.com/jiellll1219/LocalArknight) 项目的user数据，例如shop、skin等

## EX_Config参数说明

### virtualtime

供开启旧卡池使用，值小于0时为返回实时时间

可能导致基建出现问题，确定后勿随意减小该值

兼容更多时间类型，可直接输入时间戳，亦可输入如“2024/02/02 12:12:12”、“2024-02-02 12:12:12”的时间格式。请注意，在输入此类时间时请使用英文双引号""，在日期与时间之间需要一个空格，请确保填写的时间完整且合理

## user.json与syncData.json的值

在这两个文件中的user字典中，存在的项如下

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