from time import time

from flask import request


def buildingSync():

    data = request.data
    data = {
        "ts": round(time()),
        "playerDataDelta": {
            "modified": {
                "building": {},
                "event": {
                    "building": round(time()) + 3000
                }
            },
            "deleted": {}
        }
    }
    return data

def buildingGetRecentVisitors():

    data = request.data
    data = {"num":0}
    return data

def buildingGetInfoShareVisitorsNum():

    data = request.data

    return data

def buildingAssignChar():

    data = request.data

    return data

def buildingChangeDiySolution():

    data = request.data

    return data

def buildingChangeManufactureSolution():

    data = request.data

    return data

def buildingSettleManufacture():

    data = request.data

    return data

def buildingWorkshopSynthesis():

    data = request.data

    return data

def buildingUpgradeSpecialization():

    data = request.data

    return data

def buildingCompleteUpgradeSpecialization():

    data = request.data

    return data

def buildingDeliveryOrder():

    data = request.data

    return data

def buildingDeliveryBatchOrder():

    data = request.data

    return data

def buildingCleanRoomSlot():

    data = request.data

    return data

def buildinggetAssistReport():

    data = request.data
    
    return data