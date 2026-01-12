



# 小说创作与阅读平台

基于 MongoDB 的非结构化数据存储与管理系统，实现小说创作、发布、审核、阅读、购买全流程。

## 项目简介

本项目是一个完整的小说创作与阅读平台，支持：
- 用户管理（读者/创作者/管理员三种角色）
- 小说创作与发布（支持 TXT/PDF 文件导入）
- 小说审核与上线（管理员审核机制）
- 小说阅读与购买（付费/免费模式）
- 章节管理与阅读进度保存

## 技术栈

- **后端**: Python 3.9+ / Flask 2.3
- **数据库**: MongoDB 6.0
- **前端**: HTML5 / CSS3 / JavaScript
- **容器化**: Docker / Docker Compose
- **其他**: PyMongo, Bcrypt, PyPDF2

## 项目结构

```
python/
├── app.py                  # Flask 应用主文件
├── config.py               # 配置文件
├── models.py               # 数据模型
├── requirements.txt        # Python 依赖
├── Dockerfile             # Docker 镜像配置
├── docker-compose.yml     # Docker Compose 配置
├── init_data.py           # 初始化数据脚本
├── static/                # 静态资源
│   └── css/
│       └── style.css      # 样式文件
├── templates/             # 模板文件
│   ├── base.html          # 基础模板
│   ├── login.html         # 登录页面
│   ├── register.html      # 注册页面
│   ├── admin/             # 管理员页面
│   │   ├── dashboard.html
│   │   ├── users.html
│   │   └── review.html
│   ├── creator/           # 创作者页面
│   │   ├── dashboard.html
│   │   ├── novels.html
│   │   ├── create_novel.html
│   │   ├── edit_novel.html
│   │   ├── chapters.html
│   │   ├── add_chapter.html
│   │   ├── edit_chapter.html
│   │   └── import_chapters.html
│   └── reader/            # 读者页面
│       ├── dashboard.html
│       ├── novels.html
│       ├── novel_detail.html
│       ├── read_chapter.html
│       └── orders.html
└── uploads/               # 文件上传目录
```

## MongoDB 数据库设计

### 1. users 集合（用户信息）

```javascript
{
  "_id": ObjectId("..."),
  "username": "张三",
  "role": "creator",          // reader/creator/admin
  "password": "加密后的密码",
  "avatar": null,
  "tags": ["悬疑", "校园"],
  "status": 1,                // 1-正常，0-注销
  "createTime": ISODate("...")
}
```

### 2. novels 集合（小说信息）

```javascript
{
  "_id": ObjectId("..."),
  "novelId": "NOVEL20260111001",
  "title": "穿越唐朝当书生",
  "authorId": ObjectId("..."),
  "category": "玄幻",
  "tags": ["穿越", "科举", "历史"],
  "intro": "主角意外穿越到唐朝...",
  "cover": null,
  "price": 8.0,
  "status": "online",         // draft/pending/online/rejected
  "chapters": [
    {
      "chapterId": "CH001",
      "title": "第一章 意外穿越",
      "content": "章节正文...",
      "isFree": true,
      "createTime": ISODate("...")
    }
  ],
  "comments": [],
  "review": {
    "adminId": ObjectId("..."),
    "opinion": "审核通过",
    "time": ISODate("...")
  },
  "readCount": 1200,
  "saleCount": 350,
  "createTime": ISODate("...")
}
```

### 3. orders 集合（订单信息）

```javascript
{
  "_id": ObjectId("..."),
  "orderId": "ORDER20260111001",
  "readerId": ObjectId("..."),
  "novelId": ObjectId("..."),
  "amount": 8.0,
  "status": "paid",           // pending/paid/refunded
  "createTime": ISODate("..."),
  "payTime": ISODate("...")
}
```

### 4. reading_records 集合（阅读记录）

```javascript
{
  "_id": ObjectId("..."),
  "readerId": ObjectId("..."),
  "novelId": ObjectId("..."),
  "currentChapterId": "CH005",
  "page": 23,
  "updateTime": ISODate("...")
}
```

## 快速开始

### 方式一：使用 Docker Compose（推荐）

1. **确保已安装 Docker 和 Docker Compose**

```bash
docker --version
docker-compose --version
```

2. **启动服务**

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

3. **初始化数据（创建管理员账号）**

```bash
# 进入 web 容器
docker exec -it novel_platform_web bash

# 运行初始化脚本
python init_data.py

# 退出容器
exit
```

4. **访问应用**

打开浏览器访问：http://localhost:5000

默认管理员账号：
- 用户名：admin
- 密码：admin123

5. **停止服务**

```bash
docker-compose down
```

### 方式二：本地运行

1. **安装 MongoDB**

确保 MongoDB 6.0+ 已安装并运行在 localhost:27017

2. **安装 Python 依赖**

