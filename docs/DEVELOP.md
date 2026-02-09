# 此服务端的数据、代码、函数等内容的开发指南

## 函数

### run_after_response

`run_after_response` 用于在 **HTTP 响应返回客户端之后** 异步执行指定函数，实现“响应与业务后处理解耦”的执行模型。

适用于将**非关键路径逻辑**从请求处理链路中剥离，如日志、统计、通知、同步、审计等后置任务，避免阻塞接口响应时间。

本仓库常用在 `write_json` 函数中，以避免 **低速磁盘** 、 **文件锁**竞争 导致写入慢或写入出错的问题，降低接口响应时间

执行逻辑  
```go
请求处理函数执行
        ↓
HTTP Response 返回客户端
        ↓
after_this_request 回调触发
        ↓
创建异步 task
        ↓
投递到全局事件循环
        ↓
线程池执行 func(*args)
```

### load_data

独立于 `preload_json_data` 函数，用于加载其它自定义json到 **memory_cache** 中，添加 `data_path_1`、`data_path_2` 等命名规律的路径常量并加入 `data_list` 进行加载，在 **memory_cache** 中，会以文件名作为 key 值进行关联，例如 `data_path_1 = "data/rlv2/event_choices.json"` 在 **memory_cache** 中以 `{"event_choices": ...}` 存在

## 数据

### 肉鸽节点类型

| 类型 | 名称 | 能正常使用的肉鸽 | 备注 |
|:---:|:---:|:---:|:---:|
| 0 | NONE | 
| 1 | 常规作战 | 1 2 3 4 5 |  |
| 2 | 紧急作战 | 1 2 3 4 5 |  |
| 4 | 险路恶敌 | 1 2 3 4 5 |  |
| 8 | 诡异行商 | 1 |  |
| 16 | 安全的角落 | 1 2 3 4 5 |  |
| 32 | 不期而遇 | 1 2 3 4 5 |  |
| 64 | 古堡馈赠 | 1 |  |
| 128 | 幕间余兴 兴致盎然 | 1 2 3 4 |  |
| 256 | 迷雾重重 | 1 2 3 4 |  |
| 512 | 得偿所愿 | 2 3 4 5 |  |
| 1024 | 风雨际会 失与得 | 2 3 4 5 |  |
| 2048 | 紧急运输 先行一步 | 2 3 4 5 |  |
| 4096 | 诡异行商 | 2 3 4 5 |  |
| 8192 | 误入奇境 树篱之途 思维边界 | 2 3 4 5 |  |
| 16384 | 地区委托 | 2 |  |
| 32768 | 命运所指 | 3 4 5 |  |
| 65536 | 命运所指 | 3 4 5 |  |
| 131072 | 去伪存真 | 4 |  |
| 262144 | 狭路相逢 | 4 5 |  |
| 524288 | 指点迷津 | 5 |  |
| 1048576 | 误入奇境 | 5 | ro5一层end节点 |
| 7 | BATTLES |  |  |
| 913136 | CHOICES |  |  |
| 1965816 | EVENTS |  |  |
| 1965823 | ALL |  |  |

### event_choices.json 格式说明

```json
{
    "theme": { //肉鸽id
        "enter": {
            "scene_ro?_???_enter": [ //以 _enter 结尾的scence_id
                "choice_ro?_???_1",
                "choice_ro?_???_2"
                //事件起始时可用的选项
            ]
        },
        "choices": {//每个选择的效果和下一个可用选项
            "choice_ro?_???_1": { //choice的id
                "choices": ["choice_leave", "choice_ro?_???_?"], //list类型，接下来可选的选项。str类型，战斗关卡id
                "lose": null, // str类型，扣除对应物品。dict类型，扣除[player][property]下对应路径的值
                "m_lose": {}, //非必定存在的dict，扣除module下对应路径的值
                "get": null, // 最复杂的key，可以是 str|dict|list|int 中任何一个类型
                // str：藏品id或关键词，统一通过 if get in item_id: 和 item_id = random.choice(item_list) 选出藏品str id
                // dict：增加[player][property]下对应路径的值
                // list：跳过 if get in item_id: 直接赋值 item_list 进行 item_id = random.choice(item_list) 选出藏品str id
                // int：get_id 字典使用 range(get) 的边界，控制给多少个藏品，和 get_id 一起出现，注意不要下标越界
                "m_get": {}, //非必定存在的dict，增加module下对应路径的值
                "get_id": [ //非必定存在的list，和 int类型的get 一起出现
                    {"get": "", "curse": false} 
                    //get和上述的 str类型的get 一致
                    //curse和下述的 curse 一致
                ],
                "curse": false, //curse为水月肉鸽（rogue_2）独有，控制是否是 受诅藏品（debuff藏品）
                "i_get": {},
                "i_lose": {}
            }
        }
    }
}
```

## 代码

已尽力避免使用其它第三方库实现功能，且会为大型函数添加逐行注释或每段注释，应该没有什么代码看不懂吧？