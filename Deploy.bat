@CALL "%~dp0micromamba.exe" create -n Pycdc python==3.12.2 -c pytorch -c conda-forge -r "%~dp0\" -y
@CALL "%~dp0micromamba.exe" shell init --shell cmd.exe --prefix "%~dp0\"
@CALL condabin\micromamba.bat activate Pycdc
@CALL python -m pip install --upgrade pip
@CALL python -m pip install -r requirements.txt
@Echo 安装7-Zip
@CALL conda install -c conda-forge p7zip
@Echo 安装CMake 3.31.0
@CALL conda install -c conda-forge cmake=3.31.0
@Echo 安装make-3.81
@CALL conda install -c conda-forge make=3.81
@Echo 安装MinGW-w64
@CALL conda install -c conda-forge mingw
@Echo 安装完成
