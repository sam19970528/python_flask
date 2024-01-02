from app import Base
from sqlalchemy import Column
from sqlalchemy import Integer, String, Text,Numeric

class Product(Base):
  __tablename__ = "product"
  product_id = Column(Integer, primary_key=True, autoincrement=True)
  product_name = Column(String(255))
  stock = Column(Integer)
  price = Column(Numeric(10, 2))
  description = Column(Text)
  product_img = Column(String(255))

  def __init__(self,product_name,stock,price,description,product_img):
    self.product_name = product_name
    self.stock = stock
    self.price = price
    self.description = description
    self.product_img = product_img

def format_product(product):
  res = {
    'product_id': product.product_id,
    'product_name': product.product_name,
    'stock': product.stock,
    'price': float(product.price),  # 轉換 Decimal 為浮點數
    'description': product.description,
    'product_img': product.product_img
  }
  return res