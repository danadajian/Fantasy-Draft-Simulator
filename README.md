# Fantasy-Draft-Simulator

Python Dependencies:
* requests
* bs4

To create exectuable app on Windows (Command Prompt):
* Run in terminal in pip location:
	* pip install cx_Freeze
* If you encounter an error, try:
	* pip install --upgrade git+https://github.com/anthony-tuininga/cx_Freeze.git@master
* Alter setup.py file to contain correct paths to your Python location
* Run in terminal in \Fantasy-Draft-Simulator:
	* setup.py build
* A new build folder will be created; navigate here and open the subfolder
* Right click on DraftSimulator > Create Shortcut
* You now have a fully exectuable shortcut!

To create exectuable app on Mac (Terminal):
* Run in terminal in pip location:
    * pip install pyinstaller
* Run in terminal in /Fantasy-Draft-Simulator:
	* pyinstaller --windowed src/main/DraftSimulator.py
	* cd dist/DraftSimulator.app/Contents/MacOs
	* mkdir tcl tk
* Alter the below paths to your local specifications and then run in terminal:
	* cp -R /Library/Frameworks/Python.framework/Versions/3.7/lib/tcl* tcl/
	* cp -R /Library/Frameworks/Python.framework/Versions/3.7/lib/tk* tk/
	* cp -R /Library/Frameworks/Python.framework/Versions/3.7/lib/Tk* tk/
* Navigate to /dist and DraftSimulator.app is now a fully exectuable shortcut! 