@echo off

:: 使用 .\python\python.exe
set PYTHON_PATH=.\python\python.exe

:: 激活venv
.\venv\Scripts\activate

python -m PyInstaller decompiler.spec --clean

@echo pause