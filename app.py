from flask import Flask,jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from controllers.backend.user import backend_user_ctrl
from controllers.backend.product import back_product_ctrl
from controllers.backend.category import back_category_ctrl
from controllers.app.product import app_product_ctrl
from api_model import api_response
import secrets
import os

jwt_secret_key = secrets.token_urlsafe(32)

# 設定靜態檔案夾
app = Flask(__name__, static_folder='static')
#處理中文編碼問題
app.json.ensure_ascii = False
app.config['JWT_SECRET_KEY'] = jwt_secret_key
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_uri = 'mysql+pymysql://root:peipei!!!0528@34.121.3.152:3306/pythonbro'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
Base = declarative_base()
# 初始化 SQLAlchemy

db = SQLAlchemy(app)

# 定义模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# 创建数据库表
db.create_all()

# 路由和视图函数
@app.route('/')
def index():
    return 'Hello, World!'


# engine = create_engine(db_uri)
# img_folder = os.path.join(app.static_folder)


def create_session():
  Session = sessionmaker(bind=engine)
  session = Session()
  return session

jwt = JWTManager(app)
CORS(app) 

@app.route('/hello', methods=['GET'])
def hello():
  res = '測試請求成功'
  return api_response(data=res,message=res)

app.register_blueprint(backend_user_ctrl, url_prefix="/backend/user")
app.register_blueprint(back_product_ctrl, url_prefix="/backend/product")
app.register_blueprint(back_category_ctrl, url_prefix="/backend/category")
app.register_blueprint(app_product_ctrl, url_prefix="/app/product")

if __name__ == '__main__':
  app.run(debug=True,port=5000)