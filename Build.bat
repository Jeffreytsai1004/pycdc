@echo off
echo ��ʼ���� pycdc...

:: ʹ�� .\python\python.exe
set PYTHON_PATH=.\python\python.exe

:: ����venv
.\venv\Scripts\activate

:: ��������Ŀ¼
if not exist build mkdir build
cd build

:: ���� CMake
echo �������� CMake...
cmake -G "MinGW Makefiles" ..

:: ����
echo ���ڱ���...
mingw32-make

:: ��������
if %ERRORLEVEL% neq 0 (
    echo ����ʧ�ܣ�
    cd ..
    pause
    exit /b 1
)

:: ���� Release Ŀ¼�������ļ�
if not exist ..\Release mkdir ..\Release
copy pycdc.exe ..\Release\pycdc.exe

:: ����
cd ..
echo ������ɣ�pycdc.exe �Ѹ��Ƶ� Release Ŀ¼

pause 