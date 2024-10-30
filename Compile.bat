@echo off
chcp 65001 > nul

:: 激活虚拟环境
call .\venv\activate.bat
<nul set /p =虚拟环境已激活
echo.

:: 使用PyInstaller编译
<nul set /p =正在编译...
echo.
python -m PyInstaller decompiler.spec --clean

<nul set /p =编译完成！
echo.
pause