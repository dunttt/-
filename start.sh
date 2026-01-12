#!/bin/bash

# 小说平台快速启动脚本

echo "========================================"
echo "   小说创作与阅读平台 - 快速启动"
echo "========================================"
echo ""

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ 错误: 未检测到 Docker，请先安装 Docker"
    exit 1
fi

# 检查 Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ 错误: 未检测到 Docker Compose，请先安装 Docker Compose"
    exit 1
fi

echo "✓ Docker 环境检测通过"
echo ""

# 停止并删除旧容器
echo "正在清理旧容器..."
docker-compose down 2>/dev/null

# 构建并启动服务
echo "正在构建并启动服务..."
docker-compose up -d --build

# 等待服务启动
echo "等待服务启动..."
sleep 10

# 检查服务状态
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "✓ 服务启动成功！"
    echo ""
    echo "正在初始化数据库..."
    docker exec -it novel_platform_web python init_data.py
    echo ""
    echo "========================================"
    echo "   🎉 系统已就绪！"
    echo "========================================"
    echo ""
    echo "访问地址: http://localhost:5000"
    echo ""
    echo "测试账号："
    echo "  管理员 - 用户名: admin      密码: admin123"
    echo "  创作者 - 用户名: 作家小明   密码: creator123"
    echo "  读者   - 用户名: 读者小红   密码: reader123"
    echo ""
    echo "查看日志: docker-compose logs -f"
    echo "停止服务: docker-compose down"
    echo "========================================"
else
    echo ""
    echo "❌ 服务启动失败，请查看日志:"
    echo "   docker-compose logs"
fi
