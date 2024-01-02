from flask_jwt_extended import create_access_token

class AuthService:
  def authenticate(username, password):
    valid_username="sam"
    valid_password="123456"

    if username == valid_username and password == valid_password:
      return True
    else:
      return False
  
  def create_access_token(identity):
    return create_access_token(identity=identity)