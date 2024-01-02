from flask import Blueprint,request,url_for
from flask_jwt_extended import jwt_required
from extensions import get_session_interface, get_img_folder
from api_model import api_response
import random
import string
import os

back_product_ctrl = Blueprint('back_product_ctrl', __name__)

# 取得全部商品列表
@back_product_ctrl.route('/get_product_list', methods=['GET'])
# @jwt_required()
def get_product_list():
  from models.product import Product,format_product
  session = get_session_interface()

  try:
    # 從請求中獲取查詢參數
    page_size = int(request.args.get('page_size', 20))
    page_index = int(request.args.get('page_index', 1))

    # 計算分頁的起始索引
    start_index = (page_index - 1) * page_size

    # 從資料庫中進行分頁查詢
    all_prod = session.query(Product).offset(start_index).limit(page_size).all()

    # 獲得商品總量
    total_count = session.query(Product).count()

    # 計算總頁數
    total_pages = (total_count + page_size - 1) // page_size

    product_list = [
      format_product(prod)
      for prod in all_prod
    ]
    res = {
      'total_count': total_count,
      'total_pages': total_pages,
      'page_index': page_index,
      'page_size': page_size,
      'product_list': product_list
    }
    return api_response(data=res,message='取得商品列表成功!')
  except Exception as e:
    # 如果發生錯誤，回滾事務並返回錯誤信息
    session.rollback()
    return api_response(data=None,message=str(e),status_code=500)
  finally:
    session.close()

# 取得單一商品細節
@back_product_ctrl.route('/get_product', methods=['POST'])
def get_product():
    from models.product import Product,format_product
    session = get_session_interface()
    try:
      # 從請求中獲取 JSON 格式的數據
      data = request.get_json()

      # 檢查必要欄位是否存在
      if 'product_id' not in data:
        return api_response(data=None,message='Missing required field: product_id',status_code=400)

      # 從資料庫中獲取指定商品
      product_id = data['product_id']
      product = session.query(Product).get(product_id)
      if (product is None):
        return api_response(data=None,message="取得商品失敗，找不到該商品")
      
      res = format_product(product)
      session.close()

      return api_response(data=res,message="取得商品成功!")

    except Exception as e:
      # 如果發生錯誤，回滾事務並返回錯誤信息
      session.rollback()
      return api_response(data=None,message=str(e),status_code=500)

    finally:
      # 關閉資料庫連接
      session.close()

# 取得特定商品列表
def get_product_list(product_ids):
  from models.product import Product,format_product
  session = get_session_interface()
  # 將 product_ids 字串轉換為整數列表
  ids = [int(id.strip()) for id in product_ids.split(',')]
  products = session.query(Product).filter(Product.product_id.in_(ids)).all()

  format_products = [
    format_product(prod)
    for prod in products
  ]
  return format_products


# 新增一個商品
@back_product_ctrl.route('/add_product', methods=['POST'])
def add_product():
  from models.product import Product
  session = get_session_interface()
  try:
    # 從 POST 請求中獲取數據
    data = request.get_json()

    # 檢查必要的欄位是否存在
    if 'product_name' not in data:
      return api_response(data=None,message='商品名稱為必填欄位!',status_code=400)
    elif 'price' not in data:
      return api_response(data=None,message='商品價格為必填欄位!',status_code=400)
    elif 'stock' not in data:
      return api_response(data=None,message='商品庫存為必填欄位!',status_code=400)
    elif 'description' not in data:
      return api_response(data=None,message='缺少商品描述欄位',status_code=400)
    elif 'product_img' not in data:
      return api_response(data=None,message='缺少商品圖片欄位',status_code=400)

    # 創建新的產品
    new_product = Product(
      product_name=data['product_name'], 
      price=data['price'], 
      stock=data['stock'], 
      description=data['description'],
      product_img=data['product_img'],
    )

    # 將新產品添加到資料庫
    session.add(new_product)
    session.commit()

    # 返回成功訊息
    return api_response(data=True,message='新增商品成功!')
  finally:
    # 確保在操作完成後關閉 Session
    session.close()

# 更新一筆商品
@back_product_ctrl.route('/update_product', methods=['POST'])
def update_product():
  from models.product import Product,format_product
  session = get_session_interface()
  try:
      # 從請求中獲取 JSON 格式的數據
      data = request.get_json()

      # 檢查必要欄位是否存在
      required_fields = ['product_id', 'product_name', 'price', 'description', 'stock', 'product_img']
      for field in required_fields:
          if field not in data:
              return api_response(data=None,message=f'Missing required field: {field}',status_code=400)

      # 從資料庫中獲取指定商品
      product_id = data['product_id']
      product = session.query(Product).get(product_id)
      if (product is None):
        return api_response(data=None,message="更新商品失敗，找不到該商品")

      # 更新商品屬性
      for key, value in data.items():
          setattr(product, key, value)

      # 提交更改到資料庫
      session.commit()
      updated_product = session.query(Product).get(product_id)
      res = format_product(updated_product)
      return api_response(data=res,message="更新成功")

  except Exception as e:
      # 如果發生錯誤，回滾事務並返回錯誤信息
      session.rollback()
      return api_response(data=None,message=str(e),status_code=500)

  finally:
      # 關閉資料庫連接
      session.close()

# 刪除一筆商品
@back_product_ctrl.route('/delete_product', methods=['POST'])
def delete_product():
  from models.product import Product
  session = get_session_interface()
  try:
      # 從請求中獲取 JSON 格式的數據
      data = request.get_json()

      # 檢查必要欄位是否存在
      if 'product_id' not in data:
          return api_response(data=None,message='Missing required field: product_id',status_code=400)

      # 從資料庫中獲取指定商品
      product_id = data['product_id']
      product = session.query(Product).get(product_id)

      if (product is None):
        return api_response(data=None,message="刪除商品失敗，找不到該商品")

      # 刪除商品
      session.delete(product)
      session.commit()

      return api_response(data=True,message="刪除成功")

  except Exception as e:
      # 如果發生錯誤，回滾事務並返回錯誤信息
      session.rollback()
      return api_response(data=None,message=str(e),status_code=500)

  finally:
      # 關閉資料庫連接
      session.close()

# 上傳圖片 
@back_product_ctrl.route('/upload_image', methods=['POST'])
def upload_image():
    session = get_session_interface()
    try:
        file = request.files['file']

        # 檢查文件是否具有允許的擴展名（這是一個簡單的檢查，實際上你可能需要進一步的檢查和安全機制）
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return api_response(data=None,message="圖片格式錯誤",status_code=400)

        # 將文件保存到指定位置
        # 請根據實際需求指定保存的路徑

        # 生成隨機的5位數字
        random_number = ''.join(random.choices(string.digits, k=5))
        static_path = get_img_folder()
        # 將文件保存到指定位置，使用相對路徑
        filename = f'{random_number}_{file.filename}'
        file_path = os.path.join(static_path, filename)
        file.save(file_path)

        session.commit()

        # 取得當前服務器url並移除最後面的/
        server_domain = request.url_root.rstrip('/')
        # 產生動態取得圖片的API路徑
        relative_image_url = url_for('static',filename=filename)
        res = {
          'img_url': f'{server_domain}{relative_image_url}'
        }

        return api_response(data=res,message=True)

    except Exception as e:
        # 如果發生錯誤，回滾事務並返回錯誤信息
        session.rollback()
        return api_response(data=None,message=str(e),status_code=500)

    finally:
        # 關閉資料庫連接
        session.close()