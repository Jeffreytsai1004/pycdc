# Build Steps
1 Install [Python](https://www.python.org/downloads/release/python-3127/）
2 Install [CMake](https://cmake.org/download/)
3 Install [Make](https://blog.csdn.net/weixin_41896770/article/details/131262178?ops_request_misc=%257B%2522request%255Fid%2522%253A%252224C61B1D-5EF3-439D-9603-3C31BA8BD42F%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=24C61B1D-5EF3-439D-9603-3C31BA8BD42F&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-2-131262178-null-null.142^v100^pc_search_result_base9&utm_term=make%20windows)
4 Clone the repositories
```
git clone https://github.com/zrax/pycdc.git
```
5 Install Dependencies
```
python -m pip install -r requirements.txt
```
5 Build pycdc.exe
```
cd pycdc
mkdir build && cd build
cmake ..
make
```
6 Build your webui
```
python -m PyInstaller decompiler.spec
```

# Decompyle++ 
***A Python Byte-code Disassembler/Decompiler***

Decompyle++ aims to translate compiled Python byte-code back into valid
and human-readable Python source code. While other projects have achieved
this with varied success, Decompyle++ is unique in that it seeks to
support byte-code from any version of Python.

Decompyle++ includes both a byte-code disassembler (pycdas) and a 
decompiler (pycdc).

As the name implies, Decompyle++ is written in C++.
If you wish to contribute, please fork us on github at 
https://github.com/zrax/pycdc

## Building Decompyle++
* Generate a project or makefile with [CMake](http://www.cmake.org) (See CMake's documentation for details)
  * The following options can be passed to CMake to control debug features:

    | Option | Description |
    | --- | --- |
    | `-DCMAKE_BUILD_TYPE=Debug` | Produce debugging symbols |
    | `-DENABLE_BLOCK_DEBUG=ON` | Enable block debugging output |
    | `-DENABLE_STACK_DEBUG=ON` | Enable stack debugging output |

* Build the generated project or makefile
  * For projects (e.g. MSVC), open the generated project file and build it
  * For makefiles, just run `make`
  * To run tests (on \*nix or MSYS), run `make check JOBS=4` (optional
    `FILTER=xxxx` to run only certain tests)

## Usage
**To run pycdas**, the PYC Disassembler:
`./pycdas [PATH TO PYC FILE]`
The byte-code disassembly is printed to stdout.

**To run pycdc**, the PYC Decompiler: 
`./pycdc [PATH TO PYC FILE]`
The decompiled Python source is printed to stdout.
Any errors are printed to stderr.

**Marshalled code objects**:
Both tools support Python marshalled code objects, as output from `marshal.dumps(compile(...))`.

To use this feature, specify `-c -v <version>` on the command line - the version must be specified as the objects themselves do not contain version metadata.

## Authors, Licence, Credits
Decompyle++ is the work of Michael Hansen and Darryl Pogue.

Additional contributions from:
* charlietang98
* Kunal Parmar
* Olivier Iffrig
* Zlodiy

It is released under the terms of the GNU General Public License, version 3;
See LICENSE file for details.
