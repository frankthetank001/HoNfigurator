import subprocess as sp
import os
import sys

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

def update_dependencies():
    try:
        required = open(f"{application_path}\\..\\dependencies\\requirements.txt").readlines()
        for idx in range(len(required)): required[idx] = required[idx].replace("\n","")
        if len(required) == 0:
            print("unable to get contents of requirements.txt file")
            return False
        installed_packages = sp.run(['pip','freeze'],stdout=sp.PIPE,text=True)
        installed_packages = installed_packages.stdout
        installed_packages_list = installed_packages.split('\n')
        missing = set(required) - set(installed_packages_list)
        if missing:
            python = sp.getoutput('where python')
            python = python.split("\n")
            python = python[0]
            result = sp.run([python, '-m', 'pip', 'install', *missing])
            if result.returncode == 0:
                print(f"SUCCESS, upgraded the following packages: {', '.join(missing)}")
                python = sys.executable
                return result
            else:
                print(f"Error updating packages: {missing}\n error {result.stderr}")
                return result
    except Exception as e:
        print(e)
        return False