# Fantasy-Draft-Simulator

Python Dependencies:
* requests
* bs4

To create exectuable app in Terminal:
* pyinstaller --windowed myapp.py
* cd dist/myapp.app/Contents/MacOs
* mkdir tcl tk
* cp -R /Library/Frameworks/Python.framework/Versions/3.7/lib/tcl* tcl/
* cp -R /Library/Frameworks/Python.framework/Versions/3.7/lib/tk* tk/
* cp -R /Library/Frameworks/Python.framework/Versions/3.7/lib/Tk* tk/ 