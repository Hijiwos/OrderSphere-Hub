# OrderSphere?Hub 需求规格说明书 (SRS.md)

版本：1.0
日期：2026-04-29
作者：黄嘉玮

## 1. 引言
本文档为 OrderSphere?Hub 在线点餐系统的软件需求规格说明（SRS），面向产品经理、开发、测试与运维人员。包含系统功能需求、非功能需求、外部接口、数据与发布/构建规范（含前端构建与后端打包为可执行文件并生成 release 的流程）。

## 2. 项目概述
OrderSphere?Hub 是一款基于 Python (FastAPI) + Vue3 (Vite) + SQLite 的轻量单餐厅在线点餐系统。
核心能力：菜单展示（JSON 导入）、购物车、订单创建/查询、管理员接口、图片与头像静态托管、支持一键生成生产 release（前端构建 + 后端 PyInstaller 打包）。

目标：提供一个开箱可用的点餐服务端与前端，能将前端构建产物与后端可执行文件放在同一 release 目录，解压后双击 exe 即可运行服务并托管前端静态页面。

约束：采用 SQLite，适用于单店、并发量较低场景；默认管理员账号需上线前更改。

## 3. 术语
- API：应用编程接口
- 前端构建：在 frontend 目录执行 `npm run build` 生成 dist
- 后端打包：使用 PyInstaller 将 backend 打包为单文件可执行程序
- release 包：包含 exe、dist、data、db 的压缩产物

## 4. 参与者与用户角色
- 普通用户（顾客）：浏览菜单、加入购物车、下单、查询个人订单
- 管理员：管理菜单、查询全部订单、维护数据（通过管理接口）
- 运维/开发：构建、发布、部署、生成 release

## 5. 功能需求
以下需求均以可验证、可实现为准。

5.1 菜单管理
- FR-M1：支持从 backend/data/foodMsg.json 导入菜单数据（命令行或后台接口）。
- FR-M2：提供菜单查询接口，支持按类别、关键词检索与单品详情。

5.2 购物车与下单
- FR-C1：支持前端维护购物车（前端状态）并发送创建订单请求到后端。
- FR-C2：后端创建订单并生成唯一订单号、存储菜品明细、总价、状态与时间戳。
- FR-C3：提供查询个人订单与管理员查询所有订单接口。

5.3 用户与头像
- FR-U1：用户可上传头像，保存到 backend/data/user_images 并通过 /user_images 静态路径访问。
- FR-U2：启动时检查 users 表是否包含 avatar 列，如缺失执行迁移（已实现辅助脚本）。

5.4 静态资源
- FR-S1：后端必须挂载 /images（菜品图片）与 /user_images（头像）。
- FR-S2：当 backend/dist 存在或打包时在运行时提供根静态站点（托管前端 dist）。

5.5 构建与发布（重点自动化需求）
- FR-B1（最重要）：提供一键脚本（scripts/build_release.py）或等价流程，完成：
  - 在 frontend 执行前端构建（npm run build）生成 dist
  - 将 frontend/dist 拷贝到 backend/dist
  - 使用 PyInstaller 将 backend/run_server.py 打包成单文件可执行（Windows: exe）
  - 将可执行文件与 dist、data、db 放入单独 release 文件夹并生成 zip
  - 可选：上传 zip 到 GitHub Release（使用 GITHUB_TOKEN）
- FR-B2：可在本地或 CI（GitHub Actions）上运行，支持在 windows-latest 上生成 Windows exe。

## 6. 非功能需求
6.1 性能
- NF-P1：在 SQLite 场景下，常规查询（按 id/类别）响应时间 < 200ms（本地网络条件）。
- NF-P2：建议并发用户不超过 50（单文件 SQLite 限制）。

6.2 可用性与部署
- NF-A1：提供 README 中的开发部署步骤与一键构建脚本说明。
- NF-A2：release 解压后应能通过双击 exe 启动服务并托管前端静态页面。

