from flask import make_response, json


def res(code, data=False):
    status = 'success' if code == 200 else "failed"

    res = make_response()

    res.data = json.dumps({
        "code": code,
        "status": status,
        "data": data})
    res.content_type = "application/json"
    return res
