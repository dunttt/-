# 📖 悦读坊 - 小说创作与阅读平台

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![MongoDB](https://img.shields.io/badge/MongoDB-6.0%2B-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

**发现好书，分享阅读乐趣**

[快速开始](#-快速开始-windows) | [功能特性](#-功能特性) | [技术栈](#-技术栈) | [文档](#-文档)

</div>

---

## 📝 项目简介

悦读坊是一个基于 MongoDB 的小说创作与阅读平台，采用古风设计风格，提供小说创作、发布、阅读、购买的完整闭环体验。

### 🌟 核心特点

- 🎨 **古风设计**：全站23个页面统一的中国风界面
- 📚 **完整闭环**：创作 → 发布 → 审核 → 阅读 → 购买
- 👥 **三种角色**：读者、创作者、管理员
- 🔍 **智能推荐**：基于阅读历史的个性化推荐
- 💬 **互动评论**：评论回复功能
- 📊 **数据统计**：ECharts 可视化图表
- 📱 **响应式设计**：完美适配PC/平板/手机

---

## 🚀 快速开始 (Windows)

### 方式一：一键启动（推荐）

```bash
# 1. 双击运行
一键配置.bat     # 首次运行，自动配置环境

# 2. 双击运行
一键启动.bat     # 启动系统

# 3. 浏览器访问
http://127.0.0.1:5001
```

### 方式二：命令行启动

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 初始化数据库
python init_data.py

# 3. 启动应用
python app.py

# 4. 浏览器访问
http://127.0.0.1:5001
```

### 测试账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |
| 创作者 | 作家小明 | creator123 |
| 读者 | 读者小红 | reader123 |

---

## ✨ 功能特性

### 📖 读者功能

- ✅ 浏览小说广场（搜索、筛选、分页）
- ✅ 查看小说详情（简介、章节、价格）
- ✅ 免费试读（前N章免费）
- ✅ 购买小说（模拟支付）
- ✅ 在线阅读（楷体字体、舒适行距）
- ✅ 评论互动（评论、回复、删除）
- ✅ 个性化推荐（基于阅读历史）
- ✅ 订单管理（查看订单、重复阅读）
- ✅ 阅读进度（自动保存、断点续读）

### ✍️ 创作者功能

- ✅ 创建小说（标题、分类、标签、简介、定价）
- ✅ 添加章节（手动输入）
- ✅ 导入章节（TXT/PDF，自动识别章节）
- ✅ 编辑小说/章节
- ✅ 删除章节
- ✅ 设置免费试读章节
- ✅ 提交审核
- ✅ 查看创作数据（阅读量、销量）
- ✅ 草稿保存

### 👑 管理员功能

- ✅ 用户管理（查看、删除用户）
- ✅ 小说审核（通过、驳回）
- ✅ 数据统计（图表可视化）
  - 小说分类分布
  - 热门小说排行（阅读量、销量）
  - 创作者统计
  - 用户角色分布
  - 平台收益统计

---

## 🛠️ 技术栈

### 后端

- **Python 3.9+**：主要开发语言
- **Flask 2.3.3**：Web 框架
- **PyMongo 4.5.0**：MongoDB 驱动
- **bcrypt 4.0.1**：密码加密
- **PyPDF2 3.0.1**：PDF 解析

### 前端

- **HTML5 + CSS3**：页面结构和样式
- **Jinja2**：模板引擎
- **JavaScript (ES6)**：交互逻辑
- **ECharts 5.4.3**：数据可视化

### 数据库

- **MongoDB 6.0+**：NoSQL 数据库
- **GridFS**：大文件存储（章节正文）

### 设计

- **古风配色**：朱砂红、茶褐色、绿茶色、土金色
- **楷体字体**：阅读正文
- **响应式布局**：适配多种设备

---

## 📂 项目结构

```
python/
├── app.py                      # Flask 主应用
├── config.py                   # 配置文件
├── models.py                   # 数据模型
├── init_data.py                # 数据库初始化
├── requirements.txt            # Python 依赖
├── 一键启动.bat                # Windows 启动脚本
├── 一键配置.bat                # Windows 配置脚本
├── 停止服务.bat                # Windows 停止脚本
│
├── static/                     # 静态资源
│   ├── css/
│   │   ├── style.css          # 原始样式
│   │   └── ancient-style.css  # 古风样式
│   └── js/
│
├── templates/                  # HTML 模板
│   ├── base.html              # 基础模板
│   ├── base-ancient.html      # 古风基础模板
│   ├── index.html             # 首页
│   ├── login.html             # 登录
│   ├── register.html          # 注册
│   │
│   ├── reader/                # 读者模块 (6个页面)
│   │   ├── dashboard.html     # 我的书架
│   │   ├── novels.html        # 小说广场
│   │   ├── novel_detail.html  # 小说详情
│   │   ├── read_chapter.html  # 章节阅读
│   │   ├── orders.html        # 我的订单
│   │   └── recommendations.html # 为你推荐
│   │
│   ├── creator/               # 创作者模块 (7个页面)
│   │   ├── dashboard.html     # 创作者控制台
│   │   ├── novels.html        # 我的小说
│   │   ├── create_novel.html  # 创建小说
│   │   ├── edit_novel.html    # 编辑小说
│   │   ├── chapters.html      # 章节管理
│   │   ├── add_chapter.html   # 添加章节
│   │   ├── edit_chapter.html  # 编辑章节
│   │   └── import_chapters.html # 导入章节
│   │
│   └── admin/                 # 管理员模块 (4个页面)
│       ├── dashboard.html     # 管理员控制台
│       ├── users.html         # 用户管理
│       ├── review.html        # 审核小说
│       └── statistics.html    # 数据统计
│
├── uploads/                    # 上传文件存储
│
└── docs/                       # 文档
    ├── Windows用户指南.md      # 详细教程 (30页)
    ├── Windows快速入门.md      # 快速指南 (3分钟)
    ├── 使用指南.md             # 功能说明
    ├── 项目总结.md             # 项目总结
    ├── 全站古风改造完成报告.md # 设计文档
    └── README.md              # 本文件
```

---

## 📊 数据库设计

### 集合说明

```javascript
// 1. users - 用户集合
{
  "_id": ObjectId,
  "username": String,          // 用户名
  "password": String,          // 加密密码
  "role": String,              // 角色：reader/creator/admin
  "tags": Array,               // 兴趣标签
  "status": Number,            // 状态：1-正常，0-注销
  "createTime": Date
}

// 2. novels - 小说集合
{
  "_id": ObjectId,
  "novelId": String,           // 自定义ID
  "title": String,             // 标题
  "authorId": ObjectId,        // 作者ID
  "category": String,          // 分类
  "tags": Array,               // 标签
  "intro": String,             // 简介
  "price": Number,             // 定价
  "status": String,            // 状态：draft/pending/online/rejected
  "chapters": Array,           // 章节数组（嵌套）
  "comments": Array,           // 评论数组（嵌套）
  "review": Object,            // 审核记录（嵌套）
  "readCount": Number,         // 阅读量
  "saleCount": Number,         // 销量
  "createTime": Date
}

// 3. orders - 订单集合
{
  "_id": ObjectId,
  "orderId": String,           // 订单号
  "readerId": ObjectId,        // 读者ID
  "novelId": ObjectId,         // 小说ID
  "amount": Number,            // 金额
  "status": String,            // 状态：pending/paid/refunded
  "createTime": Date,
  "payTime": Date
}

// 4. reading_records - 阅读记录集合
{
  "_id": ObjectId,
  "readerId": ObjectId,        // 读者ID
  "novelId": ObjectId,         // 小说ID
  "currentChapterId": String,  // 当前章节
  "page": Number,              // 当前页码
  "updateTime": Date
}
```

---

## 📚 文档

### Windows 用户

- **[Windows用户指南.md](Windows用户指南.md)** - 30页详细教程
  - 环境准备（Python、MongoDB）
  - 项目部署
  - 启动说明
  - 常见问题解决

- **[Windows快速入门.md](Windows快速入门.md)** - 3分钟快速指南
  - 一键配置
  - 一键启动
  - 功能导览

### 功能说明

- **[使用指南.md](使用指南.md)** - 完整功能说明
- **[推荐系统功能说明.md](推荐系统功能说明.md)** - 推荐算法
- **[数据统计功能说明.md](数据统计功能说明.md)** - 统计图表
- **[搜索功能说明.md](搜索功能说明.md)** - 搜索实现

### 设计文档

- **[全站古风改造完成报告.md](全站古风改造完成报告.md)** - 设计系统
- **[项目总结.md](项目总结.md)** - 项目总结

---

## 🎨 界面预览

### 古风设计

- **主色调**：朱砂红 (#c8553d)
- **辅助色**：茶褐、绿茶、土金、青瓦
- **背景**：水墨画 SVG
- **字体**：楷体（阅读正文）
- **效果**：毛玻璃、渐变、动画

### 页面展示

- 🏠 **首页**：Hero Banner + 精选推荐 + 新书上架
- 📚 **小说广场**：搜索 + 筛选 + 卡片网格
- 📖 **阅读页面**：楷体字体 + 舒适行距
- 💬 **评论系统**：评论 + 回复 + 删除
- 📊 **数据统计**：5种 ECharts 图表

---

## 🔐 安全特性

- ✅ 密码 bcrypt 加密
- ✅ Session 会话管理
- ✅ 角色权限控制
- ✅ SQL 注入防护（NoSQL）
- ✅ XSS 防护（Jinja2 自动转义）
- ✅ CSRF 防护（Flask 内置）

---

## 📈 性能优化

- ✅ MongoDB 索引优化
- ✅ 静态资源缓存
- ✅ 懒加载图片
- ✅ 响应式图片
- ✅ CSS/JS 最小化
- ✅ GridFS 大文件存储

---

## 🐛 常见问题

### Q: 端口被占用怎么办？

**A:** 修改 `app.py` 最后一行：
```python
app.run(host='0.0.0.0', port=5002, debug=True)
```

### Q: MongoDB 连接失败？

**A:** 检查服务是否运行：
```bash
sc query MongoDB
```

### Q: 依赖安装失败？

**A:** 使用国内镜像：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 📞 技术支持

### 反馈问题

提供以下信息：
1. 操作系统版本
2. Python 版本
3. MongoDB 版本
4. 错误截图
5. 操作步骤

### 贡献代码

欢迎提交 Pull Request！

---

## 📄 开源协议

本项目采用 **MIT License** 开源协议。

---

## 🎉 致谢

感谢以下开源项目：

- [Flask](https://flask.palletsprojects.com/) - Web 框架
- [MongoDB](https://www.mongodb.com/) - 数据库
- [ECharts](https://echarts.apache.org/) - 图表库
- [Python](https://www.python.org/) - 编程语言

---

## 📮 联系方式

- **项目名称**：悦读坊
- **版本**：v2.0 Ancient Style
- **更新日期**：2026-01-11

---

<div align="center">

**悦读坊 - 发现好书，分享阅读乐趣** 📖

Made with ❤️ by Python & Flask & MongoDB

</div>
