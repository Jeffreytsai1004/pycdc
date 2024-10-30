@echo off
chcp 65001 > nul
<nul set /p =开始构建pycdc...
echo.

:: 激活虚拟环境
call .\venv\activate.bat
<nul set /p =虚拟环境已激活
echo.

:: 验证环境
<nul set /p =验证编译环境...
echo.
where gcc >nul 2>&1
if %ERRORLEVEL% neq 0 (
    <nul set /p =Error: gcc未找到，请确保已正确运行Deploy.bat
    echo.
    pause
    exit /b 1
)

where cmake >nul 2>&1
if %ERRORLEVEL% neq 0 (
    <nul set /p =Error: cmake未找到，请确保已正确运行Deploy.bat
    echo.
    pause
    exit /b 1
)

:: 创建Release目录
if not exist Release mkdir Release

:: 配置CMake
<nul set /p =正在配置CMake...
echo.
cmake -BRelease -H. -G "MinGW Makefiles"

:: 编译
<nul set /p =正在编译...
echo.
cmake --build Release

:: 检查编译
if %ERRORLEVEL% neq 0 (
    <nul set /p =编译失败！
    echo.
    pause
    exit /b 1
)

<nul set /p =编译完成！
echo.
pause
