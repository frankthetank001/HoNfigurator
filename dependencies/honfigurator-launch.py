import subprocess
python = subprocess.getoutput('where python')
python = python.split("\n")
python = python[0]
subprocess.Popen([python,'honfigurator.py'])