import os
import subprocess
import sys
import configparser
from os.path import exists
import shutil
import traceback
from pathlib import Path
import psutil

shutdown = False

def show_exception_and_exit(exc_type, exc_value, tb):
    traceback.print_exception(exc_type, exc_value, tb)
    for p in psutil.process_iter():
        if name in p.name():
            current_pid = os.getpid()
            other_pid = p.pid
            if other_pid != current_pid:
                p.kill()
    raw_input = input(f"Due to the above error, HoNfigurator has failed to launch. Ensure you have all dependencies installed by running <honfigurator-home>\\honfigurator-install-dependencies.bat.")
    sys.exit(-1)
sys.excepthook = show_exception_and_exit

def check_proc(proc_name):
    for proc in psutil.process_iter():
        if proc.name() == proc_name:
            return True
    return False
def get_service(service_name):
    service = None
    try:
        service = psutil.win_service_get(service_name)
        service = service.as_dict()
    except Exception as ex:
        # raise psutil.NoSuchProcess if no service with such name exists
        print(f"{service_name} does not exist")
        return False
        #print(str(ex))
    return service
def stop_proc(proc_name):
    for proc in psutil.process_iter():
        if proc.name() == proc_name:
            proc.kill()
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

app_name = f"adminbot{confDict['svr_id']}"

for i in sys.argv:
    if i == "shutdown":
        terminate_list = [confDict['app_name'],confDict["hon_file_name"]]
        for app in terminate_list:
            for p in psutil.process_iter():
                if app in p.name():
                    p.kill()
        sys.exit(0)
    elif i == "restart":
        service = get_service(app_name)
        if service!= None and service['status'] in ['running','paused','start_pending']:
            subprocess.Popen(['net','stop',f'{app_name}'])
        if check_proc(f"{app_name}.exe"):
            stop_proc(f"{app_name}.exe")

old_adminbot_launch_exe = f"{confDict['sdc_home_dir']}\\adminbot{confDict['svr_id']}-launch_old.exe"
if exists(old_adminbot_launch_exe):
    try:
        os.remove(old_adminbot_launch_exe)
    except:
        print(traceback.format_exc())

basename=os.path.basename(sys.argv[0])
if "-" in basename:
    exe=basename.split("-")
    name=f"{exe[0]}.exe"
else:
    exe=basename.split(".")
    name=f"{exe[0]}{confDict['svr_id']}.exe"
if confDict['use_console'] == 'True':
    print("starting in console mode")
    subprocess.Popen([name,'adminbot.py'])
    sys.exit(0)
elif confDict['use_console'] == 'False':
    print("starting service")
    #os.system(f"net start {app_name}")
    subprocess.Popen(['net','start',f'{app_name}'])
    sys.exit(0)
else:
    sys.exit(1)