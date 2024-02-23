from flask import request


def payGetUnconfirmedOrderIdList():

    data = request.data
    data = {
        "orderIdList": [],
        "playerDataDelta": {
            "deleted": {},
            "modified": {}
        }
    }

    return data


def paygetAllProductList():

    data = request.data
    data = {
        "productList": []
    }

    return data