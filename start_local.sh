#!/bin/bash

# 本地运行脚本（不使用 Docker）

echo "========================================"
echo "   小说平台 - 本地运行模式"
echo "========================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未检测到 Python3"
    exit 1
fi

echo "✓ Python3 环境检测通过"

# 检查 MongoDB
if ! pgrep -x "mongod" > /dev/null; then
    echo "⚠️  MongoDB 未运行，尝试启动..."
    
    # macOS 使用 brew 启动
    if command -v brew &> /dev/null; then
        echo "检测到 Homebrew，使用 brew 安装/启动 MongoDB..."
        
        # 检查是否已安装
        if ! brew list mongodb-community &> /dev/null 2>&1; then
            echo "正在安装 MongoDB..."
            brew tap mongodb/brew
            brew install mongodb-community@6.0
        fi
        
        echo "正在启动 MongoDB..."
        brew services start mongodb-community@6.0
        sleep 3
    else
        echo "❌ 请手动安装并启动 MongoDB"
        echo "   macOS: brew install mongodb-community@6.0"
        echo "   启动: brew services start mongodb-community@6.0"
        exit 1
    fi
fi

echo "✓ MongoDB 运行中"
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

# 设置环境变量
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
echo "访问地址: http://localhost:5000"
echo ""
echo "测试账号："
echo "  管理员 - 用户名: admin      密码: admin123"
echo "  创作者 - 用户名: 作家小明   密码: creator123"
echo "  读者   - 用户名: 读者小红   密码: reader123"
echo ""
echo "按 Ctrl+C 停止服务"
echo "========================================"
echo ""

# 启动 Flask
python app.py
