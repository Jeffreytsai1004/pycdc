@echo off
echo 正在部署开发环境...

:: 使用 .\python\python.exe
set PYTHON_PATH=.\python\python.exe

:: 使用 .\python\python.exe在本路径下新建venv
%PYTHON_PATH% -m venv venv

:: 激活venv
.\venv\Scripts\activate

:: 检查 pip 并安装 pip,如果未安装pip则安装pip
python -m ensurepip
:: 如果pip未安装则安装pip
if %ERRORLEVEL% neq 0 (
    python -m pip install --upgrade pip
)
else (
    echo pip 已安装
)

:: 安装必要的 Python 包
echo 正在安装 Python 包...
pip install customtkinter
pip install pillow
pip install pyinstaller
pip install darkdetect
pip install packaging

:: 检查 CMake
where cmake >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo 未找到 CMake，正在下载...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/Kitware/CMake/releases/download/v3.28.1/cmake-3.28.1-windows-x86_64.msi' -OutFile 'cmake-installer.msi'}"
    echo 正在安装 CMake...
    start /wait msiexec /i cmake-installer.msi /quiet
    del cmake-installer.msi
)

:: 检查 MinGW-w64
where gcc >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo 未找到 MinGW-w64，正在下载...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/niXman/mingw-builds-binaries/releases/download/13.2.0-rt_v11-rev0/x86_64-13.2.0-release-posix-seh-msvcrt-rt_v11-rev0.7z' -OutFile 'mingw64.7z'}"
    
    :: 检查 7zip
    where 7z >nul 2>nul
    if %ERRORLEVEL% neq 0 (
        echo 正在下载 7zip...
        powershell -Command "& {Invoke-WebRequest -Uri 'https://www.7-zip.org/a/7z2301-x64.exe' -OutFile '7z-installer.exe'}"
        echo 正在安装 7zip...
        start /wait 7z-installer.exe /S
        del 7z-installer.exe
    )
    
    echo 正在解压 MinGW-w64...
    "C:\Program Files\7-Zip\7z.exe" x mingw64.7z -oC:\mingw64 -y
    del mingw64.7z
    
    :: 添加到环境变量
    setx PATH "%PATH%;C:\mingw64\mingw64\bin" /M
    echo MinGW-w64 已安装到 C:\mingw64\mingw64
    echo 请重新打开命令提示符以使环境变量生效
)

echo 环境部署完成！
echo 请确保重新打开命令提示符以使所有更改生效。
pause