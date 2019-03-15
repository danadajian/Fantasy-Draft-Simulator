import cx_Freeze
import sys
import os

base = None

if sys.platform == 'win32':
    base = 'Win32GUI'

os.environ['TCL_LIBRARY'] = r"C:\Users\Dan\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\Dan\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6"

include_files = [r"C:\Users\Dan\AppData\Local\Programs\Python\Python36-32\DLLs\tcl86t.dll",
                 r"C:\Users\Dan\AppData\Local\Programs\Python\Python36-32\DLLs\tk86t.dll"]

executables = [cx_Freeze.Executable('src\main\DraftSimulator.py', base=base)]

cx_Freeze.setup(
    name="DraftSimulator",
    options={'build_exe': {'packages': ['tkinter', 'requests', 'bs4', 'idna'], 'include_files': include_files}},
    version="0.01",
    description="Draftsimulator",
    executables=executables
)
