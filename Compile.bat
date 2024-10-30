@echo off
chcp 65001 > nul

:: 设置虚拟环境路径
set "VIRTUAL_ENV=%CD%\venv"

:: 激活虚拟环境
call "%VIRTUAL_ENV%\Scripts\activate.bat"

echo 开始打包...

:: 编译
"%VIRTUAL_ENV%\python.exe" -m pyinstaller decompiler.spec --clean

if %ERRORLEVEL% neq 0 (
    echo 打包失败！
    pause
    exit /b 1
)

echo 打包完成！
pause


