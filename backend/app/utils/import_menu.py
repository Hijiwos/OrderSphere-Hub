import json
from pathlib import Path
from sqlalchemy.orm import Session
from app.models import MenuItem, Base, User
from app.database import SessionLocal, engine
import bcrypt

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_FILE = BASE_DIR / "data" / "foodMsg.json"
IMAGE_DIR = BASE_DIR / "data" / "images"

# 确保项目根目录下的 db 文件夹存在，避免首次运行导入脚本时报错
DB_DIR = BASE_DIR.parent / "db"
DB_DIR.mkdir(parents=True, exist_ok=True)

# 自动创建所有表
Base.metadata.create_all(bind=engine)


def normalize(value):
    """把 list 转成字符串，把 None 转成空字符串"""
    if isinstance(value, list):
        return "、".join(value)
    if value is None:
        return ""
    return str(value)


def create_default_admin(db: Session):
    """如果不存在 admin 用户，则创建 admin/admin123 管理员账号"""
    exists = db.query(User).filter(User.username == "admin").first()
    if exists:
        return

    hashed = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
    admin = User(username="admin", password_hash=hashed, is_admin=True)
    db.add(admin)
    db.commit()
    print("已创建默认管理员: admin / admin123")


def import_menu_from_json(db: Session):
    # 在导入菜单前尝试创建默认管理员（如果不存在）
    create_default_admin(db)

    if not DATA_FILE.exists():
        print("foodMsg.json 文件不存在...")
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    for raw_key, item in data.items():
        exists = db.query(MenuItem).filter(MenuItem.raw_key == raw_key).first()
        if exists:
            continue

        name = normalize(item.get("name", raw_key))
        price = int(item.get("price", 0))
        category = normalize(item.get("category"))
        type_ = normalize(item.get("type"))
        description = normalize(item.get("description"))
        region = normalize(item.get("region"))

        image_path = IMAGE_DIR / f"{raw_key}.png"
        image_url = f"/images/{raw_key}.png" if image_path.exists() else None

        menu_item = MenuItem(
            raw_key=raw_key,
            name=name,
            price=price,
            category=category,
            type=type_,
            description=description,
            region=region,
            image_url=image_url
        )

        db.add(menu_item)

    db.commit()
    print("菜单导入完成...")


if __name__ == "__main__":
    db = SessionLocal()
    import_menu_from_json(db)
    db.close()