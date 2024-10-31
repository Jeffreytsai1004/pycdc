# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_all, collect_submodules
from PIL import Image  # 需要安装 pillow: pip install pillow

# 转换 PNG 到 ICO
png_path = os.path.join('icon', 'logo.png')
ico_path = os.path.join('icon', 'logo.ico')

if os.path.exists(png_path):
    print(f"找到PNG图标: {png_path}")
    if not os.path.exists(os.path.dirname(ico_path)):
        os.makedirs(os.path.dirname(ico_path))
    
    # 如果 ICO 文件不存在或 PNG 文件比 ICO 文件新，则转换
    if not os.path.exists(ico_path) or os.path.getmtime(png_path) > os.path.getmtime(ico_path):
        try:
            print("正在转换图标...")
            img = Image.open(png_path)
            # 确保图像是正方形
            size = max(img.size)
            new_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            # 将原图像粘贴到中心
            offset = ((size - img.size[0]) // 2, (size - img.size[1]) // 2)
            new_img.paste(img, offset)
            # 保存为多尺寸的 ICO 文件
            new_img.save(ico_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
            print(f"图标已保存到: {ico_path}")
        except Exception as e:
            print(f"警告: 无法转换图标: {e}")
else:
    print(f"警告: 未找到图标文件: {png_path}")

# 检查 pycdc.exe 是否存在
pycdc_path = os.path.join('build', 'Release', 'pycdc.exe')
if not os.path.exists(pycdc_path):
    raise FileNotFoundError(f"找不到 pycdc.exe，请确保文件位于: {os.path.abspath(pycdc_path)}")

# Python embed 包路径
python_embed_dir = os.path.join(".", "python")
if not os.path.exists(python_embed_dir):
    raise FileNotFoundError(f"找不到 Python embed 包: {os.path.abspath(python_embed_dir)}")

block_cipher = None

# 收集 customtkinter 的所有依赖
customtkinter_datas = []
customtkinter_binaries = []
customtkinter_hiddenimports = []

# 收集 customtkinter 的所有模块和资源
ckts = collect_all('customtkinter')
customtkinter_datas.extend(ckts[0])
customtkinter_binaries.extend(ckts[1])
customtkinter_hiddenimports.extend(ckts[2])

# 基本依赖
binaries = []
datas = [(pycdc_path, '.')]
datas.extend(customtkinter_datas)  # 添加 customtkinter 数据文件

hiddenimports = [
    'tkinter',
    '_tkinter',
    'tkinter.ttk',
    'tkinter.messagebox',
    'tkinter.filedialog',
    'customtkinter',
    'darkdetect',  # customtkinter 依赖
    'typing',
    'packaging',
    'packaging.version',
    'packaging.specifiers',
    'packaging.requirements',
]
hiddenimports.extend(customtkinter_hiddenimports)  # 添加 customtkinter 隐藏导入

# 添加 Python embed 包中的 DLL
python_dlls = [
    'python312.dll',
    'vcruntime140.dll',
    'python3.dll',
    'select.pyd',
    '_socket.pyd',
    '_decimal.pyd',
    '_multiprocessing.pyd',
    '_ctypes.pyd',
    '_queue.pyd',
    '_ssl.pyd',
    '_hashlib.pyd',
    'unicodedata.pyd',
]

for dll in python_dlls:
    dll_path = os.path.join(python_embed_dir, dll)
    if os.path.exists(dll_path):
        binaries.append((dll_path, '.'))
    else:
        print(f"警告: 未找到 {dll}")

# 添加 tcl/tk 支持
tcl_tk_files = []

# 从 Python 安装目录获取 DLL
python_dlls_dir = os.path.join(sys.base_prefix, 'DLLs')
if os.path.exists(python_dlls_dir):
    tcl_dll = os.path.join(python_dlls_dir, 'tcl86t.dll')
    tk_dll = os.path.join(python_dlls_dir, 'tk86t.dll')
    if os.path.exists(tcl_dll):
        binaries.append((tcl_dll, '.'))
    if os.path.exists(tk_dll):
        binaries.append((tk_dll, '.'))

# 获取 tcl/tk 库文件
tcl_lib = os.path.join(sys.base_prefix, 'tcl')
if os.path.exists(tcl_lib):
    # tcl8.6
    tcl_path = os.path.join(tcl_lib, 'tcl8.6')
    if os.path.exists(tcl_path):
        for root, dirs, files in os.walk(tcl_path):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(root, tcl_lib)
                datas.append((full_path, rel_path))
    
    # tk8.6
    tk_path = os.path.join(tcl_lib, 'tk8.6')
    if os.path.exists(tk_path):
        for root, dirs, files in os.walk(tk_path):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(root, tcl_lib)
                datas.append((full_path, rel_path))

# 如果找不到系统安装的 tcl/tk，尝试从 embed 包中获取
if not any(binary[1] == '.' and 'tcl86t.dll' in binary[0] for binary in binaries):
    embed_dlls_dir = os.path.join(python_embed_dir, 'DLLs')
    if os.path.exists(embed_dlls_dir):
        tcl_dll = os.path.join(embed_dlls_dir, 'tcl86t.dll')
        tk_dll = os.path.join(embed_dlls_dir, 'tk86t.dll')
        if os.path.exists(tcl_dll):
            binaries.append((tcl_dll, '.'))
        if os.path.exists(tk_dll):
            binaries.append((tk_dll, '.'))

# 如果找不到系统的 tcl/tk 库文件，尝试从 embed 包中获取
embed_tcl_lib = os.path.join(python_embed_dir, 'Lib', 'tcl8.6')
embed_tk_lib = os.path.join(python_embed_dir, 'Lib', 'tk8.6')

if os.path.exists(embed_tcl_lib):
    for root, dirs, files in os.walk(embed_tcl_lib):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(root, os.path.dirname(embed_tcl_lib))
            datas.append((full_path, rel_path))

if os.path.exists(embed_tk_lib):
    for root, dirs, files in os.walk(embed_tk_lib):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(root, os.path.dirname(embed_tk_lib))
            datas.append((full_path, rel_path))

binaries.extend(customtkinter_binaries)  # 添加 customtkinter 二进制文件

# 添加图标文件到数据文件
icon_dir = os.path.join('icon')
if os.path.exists(icon_dir):
    datas.append((icon_dir, 'icon'))

a = Analysis(
    ['decompiler_gui.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    cipher=block_cipher,
    noarchive=False,
)

print(f"正在打包 pycdc.exe: {pycdc_path} -> {os.path.join(DISTPATH, 'pycdc.exe')}")

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Python反编译工具',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join('icon', 'logo.ico'),  # 直接指定图标路径
)

# 打印完成信息
print("\n打包完成!")
print(f"输出目录: {DISTPATH}")
print(f"可执行文件: {os.path.join(DISTPATH, 'Python反编译工具.exe')}") 