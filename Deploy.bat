@echo off
:: 设置代码页为UTF-8
chcp 65001 > nul

:: 使用echo命令输出UTF-8文本
echo 正在部署开发环境...

:: 检查Python路径是否存在
if not exist ".\python\python.exe" (
    echo Error: .\python\python.exe 不存在
    echo 请确保Python目录已正确放置
    pause
    exit /b 1
)

:: 创建虚拟环境目录结构
echo 创建虚拟环境...

if exist "venv" (
    rmdir /s /q venv
)

:: 直接复制整个Python目录作为虚拟环境
xcopy /E /I /Y "python" "venv"

:: 创建必要的目录
mkdir "venv\Lib" 2>nul
mkdir "venv\Lib\site-packages" 2>nul
mkdir "venv\Scripts" 2>nul

:: 设置MinGW安装路径
set "MINGW_INSTALL_PATH=%CD%\mingw64"

:: 创建激活脚本
(
echo @echo off
echo set "VIRTUAL_ENV=%CD%\venv"
echo set "PYTHON_HOME=%%VIRTUAL_ENV%%"
echo set "PATH=%%VIRTUAL_ENV%%;%%VIRTUAL_ENV%%\Scripts;%CD%\mingw64\mingw64\bin;%%PATH%%"
echo set "PYTHONPATH=%%VIRTUAL_ENV%%\Lib;%%VIRTUAL_ENV%%\DLLs;%%VIRTUAL_ENV%%\Lib\site-packages"
echo set "PROMPT=(venv) %%PROMPT%%"
) > venv\Scripts\activate.bat

:: 激活虚拟环境
call .\venv\Scripts\activate.bat

:: 复制pip相关文件
echo 配置pip...
if exist "python\Scripts\pip.exe" (
    copy "python\Scripts\pip.exe" "venv\Scripts\"
    copy "python\Scripts\pip3.exe" "venv\Scripts\"
    copy "python\Scripts\pip3.12.exe" "venv\Scripts\"
)

:: 验证pip安装
echo 验证pip安装...
"%VIRTUAL_ENV%\Scripts\pip.exe" --version
if %ERRORLEVEL% neq 0 (
    echo Error: pip安装失败
    pause
    exit /b 1
)

echo 安装其他依赖...
"%VIRTUAL_ENV%\Scripts\pip.exe" install customtkinter pillow pyinstaller darkdetect packaging
"%VIRTUAL_ENV%\Scripts\pip.exe" list

:: 下载并安装CMake
<nul set /p =正在下载CMake...
echo.
if not exist "cmake-3.28.1-windows-x86_64.msi" (
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://github.com/Kitware/CMake/releases/download/v3.28.1/cmake-3.28.1-windows-x86_64.msi' -OutFile 'cmake-3.28.1-windows-x86_64.msi'"
)

<nul set /p =正在安装CMake...
echo.
start /wait msiexec /i cmake-3.28.1-windows-x86_64.msi /quiet /norestart
del cmake-3.28.1-windows-x86_64.msi

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
