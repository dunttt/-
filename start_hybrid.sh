#!/bin/bash

# 混合运行模式：MongoDB 用 Docker，Web 应用本地运行

echo "========================================"
echo "   小说平台 - 混合运行模式"
echo "========================================"
echo ""

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ 错误: 未检测到 Docker"
    exit 1
fi

echo "✓ Docker 环境检测通过"
echo ""

# 只启动 MongoDB 容器
echo "正在启动 MongoDB 容器..."
docker run -d \
  --name novel_mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_DATABASE=novel_platform \
  mongo:6.0 \
  2>/dev/null || docker start novel_mongodb 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✓ MongoDB 容器启动成功"
else
    echo "尝试使用已有容器..."
    docker start novel_mongodb
fi

# 等待 MongoDB 启动
echo "等待 MongoDB 初始化..."
sleep 5

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未检测到 Python3"
    exit 1
fi

echo "✓ Python3 环境检测通过"
echo ""

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建 Python 虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "安装 Python 依赖..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# 设置环境变量（连接本地 MongoDB）
export MONGODB_HOST=localhost
export MONGODB_PORT=27017
export MONGODB_USER=""
export MONGODB_PASSWORD=""
export MONGODB_DB=novel_platform
export SECRET_KEY=dev-secret-key

# 初始化数据
echo ""
echo "初始化数据库..."
python init_data.py

# 启动应用
echo ""
echo "========================================"
echo "   🎉 启动成功！"
echo "========================================"
echo ""
echo "访问地址: http://localhost:5000 或 http://localhost:5001"
echo ""
echo "测试账号："
echo "  管理员 - 用户名: admin      密码: admin123"
echo "  创作者 - 用户名: 作家小明   密码: creator123"
echo "  读者   - 用户名: 读者小红   密码: reader123"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""
echo "停止 MongoDB: docker stop novel_mongodb"
echo "========================================"
echo ""

# 启动 Flask
python app.py