```bash
# 创建虚拟环境（可选）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

3. **配置环境变量**

```bash
export MONGODB_HOST=localhost
export MONGODB_PORT=27017
export MONGODB_USER=admin
export MONGODB_PASSWORD=admin123
export MONGODB_DB=novel_platform
export SECRET_KEY=your-secret-key
```

4. **初始化数据**

```bash
python init_data.py
```

5. **启动应用**

```bash
python app.py
```

6. **访问应用**

打开浏览器访问：http://localhost:5000

## 功能说明

### 1. 用户管理

#### 注册与登录
- 支持读者、创作者、管理员三种角色注册
- 密码使用 bcrypt 加密存储
- Session 会话管理

#### 管理员功能
- 查看平台统计数据（用户数、小说数等）
- 用户管理（查看、删除用户）
- 小说审核（通过/驳回待审核小说）

### 2. 小说创作（创作者）

#### 创建小说
- 填写小说基本信息（标题、分类、标签、简介、定价）
- 支持草稿保存

#### 导入章节
- **TXT 文件导入**：自动识别章节标题（支持"第X章"、"第X回"格式）
- **PDF 文件导入**：自动解析 PDF 文本内容
- 前 3 章自动设为免费试读

#### 章节管理
- 添加、编辑、删除章节
- 设置章节免费/付费属性
- 章节排序显示

#### 提交审核
- 小说完成后提交给管理员审核
- 查看审核结果和驳回原因

### 3. 小说阅读（读者）

#### 小说广场
- 浏览所有已上线小说
- 按分类筛选
- 分页显示

#### 小说详情
- 查看小说完整信息
- 查看章节列表
- 免费章节直接阅读
- 付费小说需购买后阅读

#### 阅读体验
- 清晰的章节阅读界面
- 上一章/下一章快速切换
- 自动保存阅读进度

#### 购买小说
- 一键购买小说（模拟支付）
- 查看购买历史
- 我的书架管理

## 核心特性

### MongoDB 特性应用

1. **嵌套文档**：chapters 数组嵌套在 novels 中，减少关联查询
2. **索引优化**：为常用查询字段创建单字段和复合索引
3. **聚合查询**：统计分析功能使用 MongoDB 聚合管道
4. **灵活模式**：支持动态字段，适应非结构化数据

### 安全特性

1. **密码加密**：使用 bcrypt 算法加密存储
2. **权限控制**：基于角色的访问控制（RBAC）
3. **Session 管理**：Flask Session 会话管理
4. **SQL 注入防护**：使用 PyMongo ORM

### 性能优化

1. **索引设计**：为高频查询字段创建索引
2. **分页查询**：避免一次加载过多数据
3. **状态筛选**：通过状态字段快速过滤
4. **连接池**：MongoDB 连接池复用

## 测试说明

### 测试流程

1. **注册管理员账号**（或使用初始化的账号）
   - 用户名：admin
   - 密码：admin123

2. **注册创作者账号**
   - 选择"创作者"角色
   - 登录后进入创作者控制台

3. **创建小说**
   - 填写小说信息
   - 导入 TXT/PDF 文件或手动添加章节
   - 提交审核

4. **管理员审核**
   - 使用管理员账号登录
   - 进入"审核小说"页面
   - 通过或驳回小说

5. **注册读者账号**
   - 选择"读者"角色
   - 登录后进入小说广场

6. **阅读与购买**
   - 浏览小说列表
   - 查看小说详情
   - 免费章节直接阅读
   - 付费小说购买后阅读

## 常见问题

### Q1: Docker 启动失败？
**A**: 检查 Docker 服务是否运行，端口 5000 和 27017 是否被占用。

### Q2: 无法连接 MongoDB？
**A**: 确认 MongoDB 服务已启动，检查 docker-compose.yml 中的连接配置。

### Q3: 上传文件失败？
**A**: 检查 uploads 目录权限，确保应用有写入权限。

### Q4: 密码加密失败？
**A**: 确保 bcrypt 库正确安装：`pip install bcrypt`

### Q5: PDF 解析失败？
**A**: 确保 PyPDF2 库正确安装，某些加密 PDF 可能无法解析。

## 扩展功能建议

基础功能已全部实现，可选择以下进阶功能：

1. **高级查询**
   - 多条件组合查询
   - 全文搜索
   - 模糊匹配

2. **互动功能**
   - 评论与回复
   - 点赞与收藏
   - 关注作者

3. **统计分析**
   - 阅读量统计
   - 销售额统计
   - 热门排行榜

4. **GridFS 存储**
   - 大文件章节内容存储
   - 图片封面存储

## 许可证

MIT License

## 联系方式

如有问题，请通过以下方式联系：
- 项目地址：[GitHub Repository]
- 邮箱：[your-email@example.com]

## 更新日志

### v1.0.0 (2026-01-11)
- 初始版本发布
- 实现基础功能（用户管理、小说创作、审核、阅读、购买）
- Docker 容器化部署
- MongoDB 数据库设计与索引优化
=======
# -
大作业
>>>>>>> fc7a8fec384340f1a5dab93098101746e8f6d101
