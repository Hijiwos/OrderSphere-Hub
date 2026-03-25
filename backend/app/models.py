from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


# -------------------------
# 用户表
# -------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)

    orders = relationship("Order", back_populates="user")


# -------------------------
# 菜单表
# -------------------------
class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    category = Column(String(255), nullable=True)
    type = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    region = Column(String(255), nullable=True)
    raw_key = Column(String(255), nullable=True)

    # 图片 URL
    image_url = Column(String(255), nullable=True)

    # 订单项反向关系
    order_items = relationship("OrderItem", back_populates="menu_item")


# -------------------------
# 订单表
# -------------------------
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


# -------------------------
# 订单项表
# -------------------------
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem", back_populates="order_items")
