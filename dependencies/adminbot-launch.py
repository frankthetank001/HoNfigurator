import os
import subprocess
import sys


basename=os.path.basename(sys.argv[0])
exe=basename.split("-")
name=f"{exe[0]}.exe"
subprocess.Popen([name,'adminbot.py'])