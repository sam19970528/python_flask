from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from models.user import AuthService

backend_user_ctrl = Blueprint('backend_user_ctrl', __name__)

@backend_user_ctrl.route('/login', methods=['POST'])
def login():
  data = request.get_json()

  if 'username' not in data or 'password' not in data:
    return jsonify({ 'error': 'Missing username or password' }), 400
  
  username = data['username']
  password = data['password']

  if AuthService.authenticate(username,password):
    print('有臭甲')
    access_token = AuthService.create_access_token(identity=username)
    res_data = {
      'data': access_token,
      'message': '登入成功!'
    }
    return jsonify(res_data)
  else:
    return jsonify({ 'message': '帳號或密碼錯誤!' }), 401
  
@backend_user_ctrl.route('/testjwt', methods=['GET'])
@jwt_required()
def test_jwt():
    return jsonify({ 'message': '權限成功' })