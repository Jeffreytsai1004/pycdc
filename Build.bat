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

where mingw32-make >nul 2>&1
if %ERRORLEVEL% neq 0 (
    <nul set /p =Error: mingw32-make未找到，请确保已正确运行Deploy.bat
    echo.
    pause
    exit /b 1
)

:: 创建构建目录
if not exist build mkdir build
cd build

:: 配置CMake
<nul set /p =正在配置CMake...
echo.
cmake -G "MinGW Makefiles" -DCMAKE_MAKE_PROGRAM="%CD%\..\mingw64\mingw64\bin\mingw32-make.exe" ..

:: 编译
<nul set /p =正在编译...
echo.
"%CD%\..\mingw64\mingw64\bin\mingw32-make.exe"

:: 检查编译
if %ERRORLEVEL% neq 0 (
    <nul set /p =编译失败！
    echo.
    cd ..
    pause
    exit /b 1
)

:: 创建Release目录并复制文件
if not exist ..\Release mkdir ..\Release
copy pycdc.exe ..\Release\pycdc.exe

:: 完成
cd ..
<nul set /p =编译完成！pycdc.exe 已复制到 Release 目录
echo.

pause