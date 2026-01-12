#!/bin/bash
# Windows兼容打包脚本 - 使用UTF-8编码打包

cd "$(dirname "$0")"

echo "================================================"
echo "  📦 创建Windows兼容的压缩包"
echo "================================================"
echo ""

# 压缩包名称
PACKAGE_NAME="novel-platform-v2.0-$(date +%Y%m%d).zip"

echo "📋 打包配置："
echo "  - 压缩包名称: $PACKAGE_NAME"
echo "  - 编码: UTF-8"
echo "  - 排除: venv, __pycache__, .pyc, .git, .DS_Store"
echo ""

# 检查 zip 命令是否支持 UTF-8
if zip --help 2>&1 | grep -q "UN=UTF8"; then
    echo "✅ 检测到 zip 支持 UTF-8 编码"
    echo ""
    echo "正在打包..."
    
    # 使用 UTF-8 编码打包
    zip -r -UN=UTF8 "$PACKAGE_NAME" \
        *.py \
        *.md \
        *.bat \
        *.txt \
        *.sh \
        requirements.txt \
        Dockerfile \
        docker-compose.yml \
        static/ \
        templates/ \
        -x "venv/*" \
        -x "__pycache__/*" \
        -x "*.pyc" \
        -x ".git/*" \
        -x ".DS_Store" \
        -x "uploads/*" \
        -x "*.tar.gz"
else
    echo "⚠️  当前 zip 不支持 UTF-8 选项，使用默认编码"
    echo ""
    echo "正在打包..."
    
    # 使用默认编码打包
    zip -r "$PACKAGE_NAME" \
        *.py \
        *.md \
        *.bat \
        *.txt \
        *.sh \
        requirements.txt \
        Dockerfile \
        docker-compose.yml \
        static/ \
        templates/ \
        -x "venv/*" \
        -x "__pycache__/*" \
        -x "*.pyc" \
        -x ".git/*" \
        -x ".DS_Store" \
        -x "uploads/*" \
        -x "*.tar.gz"
fi

echo ""
echo "================================================"
echo "  ✅ 打包完成！"
echo "================================================"
echo ""
echo "📦 压缩包信息："
ls -lh "$PACKAGE_NAME"
echo ""
echo "📋 包含的主要文件："
unzip -l "$PACKAGE_NAME" | head -30
echo "  ..."
echo ""
echo "🎯 给Windows用户的说明："
echo "  1. 推荐使用 7-Zip 解压（免费）：https://www.7-zip.org/"
echo "  2. 也可使用 Bandizip 或 WinRAR"
echo "  3. Windows自带解压工具也可使用（文件名已改为英文）"
echo ""
echo "📄 下一步："
echo "  - 将 $PACKAGE_NAME 发送给Windows用户"
echo "  - 附上 README-Windows.md 说明文档"
echo ""
