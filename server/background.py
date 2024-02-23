from flask import request


def backgroundSetBackground():

    data = request.data
    request_data = request.get_json()

    data = {
        "playerDataDelta": {
            "deleted": {},
            "modified": {
                "background": {
                    "selected": request_data["bgID"]
                }
            }
        }
    }
    return data

