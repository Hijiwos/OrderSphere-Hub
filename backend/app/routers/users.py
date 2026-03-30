from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.deps import get_db, get_current_user
import bcrypt

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=schemas.User)
def read_current_user(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.put("/me")
def update_current_user(
    update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    updated = False

    # 如果提供了 username，则尝试更新（并检查唯一性）
    if update.username is not None:
        new_name = update.username.strip()
        if not new_name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名不能为空")
        if new_name != current_user.username:
            exists = db.query(models.User).filter(models.User.username == new_name).first()
            if exists:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")
            current_user.username = new_name
            updated = True

    # 如果提供了 password，则执行修改密码流程
    if update.password is not None or update.confirm_password is not None or update.current_password is not None:
        # 必须同时提供 current_password, password, confirm_password（schemas 已校验 confirm）
        if not update.current_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="修改密码需提供当前密码")
        # 验证当前密码
        if not bcrypt.checkpw(update.current_password.encode(), current_user.password_hash.encode()):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="当前密码不正确")
        # 更新为新密码
        hashed = bcrypt.hashpw(update.password.encode(), bcrypt.gensalt()).decode()
        current_user.password_hash = hashed
        updated = True

    if updated:
        db.add(current_user)
        db.commit()
        db.refresh(current_user)
        return {"msg": "更新成功"}
    else:
        # 如果没有任何变更，返回 400 或可选择返回 200 并提示无变更；这里返回 400
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="没有提供可更新的字段")