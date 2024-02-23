from flask import request


def shopGetSkinGoodList():

    data = request.data
    data = {
        "goodList":[],
        "playerDataDelta":{
            "modified":{},
            "deleted":{}
        }
    }

    return data