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
    avatar: Optional[str] = None

    class Config:
        from_attributes = True


# 修改：用户更新请求体，所有字段可选
class UserUpdate(BaseModel):
    username: Optional[str] = None
    current_password: Optional[str] = None
    password: Optional[str] = None
    confirm_password: Optional[str] = None

    @field_validator("confirm_password")
    def passwords_match(cls, v, info):
        password = info.data.get("password")
        # 只有在提供密码或确认密码时才校验
        if password is not None or v is not None:
            if password is None or v is None:
                raise ValueError("修改密码时需要提供新密码与确认密码")
            if v != password:
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