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
- 默认管理员账户 username: admin, password: admin123

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

## 2. 启动后端即可访问前端

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

---

# 文档格式约定

用户文档为 [USER_GUIDE](https://github.com/Hijiwos/OrderSphere-Hub/blob/main/USER_GUIDE.md) ，请确保不要新建其他的markdown文件

推荐使用 [Visual Studio Code](https://code.visualstudio.com/Download) 作为本文档的编辑器，并安装 `.vscode/extensions.json` 中推荐的拓展以获得最佳编辑体验。

## 标题格式

- 每个标题均由简短的几个字组成，向用户说明下一节内容的大致格式
- 除首个大标题外，所有标题均应使用合理数量的`#`来指定合理的标题级别

## 用语约定

| 对象                   | 用语                                                          |
|----------------------|-------------------------------------------------------------|
| 文档阅读者                | `您`                                                         |
| 本平台                  | `OrderSphere-Hub`                                           |
| 计算机知识丰富的 Geek / 专业用户 | `高级用户`                                                      |
| 用于演示的用户名称            | `ExampleUser1`、`ExampleUser2`、`SampleUser1`、`SampleUser2` 等 |
| 用于演示的料理 ID 和名称       | `#233 一个神奇的料理`、`#5 Demo Food`                               |

如果您发明了一个新名词，请注意在不同地方使用时保持其一致性。

## 符号约定

- 用 `空格` 而不是 `Tab` 进行缩进
- 用 `\n` 进行换行，文件内通常不应出现 `\r`
- 空行不能包含空白字符，应该为单纯的 `\n\n`
- 在没有特殊说明的地方均使用半角符号，如: `:`，`.`，`<`，`>`，`(`，`)`。通常这些符号后面需要加上一个空格来确保间距合理
- 在文字段落中均采用 `，` 逗号，每句话结尾需添加 `。` 句号
- 列表条目、使用特定的代码框 等提示容器中的文本通常不以 `。` 结尾

## 文件结构

- 将所有图片放置于根目录 `images` 文件夹中，并使用 `![](images/_photos/foo-bar.png)` 的引用形式

## 设计元素

本文档支持引入图片，采用 `![](./_photos/example.png)` 的形式。


## 文本间距

在正常文本和半角标点之间应添加空格，半角标点和全角标点之间无需空格:

```markdown
文本文本 `修饰块` 文本文本 **修饰块** 文本
       ^ 空格   ^ 空格   ^ 空格     ^ 空格

文本文本 `修饰块`，文本文本 (文本文本) 文本
       ^ 空格            ^ 空格     ^ 空格

文本文本。`修饰块`、文本文本
         ^ 半角、全角标点之间无需空格
```

## 文本修饰

**请注意遵守下方粗体或斜体的修饰字符规则**

使用 `*` 添加粗体、斜体效果:

```markdown
*斜体*

**粗体**

***粗斜体***
```

## 链接格式

- 在链接到文档内部元素时，请使用 `/` 开头的绝对路径链接，并确保链接中包含了文件扩展名 `.md`  
  例：`![prprrpr](/pa47.md)`
- 在链接到外部站点时，请清理链接中不必要的追踪参数  
  正确示例：`![这是好的](https://www.bilibili.com/video/BV1va411w7aM/)`  
  错误示例：`![这很不好](https://www.bilibili.com/video/BV1va411w7aM/?share_source=xxx&yyy=zzz)`

## 无序列表

使用 `-` 作为列表标记，标记后添加一个空格:

```markdown
- ItemA
- ItemB
```

## 有序列表

使用 `1.` 作为列表标记，也可以按个人喜好用 `1.`、`2.`、`3.` 等进行标记，只要保持整个文件一致即可。

标记后添加一个空格与内容分开:

```markdown
1. ItemA
1. ItemB
1. ItemC
```

## 折叠区域/表格

在 Markdown 中，可以使用 ```<details>``` 和 ```<summary>``` 标签来创建可折叠的区域，常用于隐藏一些不必要立即展示的详细内容，比如表格、代码块、大段文字等，以节省页面空间，让文档结构更加清晰。

```<summary>``` 标签用于定义折叠区域的标题，也就是用户点击展开或折叠时看到的提示文字；```<details>``` 标签则包裹着需要折叠的具体内容。以下是一个创建可折叠表格的示例，其中表格展示了不同星级对应的“奇怪”“普通”“美味”的概率数据：

<details>
   <summary> 点击展开 </summary>
 
   | 星级	 | 奇怪    | 普通    | 美味   |
   |-----|-------|-------|------|
   | 1	  | 0.1	  | 0.15	 | 0.2  |
   | 2	  | 0.1	  | 0.1	  | 0.15 |
   | 3	  | 0.05	 | 0.1	  | 0.15 |
   | 4	  | 0.05	 | 0.05	 | 0.1  |
     
</details>

```markdown
<details>
   <summary> 点击展开 </summary>
 
   | 星级	 | 奇怪    | 普通    | 美味   |
   |-----|-------|-------|------|
   | 1	  | 0.1	  | 0.15	 | 0.2  |
   | 2	  | 0.1	  | 0.1	  | 0.15 |
   | 3	  | 0.05	 | 0.1	  | 0.15 |
   | 4	  | 0.05	 | 0.05	 | 0.1  |
     
</details>
```
