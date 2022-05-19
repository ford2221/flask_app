import json

def sendResJson(data, msg, code):

    if code != 200:
        return json.dumps(
            {
                'code': code,
                'msg': msg
            }
        ),200
    else:
        return json.dumps(
            {
                'code': code,
                'data': data
            }
        ),200