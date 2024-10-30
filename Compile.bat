@CALL "%~dp0micromamba.exe" shell init --shell cmd.exe --prefix "%~dp0\"
@CALL condabin\micromamba.bat activate Pycdc
@CALL pyinstaller decompiler.spec --clean
