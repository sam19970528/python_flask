from app import Base
from sqlalchemy import Column
from sqlalchemy import Integer, String, Text,Numeric

class Category(Base):
  __tablename__ = "category"
  id = Column(Integer, primary_key=True)
  name = Column(String(120), nullable=False)
  product_ids = Column(String(255), nullable=False)

  def __init__(self,name,product_ids):
    self.name = name
    self.product_ids = product_ids