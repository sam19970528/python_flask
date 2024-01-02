from flask import make_response,jsonify

# 統一的 API 回應格式
def api_response(data=None, message=None, status_code=200):
    response = {
        'data': data,
        'message': message,
    }
    return make_response(jsonify(response), status_code)