from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.deps import get_db
from app.auth import create_access_token
from app.config import settings
import bcrypt

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    exists = db.query(models.User).filter(models.User.username == user.username).first()
    if exists:
        raise HTTPException(status_code=400, detail="用户名已存在")

    hashed = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()

    new_user = models.User(
        username=user.username,
        password_hash=hashed,
        is_admin=False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "注册成功"}


@router.post("/register_admin")
def register_admin(user: schemas.UserCreate, secret: str, db: Session = Depends(get_db)):
    # 简单的管理员注册保护：需要提供一个预共享密钥
    if secret != settings.admin_secret:
        raise HTTPException(status_code=403, detail="管理员密钥错误")

    exists = db.query(models.User).filter(models.User.username == user.username).first()
    if exists:
        raise HTTPException(status_code=400, detail="用户名已存在")

    hashed = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()

    new_user = models.User(
        username=user.username,
        password_hash=hashed,
        is_admin=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "管理员注册成功"}


@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="用户名或密码错误")

    if not bcrypt.checkpw(user.password.encode(), db_user.password_hash.encode()):
        raise HTTPException(status_code=400, detail="用户名或密码错误")

    # 将 avatar 一并放入 token payload（可选），并在响应中返回 avatar 字段
    payload = {
        "sub": db_user.username,
        "is_admin": db_user.is_admin,
        "avatar": db_user.avatar
    }
    token = create_access_token(payload)

    return {
        "access_token": token,
        "is_admin": db_user.is_admin,
        "username": db_user.username,
        "avatar": db_user.avatar
    }