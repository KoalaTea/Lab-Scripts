# GCCIS-IST-LabAutomation
Ensure python2.4 is installed and pip is installed then run either<br>
python -m pip install -r requirements.txt<br>
or<br>
pip install -r requirements.txt<br>

to reset a 3550 to write erased state bypassing a password, ensure the serial cable is plugged into the serial port on the 3550 and the COM is correct in reset.py<br>
then run<br>
python reset.py<br>
and power cycle the 3550 and hold the mode button<br>