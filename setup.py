import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["pygame", "random"],
                     "excludes": ["numpy", "pytz", "asyncio", "concurrent", "ctypes", "distutils", "email", "html",
                                  "http", "json", "logging", "multiprocessing", "neat", "pkg_resources", "pydoc_data",
                                  "test", "tkinter", "unittest", "urllib", "xmlrpc"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Sudoku",
    options={"build_exe": build_exe_options},
    version="2.0",
    description='David Lu',
    executables=[Executable("Sudoku.py", base=base, icon='data\\sudoku.ico')]
)




