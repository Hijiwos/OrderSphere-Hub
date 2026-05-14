# 3、4任务要求

## 目录

[4: 新页面开发实施指南（每人至少实现4个页面，从20个待添加页面选择）](#新页面开发实施指南)
- [待添加页面](#待添加页面)

[3: 绘图（时序图/类图）（两种图每人各画一张，从下方选择，完成后上传至/images，命名格式参考/images内的README）](#绘图时序图类图)
- [时序图（10个）](#时序图sequence-diagrams)
- [类图（9个）](#类图class-diagram-ideas)

## 新页面开发实施指南

下面说明如何在本项目中新增页面与接口，包含文件位置、目录约定、后端路由与鉴权、数据模型与迁移、以及推荐的开发流程。

1) 前端实现（前端，建议参考已有前端界面）
- 文件位置：在 frontend/src/views 或 frontend/src/pages 下创建新目录，每个页面使用 Vue 单文件组件（.vue）。
  - 示例：frontend/src/views/AdminDashboard.vue、frontend/src/views/MenuEditor/MenuEditor.vue
- 路由注册：在 frontend/src/router/index.js 中添加路由：
  - { path: '/admin/dashboard', name: 'AdminDashboard', component: () => import('@/views/AdminDashboard.vue') }
- API 封装：在 frontend/src/api 下新增模块（如 admin.js、orders.js）使用 Axios 封装调用后端接口。
- 状态管理：使用 Pinia 或 Vuex 在 src/stores 中新增模块（如 useAdminStore）缓存 KPI、报表等数据。
- 静态资源：页面图片放在 frontend/src/assets 或由后端托管到 backend/data/images。
- 实时功能：厨房看板与通知中心建议使用 WebSocket；在 frontend/src/utils/socket.js 封装连接逻辑。

2) 后端实现（后端，建议参考已有后端接口）
- 路由位置：在 backend/app/routers 下新增文件，如 admin_menu.py、admin_orders.py、kitchen.py。
  - 每个文件定义 APIRouter，示例：router = APIRouter(prefix='/admin/menu', tags=['admin-menu'])
- 模式与校验：在 backend/app/schemas 下新增 Pydantic schema（admin.py 等）定义请求/响应模型。
- 数据模型：在 backend/app/models 或 app/database 下新增 SQLAlchemy 模型（menu_item、promotion、inventory 等）。
- 数据库迁移：当前项目使用 Base.metadata.create_all；对于已有表新增列，使用类似 add_avatar_migration 的兼容检查或引入 Alembic 进行迁移（推荐）。
- 鉴权：管理接口统一前缀 /admin/*，通过依赖注入检查管理员权限（如 get_current_admin），可复用 app.routers.auth 的逻辑或实现简易 token 校验。
- 文件上传：保存到 backend/data/images 或 backend/data/user_images，并返回静态路径（/images/... 或 /user_images/...）。
- 导出/报表：返回 CSV 文件或生成并返回下载链接。

3) 接口设计要点
- 先定义 Pydantic 请求/响应 schema，示例：
  - POST /admin/menu -> body: MenuCreate(name:str, price:float, category:str, image:str)
  - GET /admin/reports -> query: slice=week&type=sales
- 统一响应格式：{ "code":0, "message":"ok", "data": {...} }
- 错误处理：使用 HTTPException 返回合理的 HTTP 状态码与错误信息。

4) 权限与安全
- 管理端必须鉴权，建议使用 JWT 或 token。登录后在前端 localStorage 保存 token，并在 Axios 请求头中设置 Authorization: Bearer <token>。
- 后端在依赖中校验 token 并确认用户为管理员角色。

5) 开发流程建议
- 将需求拆成 Issue：每页拆分为前端/后端/数据三张票。
- API 先行：先提交 schema 与路由 stub，前端可 mock 数据并开发界面。
- 本地联调：前端运行 npm run dev，后端运行 uvicorn app.main:app，两端联调接口。
- 测试：后端增加 pytest 测试，前端增加基本单元测试。

6) 示例：新增菜单编辑页的最小实现步骤
- 后端：
  - 新建 backend/app/routers/admin_menu.py，提供 GET /admin/menu 与 POST /admin/menu。
  - 在 backend/app/schemas/admin.py 添加 MenuCreate 与 MenuOut。
  - 在 backend/app/models/menu.py 添加 MenuItem 模型并运行 Base.metadata.create_all。
  - 在 backend/app/main.py 引入并 include_router(admin_menu.router)。
- 前端：
  - 新增 frontend/src/views/MenuEditor/MenuEditor.vue，展示列表并带创建对话框。
  - 在 frontend/src/api/admin.js 添加 getMenu() 与 createMenu(payload) 封装。
  - 在 frontend/src/router 注册路由 /admin/menu/editor。

7) 代码组织建议
- frontend:
  - src/views/ 页面级组件
  - src/components/ 可复用子组件（表格、表单、图片上传）
  - src/api/ 封装 HTTP 请求
  - src/stores/ 全局状态管理
- backend:
  - app/routers/ 按功能拆分的路由文件
  - app/schemas/ Pydantic 模型
  - app/models/ SQLAlchemy 模型
  - app/services/ 业务逻辑（可选）

---

### 待添加页面

1. 管理后台总览页 /admin/dashboard
- 用途：管理员一眼查看今日订单、收入、库存告警、在线用户数。
- 关键元素：KPI 卡片、最近订单表、流量/销售折线图、快速操作按钮。
- 后端接口：GET /admin/overview、GET /admin/stats?range=
- 优先级：高
2. 菜单可视化编辑器 /admin/menu/editor
- 用途：图形化增删改菜品、拖拽排序、上传图片。
- 关键元素：菜品列表树、编辑侧栏、图片上传预览。
- 后端接口：GET/POST/PUT/DELETE /admin/menu、POST /admin/menu/upload-image
- 优先级：高
3. 分类管理页 /admin/menu/categories
- 用途：添加/合并/排序菜单分类（如主食、饮料）。
- 关键元素：分类表、排序拖拽、批量启用/禁用。
- 后端接口：CRUD /admin/categories
- 优先级：中
4. 批量导入/导出页 /admin/import
- 用途：JSON/CSV 菜单、用户、订单批量导入与导出。
- 关键元素：文件上传、字段映射、导入预览、导入日志。
- 后端接口：POST /admin/import (type=menu|users|orders)、GET /admin/import/logs
- 优先级：中
5. 促销/优惠券管理 /admin/promotions
- 用途：创建折扣规则、优惠券、满减、限时活动。
- 关键元素：规则编辑器、有效期设置、使用统计。
- 后端接口：CRUD /admin/promotions、POST /admin/promotions/apply-preview
- 优先级：中
6. 订单详情与处理页 /admin/orders/{order_no}
- 用途：查看订单详情、修改状态、打印、备注。
- 关键元素：订单时间线、菜品明细、状态切换按钮、内部备注。
- 后端接口：GET/PUT /admin/orders/{order_no}、POST /admin/orders/{order_no}/note
- 优先级：高
7. 厨房/后厨实时看板（Kitchen Display） /kitchen
- 用途：后厨展示待做/制作中/完成订单，支持标记完成与计时。
- 关键元素：分区队列、烹饪计时器、筛选（窗口/优先级）。
- 后端接口：GET /kitchen/orders, PUT /kitchen/orders/{order_no}/status
- 优先级：高
8. 顾客档案页 /admin/customers/{user_id}
- 用途：查看用户历史订单、头像、备注、积分。
- 关键元素：个人信息、订单历史、积分调整。
- 后端接口：GET /admin/users/{user_id}、PUT /admin/users/{user_id}
- 优先级：中
9. 评价与评论管理 /admin/reviews
- 用途：审核/回复/置顶用户评价、统计评分分布。
- 关键元素：评论列表、审核按钮、回复输入框、评分分布图。
- 后端接口：GET /admin/reviews、PUT /admin/reviews/{id}/status、POST /admin/reviews/{id}/reply
- 优先级：中
10. 预约/预订管理页 /reservations
- 用途：顾客在线预约座位（新功能）与管理员管理预约。
- 关键元素：日历视图、可用时段、预约表单、确认/取消。
- 后端接口：POST/GET/PUT/DELETE /reservations
- 优先级：中
11. 收藏/愿望单页面 /user/favorites
- 用途：用户收藏菜品，便于快速下单。
- 关键元素：收藏格子、批量添加到购物车、移除。
- 后端接口：GET/POST/DELETE /users/{id}/favorites
- 优先级：低
12. 注销/订单重做（Reorder）页面 /orders/reorder/{order_no}
- 用途：基于历史订单一键加入购物车并修改下单。
- 关键元素：历史菜品复选、数量调整、立即下单按钮。
- 后端接口：GET /orders/{order_no}, POST /cart/from-order
- 优先级：中
13. 通知中心 /notifications
- 用途：用户/管理员查看系统通知（订单变更、促销）。
- 关键元素：未读标识、筛选、清空/标记为已读。
- 后端接口：GET/POST/PUT /notifications, WebSocket 推送
- 优先级：中
14. 活动页面（Landing）/promo/{id}
- 用途：独立前端活动页，用于推广活动或节日套餐。
- 关键元素：Banner、活动菜品快速下单、倒计时。
- 后端接口：GET /promotions/{id}, GET /promotions/{id}/items
- 优先级：低
15. 报表/分析页 /admin/reports
- 用途：多维度报表（销售、菜品排名、时段分析、客单价）。
- 关键元素：导出 CSV/PDF、图表与表格切换、时间粒度选择。
- 后端接口：GET /admin/reports?slice=day|week|month&type=sales|items
- 优先级：高
16. 库存管理/原料页 /admin/inventory
- 用途：跟踪原料库存，自动报警、关联菜品配方（可选）。
- 关键元素：库存表、阈值设置、入库出库记录。
- 后端接口：CRUD /admin/inventory, GET /admin/inventory/alerts
- 优先级：中
17. 用户设置与资料页 /user/profile
- 用途：用户修改昵称、头像、通知偏好、地址簿。
- 关键元素：头像上传、地址管理、密码修改。
- 后端接口：GET/PUT /users/{id}, POST /users/{id}/avatar
- 优先级：高
18. 审计日志与操作历史 /admin/audit
- 用途：记录管理员操作（修改菜单、订单改动），便于追溯。
- 关键元素：时间轴、过滤器（用户/操作/时间）、导出。
- 后端接口：GET /admin/audit?user=&action=&since=
- 优先级：低
19. 帮助/常见问题页 /help
- 用途：展示使用手册、常见问题与联系方式。
- 关键元素：搜索、分类 FAQ、提交工单表单。
- 后端接口：GET /help/faqs, POST /help/ticket
- 优先级：低
20. 运营配置页 /admin/settings
- 用途：站点级配置（营业时间、税率、送餐费、默认语言）。
- 关键元素：表单保存、配置回滚、导入导出配置。
- 后端接口：GET/PUT /admin/settings
- 优先级：中

---

## 绘图（时序图/类图）


**注意：以下图表说明中包含并未实现的页面，确认所有页面和功能全部存在后在开始画图**

### 时序图（Sequence diagrams）

1. [已选]用户下单（完整链路）
- 参与者：User UI → 前端 API 层 → 后端 Orders Router → OrderService → DB → Kitchen Dispatcher → Notification Service → 前端/WebSocket → User UI
- 关键步骤：购物车提交 → 创建订单记录 → 减库存/校验 → 推送厨房看板 → 返回订单确认 → 实时通知用户。
2. 后厨接单并完成（Kitchen 执行流程）
- 参与者：Kitchen UI（Web/Tablet）→ Kitchen WS Server → 后端 Orders Router → OrderService → DB → Notification Service → 用户前端
- 关键步骤：接收新单（WS）→ 标记“制作中”→ 标记“完成”→ 更新订单状态并通知用户/打印出票据。
3. [已选]图片（菜品/头像）上传与静态托管
- 参与者：User/Admin UI → 前端上传组件 → 后端 Upload API → 文件存储（backend/data/...）→ 返回静态 URL → 前端请求静态 URL（/images 或 /user_images）
- 关键步骤：文件接收 → 保存到后端目录 → 生成并返回访问路径 → 浏览器请求并由 StaticFiles 返回。
4. 导入菜单（CSV/JSON）流程
- 参与者：Admin UI → 前端 → 后端 Import API → Import Worker/Service → DB → Import Log Store → 前端 Poll/WS 获取导入结果
- 关键步骤：上传文件 → 后端异步解析/校验 → 写入 menu_items → 记录导入日志/错误 → 前端显示导入结果。
5. 促销/优惠券发布与前端生效
- 参与者：Admin UI → 后端 Promotions API → DB → Cache/Config → 前端请求菜单/促销 → 前端渲染带优惠的价格/规则
- 关键步骤：创建促销 → 更新生效配置/缓存 → 前端刷新或通过 WS 收到促销变更 → 显示折扣价格。
6. 用户头像迁移/兼容列追加（DB 迁移兼容流程）
- 参与者：Backend startup → Migration helper (ensure_avatar_column) → DB → 后端 App 初始化
- 关键步骤：应用启动调用迁移脚本 → 若缺列则 ALTER TABLE（或复制） → 继续 create_all 与服务启动。
7. 报表生成与导出（大数据量）
- 参与者：Admin UI → 后端 Reports API → Report Worker（异步）→ DB/聚合 → 存储临时 CSV → 后端回应下载 URL → 前端触发下载
- 关键步骤：触发生成 → 后端异步聚合/导出 → 生成文件并返回链接 → 前端下载/通知。
8. 预约（Reservations）流程（含确认）
- 参与者：User UI → 前端 → 后端 Reservations API → DB → Admin 确认流程（可选）→ 通知用户确认/取消
- 关键步骤：用户提交预约 → 后端检查可用时段 → 写入 DB → 管理员确认 → 发送确认通知。
9. 历史订单重做（Reorder）与库存校验
- 参与者：User UI → 前端 → 后端 Orders/Cart API → DB → InventoryService → 返回可下单/警告 → 创建新订单
- 关键步骤：拿历史订单条目 → 校验库存/价格变动 → 生成新购物车并下单。
10. 实时通知推送链（订单状态变更）
- 参与者：OrderService → Notification Service → Push Channel（WebSocket/FCM/Email）→ User Client
- 关键步骤：订单状态变化触发事件 → 通知服务选择渠道并发送 → 客户端接收并显示。

### 类图（Class diagram ideas）

1. 订单域（Order-centric）
- 类：Order, OrderItem, MenuItem, User, PaymentInfo, OrderStatus
- 关系：Order 1─* OrderItem；OrderItem → MenuItem；Order → User；Order 包含 PaymentInfo。
2. 菜单域（Menu-centric）
- 类：MenuItem, Category, MenuImage, Tag, Nutrition
- 关系：Category 1─* MenuItem；MenuItem 1─* MenuImage；MenuItem 可有多个 Tag。
3. [已选]用户与认证（User/Auth）
- 类：User, Role, Session/Token, AvatarImage, Address
- 关系：User ── Role（多对多或一对多）；User 1─* Address；User 一对一 AvatarImage；Token 关联 User。
4. 管理/审计（Admin/Audit）
- 类：AdminUser, AuditLog, ActionType, TargetResource
- 关系：AuditLog 包含 AdminUser、ActionType 和 TargetResource 引用（Order/MenuItem/...）。
5. 库存与原料（Inventory）
- 类：InventoryItem (原料), SKU, Supplier, InventoryTransaction
- 关系：MenuItem -*-> InventoryItem（菜品配方引用多个原料）；InventoryTransaction 记录出入库，关联 InventoryItem。
6. 促销与规则（Promotion）
- 类：Promotion, Coupon, PromotionRule, EligibilityCriteria
- 关系：Promotion 关联多个 MenuItem 或 Category；Coupon 与 User 关联；PromotionRule 定义折扣逻辑。
7. 通知/实时（Notification & WS）
- 类：Notification, NotificationChannel, WebSocketConnection, PushSubscription
- 关系：Notification 关联 User/Order；WebSocketConnection 记录客户端会话；NotificationChannel 定义发送方式。
8. 报表与导出（Reporting）
- 类：ReportRequest, ReportJob, ReportResult, AggregationMetric
- 关系：ReportRequest 触发 ReportJob；ReportJob 生成 ReportResult（CSV/JSON）；AggregationMetric 定义聚合规范。
补充方向（可选，若需更多） 9. 评价与反馈（Review）
- 类：Review, ReviewImage, ModeratorNote
- 关系：Review 关联 User 与 MenuItem；ModeratorNote 关联 Review。
9. 预约/座位（Reservations）
- 类：Reservation, Table, Timeslot, ReservationPolicy
- 关系：Table 1─* Reservation；Reservation 绑定 Timeslot 与 User。
