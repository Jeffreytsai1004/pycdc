@echo off

:: 激活虚拟环境
call "%VIRTUAL_ENV%\Scripts\activate.bat"

:: 编译
"%VIRTUAL_ENV%\python.exe" -m pyinstaller decompiler.spec --clean


