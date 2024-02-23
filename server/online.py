from flask import request


def onlineV1Ping():

    data = request.data
    data = {
        "alertTime": 600,
        "interval": 3590,
        "message": "OK",
        "result": 0,
        "timeLeft": -1
    }
    
    return data


def onlineV1LoginOut():

    data = request.data
    data = {
        "error": "Not Found",
        "message": "Not Found",
        "statusCode": 404
    }
    
    return data
