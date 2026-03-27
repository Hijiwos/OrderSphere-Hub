from pydantic import BaseModel, field_validator
from typing import List, Optional


# -------------------------
# 用户相关
# -------------------------
class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    confirm_password: str

    @field_validator("confirm_password")
    def passwords_match(cls, v, info):
        password = info.data.get("password")
        if password and v != password:
            raise ValueError("两次输入的密码不一致")
        return v


class UserLogin(UserBase):
    password: str


class User(BaseModel):
    id: int
    username: str
    is_admin: bool

    class Config:
        from_attributes = True


# 新增：用户自行修改密码时的请求体
class UserUpdate(BaseModel):
    current_password: str
    password: str
    confirm_password: str

    @field_validator("confirm_password")
    def passwords_match(cls, v, info):
        password = info.data.get("password")
        if password and v != password:
            raise ValueError("两次输入的密码不一致")
        return v


# -------------------------
# 菜单相关
# -------------------------
class MenuItemBase(BaseModel):
    name: str
    price: int
    category: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    region: Optional[str] = None
    raw_key: Optional[str] = None
    image_url: Optional[str] = None


class MenuItem(MenuItemBase):
    id: int

    class Config:
        from_attributes = True


# -------------------------
# 订单相关
# -------------------------
class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int


class OrderCreate(BaseModel):
    customer_name: str
    items: List[OrderItemCreate]


class OrderItem(BaseModel):
    id: int
    menu_item_id: int
    quantity: int

    class Config:
        from_attributes = True


class Order(BaseModel):
    id: int
    customer_name: str
    items: List[OrderItem]

    class Config:
        from_attributes = True