6.3 安全
- NF-S1：默认管理员密码不得在生产环境使用，部署时提示更换。
- NF-S2：API 对管理接口应做简单鉴权（如 token 或 Basic），敏感信息不应写入公共日志。

6.4 可维护性
- NF-M1：代码遵循 PEP8 风格，API 使用 REST 风格，文档齐全。

## 7. 接口规范（概要）
列出关键后端 API（示例，具体以代码实现为准）：
- GET /health -> 健康检查
- GET /menu/ -> 列表
- GET /menu/{id} -> 菜品详情
- POST /orders -> 创建订单（payload: items[]、user info）
- GET /orders/{order_no} -> 查询订单
- POST /auth/login -> 管理员登录（返回 token）
- POST /upload/avatar -> 上传头像

返回格式：标准 JSON，包含 code、message、data 字段（或遵循当前实现）。

## 8. 数据模型（概要）
- users(id, username, password_hash, avatar, role, created_at)
- menu_items(id, name, category, price, description, image)
- orders(id, order_no, user_id or guest_info, items(JSON), total, status, created_at)

## 9. 构建与发布详细说明（开发/运维手册节选）
9.1 前端构建（本地）
- 进入 frontend
- 安装依赖：`npm ci` 或 `npm install`（若 lockfile 不一致请使用 npm install 并提交更新后的 package-lock.json）
- 构建：`npm run build` -> 生成 frontend/dist

9.2 后端打包（本地，Windows 示例）
- 确保已安装 Python 与 pip
- 在 backend 目录准备运行入口：`backend/run_server.py`（入口脚本引用 app.main: app 并用 uvicorn.run）
- 使用 PyInstaller：例如
  - `pyinstaller --onefile --name OrderSphereHub backend/run_server.py --add-data "backend/dist;dist" --add-data "backend/data;data" --add-data "db/ordersphere.db;db"`
- PyInstaller 生成的可执行文件与资源打包到 release 目录（脚本会自动收集并生成 zip）

9.3 推荐 CI（GitHub Actions）流程
- 在 windows-latest runner 上：checkout -> setup Node -> npm ci & npm run build -> copy frontend/dist to backend/dist -> setup Python -> run scripts/build_release.py --tag ${{ github.ref_name }} -> upload artifact / create GitHub Release

9.4 release 产物说明
- release.zip 解压后包含：
  - OrderSphereHub.exe (或 OrderSphereHub 可执行文件)
  - dist/ (前端静态文件)
  - data/ (菜品图片、user_images 等)
  - db/ordersphere.db
  - README.txt（如何运行说明）

运行方法：双击可执行文件或在命令行运行，服务默认监听 0.0.0.0:8000，访问 http://localhost:8000 即可看到前端页面。

## 10. 验收标准（Acceptance Criteria）
- A1：运行 scripts/build_release.py（或 CI）成功生成 release zip（无错误），解压后双击 exe 能启动服务并加载前端页面。
- A2：用户能在前端浏览菜单并完成下单流程；管理员能查看全部订单。
- A3：后端启动后 /images 与 /user_images 静态资源路径能正确返回图片。

## 11. 种子数据与示例
建议在 backend/data/foodMsg.json 中准备 20 条菜品示例，backend/data/user_images 放入 3 个示例头像，db/ordersphere.db 可包含 5 条示例订单与 3 个用户（含 admin）。

## 12. 风险与缓解
- SQLite 并发与文件锁：避免高并发写入场景，必要时迁移到 Postgres
- 前端依赖冲突（lockfile 与 package.json 不一致）：在构建前运行 npm install 并提交 lockfile
- PyInstaller 打包时资源包含与路径问题：在 run_server.py 中处理 sys._MEIPASS 以支持打包后访问静态目录

## 13. 后续可选扩展
- 支持第三方支付集成
- 支持多门店与更复杂的权限系统
- 将后端迁移到 RDBMS（Postgres）以支持高并发

## 14. 联系方式
项目维护者：见仓库 CONTRIBUTORS 或 README
