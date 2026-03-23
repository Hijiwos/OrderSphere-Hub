# OrderSphere-Hub  
### 在线餐厅点餐系统（Python + FastAPI + Vue3 + SQLite）

OrderSphere-Hub 是一个基于 **FastAPI（Python）+ Vue3（Vite）+ SQLite** 的全栈在线点餐系统。  
项目支持：

- 菜单展示（从 JSON 自动导入）
- 购物车
- 订单创建与查询
- 管理端扩展接口
- 一键启动（开发环境）
- 生产环境可由 FastAPI 托管前端静态文件

---

# 📁 项目结构

```
OrderSphere-Hub/
├─ backend/                 # FastAPI 后端
│  ├─ app/
│  ├─ data/
│  │  └─ foodMsg.json       # 菜单 JSON
│  ├─ requirements.txt
│  └─ venv/                 # 本地虚拟环境
│
├─ frontend/                # Vue3 前端
│  ├─ src/
│  ├─ dist/                 # 构建产物
│  └─ node_modules/         # 依赖
│
├─ db/
│  └─ ordersphere.db        # SQLite 数据库（自动生成）
│
├─ scripts/
│  └─ dev_run.py            # ⭐ 一键启动脚本（开发环境）
│
├─ .gitignore
└─ README.md
```

---

# 🛠 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue3 + Vite + Axios + Vue Router |
| 后端 | FastAPI + SQLAlchemy + Pydantic |
| 数据库 | SQLite |
| 工具 | Python 一键启动脚本 |

---

# 🚀 快速开始（开发环境）

## 1. 克隆项目

```bash
git clone https://github.com/你的仓库/OrderSphere-Hub.git
cd OrderSphere-Hub
```

---

# 🐍 后端部署

## 2. 创建虚拟环境并安装依赖

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
# 或 source venv/bin/activate（Linux/macOS）

pip install -r requirements.txt
```

## 3. 初始化数据库并导入菜单

菜单 JSON 文件路径为：

```
backend/data/foodMsg.json
```

运行导入脚本：

```bash
python -m app.utils.import_menu
```

成功后会生成：

```
db/ordersphere.db
```

## 4. 启动后端

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问：

- Swagger 文档： `http://127.0.0.1:8000/docs`
- 菜单接口： `http://127.0.0.1:8000/menu/`

---

# 🌐 前端部署

## 5. 安装依赖

```bash
cd ../frontend
npm install
```

## 6. 启动前端

```bash
npm run dev
```

访问：

- `http://127.0.0.1:5173/`

---

# ⭐ 一键启动（推荐）

项目提供 Python 一键启动脚本，可同时启动：

- 后端（FastAPI）
- 前端（Vite）

## 7. 运行一键启动脚本

```bash
cd scripts
python dev_run.py
```

启动后你会看到：

```
后端: http://127.0.0.1:8000
前端: http://127.0.0.1:5173
按 Ctrl+C 结束所有进程。
```

---

# 📦 生产部署（FastAPI 托管前端）

## 1. 构建前端

```bash
cd frontend
npm run build
```

生成：

```
frontend/dist/
```

## 2. 后端挂载静态文件（已在 main.py 中配置）

```python
from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")
```

## 3. 启动后端即可访问前端

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

访问：

- `http://127.0.0.1:8000`

---

# ❗ 常见问题（FAQ）

## 1. Vite 提示：

```
Could not auto-determine entry point ... Skipping dependency pre-bundling.
```

这是 **Vite 的正常提示**，不会影响开发或构建，可以忽略。

---

## 2. 后端日志出现：

```
GET /hybridaction/zybTrackerStatisticsAction ... 404
```

这是浏览器插件（如某些统计脚本）自动发出的请求，  
**不是你的项目问题**，可以忽略。

---

# 📄 许可证

无
