@echo off
echo 开始构建 pycdc...

:: 使用 .\python\python.exe
set PYTHON_PATH=.\python\python.exe

:: 激活venv
.\venv\Scripts\activate

:: 创建构建目录
if not exist build mkdir build
cd build

:: 运行 CMake
echo 正在配置 CMake...
cmake -G "MinGW Makefiles" ..

:: 编译
echo 正在编译...
mingw32-make

:: 检查编译结果
if %ERRORLEVEL% neq 0 (
    echo 编译失败！
    cd ..
    pause
    exit /b 1
)

:: 创建 Release 目录并复制文件
if not exist ..\Release mkdir ..\Release
copy pycdc.exe ..\Release\pycdc.exe

:: 清理
cd ..
echo 构建完成！pycdc.exe 已复制到 Release 目录

pause 