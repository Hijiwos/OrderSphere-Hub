from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Body
from sqlalchemy.orm import Session
from app import models, schemas
from app.deps import get_db, get_current_user
import bcrypt
from pathlib import Path
import json

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=schemas.User)
def read_current_user(current_user: models.User = Depends(get_current_user)):
    """
    返回当前用户信息，确保 liked 字段为数组（从数据库的 JSON 字符串或兼容格式解析）
    """
    liked_raw = current_user.liked or ""
    try:
        liked_list = json.loads(liked_raw) if isinstance(liked_raw, str) and liked_raw.strip() else []
        # 强制转换为 int 列表（忽略无法转换的值）
        liked_list = [int(x) for x in liked_list if str(x) != ""]
    except Exception:
        # 兼容旧格式：逗号分隔字符串
        try:
            liked_list = [int(x) for x in (liked_raw or "").split(",") if x.strip()]
        except Exception:
            liked_list = []
    # 动态附加属性以供 pydantic 从 attributes 读取
    current_user.liked = liked_list
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


# 处理上传用户头像的接口：前端 POST /users/me/avatar (form field 'file')
@router.post("/me/avatar")
async def upload_current_user_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # 仅允许图片类型
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="只支持图片文件")

    # 计算保存路径，与 main.py 中挂载的 /user_images 对应
    BASE_DIR = Path(__file__).resolve().parent.parent.parent  # backend 根目录
    USER_IMAGE_DIR = BASE_DIR / "data" / "user_images"
    USER_IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"user_{current_user.id}.png"
    file_path = USER_IMAGE_DIR / filename

    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="保存图片失败")

    # 持久化 avatar 字段到数据库（保存为静态路径 /user_images/<filename>）
    avatar_path = f"/user_images/{filename}"
    current_user.avatar = avatar_path
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    # 返回静态文件 URL，前端可直接使用
    return {"url": avatar_path}


# 处理上传收藏的接口：前端 POST /users/me/liked
@router.post("/me/liked", response_model=schemas.User)
async def upload_current_user_liked(
    payload: dict = Body(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Accept payload either:
      { "liked": [1,2,3] }
    or { "liked_string": "[1,2]" }
    Normalize to JSON string of int list and persist to current_user.liked (text column).
    Return updated user with parsed liked list.
    """
    liked_string = None

    if isinstance(payload, dict):
        if 'liked' in payload:
            liked_val = payload.get('liked')
            if isinstance(liked_val, (list, tuple)):
                # keep integer conversion safe
                try:
                    normalized = [int(x) for x in liked_val]
                except Exception:
                    normalized = []
                liked_string = json.dumps(normalized)
        elif 'liked_string' in payload:
            liked_string = payload.get('liked_string')

    if liked_string is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="缺少 liked 或 liked_string 字段")

    # 尝试解析 liked_string 为 list<int> 并写入数据库为 JSON 字符串
    try:
        parsed = json.loads(liked_string) if isinstance(liked_string, str) and liked_string.strip() else []
        normalized = []
        for v in parsed:
            try:
                normalized.append(int(v))
            except Exception:
                continue
        current_user.liked = json.dumps(normalized)
    except Exception:
        # fallback: 尝试逗号分割
        try:
            arr = [int(x) for x in str(liked_string).split(',') if x.strip()]
            current_user.liked = json.dumps(arr)
        except Exception:
            current_user.liked = json.dumps([])

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    # 返回带解析 liked 数组的 user
    try:
        liked_list = json.loads(current_user.liked) if current_user.liked else []
    except Exception:
        liked_list = []
    current_user.liked = liked_list
    return current_user