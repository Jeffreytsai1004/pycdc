@CALL "%~dp0micromamba.exe" shell init --shell cmd.exe --prefix "%~dp0\"
@CALL condabin\micromamba.bat activate Pycdc
@REM 使用CMake编译Pycdc.exe
@CALL cmake -BRelease -H.
@CALL cmake --build Release
