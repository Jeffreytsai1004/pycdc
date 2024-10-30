@echo off
chcp 65001 > nul

:: 设置虚拟环境路径
set "VIRTUAL_ENV=%CD%\venv"

:: 激活虚拟环境
call "%VIRTUAL_ENV%\Scripts\activate.bat"

echo 开始构建pycdc...
echo 虚拟环境已激活

:: 验证环境
echo 验证编译环境...
where gcc >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: gcc未找到，请确保已正确运行Deploy.bat
    pause
    exit /b 1
)

where cmake >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: cmake未找到，请确保已正确运行Deploy.bat
    pause
    exit /b 1
)

:: 创建Release目录
if not exist Release mkdir Release

:: 配置CMake
echo 正在配置CMake...
cmake -BRelease -H. -G "MinGW Makefiles"

:: 编译
echo 正在编译...
cmake --build Release

:: 检查编译
if %ERRORLEVEL% neq 0 (
    echo 编译失败！
    pause
    exit /b 1
)

echo 编译完成！
pause
