from flask import Blueprint,request,url_for
from flask_jwt_extended import jwt_required
from extensions import get_session_interface, get_img_folder
from api_model import api_response
from controllers.backend.product import get_product_list

back_category_ctrl = Blueprint('back_category_ctrl', __name__)

# 新增一個分類
@back_category_ctrl.route('/add_category', methods=['POST'])
def add_category():
  from models.category import Category
  session = get_session_interface()
  try:
    # 從 POST 請求中獲取數據
    data = request.get_json()
    if 'name' not in data or 'product_ids' not in data:
        return api_response(data=False,message='缺少必要欄位'), 400
    name = data['name']
    product_ids = data['product_ids']
    new_category = Category(name=name, product_ids=product_ids)
    # 將新產品添加到資料庫
    session.add(new_category)
    session.commit()

    # 返回成功訊息
    return api_response(data=True,message='新增分類成功!')
  finally:
    # 確保在操作完成後關閉 Session
    session.close()

# 修改一個分類
@back_category_ctrl.route('/update_category', methods=['POST'])
def update_category():
  from models.category import Category
  session = get_session_interface()
  try:
    # 從 POST 請求中獲取數據
    data = request.get_json()
    if 'id' not in data or 'name' not in data or 'product_ids' not in data:
        return api_response(data=False,message='缺少必要欄位',status_code=400)
    
    category_id = data['id']
    category = session.query(Category).get(category_id)
    if (category is None):
      return api_response(data=None,message="更新分類失敗，找不到該商品")
    
    for key, value in data.items():
      setattr(category, key, value)
    # 將新產品添加到資料庫

    session.commit()
    # 返回成功訊息
    return api_response(data=True,message='更新分類成功!')
  finally:
    # 確保在操作完成後關閉 Session
    session.close()

# 取得所有分類
@back_category_ctrl.route('/get_all_category', methods=['GET'])
def get_all_category(): 
  from models.category import Category
  session = get_session_interface()
  try:

    # 從資料庫中進行分頁查詢
    all_category = session.query(Category).all()

    res = []
    for category in all_category:
      if category.product_ids == '':
        get_products = []
      else:
        get_products = get_product_list(category.product_ids)
      data = {
        'id': category.id,
        'name': category.name,
        'product_list': get_products
      }
      res.append(data)

    return api_response(data=res,message='取得分類列表成功!')
  finally:
    # 確保在操作完成後關閉 Session
    session.close()

# 刪除一個分類
@back_category_ctrl.route('/delete_category', methods=['POST'])
def delete_category():
  from models.category import Category
  session = get_session_interface()
  try:
    # 從請求中獲取 JSON 格式的數據
    data = request.get_json()

    # 檢查必要欄位是否存在
    if 'category_id' not in data:
        return api_response(data=None,message='Missing required field: category_id',status_code=400)

    # 從資料庫中獲取指定商品
    category_id = data['category_id']
    category = session.query(Category).get(category_id)

    if (category is None):
      return api_response(data=None,message="刪除分類失敗")

    # 刪除商品
    session.delete(category)
    session.commit()

    return api_response(data=True,message="刪除成功")

  except Exception as e:
      # 如果發生錯誤，回滾事務並返回錯誤信息
      session.rollback()
      return api_response(data=None,message=str(e),status_code=500)

  finally:
      # 關閉資料庫連接
      session.close()
