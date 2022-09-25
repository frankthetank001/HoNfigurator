import os
import subprocess
import sys
import configparser
from os.path import exists
import shutil

dir=os.path.dirname(sys.argv[0])
os.chdir(dir)

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