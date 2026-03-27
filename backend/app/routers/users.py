from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.deps import get_db, get_current_user
import bcrypt

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=schemas.User)
def read_current_user(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.put("/me")
def update_current_user(update: schemas.UserUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # 验证当前密码
    if not bcrypt.checkpw(update.current_password.encode(), current_user.password_hash.encode()):
        raise HTTPException(status_code=400, detail="当前密码不正确")

    # 更新为新密码
    hashed = bcrypt.hashpw(update.password.encode(), bcrypt.gensalt()).decode()
    current_user.password_hash = hashed
    db.add(current_user)
    db.commit()
    return {"msg": "密码更新成功"}
