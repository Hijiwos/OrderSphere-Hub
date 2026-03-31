from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import Base, engine
from app.routers import menu, orders, health, auth, admin_menu, admin_orders, admin_users, users
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os

# 在启动时确保 avatar 列存在（已有的迁移脚本）
from app.utils.add_avatar_migration import ensure_avatar_column

dist_path = os.path.join(os.path.dirname(__file__), "..", "dist")

BASE_DIR = Path(__file__).resolve().parent.parent

# 菜单图片目录（保留原来位置）
MENU_IMAGE_DIR = BASE_DIR / "data" / "images"
MENU_IMAGE_DIR.mkdir(parents=True, exist_ok=True)

# 用户头像单独目录，避免与菜单图片混淆
USER_IMAGE_DIR = BASE_DIR / "data" / "user_images"
USER_IMAGE_DIR.mkdir(parents=True, exist_ok=True)

# SQLite DB 文件路径（与 settings.database_url 对应）
DB_PATH = BASE_DIR.parent / "db" / "ordersphere.db"

# 在创建表或使用之前，确保数据库中 users 表包含 avatar 列（如果表已存在但缺列）
try:
    ensure_avatar_column(DB_PATH)
except Exception:
    # 忽略迁移错误，让后续 create_all 或运行时能继续（函数内部已记录日志）
    pass

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(menu.router)
app.include_router(orders.router)
app.include_router(auth.router)
app.include_router(admin_menu.router)
app.include_router(admin_orders.router)
app.include_router(admin_users.router)
app.include_router(users.router)

# 挂载两个静态目录：
# - /images -> 菜单图片（原有）
# - /user_images -> 用户头像（单独目录，避免混淆）
app.mount("/images", StaticFiles(directory=MENU_IMAGE_DIR), name="images")
app.mount("/user_images", StaticFiles(directory=USER_IMAGE_DIR), name="user_images")
# app.mount("/", StaticFiles(directory=dist_path, html=True), name="static")
