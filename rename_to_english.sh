#!/bin/bash
# 文件名重命名脚本 - 将中文文件名改为英文，避免Windows乱码

cd "$(dirname "$0")"

echo "================================================"
echo "  📝 文件名重命名脚本"
echo "  目的：避免Windows解压时出现中文文件名乱码"
echo "================================================"
echo ""

# 创建文件名映射表
cat > FILENAME_MAPPING.txt << 'EOF'
# 中文文件名 -> 英文文件名映射表
# 生成时间: $(date)

原中文文件名                      新英文文件名
================================================
一键配置.bat                     setup.bat
一键启动.bat                     start.bat
停止服务.bat                     stop.bat
Windows用户指南.md               Windows-User-Guide.md
Windows快速入门.md               Windows-Quick-Start.md
Windows部署包清单.md             Windows-Package-List.md
Windows部署包交付总结.md         Windows-Delivery-Summary.md
📌 开始使用.txt                  START-HERE.txt
✅ Windows交付完成确认.md        Windows-Delivery-Confirmation.md
使用指南.md                      User-Guide.md
快速开始.md                      Quick-Start.md
示例小说.txt                     Sample-Novel.txt
项目总结.md                      Project-Summary.md
项目检查清单.md                  Project-Checklist.md
新功能说明.md                    New-Features.md
搜索功能说明.md                  Search-Feature.md
数据统计功能说明.md              Statistics-Feature.md
推荐系统功能说明.md              Recommendation-Feature.md
首页美化功能说明.md              Homepage-Feature.md
全站古风改造说明.md              Ancient-Style-Transformation.md
全站古风改造完成报告.md          Ancient-Style-Complete-Report.md
读者页面改造完成.md              Reader-Pages-Complete.md
实验报告.md                      Experiment-Report.md
Docker镜像加速配置.md            Docker-Mirror-Config.md
README.md                        README.md (保持不变)
README-Windows.md                README-Windows.md (保持不变)
EOF

echo "📋 创建文件名映射表: FILENAME_MAPPING.txt"
echo ""
echo "开始重命名文件..."
echo ""

# 重命名函数
rename_file() {
    local old_name="$1"
    local new_name="$2"
    
    if [ -f "$old_name" ]; then
        mv "$old_name" "$new_name"
        echo "  ✅ $old_name -> $new_name"
    else
        echo "  ⏭️  跳过（文件不存在）: $old_name"
    fi
}

# 批量重命名
rename_file "一键配置.bat" "setup.bat"
rename_file "一键启动.bat" "start.bat"
rename_file "停止服务.bat" "stop.bat"
rename_file "Windows用户指南.md" "Windows-User-Guide.md"
rename_file "Windows快速入门.md" "Windows-Quick-Start.md"
rename_file "Windows部署包清单.md" "Windows-Package-List.md"
rename_file "Windows部署包交付总结.md" "Windows-Delivery-Summary.md"
rename_file "📌 开始使用.txt" "START-HERE.txt"
rename_file "✅ Windows交付完成确认.md" "Windows-Delivery-Confirmation.md"
rename_file "使用指南.md" "User-Guide.md"
rename_file "快速开始.md" "Quick-Start.md"
rename_file "示例小说.txt" "Sample-Novel.txt"
rename_file "项目总结.md" "Project-Summary.md"
rename_file "项目检查清单.md" "Project-Checklist.md"
rename_file "新功能说明.md" "New-Features.md"
rename_file "搜索功能说明.md" "Search-Feature.md"
rename_file "数据统计功能说明.md" "Statistics-Feature.md"
rename_file "推荐系统功能说明.md" "Recommendation-Feature.md"
rename_file "首页美化功能说明.md" "Homepage-Feature.md"
rename_file "全站古风改造说明.md" "Ancient-Style-Transformation.md"
rename_file "全站古风改造完成报告.md" "Ancient-Style-Complete-Report.md"
rename_file "读者页面改造完成.md" "Reader-Pages-Complete.md"
rename_file "实验报告.md" "Experiment-Report.md"
rename_file "Docker镜像加速配置.md" "Docker-Mirror-Config.md"

echo ""
echo "================================================"
echo "  ✅ 文件重命名完成！"
echo "================================================"
echo ""
echo "📋 文件名映射表已保存到: FILENAME_MAPPING.txt"
echo ""
echo "🎯 下一步操作："
echo "  1. 检查重命名后的文件"
echo "  2. 使用 pack_for_windows.sh 打包"
echo "  3. Windows用户使用任意工具解压均可（无乱码）"
echo ""
