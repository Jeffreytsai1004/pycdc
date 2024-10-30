@echo off
:: 设置代码页为UTF-8
chcp 65001 > nul
:: 使用echo命令输出UTF-8文本
<nul set /p =正在部署开发环境...
echo.

:: 检查Python路径是否存在
if not exist ".\python\python.exe" (
    <nul set /p =Error: .\python\python.exe 不存在
    echo.
    <nul set /p =请确保Python目录已正确放置
    echo.
    pause
    exit /b 1
)

:: 设置Python路径和环境变量
set "PYTHON_PATH=%CD%\python\python.exe"
set "PYTHON_HOME=%CD%\python"
set "PATH=%PYTHON_HOME%;%PATH%"

:: 创建基础Python目录结构
if not exist ".\python\Lib" mkdir ".\python\Lib"
if not exist ".\python\Lib\site-packages" mkdir ".\python\Lib\site-packages"
if not exist ".\python\DLLs" mkdir ".\python\DLLs"
if not exist ".\python\Scripts" mkdir ".\python\Scripts"

:: 下载venv模块
<nul set /p =正在下载venv模块...
echo.
if not exist ".\python\Lib\venv" (
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/python/cpython/3.12/Lib/venv/__init__.py' -OutFile '.\python\Lib\venv.py'"
)

:: 创建虚拟环境
<nul set /p =创建虚拟环境...
echo.
if exist "venv" (
    rmdir /s /q venv
)
%PYTHON_PATH% -m venv venv

:: 激活虚拟环境
call .\venv\Scripts\activate.bat

:: 下载get-pip.py到虚拟环境
<nul set /p =正在下载pip安装程序...
echo.
if not exist "get-pip.py" (
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile 'get-pip.py'"
)

:: 在虚拟环境中安装pip
<nul set /p =正在安装pip...
echo.
python get-pip.py --no-warn-script-location

:: 删除临时文件
del get-pip.py

:: 设置pip源为清华镜像
<nul set /p =正在配置pip源...
echo.
python -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

:: 在虚拟环境中安装必要的Python包
<nul set /p =正在安装Python包...
echo.
python -m pip install customtkinter pillow pyinstaller darkdetect packaging

:: 设置MinGW安装路径
set "MINGW_INSTALL_PATH=%CD%\mingw64"

:: 检查MinGW是否已安装
if not exist "%MINGW_INSTALL_PATH%\mingw64\bin\gcc.exe" (
    :: 下载MinGW
    <nul set /p =正在下载MinGW-w64...
    echo.
    if not exist "mingw64.7z" (
        powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://github.com/niXman/mingw-builds-binaries/releases/download/13.2.0-rt_v11-rev0/x86_64-13.2.0-release-posix-seh-msvcrt-rt_v11-rev0.7z' -OutFile 'mingw64.7z'"
    ) else (
        echo mingw64.7z已存在，跳过下载
    )

    :: 下载7zip独立版
    <nul set /p =正在下载7zip...
    echo.
    if not exist "7zr.exe" (
        powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.7-zip.org/a/7zr.exe' -OutFile '7zr.exe'"
    ) else (
        echo 7zr.exe已存在，跳过下载
    )

    :: 使用7zr解压MinGW
    <nul set /p =正在解压MinGW-w64...
    echo.
    7zr.exe x mingw64.7z -o"%MINGW_INSTALL_PATH%" -y

    :: 清理下载的文件
    del mingw64.7z
    del 7zr.exe
) else (
    echo MinGW已安装，跳过安装
)

:: 设置MinGW环境变量
set "PATH=%MINGW_INSTALL_PATH%\mingw64\bin;%PATH%"

:: 验证MinGW安装
where gcc >nul 2>&1
if %ERRORLEVEL% neq 0 (
    <nul set /p =Error: MinGW安装失败，gcc命令不可用
    echo.
    pause
    exit /b 1
)

<nul set /p =环境部署完成！
echo.
<nul set /p =MinGW已安装到: %MINGW_INSTALL_PATH%
echo.
<nul set /p =虚拟环境已创建在: %CD%\venv
echo.
<nul set /p =环境变量已更新，请重新打开命令提示符以使所有更改生效。
echo.
pause