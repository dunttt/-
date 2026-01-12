@echo off
chcp 65001 >nul
title 停止服务

REM 切换到脚本所在目录（保持一致性）
cd /d "%~dp0"

echo ========================================
echo 停止悦读坊服务
echo ========================================
echo.

REM 查找并结束Python进程（运行在5001端口的）
echo 正在查找运行中的服务...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5001 ^| findstr LISTENING') do (
    set PID=%%a
    goto :found
)

echo ⚠️  未找到运行中的服务
echo.
pause
exit /b 0

:found
echo ✓ 找到进程 PID: %PID%
echo.
echo 正在停止服务...
taskkill /PID %PID% /F >nul 2>&1

if %errorlevel% equ 0 (
    echo ✓ 服务已停止
) else (
    echo ❌ 停止失败，可能需要管理员权限
    echo.
    echo 请右键选择"以管理员身份运行"此脚本
)

echo.
pause
