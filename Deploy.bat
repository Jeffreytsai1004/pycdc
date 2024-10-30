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

:: 创建虚拟环境目录结构
<nul set /p =创建虚拟环境...
echo.

if exist "venv" (
    rmdir /s /q venv
)

:: 直接复制整个Python目录作为虚拟环境
xcopy /E /I /Y "python" "venv"

:: 创建site-packages目录
mkdir "venv\Lib\site-packages"

:: 设置MinGW安装路径
set "MINGW_INSTALL_PATH=%CD%\mingw64"

:: 创建激活脚本
(
echo @echo off
echo set "VIRTUAL_ENV=%CD%\venv"
echo set "PATH=%CD%\venv;%CD%\mingw64\mingw64\bin;%%PATH%%"
echo set "PYTHONPATH=%CD%\venv\Lib;%CD%\venv\Lib\site-packages"
echo set "PROMPT=(venv) %%PROMPT%%"
) > venv\activate.bat

:: 激活虚拟环境
call .\venv\activate.bat

:: 下载get-pip.py
<nul set /p =正在下载pip安装程序...
echo.
if not exist "get-pip.py" (
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile 'get-pip.py'"
)

:: 安装pip
<nul set /p =正在安装pip...
echo.
"%VIRTUAL_ENV%\python.exe" get-pip.py --no-warn-script-location

:: 删除临时文件
del get-pip.py

:: 设置pip源为清华镜像
<nul set /p =正在配置pip源...
echo.
"%VIRTUAL_ENV%\python.exe" -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

:: 安装PyInstaller
<nul set /p =正在安装PyInstaller...
echo.

:: 安装必要的Python包
<nul set /p =正在安装Python包...
echo.
"%VIRTUAL_ENV%\python.exe" -m pip install customtkinter pillow pyinstaller darkdetect packaging cmake
:: 输出安装结果
<nul set /p =Python包安装完成！
echo.

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

    :: 下载7zip独立版（如果需要）
    if not exist "7zr.exe" (
        <nul set /p =正在下载7zip...
        echo.
        powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.7-zip.org/a/7zr.exe' -OutFile '7zr.exe'"
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