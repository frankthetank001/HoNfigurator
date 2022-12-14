import os
import subprocess
import sys
import configparser
from os.path import exists
import shutil
import traceback
from pathlib import Path

def show_exception_and_exit(exc_type, exc_value, tb):
    traceback.print_exception(exc_type, exc_value, tb)
    raw_input = input(f"Due to the above error, HoNfigurator has failed to launch. Ensure you have all dependencies installed by running <honfigurator-home>\\honfigurator-install-dependencies.bat.")
    sys.exit(-1)
sys.excepthook = show_exception_and_exit

try:
    dir=os.path.dirname(sys.argv[0])
    os.chdir(dir)
except:
    pass

print(os.getcwd())
conf_parse_global = configparser.ConfigParser()
conf_parse_local = configparser.ConfigParser(interpolation=None)

if exists("config\\local_config.ini.incoming"):
    try:
        shutil.move("config\\local_config.ini.incoming","config\\local_config.ini")
    except Exception as e: print(e)
if exists("config\\global_config.ini.incoming"):
    try:
        shutil.move("config\\global_config.ini.incoming","config\\global_config.ini")
    except Exception as e: print(e)

conf_parse_local.read("config\\local_config.ini")
conf_parse_global.read("config\\global_config.ini")
confDict = {}
for option in conf_parse_local.options("OPTIONS"):
    confDict.update({option:conf_parse_local['OPTIONS'][option]})
for option in conf_parse_global.options("OPTIONS"):
    confDict.update({option:conf_parse_global['OPTIONS'][option]})

old_adminbot_launch_exe = f"{confDict['sdc_home_dir']}\\adminbot{confDict['svr_id']}-launch_old.exe"
if exists(old_adminbot_launch_exe):
    try:
        os.remove(old_adminbot_launch_exe)
    except:
        print(traceback.format_exc())

app_name = f"adminbot{confDict['svr_id']}"
basename=os.path.basename(sys.argv[0])
exe=basename.split("-")
name=f"{exe[0]}.exe"
if confDict['use_console'] == 'True':
    print("starting in console mode")
    subprocess.Popen([name,'adminbot.py'])
    sys.exit(0)
elif confDict['use_console'] == 'False':
    print("starting service")
    os.system(f"net start {app_name}")
    sys.exit(0)
else:
    sys.exit(1)