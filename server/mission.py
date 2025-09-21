from flask import request
from utils import read_json, write_json, run_after_response
from constants import SYNC_DATA_TEMPLATE_PATH

class mission_manger:
    def __init__(self):
        self.daily_start_list = ["daily_4801","daily_4806","daily_4808","daily_4813","daily_4814","daily_4815","daily_4816","daily_4817","daily_4819","daily_4821","daily_4822","daily_4826","daily_4829","daily_4901","daily_4906","daily_4908","daily_4913","daily_4914","daily_4915","daily_4916","daily_4917","daily_4919","daily_4921","daily_4922","daily_4926","daily_4929","daily_5001","daily_5006","daily_5008","daily_5013","daily_5014","daily_5015","daily_5016","daily_5017","daily_5019","daily_5021","daily_5022","daily_5026","daily_5029","daily_5101","daily_5106","daily_5108","daily_5113","daily_5114","daily_5115","daily_5116","daily_5117","daily_5119","daily_5121","daily_5122","daily_5126","daily_5129","daily_5201","daily_5206","daily_5208","daily_5213","daily_5214","daily_5215","daily_5216","daily_5217","daily_5219","daily_5221","daily_5222","daily_5226","daily_5229","daily_5301","daily_5306","daily_5308","daily_5313","daily_5314","daily_5315","daily_5316","daily_5317","daily_5319","daily_5321","daily_5322","daily_5326","daily_5329","daily_5401","daily_5406","daily_5408","daily_5413","daily_5414","daily_5415","daily_5416","daily_5417","daily_5419","daily_5421","daily_5422","daily_5426","daily_5429","daily_5501","daily_5506","daily_5508","daily_5513","daily_5514","daily_5515","daily_5516","daily_5517","daily_5519","daily_5521","daily_5522","daily_5526","daily_5529","daily_5601","daily_5606","daily_5608","daily_5613","daily_5614","daily_5615","daily_5616","daily_5617","daily_5619","daily_5621","daily_5622","daily_5626","daily_5629","daily_5701","daily_5706","daily_5708","daily_5713","daily_5714","daily_5715","daily_5716","daily_5717","daily_5719","daily_5721","daily_5722","daily_5726","daily_5729","daily_5801","daily_5806","daily_5808","daily_5813","daily_5814","daily_5815","daily_5816","daily_5817","daily_5819","daily_5821","daily_5822","daily_5826","daily_5829","daily_5901","daily_5906","daily_5908","daily_5913","daily_5914","daily_5915","daily_5916","daily_5917","daily_5919","daily_5921","daily_5922","daily_5926","daily_5929","daily_6001","daily_6006","daily_6008","daily_6013","daily_6014","daily_6015","daily_6016","daily_6017","daily_6019","daily_6021","daily_6022","daily_6026","daily_6029","daily_6101","daily_6106","daily_6108","daily_6113","daily_6114","daily_6115","daily_6116","daily_6117","daily_6119","daily_6121","daily_6122","daily_6126","daily_6129","daily_6201","daily_6206","daily_6208","daily_6213","daily_6214","daily_6215","daily_6216","daily_6217","daily_6219","daily_6221","daily_6222","daily_6226","daily_6229","daily_6301","daily_6306","daily_6308","daily_6313","daily_6314","daily_6315","daily_6316","daily_6317","daily_6319","daily_6321","daily_6322","daily_6326","daily_6329"]
        self.weekly_start_list = ["weekly_701","weekly_707","weekly_708","weekly_713","weekly_714","weekly_715","weekly_716","weekly_718","weekly_720","weekly_723","weekly_725","weekly_729","weekly_732"]
        self.result = {
            "playerDataDelta": {
                "modified": {},
                "deleted": {}
            }
        }

    def ConfirmMission(self):
        # 获取传入 json 内容
        json_body = request.get_json()  # {"missionId": "daily_6201"}
        mission_id = str(json_body["missionId"])

        sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)
        result = self.result
        mapping = self.mapping
        finish_list = []

        # 任务类型字符串转大写
        mission_type = str((mission_id.split("_")[0]).upper())
        mission_data = sync_data["user"]["mission"]["missions"][mission_type]

        # 循环遍历该类型下每个任务
        for key, mission_id_data in mission_data.items():
            # 如果任务id匹配
            if key == mission_id:
                state = True
                # 循环每一个任务的要求并进行比较
                for data in mission_id_data["progress"]:
                    # 如果当前值小于目标值，则把任务完成状态设为 False
                    if data["value"] < data["target"]:
                        state = False
                        break
                    else:
                        continue
                
                if state:
                    # 设定任务状态为 FINISHED ，状态定义于 Torappu.MissionHoldingState 
                    mission_id_data["state"] = 3
                    finish_list.append(mission_id)

                    # 设置下一个任务状态为可见
                    mission_dict = self.mission_state_check(mission_type, key, True)
                break

        # 在 result 中添加该类型任务的数据
        result["playerDataDelta"]["modified"]["mission"] = {}
        result["playerDataDelta"]["modified"]["mission"]["missions"] = {}
        result["playerDataDelta"]["modified"]["mission"]["missions"][mission_type] = {}
        if mission_dict is not None:
            for mission_id, mission_data_item in mission_dict.items():
                result["playerDataDelta"]["modified"]["mission"]["missions"][mission_type][mission_id] = mission_data_item
        
        for mission_id in finish_list:
            result["playerDataDelta"]["modified"]["mission"]["missions"][mission_type][mission_id] = mission_data[mission_id]

        # run_after_response(write_json, sync_data, SYNC_DATA_TEMPLATE_PATH)
        return result

    def AutoConfirmMissions(self):
        json_body = request.get_json()  # {'type': 'MAIN'}
        mission_type = json_body["type"]

        sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)

        mission_data = sync_data["user"]["mission"]["missions"][mission_type]

        result = {
            "playerDataDelta": {
                "modified": {
                    "mission": {
                        "missions": {
                            mission_type: {}
                        }
                    }
                },
                "deleted": {}
            },
            "items": []
        }

        for mission_id, mission_data_item in mission_data.items():
            mission_dict = {}
            all_completed = True
            for data in mission_data_item["progress"]:
                if data["value"] < data["target"]:
                    all_completed = False
                    break

            if all_completed:
                mission_data_item["state"] = 3
                mission_dict = self.mission_state_check(mission_type, mission_id, True)

                if mission_dict is not None:
                    for mission_id2, mission_data_item2 in mission_dict.items():
                        result["playerDataDelta"]["modified"]["mission"]["missions"][mission_type][mission_id2] = {}
                        result["playerDataDelta"]["modified"]["mission"]["missions"][mission_type][mission_id2] = mission_data_item2
                result["playerDataDelta"]["modified"]["mission"]["missions"][mission_type][mission_id] = (mission_data_item)

        # run_after_response(write_json, sync_data, SYNC_DATA_TEMPLATE_PATH)
        return result



    def mission_state_check(self, mission_type: str, mission_id: str, need_result: bool=False):
        '''
        用于每日任务与每周任务的状态更新

        :param mission_type: 要检查的任务状态类型，只能是"DAILY"或"WEEKLY"
        :param mission_id: 任务id，用于检查下一个任务是否可见
        '''

        # 预设常量，读取数据
        sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)
        mission_data = sync_data["user"]["mission"]["missions"][mission_type]
        mission_dict = {}
        
        # 根据任务类型选择排除列表
        match mission_type:
            case "DAILY":
                start_list = set(self.daily_start_list)
            case "WEEKLY":
                start_list = set(self.weekly_start_list)
            case _:
                return 0

        # if mission_id is not None:
        mission_str = str(mission_id.split("_")[0]) + "_"
        num = int(mission_id.split("_")[1])
        num += 1
        new_id = mission_str + str(num)
        if new_id in start_list:
            pass
        else:
            mission_data[new_id]["state"] = 2
            mission_dict[new_id] = {}
            mission_dict[new_id] = mission_data[new_id]

        run_after_response(write_json, sync_data, SYNC_DATA_TEMPLATE_PATH)

        if need_result:
            return mission_dict

    def re_set_state(self, mission_type: str = None):
        '''
        用于重置任务状态

        :param mission_type: 要重置的任务类型
        '''

        sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)

        def process_data(data, list_a):
            for key, value in data.items():
                # 设置默认值
                value['state'] = 1
                for item in value.get('progress', []):
                    item['value'] = 0
                
                # 检查是否在list_a中
                if key in list_a:
                    value['state'] = 2

        if mission_type is None:
            mission_data = sync_data["user"]["mission"]["missions"]

            for key, value in mission_data["missionRewards"]["rewards"]["DAYLY"].items():
                mission_data["missionRewards"]["rewards"]["DAYLY"][key] = 0
            process_data(mission_data["DAILY"], self.daily_start_list)

            for key, value in mission_data["missionRewards"]["rewards"]["WEEKLY"].items():
                mission_data["missionRewards"]["rewards"]["WEEKLY"][key] = 0
            process_data(mission_data["WEEKLY"], self.weekly_start_list)
            
            
        else:
            mission_data = sync_data["user"]["mission"]["missions"][mission_type]

            for key, value in sync_data["user"]["mission"]["missions"]["missionRewards"]["rewards"][mission_type].items():
                sync_data["user"]["mission"]["missions"]["missionRewards"]["rewards"][mission_type][key] = 0
            process_data(mission_data, self.daily_start_list if mission_type == "DAILY" else self.weekly_start_list)

        run_after_response(write_json, sync_data, SYNC_DATA_TEMPLATE_PATH)
        return 0
