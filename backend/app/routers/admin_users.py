from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.deps import get_db, get_admin_user

router = APIRouter(prefix="/admin/users", tags=["admin-users"])


class UserSimple(schemas.User):
    pass


@router.get("/", response_model=List[schemas.User])
def get_all_users(db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    users = db.query(models.User).all()
    out = []
    for u in users:
        liked_raw = getattr(u, 'liked', None)
        parsed = []
        try:
            if isinstance(liked_raw, str) and liked_raw.strip():
                parsed = json.loads(liked_raw)
                if not isinstance(parsed, list):
                    parsed = []
            else:
                parsed = []
        except Exception:
            try:
                parsed = [int(x) for x in str(liked_raw).split(',') if x.strip()]
            except Exception:
                parsed = []
        u.liked = parsed
        out.append(u)
    return out


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    db.delete(user)
    db.commit()
    return {"msg": "删除成功"}


@router.post("/{user_id}/make_admin")
def make_admin(user_id: int, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    user.is_admin = True
    db.commit()
    return {"msg": "已设为管理员"}


@router.post("/{user_id}/cancel_admin")
def cancel_admin(user_id: int, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if user.username == "admin":
        raise HTTPException(status_code=404, detail="该用户不可降级！")

    user.is_admin = False
    db.commit()
    return {"msg": "已取消管理员资格"}
