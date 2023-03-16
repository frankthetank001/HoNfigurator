#import pkg_resources

import sys
import subprocess as sp
import os
import cogs.setupEnv as setup
import traceback
from sys import stdout
from sys import stderr


# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

def show_exception_and_exit(exc_type, exc_value, tb):
    traceback.print_exception(exc_type, exc_value, tb)
    try:
        os.chdir(application_path)
    except Exception:
        print(traceback.format_exc())
    def git_pull():
        output = sp.run(["git", "pull"],stdout=sp.PIPE,stderr=sp.PIPE,text=True)
        return output
    def git_reset():
        output = sp.run(["git", "reset", "--hard"],stdout=sp.PIPE,stderr=sp.PIPE,text=True)
        return output
    print("Trying to attempt to update honfigurator to fix this...")
    output = git_pull()
    if 'updating' in output.stdout:
        print(output.stdout)
        print("updated honfigurator.. attempting restart")
        python = sys.executable
        os.execl(python, '"' + python + '"', *sys.argv)
    elif 'local changes' in output.stderr:
        print(output.stderr)
        raw_input = None
        while (raw_input not in ('y','n')):
            raw_input = input(f"There were errors attempting to recover honfigurator. You have local changes. Would you like to discard the local changes and update honfigurator? (y/n)")
        if raw_input.lower() == 'y':
            output = git_reset()
            if 'HEAD is now at' in output.stdout:
                git_pull()
                python = sys.executable
                os.execl(python, '"' + python + '"', *sys.argv)
        elif raw_input.lower() == 'n':
            print("exiting code then until local changes are sorted out.")
            time.sleep(3)
            sys.exit(0)
    if 'already up to date' in output.stdout.lower():
        error_msg = f"Warning: Although HoNfigurator is up-to-date with the upstream github repository, there is some issue preventing the launch locally on this computer. Please provide a screenshot of the above errors to @FrankTheGodDamnMotherFuckenTank#8426"
    else:
        error_msg=f"Warning: HoNfigurator has failed to update and self repair."
    raw_input = input(stderr.write(error_msg))
    sys.exit()
sys.excepthook = show_exception_and_exit
packages_updated = setup.update_dependencies()
if packages_updated:
    if packages_updated.returncode == 0:
        print("Relaunching code...")
        python = sys.executable
        os.execl(python, '"' + python + '"', *sys.argv)
from asyncio.subprocess import DEVNULL
import tkinter as tk
from tkinter import Button,Label,Entry
from tkinter import getboolean, ttk
import configparser
import psutil
import socket
from asyncio.windows_events import NULL
import time
from os.path import exists
import shutil
from tkinter import PhotoImage
from tkinter.ttk import Notebook
import ctypes
from tkinter import END
import distutils
from distutils import dir_util
from threading import Thread
import git
from python_hosts import Hosts, HostsEntry
from functools import partial
# import tracemalloc
# import linecache
import gc
#from pympler.tracker import SummaryTracker
#from mem_top import mem_top

import winreg
try:
    import speedtest
except Exception:
    print(traceback.format_exc())

i=0
for proc in psutil.process_iter():
    if proc.name() == "honfigurator.exe":
        i+=1
if i > 2:
    sys.exit()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False
if is_admin():

    #tracemalloc.start(25)
    exp = f'setx HONFIGURATOR_DIR \"{application_path}\"'
    sp.Popen(exp, shell=True).wait()

    class TextRedirector(object):
        def __init__(self, widget, tag="stdout"):
            self.widget = widget
            self.tag = tag

        def write(self, str):
            self.widget.configure(state="normal")
            self.widget.insert("end", str, (self.tag,))
            self.widget.configure(state="disabled")
    config_global = os.path.abspath(application_path)+"\\config\\global_config.ini"
    config_default = f"{os.path.abspath(application_path)}\\config\\default_config.ini"
    config_local = os.path.abspath(application_path)+"\\config\\local_config.ini"
    if not exists(config_local):
        shutil.copy(config_default,config_local)
    import cogs.server_status as svrcmd
    import cogs.dataManager as dmgr
    
    global hon_api_updated
    first_check_complete = False
    first_time_installed = False
    #
    #   This changes the taskbar icon by telling windows that python is not an app but an app hoster
    #   Otherwise taskbar icon will be python shell icon
    myappid = 'honfiguratoricon.1.0' # arbitrary string
    num_rows_file = f"{application_path}\\config\\num_server_rows"
    if exists(num_rows_file):
        try:
            mod_by = open(num_rows_file).readline()
            mod_by = int(mod_by)
        except:
            mod_by=13
    else:
        mod_by=13
    # auto_refresh_var = False
    bot_tab=0
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    hon_api_updated = False
    players_connected = False
    auto_refresh_delay = 1
    update_delay = 180 / auto_refresh_delay
    update_counter = 0
    refresh_counter = 0
    refresh_delay = 40 / auto_refresh_delay
    updating = False
    first_tab_switch = True
    server_admin_loading = False
    svr_total = 0

    # lists
    btnlist = {}
    labllist = {}
    labllistrows = {}
    labllistcols = {}
    btnlistrows = {}
    btnlistcols = {}
    #
    #
    class initialise():
        global config_global
        global config_local
        global deployed_status
        #global deployed_status
        def __init__(self,data):
            global app_name
            self.data = dmgr.mData()
            #self.dataDict = self.data.returnDict()
            self.dataDict = data
            #self.startup = initialise.get_startupcfg(self)
            self.nssm = self.dataDict['nssm_exe']
            self.hon_directory = self.dataDict['hon_directory']
            self.hon_game_dir = self.dataDict['hon_game_dir']
            self.sdc_home_dir = self.dataDict['sdc_home_dir']
            self.hon_logs_dir = self.dataDict['hon_logs_dir']
            self.hon_home_dir = self.dataDict['hon_home_dir']
            self.svr_hoster = self.dataDict['svr_hoster']
            #self.svr_region = self.dataDict['svr_region']
            self.svr_region_short = self.dataDict['svr_region_short']
            self.svr_id = self.dataDict['svr_id']
            self.svr_ip = self.dataDict['svr_ip']
            self.svr_total = self.dataDict['svr_total']
            self.bot_token = self.dataDict['token']
            self.pythonLoc = self.dataDict['python_location']
            # self.master_user = self.dataDict['master_user']
            # self.master_pass = self.dataDict['master_pass']
            self.service_name_bot = f"adminbot{self.svr_id}"
            self.service_name_api = "honserver-registration"
            deployed_config = self.sdc_home_dir+"\\config\\global_config.ini"
            if exists(f"{self.dataDict['sdc_home_dir']}\\config\\local_config.ini"):
                self.deployed_status = self.data.returnDict_deployed(self.svr_id)
            if exists(deployed_config):
                config = configparser.ConfigParser()
                config.read(deployed_config)
                self.ver_existing = config['OPTIONS']['bot_version']
                try:
                    self.ver_existing = float(self.ver_existing)
                except Exception: pass
            else:
                self.ver_existing = 0
            if exists(config_global):
                config = configparser.ConfigParser()
                config.read(config_global)
                self.ver_current = config['OPTIONS']['bot_version']
                try:
                    self.ver_current = float(self.ver_current)
                except Exception: pass
            else:
                self.ver_current = 0

            #app_name=f"adminbot{self.dataDict['svr_id']}"
            app_name=f"adminbot"
            # if exists(f"{self.sdc_home_dir}\\config\\local_config.ini"):
            #     config = configparser.ConfigParser()
            #     config.read(f"{self.sdc_home_dir}\\config\\local_config.ini")
            # return
        def start_bot(self,deployed):
            #start_bot = sp.Popen(['cmd',"python",f"{self.dataDict['sdc_home_dir']}\\sdc.py"])
            if deployed:
                try:
                    if deployed_status['svr_id'] not in deployed_status['sdc_home_dir']:
                        deployed_status.update({'sdc_home_dir':f"{deployed_status['hon_home_dir']}\\Documents\\Heroes of Newerth x64\\game\\logs\\adminbot{deployed_status['svr_id']}"})
                    os.chdir(deployed_status['sdc_home_dir'])
                    #os.startfile(f"adminbot{deployed_status['svr_id']}-launch.exe")
                    Thread(target=os.startfile,args=[f"{deployed_status['sdc_home_dir']}\\adminbot{deployed_status['svr_id']}-launch.exe"]).start()
                    #sp.Popen([f"adminbot{deployed_status['svr_id']}-launch.exe"])
                    try:
                        os.chdir(application_path)
                    except Exception:
                        print(traceback.format_exc())
                    return True
                except Exception:
                    print(traceback.format_exc())
                    return False
            else:
                try:
                    os.chdir(self.dataDict['sdc_home_dir'])
                    #os.startfile(f"adminbot{self.dataDict['svr_id']}-launch.exe")
                    Thread(target=os.startfile,args=[f"{self.dataDict['sdc_home_dir']}\\adminbot{self.dataDict['svr_id']}-launch.exe"]).start()
                    #sp.Popen([f"adminbot{self.dataDict['svr_id']}-launch.exe"])
                    try:
                        os.chdir(application_path)
                    except Exception:
                        print(traceback.format_exc())
                    return True
                except Exception:
                    print(traceback.format_exc())
                    return False
        def check_proc(proc_name):
            for proc in psutil.process_iter():
                if proc.name() == proc_name:
                    return True
            return False
        def check_proc_count(proc_name):
            i=0
            for proc in psutil.process_iter():
                if proc.name() == proc_name:
                    i+=1
            return i
        def stop_bot(self,proc_name):
            for proc in psutil.process_iter():
                if proc.name() == proc_name:
                    proc.kill()
        def upload_speed():
            def bytes_to_mb(bytes):
                KB = 1024 # One Kilobyte is 1024 bytes
                MB = KB * 1024 # One MB is 1024 KB
                return int(bytes/MB)
            speed_test = speedtest.Speedtest()
            upload_speed = bytes_to_mb(speed_test.upload())
            print("Your upload speed is", upload_speed, "MB")
            return upload_speed
        def add_hosts_entry(self):
            global ip_addr

            hosts = Hosts(path='c:\\windows\\system32\\drivers\\etc\\hosts')
            mserver = self.dataDict['master_server']
            add_mserver=False
            ip_addr = None
            if ":" in mserver:
                mserver = mserver.split(":")
                mserver = mserver[0]
            try:
                ip_addr = socket.gethostbyname(mserver)
            except Exception:
                print(traceback.format_exc())
                import wmi
                c = wmi.WMI()
                x = c.Win32_PingStatus(Address=mserver)
                ip_addr = (x[0].ProtocolAddress)
                print(ip_addr)
            try:
                process = sp.run(["nslookup", mserver], stdout=sp.PIPE, text=True)
                output = process.stdout
                output = output.split('\n')
                ip_arr = []
                for data in output:
                    if 'Address' in data:
                        ip_arr.append(data.replace('Address: ',''))
                ip_arr.pop(0)
                if len(ip_arr) == 0:
                    add_mserver=True
                print (ip_arr)
            except Exception:
                print(traceback.format_exc())
            if ip_addr == None or ip_addr == '':
                if 'kongor.online' in mserver:
                    ip_addr = "73.185.77.188"
                else: return False
                print(f"Problem obtaining IP. Adding last known IP to hosts file {ip_addr}")
            if add_mserver:
                hosts.remove_all_matching(name='client.sea.heroesofnewerth.com')
                hosts.write()
                if 'kongor.online' in mserver:
                    add_entry = HostsEntry(entry_type='ipv4', address=ip_addr, names=[f'client.sea.heroesofnewerth.com  {mserver} kongor.online  #required by hon as this address is frequently used to poll for match stats'])
                else:
                    add_entry = HostsEntry(entry_type='ipv4', address=ip_addr, names=[f'client.sea.heroesofnewerth.com  {mserver}  #required by hon as this address is frequently used to poll for match stats'])
            else:
                hosts.remove_all_matching(name='client.sea.heroesofnewerth.com')
                hosts.write()
                add_entry = HostsEntry(entry_type='ipv4', address=ip_addr, names=['client.sea.heroesofnewerth.com    #required by hon as this address is frequently used to poll for match stats'])
            hosts.add([add_entry])
            hosts.write()
        def KOTF(self):
            app_svr_desc = sp.run([f'{application_path}\\cogs\\keeper.exe'],stdout=sp.PIPE, text=True)
            rc = app_svr_desc.returncode
            result = str(app_svr_desc.stdout)
            if rc == 0:
                print("hashes checked OK")
                return result
            elif rc == 1:
                print(b"ERROR CHECKING HASHES, please obtain correct server binaries")
                tex.insert(END,"ERROR CHECKING HASHES, please obtain correct server binaries\n",'warning')
                tex.insert(END,"continuing anyway")
                tex.see(tk.END)
                # returning true as I have no idea what the right hashes should be anymore
                return True
            elif rc == 3:
                print("ERROR GETTING MAC ADDR")
                tex.insert(END,"ERROR GETTING MAC ADDR\n",'warning')
                tex.see(tk.END)
                # returning true as I have no idea what the right hashes should be anymore
                return True
        # Task scheduler for updating honfigurator, didn't quite work as I wanted.
        # def getstatus_updater(self,auto_update,selected_branch):
        #     TASK_ENUM_HIDDEN = 1
        #     TASK_STATE = {0: 'Unknown',
        #                 1: 'Disabled',
        #                 2: 'Queued',
        #                 3: 'Ready',
        #                 4: 'Running'}

        #     scheduler = win32com.client.Dispatch('Schedule.Service')
        #     scheduler.Connect()

        #     n = 0
        #     folders = [scheduler.GetFolder('\\')]
        #     while folders:
        #         folder = folders.pop(0)
        #         folders += list(folder.GetFolders(0))
        #         tasks = list(folder.GetTasks(TASK_ENUM_HIDDEN))
        #         for task in tasks:
        #             if task.name == "HoNfigurator Updater":
        #                 # settings = task.Definition.Settings
        #                 # print('Path       : %s' % task.Path)
        #                 # print('Hidden     : %s' % settings.Hidden)
        #                 # print('State      : %s' % TASK_STATE[task.State])
        #                 # print('Last Run   : %s' % task.LastRunTime)
        #                 # print('Last Result: %s\n' % task.LastTaskResult)
        #                 if TASK_STATE[task.State] == "Ready" and auto_update == False:
        #                     p = sp.Popen(['SCHTASKS', '/CHANGE', '/TN', task.Path,"/DISABLE"],stdout=sp.PIPE, stderr=sp.PIPE)
        #                     return True
        #                 elif TASK_STATE[task.State] == "Disabled" and auto_update == True:
        #                     p = sp.Popen(['SCHTASKS', '/CHANGE', '/TN', task.Path,"/ENABLE"],stdout=sp.PIPE, stderr=sp.PIPE)
        #                     return False
        #                 return
        #         else: 
        #             if auto_update == True:
        #                 initialise.register_updater(self,selected_branch)
        #                 return True
        #             else:
        #                 return False
        def update_repository(self,selected_branch):
            repo = git.Repo(search_parent_directories=True)
            current_branch = repo.active_branch  # 'master'
            current_branch = current_branch.name
            if selected_branch != current_branch:
                checkout = sp.run(["git","checkout",selected_branch],stdout=sp.PIPE,stderr=sp.PIPE, text=True)
                if checkout.returncode == 0:
                    print(f"Repository: {selected_branch}\nCheckout status: {checkout.stdout}")
                    tex.insert(END,f"Repository: {selected_branch}\nCheckout Status: {checkout.stdout}")
                    print(f"Updating selected repository: {selected_branch} branch")
                    output = sp.run(["git", "pull"],stdout=sp.PIPE, text=True)
                    print(f"Repository: {selected_branch}\nUpdate Status: {output.stdout}")
                    tex.insert(END,f"Repository: {selected_branch}\nUpdate Status: {output.stdout}")
                    tex.see(tk.END)
                    return True
                else:
                    print(f"Repository: {selected_branch}\nCheckout status: {checkout.stderr}")
                    tex.insert(END,f"Repository: {selected_branch}\nCheckout Status ({checkout.returncode}): {checkout.stderr}")
                    if 'Please commit your changes or stash them before you switch branches.' in checkout.stderr:
                        print()
                    tex.see(tk.END)
                    return False
            else:
                print(f"Updating selected repository: {selected_branch} branch")
                output = sp.run(["git", "pull"],stdout=sp.PIPE, text=True)
                print(f"Repository: {selected_branch}\nUpdate Status: {output.stdout}")
                tex.insert(END,f"Repository: {selected_branch}\nUpdate Status: {output.stdout}")
                tex.see(tk.END)
                return output.returncode
        def get_startupcfg(self):
            config_startup = dmgr.mData().parse_config(os.path.abspath(application_path)+"\\config\\honfig.ini")
            return config_startup
        def get_service(service_name):
            service = None
            try:
                service = psutil.win_service_get(service_name)
                service = service.as_dict()
            except Exception:
                # raise psutil.NoSuchProcess if no service with such name exists
                return False
                #print(str(ex))
            return service
        def disable_service(service_name):
            #doesnt work
            os.system(f'net disable "{service_name}"')
        def playerCount(self):
            check = sp.Popen([self.dataDict['player_count_exe_loc'],self.dataDict['hon_file_name']],stdout=sp.PIPE, text=True)
            i = int(check.stdout.read())
            if i == -3 and self.dataDict['master_server'] == "honmasterserver.com":
                try:
                    check = sp.Popen([self.dataDict['player_count_exe_loc'],f"KONGOR_ARENA_{self.svr_id}.exe"],stdout=sp.PIPE, text=True)
                    i = int(check.stdout.read())
                except Exception: pass
            elif i == -3 and 'kongor.online' in self.dataDict['master_server']:
                try:
                    check = sp.Popen([self.dataDict['player_count_exe_loc'],f"HON_SERVER_{self.svr_id}.exe"],stdout=sp.PIPE, text=True)
                    i = int(check.stdout.read())
                except Exception: pass
            check.terminate()
            return i
        def check_port(port):
            result = os.system(f'netstat -oan |findstr 0.0.0.0:{port}')
            if result == 0:
                print(f"Port {int(port)} is open")
                #tex.insert(END,f"Port {int(port)} is open\n")
                return True
            else:
                print(f"Port {int(port)} is not open")
                tex.insert(END,f"Port {int(port)} is not open\n",'warning')
                tex.see(tk.END)
                return False
        def attempt_stop_server(self):
            print()
        def playerCountX(self,svr_id):
            pcount=-3
            if self.dataDict['master_server'] == "honmasterserver.com":
                exe = f"HON_SERVER_{svr_id}.exe"
            else:
                exe = f"KONGOR_ARENA_{svr_id}.exe"
            for proc in psutil.process_iter():
                if proc.name() == exe:
                    check = sp.Popen([self.dataDict['player_count_exe_loc'],str(proc.pid)],stdout=sp.PIPE, text=True)
                    i = int(check.stdout.read())
                    if i == -3 and self.dataDict['master_server'] == "honmasterserver.com":
                        try:
                            check = sp.Popen([self.dataDict['player_count_exe_loc'],f"KONGOR_ARENA_{svr_id}.exe"],stdout=sp.PIPE, text=True)
                            i = int(check.stdout.read())
                        except Exception: pass
                    elif i == -3 and 'kongor.online' in self.dataDict['master_server']:
                        try:
                            check = sp.Popen([self.dataDict['player_count_exe_loc'],f"HON_SERVER_{svr_id}.exe"],stdout=sp.PIPE, text=True)
                            i = int(check.stdout.read())
                        except Exception: pass
                    if i != -1:
                        pcount = i
                    check.terminate()
            return pcount
        def start_service(self,service_name,deployed):
            try:
                #os.system(f'net start "{service_name}"')
                if deployed:
                    sp.Popen(['net','start',f'{service_name}'])
                else:
                    sp.run(['net','start',f'{service_name}'])
            except Exception:
                print ('could not start service {}'.format(service_name))
                return False
            return True
        def stop_service(self,service_name,deployed):
            try:
                if deployed:
                    res = sp.Popen(['net','stop',f'{service_name}'])
                else:
                    res = sp.run(['net','stop',f'{service_name}'])
            except Exception:
                print ('could not stop service {}'.format(service_name))
                return False
            return True
        def is_tool(name):
            """Check whether `name` is on PATH and marked as executable."""

            # from whichcraft import which
            from shutil import which

            return which(name) is not None
        def set_reg(name, value, reg_path):
            try:
                winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
                registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, 
                                            winreg.KEY_WRITE)
                winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
                winreg.CloseKey(registry_key)
                return True
            except WindowsError:
                return False
        def get_reg(name,reg_path):
            try:
                registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0,
                                            winreg.KEY_READ)
                value, regtype = winreg.QueryValueEx(registry_key, name)
                winreg.CloseKey(registry_key)
                return value
            except WindowsError:
                return None
        def create_service_bot(self,service_name):
            if not exists(f"{self.dataDict['hon_directory']}nssm.exe"):
                shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\nssm.exe",f"{self.dataDict['hon_directory']}\\nssm.exe")
            else:
                if dmgr.mData.get_hash(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\nssm.exe") != dmgr.mData.get_hash(f"{self.dataDict['hon_directory']}\\nssm.exe"):
                    try:
                        shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\nssm.exe",f"{self.dataDict['hon_directory']}\\nssm.exe")
                    except Exception:
                        try:
                            shutil.move(f"{self.dataDict['hon_directory']}\\nssm.exe",f"{self.dataDict['hon_directory']}\\nssm_old.exe")
                            shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\nssm.exe",f"{self.dataDict['hon_directory']}\\nssm.exe")
                        except Exception: pass

            try:
                sp.run(['nssm', "install",service_name,f"{self.sdc_home_dir}\\adminbot{self.dataDict['svr_id']}.exe"])
            except Exception:
                sp.run([self.dataDict['nssm_exe'], "install",service_name,f"{self.sdc_home_dir}\\adminbot{self.dataDict['svr_id']}.exe"])
            return True
        def create_service_generic(self,service_name,application):
            if not exists(f"{self.dataDict['hon_directory']}nssm.exe"):
                shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\nssm.exe",f"{self.dataDict['hon_directory']}\\nssm.exe")
            try:
                sp.run(['nssm', "install",service_name,f"{self.dataDict['hon_directory']}{application}"])
            except Exception:
                sp.run([self.dataDict['nssm_exe'], "install",service_name,f"{self.dataDict['hon_directory']}{application}"])
            return True
        def configure_service_generic(self,service_name,application,arguments):
            if not exists(f"{self.dataDict['hon_directory']}nssm.exe"):
                shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\nssm.exe",f"{self.dataDict['hon_directory']}\\nssm.exe")
            try:
                sp.run(['nssm', "set",service_name,"Application",f"{self.dataDict['hon_directory']}{application}"])
                if arguments is not None:
                    sp.run(['nssm', "set",service_name,"AppParameters",arguments])
                sp.run(['nssm', "set",service_name,f"AppDirectory",f"{self.dataDict['hon_directory']}"])
                sp.run(['nssm', "set",service_name,"Start","SERVICE_DEMAND_START"])
                sp.run(['nssm', "set",service_name,f"AppExit","Default","Restart"])
                if service_name == "HoN Server Manager":
                    sp.run(['nssm', "set",service_name,"AppEnvironmentExtra",f"USERPROFILE={self.dataDict['hon_manager_dir']}"])
                elif service_name == "HoN Proxy Manager":
                    sp.run(['nssm', "set",service_name,"AppEnvironmentExtra",f"APPDATA={self.dataDict['hon_root_dir']}"])
            except Exception:
                sp.run([self.dataDict['nssm_exe'], "set",service_name,"Application",f"{self.dataDict['hon_directory']}{application}"])
                if arguments is not None:
                    sp.run([self.dataDict['nssm_exe'], "set",service_name,"AppParameters",arguments])
                sp.run([self.dataDict['nssm_exe'], "set",service_name,f"AppDirectory",f"{self.dataDict['hon_directory']}"])
                sp.run([self.dataDict['nssm_exe'], "set",service_name,"Start","SERVICE_DEMAND_START"])
                sp.run([self.dataDict['nssm_exe'], "set",service_name,f"AppExit","Default","Restart"])
                if service_name == "HoN Server Manager":
                    sp.run([self.dataDict['nssm_exe'], "set",service_name,"AppEnvironmentExtra",f"USERPROFILE={self.dataDict['hon_manager_dir']}"])
                elif service_name == "HoN Proxy Manager":
                    sp.run([self.dataDict['nssm_exe'], "set",service_name,"AppEnvironmentExtra",f"APPDATA={self.dataDict['hon_root_dir']}"])
            return True
        def configure_service_api(self,service_name):
            if not exists(f"{self.dataDict['hon_directory']}nssm.exe"):
                shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\nssm.exe",f"{self.dataDict['hon_directory']}\\nssm.exe")
            try:
                sp.run(['nssm', "set",service_name,f"Application",f"{self.dataDict['hon_directory']}API_HON_SERVER.exe"])
            except Exception:
                sp.run([self.dataDict['nssm_exe'], "set",service_name,f"Application",f"{self.dataDict['hon_directory']}API_HON_SERVER.exe"])
            return True
        def configure_service_bot(self,service_name):
            if not exists(f"{self.dataDict['hon_directory']}nssm.exe"):
                shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\nssm.exe",f"{self.dataDict['hon_directory']}\\nssm.exe")
            if not initialise.is_tool('nssm'):
                try:
                    nssm_inst = sp.run(["choco","install","nssm","-y"])
                    if nssm_inst.returncode == 0:
                        nssm = 'nssm'
                except Exception:
                    print(traceback.format_exc())
            if initialise.is_tool('nssm'):
                nssm = 'nssm'
                nssm_loc = rf"{os.environ['ProgramData']}\chocolatey\lib\NSSM\tools\nssm.exe"
            else:
                nssm = self.dataDict['nssm']
                # this hash is BAD, it means nssm is buggy, and server may close when stopping windows service, when it should stay open.
                if dmgr.mData.get_hash(nssm) != "47C112C23C7BDF2AF24A20BD512F91FF6AF76BC6":
                    nssm_loc = nssm
                else:
                    initialise.print_and_tex(self,f"[{self.service_name_bot}] There is an issue configuring windows services. The NSSM client is too old.",'warning')

            reg_path = rf"SYSTEM\CurrentControlSet\Services\{service_name}"
            existing_reg = initialise.get_reg("ImagePath",reg_path)
            reg_updated = False
            if existing_reg != nssm_loc:
                print("service is being reconfigured.")
                try:
                    if initialise.set_reg("ImagePath",nssm_loc,reg_path):
                        reg_updated = True
                except Exception:
                    print(traceback.format_exc())

            try:
                if reg_updated:
                    if initialise.get_service(service_name)['status'] in ["running","start_pending","paused"]:
                    #if initialise.check_proc(self.dataDict['hon_file_name']):
                        playercount = initialise.playerCount(self)
                        if playercount > 0:
                            initialise.print_and_tex(self,f"[{self.service_name_bot}] {playercount} Players connected. Scheduling restart instead. No action required",'warning')
                            initialise.schedule_restart(self)
                        else:
                            initialise.stop_service(self,service_name,False)
                sp.run([nssm, "set",service_name,"Application",f"{self.sdc_home_dir}\\adminbot{self.dataDict['svr_id']}.exe"])
                sp.run([nssm, "set",service_name,f"AppDirectory",f"{self.sdc_home_dir}"])
                sp.run([nssm, "set",service_name,f"AppStderr",f"{self.sdc_home_dir}\\{self.service_name_bot}.log"])
                sp.run([nssm, "set",service_name,"Start","SERVICE_DEMAND_START"])
                sp.run([nssm, "set",service_name,f"AppExit","Default","Restart"])
                sp.run([nssm, "set",service_name,"AppParameters",f"adminbot.py"])
                sp.run([nssm, "set",service_name,"AppKillProcessTree",f"0"])
                sp.run([nssm, "set",service_name,"AppStopMethodSkip",f"6"])
            except Exception:
                print(traceback.format_exc())

        def restart_service(self,service_name):
            try:
                sp.run(['net','stop',f'{service_name}'])
            except Exception:
                print ('could not stop service {}'.format(service_name))
                return False
            try:
                sp.run(['net','start',f'{service_name}'])
            except Exception:
                print ('could not start service {}'.format(service_name))
                return False
            return True
        def schedule_restart(self):
            temFile = f"{self.sdc_home_dir}\\pending_restart"
            with open(temFile, "w") as f:
                f.write("True")
            remove_me=f"{self.sdc_home_dir}\\pending_shutdown"
            if exists(remove_me):
                try:
                    os.remove(remove_me)
                except Exception:
                    print(traceback.format_exc())
        def schedule_restart_honfigurator(deployed_status):
            temFile = f"{deployed_status}\\pending_restart"
            with open(temFile, "w") as f:
                f.write("True")
            remove_me=f"{deployed_status}\\pending_shutdown"
            if exists(remove_me):
                try:
                    os.remove(remove_me)
                except Exception:
                    print(traceback.format_exc())
        def schedule_shutdown(deployed_status):
            temFile = f"{deployed_status['sdc_home_dir']}\\pending_shutdown"
            with open(temFile, "w") as f:
                f.write("True")
            remove_me=f"{deployed_status['sdc_home_dir']}\\pending_restart"
            if exists(remove_me):
                try:
                    os.remove(remove_me)
                except Exception:
                    print(traceback.format_exc())
        def check_schd_restart(deployed_status):
            temFile = deployed_status['sdc_home_dir']+"\\pending_restart"
            if exists(temFile):
                return True
            else:
                return False
        def check_schd_shutdown(deployed_status):
            temFile = deployed_status['sdc_home_dir']+"\\pending_shutdown"
            if exists(temFile):
                return True
            else:
                return False

        def create_config(self,filename,type,svr_port,voicelocal,svr_proxyport,voiceremote,serverID,serverHoster,location,svr_total,svr_ip):
            self.proxy = {}
            self.base = dmgr.mData.parse_config(self,os.path.abspath(application_path)+"\\config\\honfig.ini")
            iter = self.dataDict['incr_port']
            svr_identifier = self.dataDict['svrid_total']
            svr_ip = self.dataDict['svr_ip']
            if type == "startup":
                print("customising startup.cfg with the following values")
                print("svr_id: " + str(serverID))
                print("svr_host: " + str(serverHoster))
                print("svr_location: " + str(location))
                print("svr_total: " + str(svr_total))
                print("svr_ip: " + str(svr_ip))
                self.startup.update({'svr_port':f'"{svr_port}"'})
                self.startup.update({'svr_proxyPort':f'"{svr_proxyport}"'})
                self.startup.update({'svr_proxyLocalVoicePort':f'"{voicelocal}"'})
                self.startup.update({'svr_proxyRemoteVoicePort':f'"{voiceremote}"'})
                self.startup.update({'svr_voicePortEnd':f'"{voicelocal}"'})
                self.startup.update({'svr_voicePortStart':f'"{voicelocal}"'})
                print("svr_port: " + str(svr_port))
                print("voice_port: " + str(voicelocal))
                if self.dataDict['use_proxy']=='True':
                    self.startup.update({"man_enableProxy":f'"true"'})
                    print("===============PROXY ACTIVE===================")
                    print("svr_proxyPort: " + str(svr_proxyport))
                    print("svr_voiceProxyPort: " + str(voiceremote))
                    print("Because of use of HoN Proxy, the above values are the ones which must be port forwarded.")
                else:
                    self.startup.update({"man_enableProxy":f'"false"'})
                self.startup.update({"svr_name":f'"{serverHoster} {str(svr_identifier)}"'})
                self.startup.update({"svr_location":f'"{location}"'})
                self.startup.update({"svr_ip":f'"{svr_ip}"'})
                # uncomment if needing auth via svr_desc
                # will also need to provide below 3 variables to function when called. it's been taken out
                # self.startup.update({"svr_login":f'"{master_user}"'})
                # self.startup.update({"svr_password":f'"{master_pass}"'})
                # self.startup.update({"svr_desc":f'"{svr_desc}"'})
            elif type == "proxy":
                self.proxy.update({'redirectIP':'127.0.0.1'})
                self.proxy.update({'publicip':svr_ip})
                self.proxy.update({'publicPort':svr_proxyport})
                self.proxy.update({'redirectPort':svr_port})
                self.proxy.update({'voiceRedirectPort':voicelocal})
                self.proxy.update({'voicePublicPort':voiceremote})
                self.proxy.update({'region':'naeu'})
            #dmgr.mData.setData(NULL,filename,type,self.startup,self.proxy)
            return True
        def configure_firewall(self,name,application):
            try:
                check_rule = os.system(f"netsh advfirewall firewall show rule name=\"{name}\"")
                if check_rule == 0:
                    add_rule = os.system(f"netsh advfirewall firewall set rule name=\"{name}\" new program=\"{application}\" dir=in action=allow")
                    initialise.print_and_tex(self,f"Windows firewall configured for application: {application}",'interest')
                    return True
                elif check_rule == 1:
                    add_rule = os.system(f"netsh advfirewall firewall add rule name=\"{name}\" program=\"{application}\" dir=in action=allow")
                    print("firewall rule added.")
                    initialise.print_and_tex(self,f"Windows firewall configured for application: {application}",'interest')
                    return True
            except Exception: 
                print(traceback.format_exc())
                return False
        def configure_firewall_port(self,name,port):
            try:
                check_rule = os.system(f"netsh advfirewall firewall show rule name=\"{name}\"")
                if check_rule == 0:
                    #add_rule = os.system(f"netsh advfirewall firewall set rule name=\"{name}\" new dir=in action=allow protocol=UDP localport={port} remoteip={ip_addr}")
                    add_rule = os.system(f"netsh advfirewall firewall set rule name=\"{name}\" new dir=in action=allow protocol=UDP localport={port} remoteip=any")
                    initialise.print_and_tex(self,f"Windows firewall configured for {name} over port: {port}",'interest')
                    return True
                elif check_rule == 1:
                    #add_rule = os.system(f"netsh advfirewall firewall add rule name=\"{name}\" dir=in action=allow protocol=UDP localport={port} remoteip={ip_addr}")
                    add_rule = os.system(f"netsh advfirewall firewall add rule name=\"{name}\" dir=in action=allow protocol=UDP localport={port} remoteip=any")
                    initialise.print_and_tex(self,f"Windows firewall configured for port: {port}",'interest')
                    return True
            except Exception: 
                print(traceback.format_exc())
                return False
        def remove_firewall(self,name,application):
            try:
                check_rule = os.system(f"netsh advfirewall firewall show rule name=\"{name}\"")
                if check_rule == 0:
                    remove_rule = os.system(f"netsh advfirewall firewall delete rule name=\"{name}\"")
            except Exception: 
                print(traceback.format_exc())
                return False
        def print_and_tex(self,message,*args):
            print(message)
            if len(args) > 0:
                level = args[0].lower()
                tex.insert(END,message+"\n",level)
                tex.see(tk.END)
            else:
                tex.insert(END,message+"\n")
                tex.see(tk.END)

        def build(self,name):
            os.environ["PYTHONHASHSEED"] = "1"
            os.system(f'pyinstaller --noconfirm --onefile --console --icon .\\icons\\botico.png --uac-admin --add-data "cogs;cogs/" --add-data "config;config/"  "adminbot.py" --name {name} -y')
            return True
        def configureEnvironment(self,force_update,use_console):
            global hon_api_updated
            global players_connected
            global tex

            #self.bot_version = float(self.bot_version)
            bot_needs_update = False
            bot_first_launch = False
            exe_force_copy = False
            
            os.environ["USERPROFILE"] = self.dataDict['hon_home_dir']
            os.environ["APPDATA"] = self.dataDict['hon_root_dir']

            if self.ver_current > self.ver_existing: # or checkbox force is on:
                bot_needs_update = True
            
            print()
            print("==========================================")
            print(f"[{self.dataDict['app_name']}] CHECKING EXISTING SERVER ENVIRONMENT")
            print("==========================================")

            if exists(f"{self.hon_home_dir}\\Documents"):
                print(f"[{self.dataDict['app_name']}] Environment EXISTS for {self.service_name_bot}: " + (os.environ["USERPROFILE"] + "!"))

            else:
                os.makedirs(f"{self.hon_home_dir}\\Documents")
                print(f"[{self.dataDict['app_name']}] Environment requires creating for new server {self.service_name_bot}...")
                print(f"[{self.dataDict['app_name']}] Created & Configured HoN environment: " + (os.environ["USERPROFILE"] + "!"))
                bot_first_launch = True
            if not exists(f"{self.dataDict['hon_root_dir']}\\Documents"):
                os.makedirs(f"{self.dataDict['hon_root_dir']}\\Documents")

            if exists(f"{self.dataDict['sdc_home_dir']}\\config\\local_config.ini"):
                try:
                    if self.deployed_status['hon_directory'] != self.dataDict['hon_directory']:
                        try:
                            shutil.copy(f"{self.deployed_status['sdc_home_dir']}\\messages\\message{self.dataDict['svr_identifier']}",f"{self.dataDict['sdc_home_dir']}\\messages\message{self.dataDict['svr_identifier']}.txt")
                            shutil.copy(f"{self.deployed_status['sdc_home_dir']}\\cogs\\total_games_played",f"{self.dataDict['sdc_home_dir']}\\cogs\\total_games_played")
                        except Exception:
                            print(traceback.format_exc())
                    if self.deployed_status['svr_hoster'] != self.dataDict['svr_hoster']:
                        try:
                            shutil.copy(f"{self.deployed_status['sdc_home_dir']}\\messages\\message{self.dataDict['svr_identifier']}",f"{self.dataDict['sdc_home_dir']}\\messages\message{self.dataDict['svr_identifier']}.txt")
                        except Exception:
                            print(traceback.format_exc())
                except Exception:
                    print(traceback.format_exc())

            if not exists(self.hon_logs_dir):
                print(f"[{self.dataDict['app_name']}] creating: " + self.hon_logs_dir)
                os.makedirs(self.hon_logs_dir)
                print(f"[{self.dataDict['app_name']}] creating: {self.hon_logs_dir} ...")

            if not exists(self.sdc_home_dir):
                print(f"[{self.dataDict['app_name']}] creating: {self.sdc_home_dir} ...")
                os.makedirs(self.sdc_home_dir)
            
            if not exists(f"{self.dataDict['hon_manager_dir']}\\Documents\\Heroes of Newerth x64\\game\\replays"):
                print(f"[{self.dataDict['app_name']}] creating {self.dataDict['hon_manager_dir']}\\Documents\\Heroes of Newerth x64\\game\\replays")
                os.makedirs(f"{self.dataDict['hon_manager_dir']}\\Documents\\Heroes of Newerth x64\\game\\replays")

            if not exists(f"{self.sdc_home_dir}\\messages"):
                print(f"[{self.dataDict['app_name']}] creating: {self.sdc_home_dir}\\messages ...")
                os.makedirs(f"{self.sdc_home_dir}\\messages")
            if not exists(f"{self.sdc_home_dir}\\suspicious"):
                print(f"[{self.dataDict['app_name']}] creating: {self.sdc_home_dir}\\suspicious ...")
                os.makedirs(f"{self.sdc_home_dir}\\suspicious")
            if not exists(f"{self.sdc_home_dir}\\config"):
                print(f"[{self.dataDict['app_name']}] creating: {self.sdc_home_dir}\\config ...")
                os.makedirs(f"{self.sdc_home_dir}\\config")
            if not exists(f"{self.sdc_home_dir}\\icons"):
                print(f"[{self.dataDict['app_name']}] creating: {self.sdc_home_dir}\\icons ...")
                os.makedirs(f"{self.sdc_home_dir}\\icons")
            if not exists(f"{self.sdc_home_dir}\\cogs"):
                print(f"[{self.dataDict['app_name']}] creating: {self.sdc_home_dir}\\cogs ...")
                os.makedirs(f"{self.sdc_home_dir}\\cogs")
            if not exists(f"{self.sdc_home_dir}\\dependencies"):
                print(f"[{self.dataDict['app_name']}] creating: {self.sdc_home_dir}\\dependencies ...")
                os.makedirs(f"{self.sdc_home_dir}\\dependencies")
            if exists(f"{self.dataDict['sdc_home_dir']}\\..\\sdc\\messages\\message{self.dataDict['svr_identifier']}.txt"):
                if not exists(f"{self.dataDict['sdc_home_dir']}\\messages\\message{self.dataDict['svr_identifier']}.txt"):
                    shutil.copy(f"{self.dataDict['sdc_home_dir']}\\..\\sdc\\messages\\message{self.dataDict['svr_identifier']}.txt",f"{self.dataDict['sdc_home_dir']}\\messages\\")
                os.remove(f"{self.dataDict['sdc_home_dir']}\\..\\sdc\\messages\\message{self.dataDict['svr_identifier']}.txt")
            if exists(f"{self.dataDict['sdc_home_dir']}\\..\\sdc\\cogs\\total_games_played"):
                shutil.copy(f"{self.dataDict['sdc_home_dir']}\\..\\sdc\\cogs\\total_games_played",f"{self.dataDict['sdc_home_dir']}\\cogs\\total_games_played")
                os.remove(f"{self.dataDict['sdc_home_dir']}\\..\\sdc\\cogs\\total_games_played")
            if dmgr.mData.get_hash(f"{self.hon_directory}\\game\\game_shared_x64.dll") != dmgr.mData.get_hash(f"{self.hon_directory}game_shared_x64.dll"):
                try:
                    shutil.copy(f"{self.hon_directory}game\\game_shared_x64.dll",f"{self.hon_directory}game_shared_x64.dll")
                except PermissionError:
                    print(f"[{self.dataDict['app_name']}] {self.hon_directory}game\\game_shared_x64.dll needs to be copied into {self.hon_directory}")

            ## global networking settings ##
            iter = int(self.dataDict['incr_port'])
            self.game_port = int(self.dataDict['game_starting_port']) + iter
            self.voice_port = int(self.dataDict['voice_starting_port']) + iter
            self.game_port_proxy = self.game_port + 10000
            self.voice_port_proxy = self.voice_port + 10000
            if exists(f"{self.hon_game_dir}\\startup.cfg") and bot_first_launch != True and bot_needs_update != True and force_update != True:
                print(f"[{self.dataDict['app_name']}] Server is already configured, checking values for {self.service_name_bot}...")
                dmgr.mData.parse_config(self,f"{self.hon_game_dir}\\startup.cfg")
            if self.dataDict['use_proxy'] == "True":
                firewall = initialise.remove_firewall(self,self.dataDict['hon_file_name'],self.dataDict['hon_exe'])
            else:
                firewall = initialise.configure_firewall(self,self.dataDict['hon_file_name'],self.dataDict['hon_exe'])
            if not exists(f"{self.hon_game_dir}\\startup.cfg") or bot_first_launch == True or bot_needs_update == True or force_update == True:
                # check if exe's need to be copied, either it doesn't exist or the hash is different.
                if self.dataDict['master_server'] == "honmasterserver.com":
                    exe_path=f"{self.dataDict['hon_directory']}HON_SERVER_{self.svr_id}.exe"
                    exe_path_cut=f"{self.dataDict['hon_directory']}HON_SERVER_{self.svr_id}"
                else:
                    exe_path=f"{self.dataDict['hon_directory']}KONGOR_ARENA_{self.svr_id}.exe"
                    exe_path_cut=f"{self.dataDict['hon_directory']}KONGOR_ARENA_{self.svr_id}"
                copy=False
                if exists(exe_path):
                    hash1=dmgr.mData.get_hash(exe_path)
                    hash2=dmgr.mData.get_hash(f"{self.dataDict['hon_directory']}hon_x64.exe")
                    if hash1 != hash2:
                        copy=True
                else:
                    copy=True
                if copy:
                    try:
                        shutil.copy(f"{self.dataDict['hon_directory']}hon_x64.exe",exe_path)
                        print(f"[{self.dataDict['app_name']}] copying server exe...")
                    except Exception: 
                        shutil.move(exe_path,f"{exe_path_cut}_old.exe")
                        shutil.copy(f"{self.dataDict['hon_directory']}hon_x64.exe",exe_path)
                        exe_force_copy=True
                if not exists(f"{self.hon_game_dir}\\startup.cfg"):
                    print(f"[{self.dataDict['app_name']}] Server {self.service_name_bot} requires full configuration. No existing startup.cfg or game_settings_local.cfg. Configuring...")
                #initialise.create_config(self,f"{self.hon_game_dir}\\startup.cfg","startup",self.game_port,self.voice_port,self.game_port_proxy,self.voice_port_proxy,self.svr_id,self.svr_hoster,self.svr_region_short,self.svr_total,self.svr_ip)
                initialise.create_config(self,f"{self.hon_game_dir}\\proxy_config.cfg","proxy",self.game_port,self.voice_port,self.game_port_proxy,self.voice_port_proxy,self.svr_id,self.svr_hoster,self.svr_region_short,self.svr_total,self.svr_ip)
                print(f"[{self.dataDict['app_name']}] copying {self.service_name_bot} script and related configuration files to HoN environment: "+ self.hon_home_dir + "..")
                try:
                    shutil.copy(os.path.abspath(application_path)+"\\dependencies\\adminbot-launch.exe", f'{self.sdc_home_dir}\\{self.service_name_bot}-launch.exe')
                except PermissionError:
                    if exists(f'{self.sdc_home_dir}\\{self.service_name_bot}-launch_old.exe'):
                        try:
                            os.remove(f'{self.sdc_home_dir}\\{self.service_name_bot}-launch_old.exe')
                        except Exception: 
                            print(traceback.format_exc())
                            shutil.move(f'{self.sdc_home_dir}\\{self.service_name_bot}-launch_old.exe',f'{self.sdc_home_dir}\\{self.service_name_bot}-launch_old2.exe')
                            try:
                                os.remove(f'{self.sdc_home_dir}\\{self.service_name_bot}-launch_old2.exe')
                            except Exception: print(traceback.format_exc())
                    os.rename(f'{self.sdc_home_dir}\\{self.service_name_bot}-launch.exe',f'{self.sdc_home_dir}\\{self.service_name_bot}-launch_old.exe')
                    shutil.copy(os.path.abspath(application_path)+"\\dependencies\\adminbot-launch.exe", f'{self.sdc_home_dir}\\{self.service_name_bot}-launch.exe')
                try:
                    shutil.copy(f"{application_path}\\dependencies\\python310.dll",self.dataDict['sdc_home_dir'])
                    shutil.copy(f"{application_path}\\dependencies\\vcruntime140.dll",self.dataDict['sdc_home_dir'])
                    shutil.copy(f"{application_path}\\dependencies\\requirements.txt",f"{self.dataDict['sdc_home_dir']}\\dependencies\\requirements.txt")
                except Exception:
                    print(traceback.format_exc())
                if not exists(f'{self.sdc_home_dir}\\{self.service_name_bot}.exe') or force_update:
                    try:
                        shutil.copy(f"{self.dataDict['python_location']}", f'{self.sdc_home_dir}\\{self.service_name_bot}.exe')
                    except PermissionError:
                        if exists(f'{self.sdc_home_dir}\\{self.service_name_bot}_old.exe'):
                            try:
                                os.remove(f'{self.sdc_home_dir}\\{self.service_name_bot}_old.exe')
                            except Exception:
                                print(traceback.format_exc())
                                shutil.move(f"{self.sdc_home_dir}\\{self.service_name_bot}_old.exe",f"{self.sdc_home_dir}\\{self.service_name_bot}_old2.exe'")
                        os.rename(f'{self.sdc_home_dir}\\{self.service_name_bot}.exe',f'{self.sdc_home_dir}\\{self.service_name_bot}_old.exe')
                        shutil.copy(f"{self.dataDict['python_location']}", f'{self.sdc_home_dir}\\{self.service_name_bot}.exe')

                shutil.copy(os.path.abspath(application_path)+"\\dependencies\\adminbot.py", f'{self.sdc_home_dir}\\adminbot.py')
                src_folder = os.path.abspath(application_path)+"\\cogs\\"
                dst_folder = f'{self.sdc_home_dir}\\cogs\\'
                for file_name in os.listdir(src_folder):
                    src_file = src_folder+file_name
                    dst_file = dst_folder+file_name
                    if os.path.isfile(src_file):
                        try:
                            shutil.copy(src_file, dst_file)
                        except Exception:
                            print(traceback.format_exc())
                        print(f"[{self.dataDict['app_name']}] copied", file_name)

                src_folder = os.path.abspath(application_path)+"\\config\\"
                dst_folder = f'{self.sdc_home_dir}\\config\\'
                for file_name in os.listdir(src_folder):
                    src_file = src_folder+file_name
                    dst_file = dst_folder+file_name
                    if os.path.isfile(src_file):
                        if file_name == 'local_config.ini' or file_name == 'global_config.ini':
                            shutil.copy(src_file, f"{dst_file}.incoming")
                        else:
                            shutil.copy(src_file,dst_file)
                        print('copied', file_name)
                #distutils.dir_util.copy_tree(os.path.abspath(application_path)+"\\config", f'{self.sdc_home_dir}\\config',update=1)
                distutils.dir_util.copy_tree(os.path.abspath(application_path)+"\\icons", f'{self.sdc_home_dir}\\icons',update=1)
                print(f"[{self.dataDict['app_name']}] Done!")
                print(f"[{self.dataDict['app_name']}] Checking and creating required dependencies...")
                #
                #
                # if not exists(f"{self.dataDict['hon_directory']}{self.dataDict['player_count_exe']}" or force_update == True or bot_needs_update == True):
                try:
                    shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\{self.dataDict['player_count_exe']}",f"{self.dataDict['hon_directory']}{self.dataDict['player_count_exe']}")
                except Exception: print(traceback.format_exc())
                print(f"[{self.dataDict['app_name']}] copying other dependencies...")
                print(f"[{self.dataDict['app_name']}] Done!")
            
            if self.dataDict['master_server'] == "honmasterserver.com":
                service_api = initialise.get_service(self.service_name_api)
                if service_api:
                    #print("HON Registration API STATUS: " + self.service_name_api)
                    if service_api['status'] == 'running' or service_api['status'] == 'paused':
                        if force_update != True and bot_needs_update != True:
                            initialise.print_and_tex(self,"HON Registration API STATUS: RUNNING")
                        elif (force_update == True or bot_needs_update == True) and hon_api_updated !=True:
                            initialise.stop_service(self,self.service_name_api,False)
                            #time.sleep(1)
                            service_api = initialise.get_service(self.service_name_api)
                            if service_api['status'] == 'stopped':
                                try:
                                    shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\API_HON_SERVER.exe",f"{self.dataDict['hon_directory']}API_HON_SERVER.exe")
                                except PermissionError:
                                    initialise.print_and_tex(self,"COULD NOT UPGRADE SERVICE: " + self.service_name_api +" The service is currently runing so we cannot replace this file. We'll try again later",'warning')
                                except Exception: print(traceback.format_exc())
                            if initialise.configure_service_api(self,self.service_name_api):
                                hon_api_updated = True
                            #time.sleep(1)
                            initialise.start_service(self,self.service_name_api,False)
                    else:
                        if (force_update ==True or bot_needs_update == True) and hon_api_updated !=True:
                            try:
                                shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\API_HON_SERVER.exe",f"{self.dataDict['hon_directory']}API_HON_SERVER.exe")
                            except PermissionError:
                                initialise.print_and_tex(self,"COULD NOT UPGRADE SERVICE: " + self.service_name_api +" The service is currently in use so we cannot replace this file. We'll try again later",'warning')
                            except Exception: print(traceback.format_exc())
                            #shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\API_HON_SERVER.exe",f"{self.dataDict['hon_directory']}API_HON_SERVER.exe")
                            if initialise.configure_service_api(self,self.service_name_api):
                                hon_api_updated = True
                            #time.sleep(1)
                            initialise.start_service(self,self.service_name_api,False)
                        else:
                            print("Windows Service STARTING...")
                            initialise.start_service(self,self.service_name_api,False)
                            service_api = initialise.get_service(self.service_name_api)
                        if service_api['status'] == 'running':
                            initialise.print_and_tex(self,"HON Registration API STATUS: " + self.service_name_api +": RUNNING")
                        else:
                            initialise.print_and_tex(self,"HON Registration API STATUS: " + self.service_name_api +":  FAILED TO START!",'warning')
                        print("==========================================")
                else:
                    bot_needs_update = True
                    print("==========================================")
                    print(f"Creating hon server registration API: {self.service_name_api}..")
                    print("==========================================")
                    initialise.create_service_generic(self,self.service_name_api,"API_HON_SERVER.exe")
                    print("starting service.. " + self.service_name_api)
                    initialise.start_service(self,self.service_name_api,False)
                    print("==========================================")
                    print("HON Registration API STATUS: " + self.service_name_api)
                    service_api = initialise.get_service(self.service_name_api)
                    if service_api['status'] == 'running':
                        initialise.print_and_tex(self,"HON Registration API STATUS: " + self.service_name_api +": RUNNING")
                    else:
                        initialise.print_and_tex(self,"HON Registration API STATUS: " + self.service_name_api +":  FAILED TO START!",'warning')
                    print("==========================================")
            

            ### CHECK IF PROXY IS ONLINE ###
            if self.dataDict['use_proxy']=='True':
                if initialise.check_port(self.game_port_proxy):
                    pass
                else:
                    initialise.print_and_tex(self,f"[{self.dataDict['app_name']}] Proxy is not running. You may not start the server without the proxy first running.",'warning')
                    return
            ###
            service_bot = initialise.get_service(self.service_name_bot)

            if not use_console:
                ### Perform checks for a windows service configuration
                if not service_bot:
                    bot_needs_update = True
                    print("==========================================")
                    print(f"[{self.dataDict['app_name']}] Creating windows service..")
                    print("==========================================")
                    initialise.create_service_bot(self,self.service_name_bot)
                initialise.configure_service_bot(self,self.service_name_bot)
                service_bot = initialise.get_service(self.service_name_bot)
                if not (service_bot['status'] == 'running' or service_bot['status'] == 'paused'):
                    if initialise.check_proc(f"{self.service_name_bot}.exe"):
                        initialise.print_and_tex(self,f"[{self.service_name_bot}] You are switching from console mode to windows service.",'warning')
                        playercount = initialise.playerCount(self)
                        initialise.stop_bot(self,f"{self.service_name_bot}.exe")
                    print(f"[{self.service_name_bot}] Starting as a windows service.")
                    initialise.start_bot(self,False)
                else:
                    # stop bot is faster than restarting the service
                    initialise.stop_bot(self,f"{self.service_name_bot}.exe")
            else:
                ### Perform checks for a console app configuration
                if service_bot:
                    if (service_bot['status'] == 'running' or service_bot['status'] == 'paused'):
                        initialise.print_and_tex(self,f"[{self.service_name_bot}] You are switching from windows service to console mode.",'warning')
                        print(f"[{self.service_name_bot}] No players connected, safe to restart...")
                        sp.Popen(['net','stop',self.service_name_bot])
                print(f"[{self.service_name_bot}] Starting as a console application.")
                initialise.start_bot(self,False)

            if force_update == True or bot_first_launch == True or bot_needs_update == True:
                if exists(f"{self.dataDict['sdc_home_dir']}\\config\\local_config.ini"):
                    self.deployed_status = self.data.returnDict_deployed(self.svr_id)
                # wait = 5
                # waiting = 0
                # while not initialise.check_proc(f"{self.service_name_bot}.exe"):
                #     time.sleep(1)
                #     waiting +=1
                #     if initialise.check_proc(f"{self.service_name_bot}.exe"):
                #         waiting = 5
                #     if waiting > wait:
                #         initialise.print_and_tex(self,f"[{self.service_name_bot}] Problem starting.",'warning')
                #         break
                if use_console == True:
                    mode = "console"
                else:
                    mode = "windows service"
                initialise.print_and_tex(self,f"[{self.service_name_bot}] APPLIED v{self.ver_current} in {mode} mode!",'interest')
                if self.dataDict['use_proxy'] == 'False':
                    #initialise.print_and_tex(self,f"Server ports: Game ({self.startup['svr_port']}), Voice ({self.startup['svr_proxyLocalVoicePort']})\n")
                    ports_to_forward_game.append(self.dataDict['svr_port'])
                    ports_to_forward_voice.append(self.dataDict['svr_proxyLocalVoicePort'])
                elif self.dataDict['use_proxy'] == 'True':
                    #initialise.print_and_tex(self,f"Server ports (PROXY): Game ({self.startup['svr_proxyPort']}), Voice ({self.startup['svr_proxyRemoteVoicePort']})\n")
                    ports_to_forward_game.append(self.dataDict['svr_proxyPort'])
                    ports_to_forward_voice.append(self.dataDict['svr_proxyRemoteVoicePort'])
            else:
                initialise.print_and_tex(self,f"ADMINBOT{self.svr_id} v{self.ver_current}")
                initialise.print_and_tex(self,"NO UPDATES OR CONFIGURATION CHANGES MADE")
                #tex.insert(END,"==============================================\n")
            bot_needs_update = False
            players_connected = False
    
    class TextScrollCombo(ttk.Frame):

        def __init__(self, *args, **kwargs):
            global tex
            super().__init__(*args, **kwargs)

        # # ensure a consistent GUI size
            self.grid_propagate(False)
        # # implement stretchability
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)

        # create a Text widget
            
        # create a Scrollbar and associate it with txt
            scrollb = ttk.Scrollbar(app, command=tex.yview)
            scrollb.grid(row=16, column=1, sticky='nsew')
            tex['yscrollcommand'] = scrollb.set
    class honfigurator():
        global tex
        def __init__(self,master):
            # global self.dataDict
            self.initdict = dmgr.mData()
            self.dataDict = self.initdict.returnDict()
            self.app = master
            honfigurator.creategui(self)
            #print (self.dataDict)
            return
        def onerror(func, path, exc_info):
            """
            Error handler for ``shutil.rmtree``.

            If the error is due to an access error (read only file)
            it attempts to add write permission and then retries.

            If the error is for another reason it re-raises the error.
            
            Usage : ``shutil.rmtree(path, onerror=onerror)``
            """
            import stat
            # Is the error an access error?
            if not os.access(path, os.W_OK):
                os.chmod(path, stat.S_IWUSR)
                func(path)
            else:
                raise
        def git_current_branch(self):
            try:
                os.chdir(application_path)
            except Exception:
                print(traceback.format_exc())
            repo = git.Repo(search_parent_directories=True)
            current_branch = repo.active_branch  # 'master'
            current_branch = current_branch.name
            return current_branch
        def git_all_branches(self):
            repositories = []
            repo = git.Repo('.')
            remote_refs = repo.remote().refs
            for refs in remote_refs:
                repos = refs.name.replace('origin/','')
                if 'main' in repos or 'Development' in repos or 'TH' in repos:
                    repositories.append(repos)            
            return repositories
        def coreassign(self):
            return ["one core/server","two cores/server","two servers/core","three servers/core","four servers/core"]
        def incrementport(self):
            return["1","10","100","200","500","1000"]
        def priorityassign(self):
            return ["normal","high","realtime"]
        def coreadjust(self,var,index,mode):
            cores = []
            total_cores = psutil.cpu_count(logical = True)
            if total_cores > 4:
                total_cores = total_cores - 2
            elif total_cores >= 30:
                total_cores = total_cores - 4
            else:
                total_cores = total_cores - 1
                
            half_core_count = total_cores / 2
            half_core_count = int(half_core_count)
            two_servers_core = total_cores * 2
            three_servers_core = total_cores * 3
            four_servers_core = total_cores * 4
            core_assignment = str(self.core_assign.get()).lower()
            selected_id = str(self.from_svr_var.get())
            if core_assignment == "one core/server":
                if int(self.svr_total_var.get()) > total_cores:
                    self.svr_total_var.set(total_cores)
                if int(selected_id) > int(self.svr_total_var.get()):
                    self.from_svr_var.set(total_cores)
                for i in range(total_cores):
                    cores.append(i+1)
                self.tab1_servertd['values']=cores
                self.tab1_from_svr['values']=cores
                return
            elif core_assignment == "two cores/server":
                #if int(self.svr_total_var.get()) > half_core_count:
                self.svr_total_var.set(half_core_count)
                if int(selected_id) > int(self.svr_total_var.get()):
                    self.from_svr_var.set(half_core_count)
                for i in range(half_core_count):
                    cores.append(i+1)
                self.tab1_servertd['values']=cores
                self.tab1_from_svr['values']=cores
                return
            elif core_assignment == "two servers/core":
                #if int(self.svr_total_var.get()) > two_servers_core:
                self.svr_total_var.set(two_servers_core)
                if int(selected_id) > int(self.svr_total_var.get()):
                    self.from_svr_var.set(two_servers_core)
                for i in range(two_servers_core):
                    cores.append(i+1)
                self.tab1_servertd['values']=cores
                self.tab1_from_svr['values']=cores
                return
            elif core_assignment == "three servers/core":
                #if int(self.svr_total_var.get()) > two_servers_core:
                self.svr_total_var.set(three_servers_core)
                if int(selected_id) > int(self.svr_total_var.get()):
                    self.from_svr_var.set(three_servers_core)
                for i in range(three_servers_core):
                    cores.append(i+1)
                self.tab1_servertd['values']=cores
                self.tab1_from_svr['values']=cores
                return
            elif core_assignment == "four servers/core":
                #if int(self.svr_total_var.get()) > two_servers_core:
                self.svr_total_var.set(four_servers_core)
                if int(selected_id) > int(self.svr_total_var.get()):
                    self.from_svr_var.set(four_servers_core)
                for i in range(four_servers_core):
                    cores.append(i+1)
                self.tab1_servertd['values']=cores
                self.tab1_from_svr['values']=cores
                return
        def corecount(self):
            cores = []
            total_cores = psutil.cpu_count(logical = True)
            if total_cores > 4:
                total_cores = total_cores - 2
            elif total_cores >= 30:
                total_cores = total_cores - 4
            else:
                total_cores = total_cores - 1
                
            half_core_count = total_cores / 2
            half_core_count = int(half_core_count)
            if self.dataDict['core_assignment'] == "two cores/server":
                total_cores = half_core_count
                #for i in range(half_core_count):
                    #cores.append(i+1)
                #self.svr_total_var.set(half_core_count)
            elif self.dataDict['core_assignment'] == "two servers/core":
                total_cores = total_cores * 2
            elif self.dataDict['core_assignment'] == "three servers/core":
                total_cores = total_cores * 3
            elif self.dataDict['core_assignment'] == "four servers/core":
                total_cores = total_cores * 4
            for i in range(total_cores):
                cores.append(i+1)
                
            return cores
        def send_msg(msg):
            win = tk.Toplevel()
            win.wm_title("Window")
            var = tk.IntVar()

            l = tk.Label(win, text=msg)
            l.grid(row=0, column=0)

            b = ttk.Button(win, text="Okay", command=lambda: var.set(1))
            #b = ttk.Button(win, text="Okay", command=win.destroy())
            b.grid(row=1, column=0)
            b.wait_variable(var)
            return True
        def popup_bonus():
            win = tk.Toplevel()
            win.wm_title("Window")
            var = tk.IntVar()

            l = tk.Label(win, text="HoNfigurator will be updated.")
            l.grid(row=0, column=0)

            b = ttk.Button(win, text="Okay", command=lambda: var.set(1))
            #b = ttk.Button(win, text="Okay", command=win.destroy())
            b.grid(row=1, column=0)
            b.wait_variable(var)
            return True
        def warning(message):
            win = tk.Toplevel()
            win.wm_title("Window")
            var = tk.IntVar()

            l = tk.Label(win, text=message)
            l.grid(row=0, column=0)

            b = ttk.Button(win, text="Okay", command=lambda: var.set(1))
            #b = ttk.Button(win, text="Okay", command=win.destroy())
            b.grid(row=1, column=0)
            b.wait_variable(var)
            return True
            
        def regions(self):
            return ["USW","USE","TH","AU","SEA","RU","EU","BR","NEWERTH"]
        def masterserver(self):
            return ["api.kongor.online","honmasterserver.com"]
        # def reg_def_link(self,var,index,mode):
        #     reglist = self.regions()
        #     svrloc = str(self.svr_loc.get()).lower()
        #     for reg in reglist[0]:
        #         if svrloc == reg.lower():
        #             self.svr_loc.set(reglist[0][reglist[0].index(reg)])
        #             self.svr_reg_code.set(reglist[1][reglist[0].index(reg)])
        def port_mode(self,var,index,mode):
            game_port = int(self.tab3_game_port.get())
            voice_port = int(self.tab3_voice_port.get())
            
            #   The below 2 lines address a bug where the port was accidentally reduced by 10000.
            #   If the ports are below 10k, then this has happened, and they should be changed
            if game_port < 10000 and voice_port < 10000:
                game_port = game_port+10000
                voice_port = voice_port+10000
            if self.useproxy.get() == True:
                self.tab1_restart_proxy.configure(state='enabled')
                self.tab3_game_port.delete(0,END)
                self.tab3_voice_port.delete(0,END)
                self.tab3_game_port.insert(0,str(game_port+10000))
                self.tab3_voice_port.insert(0,str(voice_port+10000))
            else:
                self.restart_proxy.set(False)
                self.tab1_restart_proxy.configure(state='disabled')
                self.tab3_game_port.delete(0,END)
                self.tab3_voice_port.delete(0,END)
                self.tab3_game_port.insert(0,game_port-10000)
                self.tab3_voice_port.insert(0,voice_port-10000)

        def switch_widget_state(self,var,index,mode):
            if self.enablebot.get() == True:
                current_text = self.tab3_discordadmin.get()
                self.tab3_discordadmin.configure(state="disabled",foreground="grey")

                
                self.tab3_discord_title['text'] = "Discord Bot Data (DISABLED)"
                self.tab1_discord_title['text'] = "Discord Bot Settings (DISABLED)"
                
                self.tab3_bottokd.configure(state="disabled",foreground="grey")
                self.tab1_alert_on_crash_btn.configure(state="disabled")
                self.tab1_alert_on_lag_btn.configure(state="disabled")
                self.tab1_alertlist_limit.configure(state="disabled",foreground="grey")
                self.tab1_eventlist_limit.configure(state="disabled",foreground="grey")
                self.tab1_debugmode_btn.configure(state="disabled")
            else:
                current_text = self.tab3_discordadmin.get()
                self.tab3_discordadmin.configure(state="enabled",foreground="white")
                self.tab3_discordadmin.delete(0,END)
                self.tab3_discordadmin.insert(0,current_text.replace(" (DISABLED)",""))

                self.tab3_discord_title['text'] = "Discord Bot Data"
                self.tab1_discord_title['text'] = "Discord Bot Settings"

                current_text = self.tab3_bottokd.get()
                self.tab3_bottokd.configure(state="enabled",foreground="white")
                self.tab3_bottokd.delete(0,END)
                self.tab3_bottokd.insert(0,current_text.replace(" (DISABLED)",""))

                self.tab1_alert_on_crash_btn.configure(state="enabled")
                self.tab1_alert_on_lag_btn.configure(state="enabled")
                self.tab1_alertlist_limit.configure(state="enabled",foreground="white")
                self.tab1_eventlist_limit.configure(state="enabled",foreground="white")
                self.tab1_debugmode_btn.configure(state="enabled")
        def svr_num_link(self,var,index,mode):
            if self.from_svr_var.get() == "(for single server)":
                return
            elif int(self.from_svr_var.get()) > int(self.svr_total_var.get()):
                self.from_svr_var.set(self.svr_total_var.get())
            elif int(self.svr_total_var.get()) < int(self.to_svr_var.get()):
                self.to_svr_var.set(self.svr_total_var.get())
            # elif str(self.core_assign.get()).lower() == "two":
            #     self.svr_total_var.set()
        def svr_num_link2(self,var,index,mode):
            if self.from_svr_var.get() == "(for single server)":
                return
            elif int(self.from_svr_var.get()) > int(self.to_svr_var.get()):
                self.from_svr_var.set(self.to_svr_var.get())
            elif int(self.to_svr_var.get()) > int(self.svr_total_var.get()):
                self.to_svr_var.set(self.svr_total_var.get())
                initialise.print_and_tex(self,f"You can't choose a \"to server\" value greater than the total server count ({self.svr_total_var.get()})",'warning')

        def change_to_proxy(self):
            if self.useproxy.get() == True:
                return("test")
            else:
                return("wow")
        def change_to_proxy2(self,var,index,mode):
            if self.useproxy.get() == True:
                self.game_port.set("test")
            else:
                self.game_port.set("wow")
        def update_repository(self,var,index,mode):
            global update_counter
            update_counter=0
            try:
                os.chdir(application_path)
            except Exception:
                print(traceback.format_exc())
            selected_branch = self.git_branch.get()
            repo = git.Repo(search_parent_directories=True)
            current_branch = repo.active_branch  # 'master'
            current_branch = current_branch.name
            # if selected_branch != current_branch:
            checkout = sp.run(["git","checkout",selected_branch],stdout=sp.PIPE,stderr=sp.PIPE, text=True)
            if checkout.returncode == 0:
                # print(f"Repository: {selected_branch}\nCheckout status: {checkout.stdout}")
                #tex.insert(END,f"Repository: {selected_branch}\nCheckout Status: {checkout.stdout}")
                print(f"Updating selected repository: {selected_branch} branch")
                output = sp.run(["git", "pull"],stdout=sp.PIPE, text=True)
                print(f"Repository: {selected_branch}\nUpdate Status: {output.stdout}")
                tex.insert(END,f"Repository: {selected_branch}\nUpdate Status: {output.stdout}")
                tex.insert(END,"==========================================\n")
                #os.execv(sys.argv[0], sys.argv)
                try:
                    if 'updating' in output.stdout.lower() or 'switched to branch' in checkout.stderr.lower():
                        #if honfigurator.popup_bonus():
                        #os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
                        python = sys.executable
                        os.execl(python, '"' + python + '"', *sys.argv)
                except Exception: print(traceback.format_exc())
                return True
            else:
                print(f"Repository: {selected_branch}\nCheckout status: {checkout.stderr}")
                tex.insert(END,f"Repository: {selected_branch}\nCheckout Status ({checkout.returncode}): {checkout.stderr}")
                if 'Please commit your changes or stash them before you switch branches.' in checkout.stderr:
                    print()
                tex.insert(END,"==========================================\n")
                tex.see(tk.END)
                self.git_branch.set(current_branch)
                return False
        def forceupdate_hon(self,force,identifier,hoster, regionshort, serverid, servertotal,hondirectory,honreplay,svr_login,svr_password,static_ip, bottoken,discordadmin,master_server,force_update,disable_bot,alert_on_crash,alert_on_lag,alert_list_limit,event_list_limit,auto_update,use_console,use_proxy,restart_proxy,game_port,voice_port,core_assignment,process_priority,botmatches,debug_mode,selected_branch,increment_port):
            global update_counter
            global first_check_complete
            global update_counter
            global updating
            
            update_counter=0
            timeout=0
            patch_succesful = False
            current_version=dmgr.mData.check_hon_version(self,f"{self.dataDict['hon_directory']}hon_x64.exe")
            latest_version=svrcmd.honCMD().check_upstream_patch()

            #   add trailing slash to directory name if missing
            hondirectory = os.path.join(hondirectory, '')
            current_hon_version=current_version.split('.')

            wrong_bins = False
            if len(current_hon_version) == 0:
                wrong_bins = True
                return False
            else:
                try:
                    for i in current_hon_version:
                        ver = int(i)
                except:
                    wrong_bins = True
            if wrong_bins:
                initialise.print_and_tex(self,"An incorrect HoN exe was detected. The version from the file is unable to be read. Indicating this is not the correct hon exe file.\nPlease copy in correct server binaries and try again.",'WARNING')
                return False
            
            if latest_version != False:
                latest_version_list = latest_version.split('.')
                if len(latest_version_list) == 3:
                    latest_version = f"{'.'.join(latest_version_list)}.0"

            if ((current_version != latest_version) and latest_version != False and not updating) or force:
                updating = True
                print(f"Update available. {current_version} --> {latest_version}")
                tex.insert(END,f"Update available. {current_version} --> {latest_version}")
                tex.see(tk.END)
                ready_for_update = honfigurator.stop_all_for_update(self)
                if ready_for_update:
                    os.chdir(hondirectory)
                    #sp.call(["hon_x64.exe","-update","-masterserver",master_server])
                    #sp.call(["hon_update_x64.exe"])
                    update_running = initialise.check_proc("hon_update_x64.exe")
                    if update_running:
                        svrcmd.honCMD.stop_proc_by_name("hon_update_x64.exe")
                    if exists("Update\\hon_update_x64.exe.zip"):
                        os.remove("Update\\hon_update_x64.exe.zip")
                    #sp.Popen(["hon_update_x64.exe"])
                    sp.Popen(["hon_x64.exe","-update","-masterserver",master_server])
                    while (current_version != latest_version):
                        time.sleep(30)
                        current_version = dmgr.mData.check_hon_version(self,f"{self.dataDict['hon_directory']}hon_x64.exe")
                        print("still updating...")
                        timeout+=1
                        if timeout==6:
                            if svrcmd.honCMD.check_proc("hon_update_x64.exe"):
                                svrcmd.honCMD.stop_proc_by_name("hon_update_x64.exe")
                            break
                    try:
                        os.chdir(application_path)
                    except Exception:
                        print(traceback.format_exc())
                    if dmgr.mData.check_hon_version(self,f"{self.dataDict['hon_directory']}hon_x64.exe") == latest_version:
                        print("Patch successful!")
                        if force:
                            print("Please wait 60 seconds..")
                            time.sleep(60)
                        if svrcmd.honCMD.check_proc("hon_x64_tmp.exe"):
                            svrcmd.honCMD.stop_proc_by_name("hon_x64_tmp.exe")
                        if svrcmd.honCMD.check_proc("hon_update_x64.exe"):
                            svrcmd.honCMD.stop_proc_by_name("hon_update_x64.exe")
                        tex.insert(END,"Patch successful!")
                        if not first_time_installed:
                            print("Relaunching servers")
                            honfigurator.sendData(self,identifier,hoster,regionshort,serverid,0,servertotal,hondirectory,honreplay,svr_login,svr_password,static_ip, bottoken,discordadmin,master_server,True,disable_bot,alert_on_crash,alert_on_lag,alert_list_limit,event_list_limit,auto_update,use_console,use_proxy,True,game_port,voice_port,core_assignment,process_priority,botmatches,debug_mode,selected_branch,increment_port)
                        else:
                            initialise.print_and_tex(self,"Servers updated successfully, now ready to be configured.","interest")
                        update_counter = update_delay
                        updating = False
                        return True
                    else:
                        initialise.print_and_tex(self,"Patch failed! Please try again later or use force update hon",'warning')
                        updating = False
                        return False
                initialise.print_and_tex(self,"not all servers are ready for update. Trying again later",'warning')
            else:
                if updating:
                    initialise.print_and_tex(self,"already updating.")
                else:
                    tex.insert(END,f"Server is already at the latest version ({latest_version}).\n")
                    print(f"Server is already at the latest version ({latest_version}).")
                    tex.see(tk.END)
        def save_settings(self,*args, **kwargs):
            honfigurator.update_local_config(self,*args, **kwargs)
            self.dataDict = dmgr.mData().returnDict()
            initialise.print_and_tex(self,"Settings Saved.",'interest')
        def update_local_config_val(self,key,val):
            key = str(key)
            val = str(val)
            conf_local = configparser.ConfigParser()
            conf_local.read(config_local)
            self.confDict = {}
            for option in conf_local.options("OPTIONS"):
                self.confDict.update({option:conf_local['OPTIONS'][option]})
            conf_local.set("OPTIONS",key,val)
            with open(config_local, "w") as c:
                conf_local.write(c)
            c.close()
        def update_local_config(self,hoster,regionshort,serverid,servertotal,hondirectory,honreplay,svr_login,svr_password,static_ip,bottoken,discordadmin,master_server,force_update,disable_bot,alert_on_crash,alert_on_lag,alert_list_limit,event_list_limit,auto_update,use_console,use_proxy,restart_proxy,game_port,voice_port,core_assignment,process_priority,botmatches,debug_mode,selected_branch,increment_port):
            conf_local = configparser.ConfigParser()
            #conf_local.read(config_local)
            self.basic_dict = dmgr.mData.returnDict_basic(self,serverid)

            hondirectory = os.path.join(hondirectory, '') #   adds a trailing slash to the end of the path if there isn't one. Required because the code breaks if a slash isn't provided
            honreplay = os.path.join(honreplay,'')

            discordadmin = discordadmin.replace(" (DISABLED)","")
            bottoken = bottoken.replace(" (DISABLED)","")

            if use_proxy:
                game_port = int(game_port) - 10000
                voice_port = int(voice_port) - 10000
                if game_port < 5000:
                    game_port +=10000
                if voice_port < 5000:
                    voice_port +=10000
                if game_port > 18000:
                    game_port -=10000
                if voice_port > 18000:
                    voice_port -=10000
            #
            #   local config
            if not conf_local.has_section("OPTIONS"):
                conf_local.add_section("OPTIONS")
            conf_local.set("OPTIONS","svr_hoster",hoster)
            #conf_local.set("OPTIONS","svr_region",region)
            conf_local.set("OPTIONS","svr_region_short",regionshort)
            conf_local.set("OPTIONS","svr_id",str(serverid))
            if static_ip != '':
                conf_local.set("OPTIONS","static_ip",'True')
                conf_local.set("OPTIONS","svr_ip",str(static_ip))
            else:
                conf_local.set("OPTIONS","svr_ip",self.dataDict['svr_ip'])
            conf_local.set("OPTIONS","svr_total",servertotal)
            conf_local.set("OPTIONS","token",bottoken)
            conf_local.set("OPTIONS","hon_directory",hondirectory)
            conf_local.set("OPTIONS","hon_manager_dir",honreplay)
            conf_local.set("OPTIONS","discord_admin",discordadmin)
            conf_local.set("OPTIONS","master_server",master_server)
            conf_local.set("OPTIONS","allow_botmatches",f'{botmatches}')
            conf_local.set("OPTIONS","core_assignment",core_assignment)
            conf_local.set("OPTIONS","process_priority",process_priority)
            conf_local.set("OPTIONS","incr_port_by",increment_port)
            conf_local.set("OPTIONS","game_starting_port",str(game_port))
            conf_local.set("OPTIONS","voice_starting_port",str(voice_port))
            conf_local.set("OPTIONS","github_branch",str(selected_branch))
            conf_local.set("OPTIONS","debug_mode",str(debug_mode))
            conf_local.set("OPTIONS","use_proxy",str(use_proxy))
            conf_local.set("OPTIONS","svr_login",svr_login)
            conf_local.set("OPTIONS","svr_password",svr_password)
            conf_local.set("OPTIONS","use_console",str(use_console))
            conf_local.set("OPTIONS","sdc_home_dir",self.basic_dict['sdc_home_dir'])
            conf_local.set("OPTIONS","disable_bot",str(disable_bot))
            conf_local.set("OPTIONS","disc_alert_on_crash",str(alert_on_crash))
            conf_local.set("OPTIONS","disc_alert_on_lag",str(alert_on_lag))
            conf_local.set("OPTIONS","disc_alert_list_limit",str(alert_list_limit))
            conf_local.set("OPTIONS","disc_event_list_limit",str(event_list_limit))
            conf_local.set("OPTIONS","auto_update",str(auto_update))
            with open(config_local, "w") as c:
                conf_local.write(c)
            c.close()
            #self.dataDict = dmgr.mData().returnDict()
            #initialise.print_and_tex(self,"NOTE: These settings will not be applied until you configure servers with the new values.",'warning')
        def return_currentver(self):
            manifest=f"{self.dataDict['hon_directory']}Update\\manifest.xml"
            if exists(manifest):
                with open(manifest,'r') as f:
                    for line in f:
                        if "manifest version=" in line:
                            ver=line.split(" ")
                            return ver
            return "couldn't find version number."
        def sendData(self,identifier,hoster, regionshort, serverid,serverto,servertotal,hondirectory,honreplay,svr_login,svr_password,static_ip, bottoken,discordadmin,master_server,force_update,disable_bot,alert_on_crash,alert_on_lag,alert_list_limit,event_list_limit,auto_update,use_console,use_proxy,restart_proxy,game_port,voice_port,core_assignment,process_priority,botmatches,debug_mode,selected_branch,increment_port):
            global config_local
            global config_global
            global ports_to_forward_game
            global ports_to_forward_voice

            self.dataDict = self.initdict.returnDict()

            current_hon_version=dmgr.mData.check_hon_version(self,f"{self.dataDict['hon_directory']}hon_x64.exe")
            current_hon_version=current_hon_version.split('.')

            hondirectory = os.path.join(hondirectory, '') #   adds a trailing slash to the end of the path if there isn't one. Required because the code breaks if a slash isn't provided
            honreplay = os.path.join(honreplay,'')

            # if use_proxy:
            #game_port = str(int(game_port) - 10000)
            #voice_port = str(int(voice_port) - 10000)

            wrong_bins = False
            if len(current_hon_version) == 0:
                wrong_bins = True
                return False
            else:
                try:
                    for i in current_hon_version:
                        ver = int(i)
                except:
                    wrong_bins = True
            if wrong_bins:
                initialise.print_and_tex(self,"An incorrect HoN exe was detected. The version from the file is unable to be read. Indicating this is not the correct hon exe file.\nPlease copy in correct server binaries and try again.",'WARNING')
                return False

            checks=True
            initialise.print_and_tex(self,"\n************* Preparing environment *************",'header')
            if " " in hoster:
                checks=False
                initialise.print_and_tex(self,"FIXME: Please ensure there are no spaces in the server name field.",'warning')
            if " " not in hondirectory:
                checks=False
                initialise.print_and_tex(self,"FIXME: Please ensure there is a space in the HoN Directory path.",'warning')
            if bottoken=='' and disable_bot == False:
                checks=False
                initialise.print_and_tex(self,"FIXME: Please provide a bot token.",'warning')
            if discordadmin=='' and disable_bot == False:
                checks=False
                initialise.print_and_tex(self,"FIXME: Please provide a discord user ID (10 digit number).",'warning')
            if not exists(hondirectory+'proxy.exe'):
                initialise.print_and_tex(self,f"FIXME: NO PROXY.EXE FOUND. Please obtain this and place it into {hondirectory} and try again.\nOr disable proxy and try again..",'warning')
                checks=False
            if not exists(hondirectory+'proxymanager.exe'):
                initialise.print_and_tex(self,f"FIXME: NO PROXYMANAGER.EXE FOUND. Please obtain this and place it into {hondirectory} and try again.\nOr disable proxy and try again..",'warning')
                checks=False
            if static_ip != '':
                try:
                    # legal
                    socket.inet_aton(static_ip)
                    initialise.print_and_tex(self,f"Static IP configured. {static_ip} will be used to start your servers.",'interest')
                except socket.error:
                    # Not legal
                    checks=False
                    initialise.print_and_tex(self,"FIXME: Please provide a valid IPv4 address.",'warning')
            if checks == False:
                return
            else:
                ports_to_forward_game=[]
                ports_to_forward_voice=[]
                initialise.add_hosts_entry(self)
                #   initialise.print_and_tex(self,("UDP PORTS TO FORWARD (Auto-Server-Selector): "+str((int(self.dataDict['game_starting_port']) - 1))))
                firewall = initialise.configure_firewall_port(self,'HoN Ping Responder',int(game_port) - 1)
                if honreplay != self.dataDict['hon_manager_dir']:
                    force_update = True
                    if not exists(honreplay):
                        try:
                            os.makedirs(honreplay)
                            initialise.print_and_tex(self,f"CHECKME: Base directory {honreplay} has been created. Continuing on",'warning')
                        except Exception:
                            print(traceback.format_exc())
                            initialise.print_and_tex(self,f"FIXME: Unable to create directory: {honreplay} is it a valid path?",'warning')
                            return
                    if exists(honreplay):
                        print("migrating data")
                        if not exists(honreplay+"\\Documents\\Heroes of Newerth x64\\game\\replays"):
                            try:
                                os.makedirs(honreplay+"\\Documents\\Heroes of Newerth x64\\game\\replays")
                            except Exception:
                                print(traceback.format_exc())
                            initialise.print_and_tex(self,f"FIXME: Failed to create directory {honreplay}\\Documents\\Heroes of Newerth x64\\game\\replays\nIs it a valid path?",'warning')    
                        try:
                            distutils.dir_util.copy_tree(f"{self.dataDict['hon_manager_dir']}\\Documents\\Heroes of Newerth x64\\game\\replays",f"{honreplay}\\Documents\\Heroes of Newerth x64\\game\\replays",update=1)
                            initialise.print_and_tex(self,"You have changed the hon replays directory. Please ensure you configure all servers.",'interest')
                            initialise.print_and_tex(self,f"All replays migrated to {honreplay}\\Documents\\Heroes of Newerth x64\\game\\replays.\nYou may want to manually clean up the old directory: {self.dataDict['hon_manager_dir']} to free up disk space.",'interest')
                            self.dataDict.update({'hon_manager_dir':honreplay})
                        except Exception:
                            print(traceback.format_exc())
                            initialise.print_and_tex(self,f"FIXME: Failed to migrate data from {self.dataDict['hon_manager_dir']} to {honreplay}",'warning')
                # stop services that sit outside the total server range
                if int(servertotal) < int(self.dataDict['svr_total']):
                    x=int(self.dataDict['svr_total']) - int(servertotal)
                    for i in range (1,x+1):
                        o=int(servertotal)+i
                        temp_dict = dmgr.mData.returnDict_basic(self,o)
                        initialise.print_and_tex(self,"disable "+str(o),'warning')
                        playercount=initialise.playerCountX(self,o)
                        service_state = initialise.get_service(f"adminbot{o}")
                        if playercount == 0:
                            if service_state:
                                if service_state['status'] == 'running':
                                    initialise.stop_service(self,f"adminbot{o}",False)
                            initialise.stop_bot(self,f"adminbot{o}.exe")
                            initialise.stop_bot(self,f"KONGOR_ARENA_{o}.exe")
                            initialise.stop_bot(self,f"HON_SERVER_{o}.exe")
                        elif playercount > 0:
                            print("scheduled shutdown of no longer required service as it sits outside the total servers range")
                            initialise.schedule_shutdown(temp_dict)
                elif int(servertotal) > int(self.dataDict['svr_total']) and restart_proxy == False:
                    initialise.print_and_tex(self,f"Servers {int(self.dataDict['svr_total'])+1} to {servertotal} are not configured to run under the proxy. The proxy was only configured for servers 1 to {self.dataDict['svr_total']}",'warning')
                    initialise.print_and_tex(self,f"Select 'restart proxy in next configure' to resolve this. This may disrupt games which are in progress.",'warning')

                
                # write config to file
                honfigurator.update_local_config(self,hoster,regionshort, serverid, servertotal,hondirectory,honreplay,svr_login,svr_password,static_ip, bottoken,discordadmin,master_server,force_update,disable_bot,alert_on_crash,alert_on_lag,alert_list_limit,event_list_limit,auto_update,use_console,use_proxy,restart_proxy,game_port,voice_port,core_assignment,process_priority,botmatches,debug_mode,selected_branch,increment_port)

                self.dataDict = self.initdict.returnDict()

                if use_proxy:
                    firewall = initialise.configure_firewall(self,"HoN Proxy",hondirectory+'proxy.exe')
                #service_proxy_name="HoN Proxy Manager"
                service_manager_name="HoN Server Manager"
                manager_application=f"KONGOR ARENA MANAGER.exe"
                #service_proxy = initialise.get_service(service_proxy_name)
                service_manager = initialise.get_service(service_manager_name)
                default_voice_port=11435
                if self.dataDict['use_proxy'] == 'False':
                    udp_listener_port = int(self.dataDict['game_starting_port']) - 1
                else:
                    udp_listener_port = int(self.dataDict['game_starting_port']) + 10000 - 1
                manager_arguments=f"Set svr_port {udp_listener_port}; Set man_masterLogin {self.dataDict['svr_login']}:;Set man_masterPassword {self.dataDict['svr_password']};Set upd_checkForUpdates False;Set man_numSlaveAccounts 0;Set man_startServerPort {self.dataDict['game_starting_port']};Set man_endServerPort {int(self.dataDict['game_starting_port'])+(int(self.dataDict['svr_total'])-1)};Set man_voiceProxyStartPort {self.dataDict['voice_starting_port']};Set man_voiceProxyEndPort {int(self.dataDict['voice_starting_port'])+(int(self.dataDict['svr_total'])-1)};Set man_maxServers {self.dataDict['svr_id']};Set man_enableProxy {self.dataDict['use_proxy']};Set man_broadcastSlaves true;Set http_useCompression false;Set man_autoServersPerCPU 1;Set man_allowCPUs 0;Set host_affinity -1;Set man_uploadToS3OnDemand 1;Set man_uploadToCDNOnDemand 0;Set svr_name {self.dataDict['svr_hoster']} 0 0;Set svr_location {self.dataDict['svr_region_short']};Set svr_ip {self.dataDict['svr_ip']}"
                os.environ["USERPROFILE"] = self.dataDict['hon_manager_dir']

                manager_running=svrcmd.honCMD.check_proc(manager_application)
                copy_retry = False
                
                hash1=dmgr.mData.get_hash(f"{hondirectory}{manager_application}")
                hash2=dmgr.mData.get_hash(f"{hondirectory}hon_x64.exe")
                if not exists(f"{hondirectory}KONGOR ARENA MANAGER.exe") or (hash1 != hash2):
                    try:
                        shutil.copy(f"{hondirectory}hon_x64.exe",f"{hondirectory}{manager_application}")
                    except PermissionError:
                        copy_retry=True

                if force_update or manager_running==False:
                    initialise.print_and_tex(self,"\n************* Configuring Replay Manager *************","header")
                    if service_manager:
                        if use_console == False:
                            initialise.configure_service_generic(self,service_manager_name,manager_application,f"-manager -noconfig -execute \"{manager_arguments}\" -masterserver {master_server}")
                        if service_manager['status'] == 'running' or service_manager['status'] == 'paused':
                            initialise.stop_service(self,service_manager_name,False)
                        else:
                            if svrcmd.honCMD.check_proc(manager_application):
                                svrcmd.honCMD.stop_proc_by_name(manager_application)
                        if copy_retry:
                            shutil.copy(f"{hondirectory}hon_x64.exe",f"{hondirectory}{manager_application}")
                        if use_console == False:
                            initialise.start_service(self,service_manager_name,False)
                        else:
                            sp.Popen([hondirectory+manager_application,"-manager","-noconfig","-execute",manager_arguments,"-masterserver",master_server])
                    else:
                        if svrcmd.honCMD.check_proc(manager_application):
                            svrcmd.honCMD.stop_proc_by_name(manager_application)
                        if use_console == False:
                            initialise.create_service_generic(self,service_manager_name,manager_application)
                            initialise.configure_service_generic(self,service_manager_name,manager_application,f"-manager -noconfig -execute \"{manager_arguments}\" -masterserver {master_server}")
                            initialise.start_service(self,service_manager_name,False)
                        else:
                            sp.Popen([hondirectory+manager_application,"-manager","-noconfig","-execute",manager_arguments,"-masterserver",master_server])
                    if svrcmd.honCMD.check_proc(manager_application):
                        initialise.print_and_tex(self,"Done.",'interest')
                if use_proxy:
                    initialise.print_and_tex(self,"\n************* Configuring Proxy Manager *************","header")
                    proxy_running=False
                    os.environ["APPDATA"] = self.dataDict['hon_root_dir']
                    application="proxymanager.exe"
                    service_proxy_name="HoN Proxy Manager"
                    service_proxy = initialise.get_service(service_proxy_name)
                    if svrcmd.honCMD.check_proc(application):
                        proxy_running=True
                    # if service_proxy:
                    print("proxy exists")
                    proxy_config=[f"count={servertotal}",f"ip={self.dataDict['svr_ip']}",f"startport={int(game_port)-10000}",f"startvoicePort={int(voice_port)-10000}","region=naeu"]
                    proxy_config_location=f"{self.dataDict['hon_root_dir']}\\HonProxyManager"
                    if not exists(proxy_config_location):
                        os.makedirs(proxy_config_location)
                    proxy_config_location=f"{proxy_config_location}\\config.cfg"
                    with open(proxy_config_location,"w") as f:
                        for items in proxy_config:
                            f.write(f"{items}\n")
                    if restart_proxy or proxy_running==False:
                        # if use_console == False:
                        if service_proxy:
                            initialise.configure_service_generic(self,service_proxy_name,application,None)
                            if service_proxy['status'] == 'running' or service_proxy['status'] == 'paused':
                                initialise.stop_service(self,service_proxy_name,False)
                            if svrcmd.honCMD.check_proc(application):
                                svrcmd.honCMD.stop_proc_by_name(application)
                            if svrcmd.honCMD.check_proc("proxy.exe"):
                                svrcmd.honCMD.stop_proc_by_name("proxy.exe")
                            initialise.start_service(self,service_proxy_name,False)
                        else:
                            if svrcmd.honCMD.check_proc(application):
                                svrcmd.honCMD.stop_proc_by_name(application)
                            initialise.create_service_generic(self,service_proxy_name,application)
                            initialise.configure_service_generic(self,service_proxy_name,application,None)
                            initialise.start_service(self,service_proxy_name,False)
                        tem_counter = 0
                        while not initialise.check_port(int(self.dataDict['svr_proxyPort'])):
                            time.sleep(1)
                            print(f"waiting {tem_counter}/30 seconds for proxy to finish setting up ports...")
                            tem_counter +=1
                            if tem_counter == 30:
                                initialise.print_and_tex(self,f"timed out waiting for proxy to start listening on port {self.dataDict['svr_proxyPort']}",'WARNING')
                                return False
                        self.restart_proxy.set(False)
                    if svrcmd.honCMD.check_proc(application):
                        initialise.print_and_tex(self,"Done.",'interest')
                
                initialise.print_and_tex(self,f"\n************* Configuring adminbots *************","header")
                if identifier == "selected":
                    # self.dataDict = dmgr.mData().returnDict()
                    # print()
                    for i in range(int(serverid),int(serverto)+1):
                        serverid = i
                        honfigurator.update_local_config(self,hoster,regionshort, serverid, servertotal,hondirectory,honreplay,svr_login,svr_password,static_ip, bottoken,discordadmin,master_server,force_update,disable_bot,alert_on_crash,alert_on_lag,alert_list_limit,event_list_limit,auto_update,use_console,use_proxy,restart_proxy,game_port,voice_port,core_assignment,process_priority,botmatches,debug_mode,selected_branch,increment_port)
                        self.dataDict = dmgr.mData().returnDict()
                        hon_api_updated = False
                        initialise(self.dataDict).configureEnvironment(force_update,use_console)

                elif identifier == "all":
                    print("Selected option to configure ALL servers\n")
                    threads = []
                    for i in range(0,int(servertotal)):
                        serverid = i + 1
                        honfigurator.update_local_config(self,hoster,regionshort,serverid,servertotal,hondirectory,honreplay,svr_login,svr_password,static_ip,bottoken,discordadmin,master_server,force_update,disable_bot,alert_on_crash,alert_on_lag,alert_list_limit,event_list_limit,auto_update,use_console,use_proxy,restart_proxy,game_port,voice_port,core_assignment,process_priority,botmatches,debug_mode,selected_branch,increment_port)
                        self.dataDict = dmgr.mData().returnDict()
                        hon_api_updated = False
                        initialise(self.dataDict).configureEnvironment(force_update,use_console)
                        
                initialise.print_and_tex(self,"\n************ Summary **************","header")
                #   a group has been selected
                if identifier == 'selected':
                    first = int(serverid)
                    last = int(serverto)
                #   total servers selected, do all
                else:
                    first = 0
                    last = int(servertotal)
                time.sleep(2)
                successful = []
                failed = []
                if last - first == 0:
                    if initialise.check_proc(f"adminbot{first}.exe"):
                        successful.append(f"adminbot{first}")
                    else:
                        failed.append(f"adminbot{first}")
                else:
                    for i in range(first,last):
                        if initialise.check_proc(f"adminbot{i+1}.exe"):
                            successful.append(f"adminbot{i+1}")
                        else:
                            failed.append(f"adminbot{i+1}")
                if len(successful) > 0:
                    initialise.print_and_tex(self,f"SUCCESSFULLY CONFIGURED: {', '.join(successful)}",'interest')
                if len(failed) > 0:
                    initialise.print_and_tex(self,f"FAILED TO CONFIGURE: {', '.join(failed)}",'warning')
                initialise.print_and_tex(self,f"UDP PORTS TO FORWARD (Game): {', '.join(map(str,ports_to_forward_game))}",'interest')
                initialise.print_and_tex(self,f"UDP PORTS TO FORWARD (Voice): {', '.join(map(str,ports_to_forward_voice))}",'interest')
                if self.dataDict['use_proxy'] == 'False':
                    initialise.print_and_tex(self,("UDP PORTS TO FORWARD (Auto-Server-Selector): "+str((int(self.dataDict['game_starting_port']) - 1))),'interest')
                else:
                    initialise.print_and_tex(self,("UDP PORTS TO FORWARD (Auto-Server-Selector): "+str((int(self.dataDict['game_starting_port']) + 10000 - 1))),'interest')
                return
        def check_deployed_update(self):
            global ports_to_forward_game
            global ports_to_forward_voice
            global first_check_complete

            ports_to_forward_game=[]
            ports_to_forward_voice=[]
            t = self.dataDict['svr_total']
            current_ver = float(self.dataDict['bot_version'])
            for i in range (1,(int(t)+1)):
                temp={}
                temp_incoming={}
                deployed_server={}
                try:
                    temp = dmgr.mData.returnDict_deployed(self,i)
                    temp_incoming = dmgr.mData.returnDict_temp(temp)
                    deployed_server = temp_incoming | temp
                    deployed_ver = float(deployed_server['bot_version'])
                except KeyError:
                    print(f"adminbot{i} is not properly configured. It may require reconfiguration.")
                    return
                except Exception as e:
                    print(traceback.format_exc())
                    return
                if deployed_ver != current_ver:
                    game_port = int(deployed_server['game_starting_port'])
                    voice_port = int(deployed_server['voice_starting_port'])
                    if deployed_server['use_console'] == "True":
                        use_console=True
                    else:
                        use_console=False
                    if deployed_server['use_proxy'] == 'True':
                        if game_port < 10000: game_port = game_port + 20000
                        else: game_port = game_port + 10000
                        if voice_port < 10000: voice_port = voice_port + 20000
                        voice_port = voice_port + 10000
                    #initialise.print_and_tex(self,f"\nServer requires update (adminbot{i})")
                    #initialise.print_and_tex(self,f"\n==============================================\nHoNfigurator version change from {deployed_ver} ---> {current_ver}.\nAutomatically reconfiguring idle server instances, scheduling a restart for the rest.")
                    #honfigurator.update_local_config(self,self.tab3_hosterd.get(),self.tab3_regionsd.get(),i,self.tab1_servertd.get(),self.tab3_hondird.get(),self.tab3_honreplay.get(),self.tab3_user.get(),self.tab3_pass.get(),self.tab3_ip.get(),self.tab3_bottokd.get(),self.tab3_discordadmin.get(),self.tab3_masterserver.get(),True,self.enablebot.get(),use_console,self.useproxy.get(),self.restart_proxy.get(),self.tab3_game_port.get(),self.tab3_voice_port.get(),self.core_assign.get(),self.priority.get(),self.botmatches.get(),self.debugmode.get(),self.git_branch.get(),self.increment_port.get())
                    honfigurator.update_local_config(self,deployed_server['svr_hoster'],deployed_server['svr_region_short'],deployed_server['svr_id'],deployed_server['svr_total'],deployed_server['hon_directory'],deployed_server['hon_manager_dir'],deployed_server['svr_login'],deployed_server['svr_password'],deployed_server['svr_ip'],deployed_server['token'],deployed_server['discord_admin'],deployed_server['master_server'],True,deployed_server['disable_bot'],deployed_server['disc_alert_on_crash'],deployed_server['disc_alert_on_lag'],deployed_server['disc_alert_list_limit'],deployed_server['disc_event_list_limit'],deployed_server['auto_update'],deployed_server['use_console'],deployed_server['use_proxy'],False,game_port,voice_port,deployed_server['core_assignment'],deployed_server['process_priority'],deployed_server['allow_botmatches'],deployed_server['debug_mode'],deployed_server['github_branch'],deployed_server['incr_port_by'])
                    #if initialise.playerCountX(self,i) >= 0:
                    initialise.print_and_tex(self,f"\n************* Configuring adminbot{i} *************","header")
                    initialise.print_and_tex(self,f"HoNfigurator version change from {deployed_ver} ---> {current_ver}.",'warning')
                    initialise(deployed_server).configureEnvironment(True,use_console)
                    #honfigurator.sendData(self,False,"all",self.tab3_hosterd.get(),self.tab3_regionsd.get(),i,self.tab1_servertd.get(),self.tab3_hondird.get(),self.tab3_honreplay.get(),self.tab3_user.get(),self.tab3_pass.get(),self.tab3_ip.get(),self.tab3_bottokd.get(),self.tab3_discordadmin.get(),self.tab3_masterserver.get(),True,self.enablebot.get(),self.autoupdate.get(),self.console.get(),self.useproxy.get(),self.restart_proxy.get(),self.tab3_game_port.get(),self.tab3_voice_port.get(),self.core_assign.get(),self.priority.get(),self.botmatches.get(),self.debugmode.get(),self.git_branch.get(),self.increment_port.get())
        def stop_all_for_update(self):
            global first_time_installed

            players=False
            print("attempting to stop servers")
            for i in range (1,(int(self.dataDict['svr_total']) +1)):
                try:
                    pcount=initialise.playerCountX(self,i)
                    try:
                        deployed_status = dmgr.mData.returnDict_deployed(self,i)
                    except KeyError as e:
                        first_time_installed = True
                        print("first time launch")
                        return True
                    service_name=f"adminbot{i}"
                    service_check = initialise.get_service(service_name)
                    if pcount <= 0:
                        if service_check:
                            if service_check['status'] == 'running':
                                if initialise.stop_service(self,service_name,True):
                                    initialise.print_and_tex(self,f"{service_name} stopped successfully.")
                                else:
                                    initialise.print_and_tex(self,f"{service_name} failed to stop.")
                        bot_running=svrcmd.honCMD.check_proc(f"{service_name}.exe") # if there is still an adminbot process - the app is running in console mode, stop it
                        hon_running=svrcmd.honCMD.check_proc(deployed_status['hon_file_name'])
                        if bot_running or hon_running:
                            initialise.stop_bot(self,f"{service_name}.exe")
                            initialise.stop_bot(self,f"KONGOR_ARENA_{i}.exe")
                            initialise.stop_bot(self,f"HON_SERVER_{i}.exe")
                        else:
                            initialise.stop_bot(self,f"KONGOR_ARENA_{i}.exe")
                            initialise.stop_bot(self,f"HON_SERVER_{i}.exe")
                    else:
                        players=True
                        initialise.schedule_shutdown(deployed_status)
                except Exception:
                    print(traceback.format_exc())
                    return False
            if players==True:
                initialise.print_and_tex(self,"There are still some games in progress. Update requires that all servers are shutdown.\nA scheduled shutdown has been commenced. Server will update and restart automatically when all games complete","WARNING")
                return False
            else:
                print("Stopped all hon servers. Moving to update.")
                service_manager_name = "HoN Server Manager"
                manager_application = "KONGOR ARENA MANAGER.exe"
                service_manager = initialise.get_service(service_manager_name)
                if service_manager:
                    if service_manager['status'] == 'running' or service_manager['status'] == 'paused':
                        initialise.stop_service(self,service_manager_name,False)
                if svrcmd.honCMD.check_proc(manager_application):
                    svrcmd.honCMD.stop_proc_by_name(manager_application)
                service_proxy_name = "HON Proxy Manager"
                proxy_application = "proxymanager.exe"
                service_proxy = initialise.get_service(service_proxy_name)
                if service_proxy:
                    if service_proxy['status'] == 'running' or service_proxy['status'] == 'paused':
                        initialise.stop_service(self,service_proxy_name,False)
                if svrcmd.honCMD.check_proc(proxy_application):
                    svrcmd.honCMD.stop_proc_by_name(proxy_application)
                return True
        def botCount(self,num_of_bots):
            for i in range(0,num_of_bots):
                        row = i%8
                        column1 = (i/8)
                        column2 = int(column1)*2
                        column3 = int(column1)*3
                        if int(column2)==0:
                            column2 = 1
                            column3 = 2
                        if column1%1 == 0:
                            column2
                        self.bot_cmd_buttons[i][0].grid(column=int(column1),row=row,sticky='e',padx=2,pady=2)
                        self.bot_cmd_buttons[i][1].grid(column=column2,row=row,sticky='w',padx=[0,60],pady=0)
                        self.bot_cmd_buttons[i][1].grid(column=column3,row=row,sticky='w',padx=[0,60],pady=0)
                        self.bot_cmd_buttons[i][1].configure(textvariable=self.bot_cmd_buttons[i][2])
        class CreateToolTip(object):
            """
            create a tooltip for a given widget
            """
            def __init__(self, widget, text='widget info'):
                self.waittime = 500     #miliseconds
                self.wraplength = 180   #pixels
                self.widget = widget
                self.text = text
                self.widget.bind("<Enter>", self.enter)
                self.widget.bind("<Leave>", self.leave)
                self.widget.bind("<ButtonPress>", self.leave)
                self.id = None
                self.tw = None

            def enter(self, event=None):
                self.schedule()

            def leave(self, event=None):
                self.unschedule()
                self.hidetip()

            def schedule(self):
                self.unschedule()
                self.id = self.widget.after(self.waittime, self.showtip)

            def unschedule(self):
                id = self.id
                self.id = None
                if id:
                    self.widget.after_cancel(id)

            def showtip(self, event=None):
                x = y = 0
                x, y, cx, cy = self.widget.bbox("insert")
                x += self.widget.winfo_rootx() + 25
                y += self.widget.winfo_rooty() + 20
                # creates a toplevel window
                self.tw = tk.Toplevel(self.widget)
                # Leaves only the label and removes the app window
                self.tw.wm_overrideredirect(True)
                self.tw.wm_geometry("+%d+%d" % (x, y))
                label = tk.Label(self.tw, text=self.text, justify='left',
                            background="#ffffff", relief='solid', borderwidth=1,
                            wraplength = self.wraplength)
                label.pack(ipadx=1)

            def hidetip(self):
                tw = self.tw
                self.tw= None
                if tw:
                    tw.destroy()
        def creategui(self):
            global ButtonString,LablString
            ButtonString = ['View Log', 'Start', 'Clean', 'Uninstall']
            LablString = ['hon_server_','status']
            class viewButton():
                class Autoresized_Notebook(Notebook):
                    def __init__(self, master=None, **kw):
                        Notebook.__init__(self, master, **kw)
                        self.bind("<<NotebookTabChanged>>",self._on_tab_changed)
        
                    def _on_tab_changed(self,event):
                        global pb

                        app.winfo_toplevel().geometry("")
                        # if tabgui.index("current") == 2:
                        # #         for o in range(mod_by):
                        # #             Label(tab2,text="",foreground='white',background=maincolor).grid(row=o,column=7)
                        #     if server_admin_loading:
                        #         #progressbar
                        #         pb = ttk.Progressbar(
                        #             tabgui,
                        #             orient='horizontal',
                        #             mode='indeterminate',
                        #             length=280
                        #         )
                        #         # place the progressbar
                        #         pb.grid(column=0,sticky='n',row=2, columnspan=8, padx=10, pady=[30,10])
                        #         pb.start()
                        event.widget.update_idletasks()
                        tab = event.widget.nametowidget(event.widget.select())
                        event.widget.configure(height=tab.winfo_reqheight())
                    def _on_demand(self,tab):
                        tab.configure(height=tab.winfo_reqheight())
                # tabgui2 = ttk.Notebook(tab2)
                # tabgui2.grid(column=0,row=14)
                #def __init__(self,btn,i,pcount):
                def __init__(self,btn,i,p):
                    global id
                    global pcount
                    global deployed_status
                    global service_name

                    self.base = dmgr.mData.parse_config(self,os.path.abspath(application_path)+"\\config\\honfig.ini")
                    service_name = f"adminbot{i}"
                    id = i
                    pcount = p
                    self.initdict = dmgr.mData()
                    self.dataDict = self.initdict.returnDict()
                    deployed_status = dmgr.mData.returnDict_deployed(self,id)
                    # self.pcount = pcount
                    print(f"{i} {btn}")
                    if btn == "View Log":
                        Thread(target=viewButton.ViewLog,args=[self]).start()
                    elif btn == "Stop":
                        Thread(target=viewButton.Stop,args=[self]).start()
                    elif btn == "Start":
                        Thread(target=viewButton.Start,args=[self]).start()
                        #viewButton.refresh()
                    elif btn == "Clean":
                        Thread(target=viewButton.Clean,args=[self]).start()
                    elif btn == "Uninstall":
                        viewButton.Uninstall(self,id)
                def clear_frame():
                    list = tab2.grid_slaves()
                    for l in list:
                        l.destroy()
                def clear_frame_1():
                    list = tab1.grid_slaves()
                    for l in list:
                        l.destroy()
                def clear_frame_2():
                    list = tab2.grid_slaves()
                    for l in list:
                        l.destroy()
                def clear_frame_3():
                    list = tab3.grid_slaves()
                    for l in list:
                        l.destroy()
                def elapsed_since(start):
                    return time.strftime("%H:%M:%S", time.gmtime(time.time() - start))
                
                
                def get_process_memory():
                    process = psutil.Process(os.getpid())
                    mem_info = process.memory_info()
                    return mem_info.rss

                def profile(func):
                    def wrapper(*args, **kwargs):
                        mem_before = viewButton.get_process_memory()
                        start = time.time()
                        result = func(*args, **kwargs)
                        elapsed_time = viewButton.elapsed_since(start)
                        mem_after = viewButton.get_process_memory()
                        print("{}: memory before: {:,}, after: {:,}, consumed: {:,}; exec time: {}".format(
                            func.__name__,
                            mem_before, mem_after, mem_after - mem_before,
                            elapsed_time))
                        return result
                    return wrapper
                def display_top(snapshot, key_type='lineno', limit=10, where=''):
                    print('======================================================================')
                    if where != '':
                        print(f'Printing stats:\n    {where}')
                        print('======================================================================')
                    

                    snapshot = snapshot.filter_traces((
                        tracemalloc.Filter(False, '<frozen importlib._bootstrap>'),
                        tracemalloc.Filter(False, '<unknown>'),
                    ))
                    top_stats = snapshot.statistics(key_type)

                    print(f'Top {limit} lines')
                    for index, stat in enumerate(top_stats[:limit], 1):
                        frame = stat.traceback[0]
                        # replace '/path/to/module/file.py' with 'module/file.py'
                        filename = os.sep.join(frame.filename.split(os.sep)[-2:])
                        print(f'#{index}: {filename}:{frame.lineno}: {stat.size / 1024:.1f} KiB')
                        line = linecache.getline(frame.filename, frame.lineno).strip()
                        if line:
                            print(f'    {line}')

                    other = top_stats[limit:]
                    if other:
                        size = sum(stat.size for stat in other)
                        print(f'{len(other)} other: {size / 1024:.1f} KiB')
                    total = sum(stat.size for stat in top_stats)
                    print()
                    print(f'=====> Total allocated size: {total / 1024:.1f} KiB')
                    print()
                def refresh(*args):
                    global mod_by
                    global refresh_next
                    global refresh_counter
                    # global auto_refresh_var
                    global stretch
                    global first_tab_switch
                    global server_admin_loading
                    global labllist
                    refresh_next=False
                    refresh_counter = 0
                    global thread
                    #if not first_tab_switch: tracker = SummaryTracker()
                    #Autoresized_Notebook._on_tab_changed()
                    if tabgui.index("current") in [0,1]:    
                        ver=dmgr.mData.check_hon_version(self,f"{self.dataDict['hon_directory']}hon_x64.exe")
                        status = Entry(self.app,background=maincolor,foreground='white',width="200")
                        status.delete(0,END)
                        status.insert(0,f"HoN Server Version: {ver}     |     Version on Master Server: {svrcmd.honCMD().check_upstream_patch()}")
                        status.grid(row=21,column=0,sticky='w')

                    # if len(args) >= 1 and type(args[0]) is int:
                    #     mod_by = args[0]
                    try: 
                        if (mod_by != int(stretch.get())+3):
                            print("Number of servers to display has changed. Resizing window.")
                            mod_by = int(stretch.get())+3
                            labllist.clear()
                            viewButton.clear_frame()
                        # else:
                        #     honfigurator.CreateToolTip.leave()
                    except Exception: pass
                    if not server_admin_loading:
                        #print("REFRESHING")
                        if (first_tab_switch and tabgui.index("current") == 2):
                            viewButton.load_server_mgr(self)
                        else:
                            #viewButton.load_server_mgr(self)
                            thread = Thread(target=viewButton.load_server_mgr,args=[self])
                            thread.start()
                    
                    # snapshot = tracemalloc.take_snapshot()
                    # top_stats = snapshot.statistics('lineno')

                    # print("[ Top 10 ]")
                    # for stat in top_stats[:10]:
                    #     print(stat)
                    # if not first_tab_switch:
                    #     #tracker.print_diff()
                    #     print(mem_top())
                    
                def load_log(self,*args):
                    global bot_tab
                    try:
                        if (tabgui.index("current")) == 2:
                            if bot_tab !=tabgui2.index("current"):
                                Thread(target=viewButton.ViewLog,args=[self]).start()
                            bot_tab=tabgui2.index("current")
                            #viewButton.ViewLog(self)
                    except Exception: pass

                def ViewLog(self):
                    global latest_file
                    tex.delete('1.0', END)
                    try:
                        logs_dir = f"{deployed_status['hon_logs_dir']}\\"
                    except NameError:
                        print("please select 'view log' on a server to begin.")
                        tex.insert(END,"please select 'view log' on a server to begin.")
                        return
                    #print(str(deployed_status))
                    # Server Log
                    try:
                        if tabgui2.index("current") == 0:
                            if pcount <=0:
                                log_File = f"Slave*.log"
                            else:
                                log_File = f"Slave*{id}*.clog"
                            try:
                                list_of_files = glob.glob(logs_dir + log_File) # * means all if need specific format then *.csv
                                latest_file = max(list_of_files, key=os.path.getctime)
                                info=["New session cookie "," Connected","[ALL]","lag","spike","ddos"]
                                warnings=["Skipped","Session cookie request failed!","No session cookie returned!","Timeout","Disconnected","Connection to chat server terminated."]
                                with open(latest_file,'r',encoding='utf-16-le') as file:
                                    for line in file:
                                        tem=line.lower()
                                        if any(x.lower() in tem for x in warnings):
                                            tex.insert(tk.END,line,'warning')
                                        elif any(x.lower() in tem for x in info):
                                            tex.insert(tk.END,line,'interest')
                                        else:
                                            tex.insert(tk.END,line)
                                tex.see(tk.END)
                            except ValueError:
                                print("This service has most likely yet to be configured.")
                                tex.insert(END,"This service has most likely yet to be configured.",'WARNING')
                                tex.see(tk.END)

                        if (tabgui2.index("current")) == 1:
                            if pcount > 0:
                                logs_dir = f"{deployed_status['hon_logs_dir']}\\"
                                log_File = "M*.log"
                            else:
                                tex.insert(END,'No match in progress.')
                                tex.see(tk.END)
                                return
                            list_of_files = glob.glob(logs_dir + log_File) # * means all if need specific format then *.csv
                            latest_file = max(list_of_files, key=os.path.getctime)
                            info=["[ALL]","chat","lag","spike","ddos"]
                            warnings=["Skipped","Session cookie request failed!","No session cookie returned!"]
                            with open(latest_file,'r',encoding='utf-16-le') as file:
                                for line in file:
                                    tem=line.lower()
                                    if any(x.lower() in tem for x in warnings):
                                        tex.insert(tk.END,line,'warning')
                                    elif any(x.lower() in tem for x in info):
                                        tex.insert(tk.END,line,'interest')
                                    else:
                                        tex.insert(tk.END,line)
                            tex.see(tk.END)
                        if (tabgui2.index("current")) == 2:
                            logs_dir = f"{deployed_status['sdc_home_dir']}\\"
                            log_File = f"adminbot{id}.log"
                            list_of_files = glob.glob(logs_dir + log_File) # * means all if need specific format then *.csv
                            latest_file = max(list_of_files, key=os.path.getctime)
                            with open(latest_file,'r') as file:
                                for line in file:
                                    tem=line.lower()
                                    tex.insert(tk.END,line)
                            tex.see(tk.END)
                        if (tabgui2.index("current")) == 3:
                            logs_dir1 = f"{deployed_status['hon_root_dir']}\\HoNProxyManager\\"
                            #logs_dir2 = f"C:\\Windows\\SysWOW64\\config\\systemprofile\\AppData\\Roaming\\HonProxyManager\\"
                            log_File = f"proxy_{20000 + int(id) - 1}*.log"
                            list_of_files1 = glob.glob(logs_dir1 + log_File) # * means all if need specific format then *.csv
                            #list_of_files2 = glob.glob(logs_dir2 + log_File)
                            #list_of_files = list_of_files1 + list_of_files2
                            latest_file = max(list_of_files1, key=os.path.getctime)
                            warnings=["BANNED","BLOCKED","CLOSED","UNDER ATTACK"]
                            with open(latest_file,'r') as file:
                                for line in file:
                                    tem=line.lower()
                                    if any(x.lower() in tem for x in warnings):
                                        tex.insert(tk.END,line,'warning')
                                    else:
                                        tex.insert(tk.END,line)
                            tex.see(tk.END)
                        status = Entry(app,background=maincolor,foreground='white',width="200")
                        status.insert(0,f"Viewing hon_server_{id}: {latest_file}")
                        status.grid(columnspan=total_columns,row=21,column=0,sticky='w')
                        print(latest_file)                   
                        tex.see(tk.END)
                    except Exception: print(traceback.format_exc())

                def Start(self):
                    global refresh_counter
                    global refresh_delay
                    pcount = initialise.playerCountX(self,id)
                    deployed_status = dmgr.mData.returnDict_deployed(self,id)
                    if pcount == -3:
                        service_name=f"adminbot{id}"
                        if svrcmd.honCMD.check_proc(f"{service_name}.exe"):
                            svrcmd.honCMD.stop_proc_by_name(f"{service_name}.exe")
                        if self.dataDict['use_proxy']=='True':
                            if initialise.check_port(deployed_status['svr_proxyPort']):
                                pass
                            else:
                                tex.insert(END,"Proxy is not running. You may not start the server without the proxy first running.\n",'warning')
                                tex.see(tk.END)
                                return
                        if initialise.start_bot(self,True):
                            tex.insert(END,f"{deployed_status['app_name']} started successfully\n")
                            tex.see(tk.END)
                        t_out=0
                        while t_out < 15:
                            t_out +=1
                            time.sleep(1)
                            if initialise.check_proc(deployed_status['hon_file_name']):
                                if initialise.playerCountX(self,id) >= 0:
                                    t_out = 15
                        refresh_counter = refresh_delay
                        #viewButton.refresh()
                        return
                def StartProxy(self):
                    global refresh_counter
                    global refresh_delay
                    if not self.dataDict['use_proxy']=='True':
                        initialise.print_and_tex(self,"Proxy not enabled. Please configure some servers using the proxy.",'warning')
                        return
                    proxy_service = initialise.get_service("HoN Proxy Manager")
                    if not proxy_service:   
                        initialise.print_and_tex(self,"Proxy is not yet configured.")
                        return
                    initialise.start_service(self,"HoN Proxy Manager",True)
                    # time.sleep(1)
                    # if initialise.check_proc("proxymanager.exe"):
                    #     initialise.print_and_tex(self,"Proxy started.")
                    #     refresh_counter = refresh_delay
                    # else:
                    #     initialise.print_and_tex(self,"Failed to start the proxy service.")
                    #     refresh_counter = refresh_delay
                    # return
                    refresh_counter = refresh_delay

                def StopProxy(self):
                    global refresh_counter
                    global refresh_delay
                    if not self.dataDict['use_proxy']=='True':
                        initialise.print_and_tex(self,"Proxy not enabled. Please configure some servers using the proxy.",'WARNING')
                        return
                    proxy_service = initialise.get_service("HoN Proxy Manager")
                    if not proxy_service:   
                        initialise.print_and_tex(self,"Proxy is not yet configured.")
                        return
                    initialise.stop_service(self,"HoN Proxy Manager",True)
                    # time.sleep(1)
                    # if initialise.check_proc("proxymanager.exe"):
                    #     initialise.print_and_tex(self,"HoN Proxy Manager started.")
                    #     refresh_counter = refresh_delay
                    # else:
                    #    initialise.print_and_tex(self,"HoN Proxy Manager failed to start.")
                    refresh_counter = refresh_delay
                    #return

                def StartManager(self):
                    global refresh_counter,refresh_delay,labl_manager,btn_manager
                    
                    service_manager_name="HoN Server Manager"
                    manager_application=f"KONGOR ARENA MANAGER.exe"

                    if self.dataDict['use_proxy'] == 'False':
                        udp_listener_port = int(self.dataDict['game_starting_port']) - 1
                    else:
                        udp_listener_port = int(self.dataDict['game_starting_port']) + 10000 - 1

                    manager_arguments=f"Set svr_port {udp_listener_port}; Set man_masterLogin {self.dataDict['svr_login']}:;Set man_masterPassword {self.dataDict['svr_password']};Set upd_checkForUpdates False;Set man_numSlaveAccounts 0;Set man_startServerPort {self.dataDict['game_starting_port']};Set man_endServerPort {int(self.dataDict['game_starting_port'])+(int(self.dataDict['svr_total'])-1)};Set man_voiceProxyStartPort {self.dataDict['voice_starting_port']};Set man_voiceProxyEndPort {int(self.dataDict['voice_starting_port'])+(int(self.dataDict['svr_total'])-1)};Set man_maxServers {self.dataDict['svr_id']};Set man_enableProxy {self.dataDict['use_proxy']};Set man_broadcastSlaves true;Set http_useCompression false;Set man_autoServersPerCPU 1;Set man_allowCPUs 0;Set host_affinity -1;Set man_uploadToS3OnDemand 1;Set man_uploadToCDNOnDemand 0;Set svr_name {self.dataDict['svr_hoster']} 0 0;Set svr_location {self.dataDict['svr_region_short']};Set svr_ip {self.dataDict['svr_ip']}"
                    os.environ["USERPROFILE"] = self.dataDict['hon_manager_dir']

                    if initialise.check_proc(service_manager_name):
                        initialise.print_and_tex(self,"HoN Proxy Manager already started.")
                        return
                    if self.dataDict['use_console'] == 'False':
                        initialise.start_service(self,service_manager_name,True)
                    else:
                        sp.Popen([self.dataDict['hon_directory']+manager_application,"-manager","-noconfig","-execute",manager_arguments,"-masterserver",self.dataDict['master_server']])
                    # time.sleep(1)
                    # if initialise.check_proc(manager_application):
                    #     initialise.print_and_tex(self,"HoN Server Manager started.")
                    #     refresh_counter = refresh_delay
                    # else:
                    #     initialise.print_and_tex(self,"HoN Server Manager failed to start.",'warning')
                    # return
                    refresh_counter = refresh_delay


                def StopManager(self):
                    global refresh_counter,refresh_delay,labl_manager,btn_manager
                    
                    service_manager_name="HoN Server Manager"
                    manager_application=f"KONGOR ARENA MANAGER.exe"
                    service_manager = initialise.get_service(service_manager_name)
                    if not initialise.check_proc(manager_application):
                        initialise.print_and_tex(self,"HoN Proxy Manager isn't running.")
                        return
                    if service_manager and service_manager['status'] in ['running','paused']:
                        initialise.stop_service(self,service_manager_name,True)
                    else:
                        initialise.stop_bot(self,manager_application)
                    # time.sleep(1)
                    # if not initialise.check_proc(manager_application):
                    #     initialise.print_and_tex(self,"HoN Server Manager stopped.")
                    #     refresh_counter = refresh_delay
                    # else:
                    #     initialise.print_and_tex(self,"HoN Server Manager failed to stop.")
                    #     refresh_counter = refresh_delay
                    refresh_counter = refresh_delay
                    
                def Stop(self):
                    global refresh_counter,refresh_delay
                    pcount = initialise.playerCountX(self,id)
                    service_name=f"adminbot{id}"
                    service_check = initialise.get_service(service_name)
                    if pcount <= 0:
                        if service_check:
                            if service_check['status'] == 'running':
                                if initialise.stop_service(self,service_name,True):
                                    tex.insert(END,f"{service_name} stopped successfully.\n")
                                else:
                                    tex.insert(END,f"{service_name} failed to stop.\n")
                                tex.see(tk.END)
                        bot_running=initialise.check_proc(f"{service_name}.exe")
                        hon_running=initialise.check_proc(f"KONGOR_ARENA_{id}.exe")
                        if bot_running or hon_running:
                            initialise.stop_bot(self,f"{service_name}.exe")
                            initialise.stop_bot(self,f"KONGOR_ARENA_{id}.exe")
                            initialise.stop_bot(self,f"HON_SERVER_{id}.exe")
                                #viewButton.refresh()
                        refresh_counter = refresh_delay
                        return True
                    else:
                        print(f"[adminbot{id}] [ABORT] players are connected. Scheduling shutdown instead..")
                        initialise.schedule_shutdown(deployed_status)
                        return False
                    #viewButton.refresh()
                def Clean(self):
                    paths = [f"{deployed_status['hon_logs_dir']}",f"{deployed_status['hon_logs_dir']}\\diagnostics",f"{deployed_status['hon_home_dir']}\\HoNProxyManager"]
                    now = time.time()
                    count=0
                    for path in paths:
                        for f in os.listdir(path):
                            f = os.path.join(path, f)
                            if os.stat(f).st_mtime < now - 7 * 86400:
                                if os.path.isfile(f):
                                    try:
                                        os.remove(os.path.join(path, f))
                                        count+=1
                                        print("removed "+f)
                                    except Exception: print(traceback.format_exc())
                    replays = f"{deployed_status['hon_game_dir']}\\replays"
                    for f in os.listdir(replays):
                        f = os.path.join(replays, f)
                        if os.stat(f).st_mtime < now - 7 * 86400:
                            if os.path.isfile(f):
                                try:
                                    os.remove(os.path.join(replays, f))
                                    count+=1
                                    print("removed "+f)
                                except Exception: print(traceback.format_exc())
                            else:
                                try:
                                    shutil.rmtree(f,onerror=honfigurator.onerror)
                                    count+=1
                                    print("removed "+f)
                                except Exception: print(traceback.format_exc())
                    print(f"DONE. Cleaned {count} files.")
                def Uninstall(self,x):
                    global refresh_counter
                    if self.Stop():
                        service_state = initialise.get_service(service_name)
                        if service_state == False or service_state['status'] == 'stopped':
                            try:
                                #shutil.copy(f"{deployed_status['sdc_home_dir']}\\cogs\\total_games_played")
                                rem = shutil.rmtree(deployed_status['hon_home_dir'],onerror=honfigurator.onerror,ignore_errors=True)
                                tex.insert(END,f"removed files: {deployed_status['hon_home_dir']}")
                                tex.see(tk.END)
                            except Exception:
                                print(traceback.format_exc())
                            try:
                                remove_service = sp.run(['sc.exe','delete',f'adminbot{x}'])
                            except Exception:
                                print(traceback.format_exc())
                    else:
                        print(f"[adminbot{x}] [ABORT] players are connected. You must stop the service before uninstalling..")
                        tex.insert(END,"[adminbot{x}] [ABORT] players are connected. You must stop the service before uninstalling..\n")
                        tex.see(tk.END)
                        initialise.schedule_shutdown(deployed_status)

                #@profile
                def do_everything(self,x,deployed_status,update):
                    #tracemalloc.start(25)
                    #viewButton.display_top(tracemalloc.take_snapshot(), where='before loading server')
                    c_len = len(ButtonString)+len(LablString)
                    global i
                    global c
                    global incr
                    global labllist,btnlist,labllistrows,labllistcols,btnlistrows,btnlistcols
                    x+=1
                    i+=1
                    service_name = f"adminbot{x}"
                    dir_name = f"{deployed_status['hon_logs_dir']}\\"
                    try:
                        proc_priority = svrcmd.honCMD.get_process_priority(f"KONGOR_ARENA_{x}.exe")
                    except Exception:
                        proc_priority = "N/A"
                    file = "Slave*.log"
                    log = False
                    try:
                        list_of_files = glob.glob(dir_name + file) # * means all if need specific format then *.csv
                        log = max(list_of_files, key=os.path.getctime)
                    except Exception:
                        print(traceback.format_exc())
                    if log != False:
                        cookie = svrcmd.honCMD.check_cookie(deployed_status,log,"honfigurator_log_check")
                    else:
                        cookie = "pending"
                    schd_restart = False
                    schd_shutdown = False
                    schd_restart=initialise.check_schd_restart(deployed_status)
                    schd_shutdown=initialise.check_schd_shutdown(deployed_status)
                    service_state = initialise.get_service(service_name)
                    pcount = initialise.playerCountX(self,x)
                    #
                    # when total servers goes over <num>, move to the next column, and set row back to 1.
                    if i%mod_by==0:
                        c+=c_len
                        i=3
                    if pcount > 0:
                        ButtonString[1] = "Stop"
                        logs_dir = f"{deployed_status['hon_logs_dir']}\\"
                        log_File = f"Slave*{x}*.clog"
                        list_of_files = glob.glob(logs_dir + log_File) # * means all if need specific format then *.csv
                        try:
                            latest_file = max(list_of_files, key=os.path.getctime)
                            match_status = svrcmd.honCMD.simple_match_data(latest_file,"match")
                            if 'match_id' not in match_status: match_status.update({'match_id':'TBA'})
                        except Exception:
                            print(traceback.format_exc())
                    elif pcount >= 0:
                        ButtonString[1] = "Stop"
                    else:
                        ButtonString[1] = "Start"
                    if 'use_console' not in deployed_status:
                        svc_or_con = ''
                    else:
                        if service_state is not None and deployed_status['use_console'] == 'False':
                            svc_or_con="svc"
                        elif deployed_status['use_console'] == 'True':
                            svc_or_con="con"
                    LablString[0]=f"{x}-{proc_priority}-{svc_or_con}"
                    if pcount < 0:
                        colour = 'OrangeRed4'
                        LablString[1]="Offline"
                    elif pcount == 0:
                        if schd_shutdown:
                            colour = 'chocolate4'
                            LablString[1]=f"I should be off"
                        elif schd_restart:
                            colour = 'chocolate4'
                            LablString[1]=f"I should have restarted"
                        else:
                            colour = 'MediumPurple3'
                            if cookie == 'connected':
                                LablString[1]="Available"
                            elif cookie == 'no cookie':
                                LablString[1]="No cookie"
                                colour = 'chocolate4'
                            else:
                                LablString[1]="Pending Info"
                    elif pcount >0:
                        if schd_restart:
                            colour='indian red'
                            LablString[1]=f"skips({match_status['skipped_frames']}) {match_status['match_id']} ({pcount}p)"
                        elif schd_shutdown:
                            colour='indian red'
                            LablString[1]=f"skips({match_status['skipped_frames']}) {match_status['match_id']} ({pcount}p)"
                        else:
                            colour = 'SpringGreen4'
                            LablString[1]=f"skips({match_status['skipped_frames']}) {match_status['match_id']} ({pcount}p)"
                    for index1, labl_name in enumerate(LablString):
                        c_pos1 = index1 + c
                        if index1==0:
                            if update:
                                labllist[f"{x}-{index1}"].configure(text=labl_name,background=colour)
                                # labllist[f"{x}-{index1}"]['text'] = labl_name
                                # labllist[f"{x}-{index1}"]['background'] = colour
                            else:
                                labllist.update({f"{x}-{index1}":Label(tab2,width=13,text=f"{labl_name}", background=colour, foreground='white')})
                                labllistrows.update({f"{x}-{index1}":i})
                                labllistcols.update({f"{x}-{index1}":c_pos1})
                            # try:
                            #     honfigurator.CreateToolTip(labllist[f"{x}-{index1}"], \
                            #     f"HoNfigurator Version: {deployed_status['bot_version']}\nHoN Version: {deployed_status['hon_version']}\nCPU Affinity: {deployed_status['svr_affinity']}\nCPU Mode: {deployed_status['core_assignment']}\nProcess Priority: {proc_priority}")
                            # except Exception: pass
                        elif index1==1:
                            if update:
                                labllist[f"{x}-{index1}"].configure(text=labl_name,background=colour)
                                # labllist[f"{x}-{index1}"]['text']=labl_name
                                # labllist[f"{x}-{index1}"]['background']=colour
                            else:
                                labllist.update({f"{x}-{index1}":Label(tab2,width=18,text=f"{labl_name}", background=colour, foreground='white')})
                                labllistrows.update({f"{x}-{index1}":i})
                                labllistcols.update({f"{x}-{index1}":c_pos1})
                            # if 'available' in labl_name.lower():
                            #     honfigurator.CreateToolTip(labllist[f"{x}-{index1}"], \
                            #         f"Server is available and connected to the master server.")
                            # elif 'error' in labl_name.lower():
                            #     honfigurator.CreateToolTip(labllist[f"{x}-{index1}"], \
                            #         f"Potential outage.\nServer does not have a session cookie. Not connected to masterserver.\nRun in console mode, or view server logs to debug further.")
                            # elif 'pending' in labl_name.lower():
                            #     honfigurator.CreateToolTip(labllist[f"{x}-{index1}"], \
                            #         f"Waiting for server log to show whether we have a successful connection.")
                            # elif schd_restart:
                            #     honfigurator.CreateToolTip(labllist[f"{x}-{index1}"], \
                            #         f"A scheduled restart was requested, but the server has ignored it. Check the 'bot log' for this server for any errors.")
                            # elif schd_shutdown:
                            #     honfigurator.CreateToolTip(labllist[f"{x}-{index1}"], \
                            #         f"A scheduled shutdown was requested, but the server has ignored it. Check the 'bot log' for this server for any errors.")
                            # elif pcount > 0:
                            #     honfigurator.CreateToolTip(labllist[f"{x}-{index1}"], \
                            #         f"Game in progress ({match_status['match_id']})\n{pcount} players connected\nMatch time: {match_status['match_time']}\nSkipped server frames: {match_status['skipped_frames']}\nLargest skipped frame: {match_status['largest_skipped_frame']}\nScheduled shutdown: {schd_shutdown}\nScheduled restart: {schd_restart}")
                        for index2, btn_name in enumerate(ButtonString):
                            index2 +=len(LablString)
                            c_pos2 = index2 + c
                            if update:
                                if btnlist[f"{x}-{index2}"]['text'] != btn_name:
                                    btnlist[f"{x}-{index2}"].configure(text=btn_name)
                                    btnlist[f"{x}-{index2}"].configure(command=partial(viewButton,btn_name,x,pcount))

                                #btnlist[f"{x}-{index2}"].configure(text=btn_name,command=partial(viewButton,btn_name,x,pcount))
                                # btnlist[f"{x}-{index2}"]['text']=btn_name
                                # btnlist[f"{x}-{index2}"]['command']=partial(viewButton,btn_name,x,pcount)
                            else:
                                btnlist.update({f"{x}-{index2}":Button(tab2,text=btn_name, command=partial(viewButton,btn_name,x,pcount))})
                                btnlistrows.update({f"{x}-{index2}":i})
                                btnlistcols.update({f"{x}-{index2}":c_pos2})
                            # if btn_name == "View Log":
                            #     btn_ttp = honfigurator.CreateToolTip(btnlist[f"{x}-{index2}"], \
                            #         "View the server logs")
                            # elif btn_name == "Start":
                            #     btn_ttp = honfigurator.CreateToolTip(btnlist[f"{x}-{index2}"], \
                            #         "Start the server with the current configuration.")
                            # elif btn_name == "Stop":
                            #     btn_ttp = honfigurator.CreateToolTip(btnlist[f"{x}-{index2}"], \
                            #         "Schedule a shutdown of this server. Does NOT disconnect current games.")
                            # elif btn_name == "Clean":
                            #     btn_ttp = honfigurator.CreateToolTip(btnlist[f"{x}-{index2}"], \
                            #         "Remove unnecessary files (7 days or older), such as old log files.")
                            # elif btn_name == "Uninstall":
                            #     btn_ttp = honfigurator.CreateToolTip(btnlist[f"{x}-{index2}"], \
                            #         "Remove this server and bot, also removes folders and files.")
                            #btn.grid(row=i, column=c_pos2)
                    gc.collect()
                    #viewButton.display_top(tracemalloc.take_snapshot(), where='after loading server')
                #@profile
                def load_server_mgr(self,*args):
                    # tracemalloc.start(25)
                    global i
                    global c
                    global incr
                    global labllist,btnlist,labllistrows,labllistcols,btnlistrows,btnlistcols
                    global first_tab_switch
                    global server_admin_loading
                    first_tab_switch = False
                    server_admin_loading = True
                    #i=2
                    c=0
                    i=2
                    incr=0
                    #progressbar
                    pb = ttk.Progressbar(
                        app,
                        orient='horizontal',
                        mode='indeterminate',
                        length=280
                    )
                    # place the progressbar
                    pb.grid(column=0,sticky='n',row=1, columnspan=8, padx=10, pady=[0,0])
                    pb.start()
                    #print("Preparing Server Administration tab...")

                    global total_columns
                    global mod_by
                    global bot_tab
                    global tab2_cleanall
                    global tab2_stopall
                    global tab2_startall
                    global tabgui2
                    global stretch
                    global labl_proxy
                    global btn_proxy
                    global labl_manager
                    global btn_manager
                    
                    app.lift()
                    for o in range(100):
                        tab2.columnconfigure(o, weight=1,pad=0)
                    # for o in range(mod_by+5):
                    #     tab2.rowconfigure(o, weight=1,pad=0)
                    try:
                        #viewButton.display_top(tracemalloc.take_snapshot(), where='before loading any servers')
                        if len(labllist) == 0:
                            update=False
                            for x in range(int(self.dataDict['svr_total'])):
                                deployed_status = dmgr.mData.returnDict_deployed(self,x+1)
                                viewButton.do_everything(self,x,deployed_status,update)
                            ########
                            for k in (labllist):
                                labllist[k].grid(row=labllistrows[k], column=labllistcols[k])
                            for k in (btnlist):
                                btnlist[k].grid(row=btnlistrows[k], column=btnlistcols[k])
                            
                            column_rows=(tab2.grid_size())
                            total_columns=column_rows[0]
                            total_rows=column_rows[1]
                            #viewButton.display_top(tracemalloc.take_snapshot(), where='after loading servers, before checking server manager')
                            #Proxy and Manager
                            if svrcmd.honCMD.check_proc("proxymanager.exe"):
                                if update:
                                    labl_proxy.configure(text="Proxy Manager - UP",background="green")
                                    # labl_proxy['text'] = "Proxy Manager - UP"
                                    # labl_proxy['background'] = "green"
                                    btn_proxy.configure(text="Stop",command=lambda: viewButton.StopProxy(self))
                                    # btn_proxy['text'] = "Stop"
                                    # btn_proxy['command'] = lambda: viewButton.StopProxy(self)
                                else:
                                    labl_proxy = Label(tab2,width=25,text=f"Proxy Manager - UP", background="green", foreground='white')
                                    btn_proxy = Button(tab2, text="Stop",command=lambda: viewButton.StopProxy(self))
                            else:
                                if update:
                                    labl_proxy.configure(text="Proxy Manager - Down",background="red")
                                    # labl_proxy['text'] = "Proxy Manager - Down"
                                    # labl_proxy['background'] = "red"
                                    btn_proxy.configure(text="Start",command=lambda: lambda: viewButton.StartProxy(self))
                                    # btn_proxy['text'] = "Start"
                                    # btn_proxy['comand'] = lambda: viewButton.StartProxy(self)
                                else:
                                    labl_proxy = Label(tab2,width=25,text=f"Proxy Manager - Down", background="red", foreground='white')
                                    btn_proxy = Button(tab2, text="Start",command=lambda: viewButton.StartProxy(self))
                            btn_proxy.grid(columnspan=total_columns,column=0, row=1,sticky='n',padx=[430,0])
                            labl_proxy.grid(row=1, column=0,columnspan=total_columns,padx=[200,0],sticky='n',pady=[2,4])
                            if svrcmd.honCMD.check_proc("KONGOR ARENA MANAGER.exe"):
                                if update:
                                    if labl_manager['text'] != "Server Manager - UP":
                                        labl_manager.configure(text="Server Manager - UP",background="green")
                                        # labl_manager['text'] = "Server Manager - UP"
                                        # labl_manager['background'] = "green" "Stop="
                                    if btn_manager['text'] != "Stop":
                                        btn_manager.configure(text="Stop",command=lambda: viewButton.StopManager(self))
                                        # btn_manager['text'] = "Stop"
                                        # btn_manager['command'] = lambda: viewButton.StopManager(self)
                                else:
                                    labl_manager = Label(tab2,width=25,text=f"Server Manager - UP", background="green", foreground='white')
                                    btn_manager = Button(tab2, text="Stop",command=lambda: viewButton.StopManager(self))
                            else:
                                if update:
                                    if labl_manager['text'] != "Server Manager - Down":
                                        labl_manager.configure(text="Server Manager - Down",background="red")
                                        # labl_manager['text'] = "Server Manager - Down"
                                        # labl_manager['background'] = "red"
                                    if btn_manager['text'] != "Start":
                                        btn_manager.configure(text="Start",command=lambda: viewButton.StartManager(self))
                                        # btn_manager['text'] = "Start"
                                        # btn_manager['command'] = lambda: viewButton.StopManager(self)
                                else:
                                    labl_manager = Label(tab2,width=25,text=f"Server Manager - Down", background="red", foreground='white')
                                    btn_manager = Button(tab2, text="Start",command=lambda: viewButton.StartManager(self))
                            btn_manager.grid(columnspan=total_columns,column=0, row=1,sticky='n',padx=[0,430])
                            labl_manager.grid(row=1, column=0,columnspan=total_columns,padx=[0,200],sticky='n',pady=[2,4])
                            stretch_lbl = Label(tab2,width=15,text="servers per column",background=maincolor,foreground='white')
                            stretch_lbl.grid(row=1, column=0,columnspan=total_columns,padx=[5,0],sticky='w',pady=[2,4])
                            stretch = Entry(tab2,width=5)
                            stretch.insert(0,mod_by-3)
                            stretch.grid(row=1, column=0,columnspan=total_columns,padx=[120,0],sticky='w',pady=[2,4])
                            tab2_savesettings = applet.Button(tab2, text="Save Setting",command=lambda: save_num_rows(str(int(stretch.get())+3)))
                            tab2_savesettings.grid(row=1, column=0,columnspan=total_columns,padx=[160,0],sticky='w',pady=[2,4])
                            # tab2_savesettings_ttp = honfigurator.CreateToolTip(tab2_savesettings, \
                            #                 f"Save the setting so that next time the number of rows remains the same.")
                            
                            tabgui2 = ttk.Notebook(tab2)
                            tab11 = ttk.Frame(tabgui2)
                            tab22 = ttk.Frame(tabgui2)
                            tab23 = ttk.Frame(tabgui2)
                            tab24 = ttk.Frame(tabgui2)
                            tabgui2.add(tab11,text="Server Log")
                            tabgui2.add(tab22,text="Match Log")
                            tabgui2.add(tab23,text="Bot Log")
                            tabgui2.add(tab24,text="Proxy Log")
                            tabgui2.grid(column=0,row=30,sticky='ew',columnspan=total_columns)
                            tabgui2.select(bot_tab)
                            Thread(target=tabgui2.bind,args=('<<NotebookTabChanged>>',viewButton.load_log)).start()

                            #tab2.grid_rowconfigure(1,weight=1)
                            applet.Label(tab2,text=f"HoNfigurator",background=maincolor,foreground='white',image=honlogo).grid(columnspan=total_columns,column=0, row=0,pady=[10,0],sticky='n')
                            applet.Label(tab2,text=f"v{self.dataDict['bot_version']}-{self.dataDict['environment']}",background=maincolor,foreground='white',font=Font_Title).grid(columnspan=total_columns,column=0, row=0,sticky="e",pady=[0,20],padx=[0,30])
                            #   Buttons
                            tab2_cleanall = applet.Button(tab2, text="Clean All",command=lambda: clean_all())
                            tab2_cleanall.grid(columnspan=total_columns,column=0, row=mod_by+1,sticky='n',padx=[300,0],pady=[20,10])
                            tab2_cleanall_ttp = honfigurator.CreateToolTip(tab2_cleanall, \
                                            f"Remove ALL unnecessary files (7 days or older), such as old log files.")
                            tab2_stopall = applet.Button(tab2, text="Stop All",command=lambda: stop_all())
                            tab2_stopall.grid(columnspan=total_columns,column=0, row=mod_by+1,sticky='n',padx=[100,0],pady=[20,10])
                            tab2_refresh_ttp = honfigurator.CreateToolTip(tab2_stopall, \
                                            f"Schedule a shut down of all servers. Does NOT disconnect games in progress.")
                            tab2_startall = applet.Button(tab2, text="Start All",command=lambda: start_all())
                            tab2_startall.grid(columnspan=total_columns,column=0, row=mod_by+1,sticky='n',padx=[0,100],pady=[20,10])
                            tab2_startall_ttp = honfigurator.CreateToolTip(tab2_startall, \
                                            f"Start all stopped servers with their current configuration.")
                            tab2_refresh = applet.Button(tab2, text="Refresh",command=lambda: viewButton.refresh())
                            tab2_refresh.grid(columnspan=total_columns,column=0, row=mod_by+1,sticky='n',padx=[0,300],pady=[20,10])
                            tab2_refresh_ttp = honfigurator.CreateToolTip(tab2_startall, \
                                            f"Start all stopped servers with their current configuration.")
                        else:
                            update=True
                            num_total_svr = int(self.dataDict['svr_total'])
                            num_current_svr = int(len(labllist)/2)
                            if num_current_svr != num_total_svr:
                                if num_total_svr > num_current_svr:
                                    action = "add"
                                else:
                                    diff = num_current_svr - num_total_svr
                                    action = "subtract"
                                if action == "subtract":
                                    for i in range(diff*len(LablString)):
                                        list(labllist.values())[-1].destroy()
                                        labllist.popitem()
                                    for i in range(diff*len(ButtonString)):
                                        list(btnlist.values())[-1].destroy()
                                        btnlist.popitem()
                                else:
                                    # from_item = int(len(labllist) / 2)
                                    # to_item = int(num_total_svr / 2)
                                    # c=0
                                    # for x in range(from_item,to_item):
                                    #     deployed_status = dmgr.mData.returnDict_deployed(self,x+1)
                                    #     do_everything(self,x+1,deployed_status,update=False)
                                    #     list(labllist.values())[x*2].grid(row=list(labllistrows.values())[x*2], column=list(labllistcols.values())[x*2])
                                    #     list(btnlist.values())[x*2].grid(row=list(btnlistrows.values())[x*2], column=list(btnlistcols.values())[x*2])

                                    # TODO: rather than iterating over all servers, try to just iterate over the newly added ones. It was placing them in the wrong location.
                                    for x in range(int(self.dataDict['svr_total'])):
                                        deployed_status = dmgr.mData.returnDict_deployed(self,x+1)
                                        viewButton.do_everything(self,x,deployed_status,update=False)
                            else:
                                for x in range(int(self.dataDict['svr_total'])):
                                    deployed_status = dmgr.mData.returnDict_deployed(self,x+1)
                                    viewButton.do_everything(self,x,deployed_status,update)
                    
                            column_rows=(tab2.grid_size())
                            total_columns=column_rows[0]
                            total_rows=column_rows[1]
                            
                            #viewButton.display_top(tracemalloc.take_snapshot(), where='after loading servers, before checking server manager')
                            #Proxy and Manager
                            if svrcmd.honCMD.check_proc("proxymanager.exe"):
                                if update:
                                    labl_proxy['text'] = "Proxy Manager - UP"
                                    labl_proxy['background'] = "green"
                                    btn_proxy['text'] = "Stop"
                                    btn_proxy['command'] = lambda: viewButton.StopProxy(self)
                                else:
                                    labl_proxy = Label(tab2,width=25,text=f"Proxy Manager - UP", background="green", foreground='white')
                                    btn_proxy = Button(tab2, text="Stop",command=lambda: viewButton.StopProxy(self))
                            else:
                                if update:
                                    labl_proxy['text'] = "Proxy Manager - Down"
                                    labl_proxy['background'] = "red"
                                    btn_proxy['text'] = "Start"
                                    btn_proxy['command'] = lambda: viewButton.StartProxy(self)
                                else:
                                    labl_proxy = Label(tab2,width=25,text=f"Proxy Manager - Down", background="red", foreground='white')
                                    btn_proxy = Button(tab2, text="Start",command=lambda: viewButton.StartProxy(self))
                            btn_proxy.grid(columnspan=total_columns,column=0, row=1,sticky='n',padx=[430,0])
                            labl_proxy.grid(row=1, column=0,columnspan=total_columns,padx=[200,0],sticky='n',pady=[2,4])
                            if svrcmd.honCMD.check_proc("KONGOR ARENA MANAGER.exe"):
                                if update:
                                    if labl_manager['text'] != "Server Manager - UP":
                                        labl_manager.configure(text='Server Manager - UP',background='green')
                                    if btn_manager['text'] != "Stop":
                                        btn_manager.configure(text='Stop',command=lambda: viewButton.StopManager(self))
                                else:
                                    labl_manager = Label(tab2,width=25,text=f"Server Manager - UP", background="green", foreground='white')
                                    btn_manager = Button(tab2, text="Stop",command=lambda: viewButton.StopManager(self))
                            else:
                                if update:
                                    if labl_manager['text'] != "Server Manager - Down":
                                        labl_manager.configure(text='Server Manager - Down',background='red')
                                    if btn_manager['text'] != "Start":
                                        btn_manager.configure(text='Start',command=lambda: viewButton.StartManager(self))
                                else:
                                    labl_manager = Label(tab2,width=25,text=f"Server Manager - Down", background="red", foreground='white')
                                    btn_manager = Button(tab2, text="Start",command=lambda: viewButton.StartManager(self))
                            btn_manager.grid(columnspan=total_columns,column=0, row=1,sticky='n',padx=[0,430])
                            labl_manager.grid(row=1, column=0,columnspan=total_columns,padx=[0,200],sticky='n',pady=[2,4])

                            for k in (labllist):
                                labllist[k].grid(row=labllistrows[k], column=labllistcols[k])
                            for k in (btnlist):
                                btnlist[k].grid(row=btnlistrows[k], column=btnlistcols[k])
                    except Exception:
                        print(traceback.format_exc())
                    
                    if (tabgui.index("current")) == 2: tabgui.configure(height=tab2.winfo_reqheight())
                    server_admin_loading = False                
                    pb.stop()
                    pb.destroy()
                    gc.collect()
                    # viewButton.display_top(tracemalloc.take_snapshot(), where='after loading all servers')
                    # check_me_list = [self.dataDict,deployed_status,labllist,labllistcols,labllistrows,btnlist,btnlistcols,btnlistrows]
                    # for check_me in check_me_list:
                    #     print(f"size: {sys.getsizeof(check_me)}")
                    #     print(f"ref: {sys.getrefcount(check_me)}")
                    # snapshot = tracemalloc.take_snapshot()
                    # top_stats = snapshot.statistics('lineno')

                    # print("[ Top 10 ]")
                    # for stat in top_stats[:10]:
                    #     print(stat)
                    # return
                    #print("Finished preparing Server Administration Tab")
                def Tools():
                    pass
            global tex
            applet = ttk
            self.app.title(f"HoNfigurator v{self.dataDict['bot_version']} by @{self.dataDict['bot_author']}")
            #   importing icon
            honico = PhotoImage(file = os.path.abspath(application_path)+f"\\icons\\honico.png")
            self.app.iconphoto(False, honico) 
            honlogo = PhotoImage(file = os.path.abspath(application_path)+f"\\icons\\logo.png")
            #colors
            maincolor = '#14283A'
            titlecolor = 'black'
            textbox = "#152035"
            textcolor = 'white'
            bordercolor = '#48505D'
            buttoncolorselect = "#782424"
            buttoncolor = '#4F1818'
            style= ttk.Style()
            style.theme_use('clam')
            #selectbackground, selectforeground
            style.configure("TCombobox", fieldbackground= textbox, background= maincolor,lightcolor=bordercolor,bordercolor=bordercolor,darkcolor=bordercolor)
            style.configure('TEntry', fieldbackground= textbox, background= maincolor,lightcolor=bordercolor,bordercolor=bordercolor,darkcolor=bordercolor)
            #
            #Checkbutton style options
            #   background, compound, foreground, indicatorbackground, indicatorcolor, indicatormargin, indicatorrelief, padding
            #   states
            #   active, alternate, disabled, pressed, selected, readonly.
            style.configure("TCheckbutton", background= maincolor,indicatorcolor=maincolor)
            style.map('TCheckbutton', background=[('active',maincolor)])
            #   styling colors
            #   background, bordercolor, darkcolor, foreground, highlightcolor, lightcolor
            #   anchor, compound, font, highlightthickness, padding, relief, sihftrelief, width
            #   state
            #   active, disabled, pressed, readonly.
            style.configure('TButton', background=buttoncolor,foreground='white',lightcolor=bordercolor,bordercolor=bordercolor,darkcolor=bordercolor)
            style.map('TButton', background=[('active',buttoncolorselect)])
            style.configure('TNotebook',tabposition = 'n',background = maincolor,bordercolor =maincolor)
            style.configure('TFrame', background=maincolor,padx=[10,10])
            style.configure('TEntry',insertcolor='white',insertwidth=1)
            gui = tk.Frame(self.app,bg=maincolor,padx=10,pady=10)
            #self.app.geometry('1600x900')
            self.app.configure(bg=maincolor)
            gui.grid()

            #tabgui = ttk.Notebook(gui)
            tabgui = viewButton.Autoresized_Notebook(gui)
            tabgui.grid(column=0,row=0)
            tab1 = ttk.Frame(tabgui)
            tab2 = ttk.Frame(tabgui)
            tab3 = ttk.Frame(tabgui)

            tabgui.add(tab3,text="Base Settings")
            tabgui.add(tab1,text="Server Setup")
            tabgui.add(tab2,text="Server Administration")

            tabgui.select(tab1)

            #   title fonts
            Font_Title = ("Bahnschrift Condensed", 16, "bold")
            Font_SubHeading = ("Bahnschrift Condensed", 12, "bold")
            """
            Base Settings Tab
            """
            #   title
            applet.Label(tab3,text=f"HoNfigurator",background=maincolor,foreground='white',image=honlogo).grid(columnspan=7,column=0, row=0,sticky="n",pady=[10,0],padx=[0,0])
            applet.Label(tab3,text=f"v{self.dataDict['bot_version']}-{self.dataDict['environment']}",background=maincolor,foreground='white',font=Font_Title).grid(columnspan=7,column=0, row=0,sticky="e",pady=[0,0],padx=[0,30])
            #
            #    Server Data section
            applet.Label(tab3, text="Server Data",background=maincolor,foreground='white',font=Font_Title).grid(column=1, row=1,sticky="w")
            #   Server Name
            applet.Label(tab3, text="Server Name:",background=maincolor,foreground='white').grid(column=0,row=2,sticky="e")
            self.tab3_hosterd = applet.Entry(tab3,foreground=textcolor,width=16)
            honfigurator.CreateToolTip(self.tab3_hosterd, \
                    f"The server name which will appear in HoN. Also the name which the Discord bots will be called by.\nCannot contain spaces.")
            self.tab3_hosterd.insert(0,self.dataDict['svr_hoster'])
            self.tab3_hosterd.grid(column= 1 , row = 2,sticky="w",pady=4,padx=[0,130])
            #   User name
            applet.Label(tab3, text="HoN Username:",background=maincolor,foreground='white').grid(column=0,row=3,sticky="e")
            self.tab3_user = applet.Entry(tab3,foreground=textcolor,width=16)
            honfigurator.CreateToolTip(self.tab3_user, \
                    f"This must be a unique username per VM / Dedicated Host.\nUsing the same user on multiple server hosting infrastructures will cause the inability for players to download replays.")
            self.tab3_user.insert(0,self.dataDict['svr_login'])
            self.tab3_user.grid(column= 1 , row = 3,sticky="w",pady=4,padx=[0,130])
            #   password
            applet.Label(tab3, text="HoN Password:",background=maincolor,foreground='white').grid(column=0,row=4,sticky="e")
            self.tab3_pass = applet.Entry(tab3,foreground=textcolor,width=16,show="*")
            self.tab3_pass.insert(0,self.dataDict['svr_password'])
            self.tab3_pass.grid(column= 1 , row = 4,sticky="w",pady=4)
            #   HoN master server
            self.master_server = tk.StringVar(self.app,self.dataDict['master_server'])
            applet.Label(tab3, text="HoN Master Server:",background=maincolor,foreground='white').grid(column=0, row=5,sticky="e",padx=[20,0])
            self.tab3_masterserver = applet.Combobox(tab3,foreground=textcolor,value=self.masterserver(),textvariable=self.master_server,width=16)
            self.tab3_masterserver.grid(column= 1, row = 5,sticky="w",pady=4,padx=[0,130])
            #   Region
            self.svr_reg_code = tk.StringVar(self.app,self.dataDict["svr_region_short"])
            applet.Label(tab3, text="Region:",background=maincolor,foreground='white').grid(column=0, row=6,sticky="e")
            self.tab3_regionsd = applet.Combobox(tab3,foreground=textcolor,value=self.regions(),textvariable=self.svr_reg_code,width=6)
            honfigurator.CreateToolTip(self.tab3_regionsd, \
                    f"These are the only valid region codes. Any others will not show up in-game.")
            self.tab3_regionsd.grid(column= 1 , row = 6,sticky="w",pady=4)
            #  allow bot matches 
            applet.Label(tab3, text="Allow bot matches:",background=maincolor,foreground='white').grid(column=0, row=7,sticky="e",padx=[20,0])
            self.botmatches = tk.BooleanVar(self.app)
            tab3_botmatches_btn = applet.Checkbutton(tab3,variable=self.botmatches)
            honfigurator.CreateToolTip(tab3_botmatches_btn, \
                    f"Bot matches are disabled by default. Check this box to enable bot matches to be played.")
            tab3_botmatches_btn.grid(column= 1, row = 7,sticky="w",pady=4)
            #
            #    Network Section
            applet.Label(tab3, text="Networking",background=maincolor,foreground='white',font=Font_Title).grid(column=1, row=8,sticky="w")
            #   use proxy
            #   Ports
            applet.Label(tab3, text="Starting game port:",background=maincolor,foreground='white').grid(column=0,row=9,sticky="e")
            self.tab3_game_port = applet.Entry(tab3,foreground=textcolor,width=5)
            honfigurator.CreateToolTip(self.tab3_game_port, \
                    f"The starting voice port defaults to 10000.\nEach server is started on the starting voice port + the nth server\nif using the proxy, the public ports will be an additional 10000 ontop of this.\nHoNfigurator will output the required ports to forward after configuring a server.")
            self.tab3_game_port.insert(0,self.dataDict['game_starting_port'])
            self.tab3_game_port.grid(column=1,row = 9,sticky="w",pady=4)

            applet.Label(tab3, text="Starting voice port:",background=maincolor,foreground='white').grid(column=0,row=10,sticky="e")
            self.tab3_voice_port = applet.Entry(tab3,foreground=textcolor,width=5)
            honfigurator.CreateToolTip(self.tab3_voice_port, \
                    f"The starting game port defaults to 10000.\nEach server is started on the starting game port + the nth server\nif using the proxy, the public ports will be an additional 10000 ontop of this.\nHoNfigurator will output the required ports to forward after configuring a server.")
            self.tab3_voice_port.insert(0,self.dataDict['voice_starting_port'])
            self.tab3_voice_port.grid(column=1,row = 10,sticky="w",pady=4)
            #  increment by
            self.increment_port = tk.StringVar(self.app,self.dataDict['incr_port_by'])
            applet.Label(tab3, text="Increment ports by:",background=maincolor,foreground='white').grid(column=0, row=11,sticky="e",padx=[20,0])
            tab3_increment_port = applet.Combobox(tab3,foreground=textcolor,value=self.incrementport(),textvariable=self.increment_port,width=5)
            honfigurator.CreateToolTip(tab3_increment_port, \
                    f"The number of network ports to skip between each server. Example, increment of 2 would make server ports like: 10000, 10002, 10004, etc.\nThe default value is 1.")
            tab3_increment_port.grid(column= 1, row = 11,sticky="w",pady=4)
            #   optional static IP
            applet.Label(tab3, text="Static IP (optional):",background=maincolor,foreground='white').grid(column=0,row=12,sticky="e")
            self.tab3_ip = applet.Entry(tab3,foreground=textcolor,width=16)
            honfigurator.CreateToolTip(self.tab3_ip, \
                    f"An optional static IP. Otherwise, your IP will be set to {self.dataDict['svr_ip']}")
            if 'static_ip' in self.dataDict:
                self.tab3_ip.insert(0,self.dataDict['svr_ip'])
            self.tab3_ip.grid(column= 1 , row = 12,sticky="w",pady=4)
            applet.Label(tab3, text="Use proxy (anti-DDOS):",background=maincolor,foreground='white').grid(column=0, row=13,sticky="e",padx=[20,0])
            self.useproxy = tk.BooleanVar(self.app)
            if self.dataDict['use_proxy'] == 'True':
                self.useproxy.set(True)
            tab3_useproxy_btn = applet.Checkbutton(tab3,variable=self.useproxy)
            honfigurator.CreateToolTip(tab3_useproxy_btn, \
                    f"Enable this option to use the HoN Proxy service.\nThis creates a layer of protection by ensuring all game server data is dealt with by the proxy first, eliminating malicious DoS attempts.\nIf using the proxy. Observe carefully the HoNfigurator output, and only port forward the Proxy ports on your router.")
            tab3_useproxy_btn.grid(column= 1, row = 13,sticky="w",pady=4)
            self.useproxy.trace_add('write', self.port_mode)
            #
            #    Discord Section
            self.tab3_discord_title = applet.Label(tab3, text="",background=maincolor,foreground='white',font=Font_Title)
            self.tab3_discord_title.grid(column=3, row=1,sticky="w")
            #   Owner
            applet.Label(tab3, text="Bot Owner (discord ID):",background=maincolor,foreground='white').grid(column=2, row=2,sticky="e",padx=[20,0])
            self.tab3_discordadmin = applet.Entry(tab3,foreground=textcolor,width=45)
            honfigurator.CreateToolTip(self.tab3_discordadmin, \
                    f"YOUR Discord user ID.\nObtainable by enabling developer options in Discord advanced settings, then right clicking your name in the members list on any Discord guild, and selecting \"Copy ID\".")
            self.tab3_discordadmin.insert(0,self.dataDict['discord_admin'])
            self.tab3_discordadmin.grid(column= 3, row = 2,sticky="w",pady=4)
            #   token
            applet.Label(tab3, text="Bot Token (SECRET):",background=maincolor,foreground='white').grid(column=2, row=3,sticky="e",padx=[20,0])
            self.tab3_bottokd = applet.Entry(tab3,foreground=textcolor,width=45)
            honfigurator.CreateToolTip(self.tab3_bottokd, \
                    f"The secret token which your bot uses to authenticate to Discord. View github to see instructions on creating your own Discord bot.\nPermissions integer: 533650040896.\nRequires message content intent.")
            self.tab3_bottokd.insert(0,self.dataDict['token'])
            self.tab3_bottokd.grid(column= 3, row = 3,sticky="w",pady=4,padx=[0,20])
            #  Run without bots
            applet.Label(tab3, text="Disable discord bots:",background=maincolor,foreground='white').grid(column=2, row=4,sticky="e",padx=[20,0])
            self.enablebot = tk.BooleanVar(self.app)
            if self.dataDict['disable_bot'] == 'True':
                self.enablebot.set(True)
            else:
                self.enablebot.set(False)
            tab3_disablebot_btn = applet.Checkbutton(tab3,variable=self.enablebot)
            honfigurator.CreateToolTip(tab3_disablebot_btn, \
                    f"Run the with the addition of discord bots (receive personalised alerts).")
            tab3_disablebot_btn.grid(column= 3, row = 4,sticky="w",pady=4)
            self.enablebot.trace_add('write', self.switch_widget_state)
            #
            #    HF Section
            applet.Label(tab3, text="HoNfigurator Data",background=maincolor,foreground='white',font=Font_Title).grid(column=3, row=5,sticky="w")
            # auto configure servers on update
            applet.Label(tab3, text="Auto-Configure servers on update:",background=maincolor,foreground='white').grid(column=2, row=6,sticky="e",padx=[20,0])
            self.autoupdate = tk.BooleanVar(self.app)
            if self.dataDict['auto_update'] == 'True':
                self.autoupdate.set(True)
            tab3_autoupdate_btn = applet.Checkbutton(tab3,variable=self.autoupdate)
            honfigurator.CreateToolTip(tab3_autoupdate_btn, \
                    f"When HoNfigurator is open, and upstream updates are received via github, automatically deploy and configure servers to the latest version.")
            tab3_autoupdate_btn.grid(column= 3, row = 6,sticky="w",pady=4)
            # Github Branch
            self.git_branch = tk.StringVar(self.app,self.git_current_branch())
            applet.Label(tab3, text="Currently selected branch:",background=maincolor,foreground='white').grid(column=2, row=7,sticky="e",padx=[20,0])
            tab3_git_branch = applet.Combobox(tab3,foreground=textcolor,value=self.git_all_branches(),textvariable=self.git_branch)
            tab3_git_branch.grid(column= 3, row = 7,sticky="w",pady=4)
            self.git_branch.trace_add('write', self.update_repository)
            #
            #    file storage Section
            applet.Label(tab3, text="File Storage",background=maincolor,foreground='white',font=Font_Title).grid(column=3, row=8,sticky="w")
            #   Install Directory
            applet.Label(tab3, text="HoN Directory:",background=maincolor,foreground='white').grid(column=2, row=9,sticky="e",padx=[20,0])
            self.tab3_hondird = applet.Entry(tab3,foreground=textcolor,width=70)
            self.tab3_hondird.insert(0,self.dataDict['hon_directory'])
            self.tab3_hondird.grid(columnspan=3,column= 3, row = 9,sticky="w",pady=4,padx=[0,10])
            #   Replays directory
            applet.Label(tab3, text="HoN Storage Folder\n(replays, long term storage):",background=maincolor,foreground='white').grid(column=2, row=10,sticky="e",padx=[20,0])
            self.tab3_honreplay = applet.Entry(tab3,foreground=textcolor,width=70)
            honfigurator.CreateToolTip(self.tab3_honreplay, \
                    f"Use to store HoN replays.")
            self.tab3_honreplay.insert(0,self.dataDict['hon_manager_dir'])
            self.tab3_honreplay.grid(columnspan=3,column= 3, row = 10,sticky="w",pady=4,padx=[0,10])
            """
            Server Setup Tab
            """
            # # create a grid of 2x6
            # for t in range(25):
            #     tab1.rowconfigure(t, weight=1,pad=0)
            for o in range(7):
                tab1.columnconfigure(o, weight=1,pad=0)
            #   title
            applet.Label(tab1,text=f"HoNfigurator",background=maincolor,foreground='white',image=honlogo).grid(columnspan=8,column=0, row=0,sticky="n",pady=[10,0],padx=[0,0])
            # tab1.rowconfigure(0,weight=1)
            applet.Label(tab1,text=f"v{self.dataDict['bot_version']}-{self.dataDict['environment']}",background=maincolor,foreground='white',font=Font_Title).grid(columnspan=12,column=0, row=0,sticky="e",pady=[0,0],padx=[0,30])
            #
            #    Server Setup section
            applet.Label(tab1, text="Server Setup",background=maincolor,foreground='white',font=Font_Title).grid(column=1, row=1,sticky="w")
            #   server total    
            self.svr_total_var = tk.StringVar(self.app,self.dataDict['svr_total'])
            applet.Label(tab1, text="Total Servers:",background=maincolor,foreground='white').grid(column=0, row=2,sticky="e")
            self.tab1_servertd = applet.Combobox(tab1,foreground=textcolor,value=self.corecount(),textvariable=self.svr_total_var,width=5)
            honfigurator.CreateToolTip(self.tab1_servertd, \
                    f"The total servers allowed by your CPU core count.")
            self.tab1_servertd.grid(column= 1 , row = 2,sticky="w",pady=4)
            self.svr_total_var.trace_add('write', self.svr_num_link)
            #  one or two cores
            self.core_assign = tk.StringVar(self.app,self.dataDict['core_assignment'])
            applet.Label(tab1, text="CPU cores assigned per server:",background=maincolor,foreground='white').grid(column=0, row=3,sticky="e",padx=[20,0])
            tab1_core_assign = applet.Combobox(tab1,foreground=textcolor,value=self.coreassign(),textvariable=self.core_assign,width=16)
            honfigurator.CreateToolTip(tab1_core_assign, \
                    f"Multiple servers can be started on a single CPU core.\nThe recommended value is 1 core per server.\nIf you have reports of lag, try 2 cores per server\nIf you have a very strong CPU, try 2 servers per core.")
            tab1_core_assign.grid(column= 1, row = 3,sticky="w",pady=4,padx=[0,130])
            self.core_assign.trace_add('write', self.coreadjust)
            
            #  one or two cores
            self.priority = tk.StringVar(self.app,self.dataDict['process_priority'])
            applet.Label(tab1, text="In-game CPU process priority:",background=maincolor,foreground='white').grid(column=0, row=4,sticky="e",padx=[20,0])
            tab1_priority = applet.Combobox(tab1,foreground=textcolor,value=self.priorityassign(),textvariable=self.priority,width=16)
            honfigurator.CreateToolTip(tab1_priority, \
                    f"Default option: Realtime. There is no need to change this unless you are being experimental.")
            tab1_priority.grid(column= 1, row = 4,sticky="w",pady=4,padx=[0,130])
            #
            #   force proxy restart
            applet.Label(tab1, text="Restart Proxy (in next configure)",background=maincolor,foreground='white').grid(column=0, row=6,sticky="e",padx=[20,0])
            self.restart_proxy = tk.BooleanVar(self.app)
            self.tab1_restart_proxy = applet.Checkbutton(tab1,variable=self.restart_proxy)
            honfigurator.CreateToolTip(self.tab1_restart_proxy, \
                    f"Enable this option to ensure the proxy is restarted on the next configure. This may disrupt games in progress.")
            self.tab1_restart_proxy.grid(column= 1, row = 6,sticky="w",pady=4)
            honfigurator.port_mode(self,NULL,NULL,NULL)
            
            #   console windows, for launching servers locally (not as windows services)
            applet.Label(tab1, text="Launch servers in console mode:",background=maincolor,foreground='white').grid(column=0, row=5,sticky="e",padx=[20,0])
            self.console = tk.BooleanVar(self.app)
            if self.dataDict['use_console'] == 'True':
                self.console.set(True)
            else:
                self.console.set(False)
            tab1_console_btn = applet.Checkbutton(tab1,variable=self.console)
            honfigurator.CreateToolTip(tab1_console_btn, \
                    f"Use this option to run servers in console app mode. This is more CPU intensive, and you must remain logged in.\nDefault mode runs servers as a windows service, and you don't need to remain logged in.")
            tab1_console_btn.grid(column= 1, row = 5,sticky="w",pady=2)
            
            #
            #    Discord Bot Settings
            self.tab1_discord_title = applet.Label(tab1, text="",background=maincolor,foreground='white',font=Font_Title)
            self.tab1_discord_title.grid(column=3,columnspan=2, row=1,sticky="n",padx=[100,0])
            # crashing
            applet.Label(tab1, text="Alert on server crash:",background=maincolor,foreground='white').grid(column=3, row=2,sticky="e",padx=[20,0])
            self.alert_on_crash = tk.BooleanVar(self.app)
            if self.dataDict['disc_alert_on_crash'] == 'True':
                self.alert_on_crash.set(True)
            self.tab1_alert_on_crash_btn = applet.Checkbutton(tab1,variable=self.alert_on_crash)
            honfigurator.CreateToolTip(self.tab1_alert_on_crash_btn, \
                    f"Enable alerting when the server crashes abnormally. Recommended to be ON.")
            self.tab1_alert_on_crash_btn.grid(column= 4, row = 2,sticky="w",pady=4,padx=[0,0])
            # lag spikes
            applet.Label(tab1, text="Alert on lag spikes:",background=maincolor,foreground='white').grid(column=3, row=3,sticky="e",padx=[20,0])
            self.alert_on_lag = tk.BooleanVar(self.app)
            if self.dataDict['disc_alert_on_lag'] == 'True':
                self.alert_on_lag.set(True)
            self.tab1_alert_on_lag_btn = applet.Checkbutton(tab1,variable=self.alert_on_lag)
            honfigurator.CreateToolTip(self.tab1_alert_on_lag_btn, \
                    f"Enable alerting when there are large lag spikes in-game. Recommended to be ON.")
            self.tab1_alert_on_lag_btn.grid(column= 4, row = 3,sticky="w",pady=4,padx=[0,0])
            # event list limit
            applet.Label(tab1, text="Event list limit:",background=maincolor,foreground='white').grid(column=3, row=4,sticky="e",padx=[20,0])
            self.tab1_eventlist_limit = applet.Entry(tab1,foreground=textcolor,width=5)
            self.tab1_eventlist_limit.insert(0,self.dataDict['disc_event_list_limit'])
            honfigurator.CreateToolTip(self.tab1_eventlist_limit, \
                    f"Limit the # of server log entries within the received discord DM.")
            self.tab1_eventlist_limit.grid(column=4, row = 4,sticky="w",pady=4,padx=[0,0])
            # alert list limit
            applet.Label(tab1, text="Alert list limit:",background=maincolor,foreground='white').grid(column=3, row=5,sticky="e",padx=[20,0])
            self.tab1_alertlist_limit = applet.Entry(tab1,foreground=textcolor,width=5)
            self.tab1_alertlist_limit.insert(0,self.dataDict['disc_alert_list_limit'])
            honfigurator.CreateToolTip(self.tab1_alertlist_limit, \
                    f"Limit the # of previous alerts within the received discord DM.")
            self.tab1_alertlist_limit.grid(column=4, row = 5,sticky="w",pady=4,padx=[0,0])
            applet.Label(tab1, text=" ",background=maincolor,foreground='white').grid(column=5, row=5,sticky="e",padx=[20,0])
            applet.Label(tab1, text=" ",background=maincolor,foreground='white').grid(column=6, row=5,sticky="e",padx=[20,0])
            applet.Label(tab1, text=" ",background=maincolor,foreground='white').grid(column=7, row=5,sticky="e",padx=[20,0])
            #  Debug mode 
            applet.Label(tab1, text="Debug mode:",background=maincolor,foreground='white').grid(column=3, row=6,sticky="e",padx=[20,0])
            self.debugmode = tk.BooleanVar(self.app)
            if self.dataDict['debug_mode'] == 'True':
                self.debugmode.set(True)
            self.tab1_debugmode_btn = applet.Checkbutton(tab1,variable=self.debugmode)
            honfigurator.CreateToolTip(self.tab1_debugmode_btn, \
                    f"Enhanced logging, specifically in eventlog sent to Discord DM by bot. Only relevant if discord bots are enabled.")
            self.tab1_debugmode_btn.grid(column= 4, row = 6,sticky="w",pady=4)
            honfigurator.switch_widget_state(self,NULL,NULL,NULL)
            ##########################
            # applet.Label(tab1,text="",background=maincolor,foreground='white').grid(column=0,row=7)
            # applet.Label(tab1,text="",background=maincolor,foreground='white').grid(column=0,row=8)
            # applet.Label(tab1,text="",background=maincolor,foreground='white').grid(column=0,row=9)
            # applet.Label(tab1,text="",background=maincolor,foreground='white').grid(column=0,row=10)
            # applet.Label(tab1,text="",background=maincolor,foreground='white').grid(column=0,row=11)
            # applet.Label(tab1,text="",background=maincolor,foreground='white').grid(column=0,row=12)
            tab1_savesettings = applet.Button(tab1,width=22, text="Save Settings",command=lambda: Thread(target=self.save_settings,args=(self.tab3_hosterd.get(),self.tab3_regionsd.get(),self.tab1_from_svr.get(),self.tab1_servertd.get(),self.tab3_hondird.get(),self.tab3_honreplay.get(),self.tab3_user.get(),self.tab3_pass.get(),self.tab3_ip.get(),self.tab3_bottokd.get(),self.tab3_discordadmin.get(),self.tab3_masterserver.get(),True,self.enablebot.get(),self.alert_on_crash.get(),self.alert_on_lag.get(),self.tab1_alertlist_limit.get(),self.tab1_eventlist_limit.get(),self.autoupdate.get(),self.console.get(),self.useproxy.get(),self.restart_proxy.get(),self.tab3_game_port.get(),self.tab3_voice_port.get(),self.core_assign.get(),self.priority.get(),self.botmatches.get(),self.debugmode.get(),self.git_branch.get(),self.increment_port.get())).start())
            tab1_savesettings.grid(columnspan=7,column=0, row=5,stick='n',padx=[0,0],pady=[0,10])
            honfigurator.CreateToolTip(tab1_savesettings, \
                    f"Save the current configuration settings.")
            tab1_singlebutton = applet.Button(tab1,width=22, text="Configure Server Group",command=lambda: Thread(target=self.sendData,args=("selected",self.tab3_hosterd.get(),self.tab3_regionsd.get(),self.tab1_from_svr.get(),self.tab1_to_svr.get(),self.tab1_servertd.get(),self.tab3_hondird.get(),self.tab3_honreplay.get(),self.tab3_user.get(),self.tab3_pass.get(),self.tab3_ip.get(),self.tab3_bottokd.get(),self.tab3_discordadmin.get(),self.tab3_masterserver.get(),True,self.enablebot.get(),self.alert_on_crash.get(),self.alert_on_lag.get(),self.tab1_alertlist_limit.get(),self.tab1_eventlist_limit.get(),self.autoupdate.get(),self.console.get(),self.useproxy.get(),self.restart_proxy.get(),self.tab3_game_port.get(),self.tab3_voice_port.get(),self.core_assign.get(),self.priority.get(),self.botmatches.get(),self.debugmode.get(),self.git_branch.get(),self.increment_port.get())).start())
            tab1_singlebutton.grid(columnspan=7,column=0, row=2,stick='n',padx=[0,0],pady=[0,10])
            honfigurator.CreateToolTip(tab1_singlebutton, \
                    f"Configure the currently selected server ID only.")
            #   configurable server FROM
            self.from_svr_var = tk.StringVar(self.app,"1")
            applet.Label(tab1, text="From:",background=maincolor,foreground='white').grid(columnspan=7,column=0,row=3,rowspan=3,stick='n',padx=[0,95],pady=[0,0])
            self.tab1_from_svr = applet.Combobox(tab1,foreground=textcolor,value=self.corecount(),textvariable=self.from_svr_var,width=2)
            self.tab1_from_svr.grid(columnspan=7,column=0,row=3,stick='n',padx=[0,30],pady=[0,0])
            self.from_svr_var.trace_add('write', self.svr_num_link2)
            #   configurable server TO
            self.to_svr_var = tk.StringVar(self.app,self.dataDict['svr_total'])
            applet.Label(tab1, text="To:",background=maincolor,foreground='white').grid(columnspan=7,column=0,row=3,rowspan=3,stick='n',padx=[35,0],pady=[0,0])
            self.tab1_to_svr = applet.Combobox(tab1,foreground=textcolor,value=self.corecount(),textvariable=self.to_svr_var,width=2)
            self.tab1_to_svr.grid(columnspan=7,column=0,row=3,stick='n',padx=[95,0],pady=[0,0])
            self.to_svr_var.trace_add('write', self.svr_num_link2)

            tab1_allbutton = applet.Button(tab1,width=22, text="Configure All Servers",command=lambda: Thread(target=self.sendData,args=("all",self.tab3_hosterd.get(),self.tab3_regionsd.get(),self.tab1_from_svr.get(),self.tab1_to_svr.get(),self.tab1_servertd.get(),self.tab3_hondird.get(),self.tab3_honreplay.get(),self.tab3_user.get(),self.tab3_pass.get(),self.tab3_ip.get(),self.tab3_bottokd.get(),self.tab3_discordadmin.get(),self.tab3_masterserver.get(),True,self.enablebot.get(),self.alert_on_crash.get(),self.alert_on_lag.get(),self.tab1_alertlist_limit.get(),self.tab1_eventlist_limit.get(),self.autoupdate.get(),self.console.get(),self.useproxy.get(),self.restart_proxy.get(),self.tab3_game_port.get(),self.tab3_voice_port.get(),self.core_assign.get(),self.priority.get(),self.botmatches.get(),self.debugmode.get(),self.git_branch.get(),self.increment_port.get())).start())
            tab1_allbutton.grid(columnspan=7,column=0, row=4,stick='n',padx=[0,0],pady=[0,10])
            tab3_savesettings = applet.Button(tab3,width=22, text="Save Settings",command=lambda: Thread(target=self.save_settings,args=(self.tab3_hosterd.get(),self.tab3_regionsd.get(),self.tab1_from_svr.get(),self.tab1_servertd.get(),self.tab3_hondird.get(),self.tab3_honreplay.get(),self.tab3_user.get(),self.tab3_pass.get(),self.tab3_ip.get(),self.tab3_bottokd.get(),self.tab3_discordadmin.get(),self.tab3_masterserver.get(),True,self.enablebot.get(),self.alert_on_crash.get(),self.alert_on_lag.get(),self.tab1_alertlist_limit.get(),self.tab1_eventlist_limit.get(),self.autoupdate.get(),self.console.get(),self.useproxy.get(),self.restart_proxy.get(),self.tab3_game_port.get(),self.tab3_voice_port.get(),self.core_assign.get(),self.priority.get(),self.botmatches.get(),self.debugmode.get(),self.git_branch.get(),self.increment_port.get())).start())
            tab3_savesettings.grid(columnspan=7,column=0, row=14,stick='n',padx=[0,300],pady=[0,10])
            honfigurator.CreateToolTip(tab3_savesettings, \
                    f"Save the current configuration settings.")
            honfigurator.CreateToolTip(tab1_allbutton, \
                    f"Configure ALL total servers.")
            tab3_updatebutton = applet.Button(tab3,width=22, text="Update HoNfigurator",command=lambda: self.update_repository(NULL,NULL,NULL))
            tab3_updatebutton.grid(columnspan=7,column=0, row=14,stick='n',padx=[0,0],pady=[0,10])
            honfigurator.CreateToolTip(tab3_updatebutton, \
                    f"Update this application. Pulls latest commits from GitHub.")
            tab3_updatehon = applet.Button(tab3,width=22,text="Force Update HoN",command=lambda: Thread(target=self.forceupdate_hon,args=(True,"all",self.tab3_hosterd.get(),self.tab3_regionsd.get(),self.tab1_from_svr.get(),self.tab1_servertd.get(),self.tab3_hondird.get(),self.tab3_honreplay.get(),self.tab3_user.get(),self.tab3_pass.get(),self.tab3_ip.get(),self.tab3_bottokd.get(),self.tab3_discordadmin.get(),self.tab3_masterserver.get(),True,self.enablebot.get(),self.alert_on_crash.get(),self.alert_on_lag.get(),self.tab1_alertlist_limit.get(),self.tab1_eventlist_limit.get(),self.autoupdate.get(),self.console.get(),self.useproxy.get(),self.restart_proxy.get(),self.tab3_game_port.get(),self.tab3_voice_port.get(),self.core_assign.get(),self.priority.get(),self.botmatches.get(),self.debugmode.get(),self.git_branch.get(),self.increment_port.get())).start())
            tab3_updatehon.grid(columnspan=7,column=0, row=14,stick='n',padx=[300,0],pady=[0,10])
            honfigurator.CreateToolTip(tab3_updatehon, \
                    f"Used when there is a HoN server udpate available. All servers must first be stopped for this to work.")
            self.app.rowconfigure(14,weight=1)
            self.app.rowconfigure(15,weight=1)
            self.app.columnconfigure(0,weight=1)
            tex = tk.Text(self.app,foreground=textcolor,background=textbox,height=10)
            tex.grid(row=16, column=0, sticky="nsew", padx=2, pady=2)
            tex.tag_config('warning', background="yellow", foreground="red")
            tex.tag_config('interest', background="green")
            tex.tag_config('header', background="white",foreground="black")
            tex.tag_configure("stderr", foreground="#b22222")
            #   Below is to redirect console to honfigurator window
            #       sys.stdout = TextRedirector(tex, "stdout")
            #       sys.stderr = TextRedirector(tex, "stderr")

            # logolabel_tab2 = applet.Label(tab2,text="HoNfigurator",background=maincolor,foreground='white',image=honlogo)
            # logolabel_tab2.grid(columnspan=2,column=, row=0,sticky="n",pady=[10,0])
            def quit_window(icon, item):
                icon.stop()
                self.app.destroy()
            def show_window(icon, item):
                icon.stop()
                self.app.after(0,self.app.deiconify())
            def hide_window():
                self.app.withdraw()
                image=Image.open(os.path.abspath(application_path)+f"\\icons\\honico.png")
                menu=(item('Quit', quit_window), item('Show', show_window))
                icon=pystray.Icon("name", image, "HoNfigurator", menu)
                icon.run()
            
            
            """
            
            This is the bot command center tab
            
            """


            # Calling this function from somewhere else via Queue
            import fnmatch
            import glob
            def clean_all():
                count=0
                for i in range (1,int(self.dataDict['svr_total'])):
                    deployed_status = dmgr.mData.returnDict_deployed(self,i)
                    paths = [f"{deployed_status['hon_logs_dir']}",f"{deployed_status['hon_logs_dir']}\\diagnostics",f"{self.dataDict['hon_home_dir']}\\HoNProxyManager"]
                    now = time.time()
                    try:
                        for path in paths:
                            for f in os.listdir(path):
                                f = os.path.join(path, f)
                                if os.stat(f).st_mtime < now - 7 * 86400:
                                    if os.path.isfile(f):
                                        os.remove(os.path.join(path, f))
                                        count+=1
                                        print("removed "+f)
                    except Exception:
                        print(traceback.format_exc())
                    replays = f"{deployed_status['hon_game_dir']}\\replays"
                    for f in os.listdir(replays):
                        f = os.path.join(replays, f)
                        if os.stat(f).st_mtime < now - 7 * 86400:
                            if os.path.isfile(f):
                                os.remove(os.path.join(replays, f))
                                count+=1
                                print("removed "+f)
                            else:
                                shutil.rmtree(f,onerror=honfigurator.onerror)
                                count+=1
                                print("removed "+f)
                print(f"DONE. Cleaned {count} files.")
            def start_all():
                global deployed_status
                for i in range (1,(int(self.dataDict['svr_total']) +1)):
                    pcount=initialise.playerCountX(self,i)
                    deployed_status = dmgr.mData.returnDict_deployed(self,i)
                    service_name=f"adminbot{i}"
                    bot_running=svrcmd.honCMD.check_proc(f"{service_name}.exe")
                    if exists(f"{deployed_status['sdc_home_dir']}\\pending_shutdown"):
                        os.remove(f"{deployed_status['sdc_home_dir']}\\pending_shutdown")
                    if bot_running == False:
                        if pcount == -3:
                            if self.dataDict['use_proxy']=='True':
                                if initialise.check_port(deployed_status['svr_proxyPort']):
                                    pass
                                else:
                                    tex.insert(END,"Proxy is not running. You may not start the server without the proxy first running.\n",'warning')
                                    tex.see(tk.END)
                                    return
                            initialise.start_bot(self,True)
                            #viewButton.refresh()
                viewButton.refresh()
                #self.app.after(15000,viewButton.refresh())
            def stop_all():
                for i in range (1,(int(self.dataDict['svr_total']) +1)):
                    pcount=initialise.playerCountX(self,i)
                    deployed_status = dmgr.mData.returnDict_deployed(self,i)
                    service_name=f"adminbot{i}"
                    service_check = initialise.get_service(service_name)
                    if pcount <= 0:
                        if service_check:
                            if service_check['status'] == 'running':
                                if initialise.stop_service(self,service_name,True):
                                    tex.insert(END,f"{service_name} stopped successfully.\n")
                                else:
                                    tex.insert(END,f"{service_name} failed to stop.\n")
                        bot_running=svrcmd.honCMD.check_proc(f"{service_name}.exe")
                        bot_running=initialise.check_proc(f"{service_name}.exe")
                        hon_running=initialise.check_proc(f"KONGOR_ARENA_{i}.exe")
                        if bot_running or hon_running:
                            initialise.stop_bot(self,f"{service_name}.exe")
                            initialise.stop_bot(self,f"KONGOR_ARENA_{i}.exe")
                            initialise.stop_bot(self,f"HON_SERVER_{i}.exe")
                    else:
                        print("[ABORT] players are connected. Scheduling shutdown instead..")
                        initialise.schedule_shutdown(deployed_status)
                viewButton.refresh()
            def save_num_rows(mod_by):
                num_rows_file = f"{application_path}\\config\\num_server_rows"
                with open(num_rows_file,'w') as f:
                    f.write(mod_by)
                return

            def get_size(start_path):
                    total_size = 0
                    for dirpath, dirnames, filenames in os.walk(start_path):
                        for f in filenames:
                            fp = os.path.join(dirpath, f)
                            # skip if it is symbolic link
                            if not os.path.islink(fp):
                                total_size += os.path.getsize(fp)
                    return total_size
            """ tk_ToolTip_class101.py
            gives a Tkinter widget a tooltip as the mouse is above the widget
            tested with Python27 and Python34  by  vegaseat  09sep2014
            www.daniweb.com/programming/software-development/code/484591/a-tooltip-class-for-tkinter

            Modified to include a delay time by Victor Zaccardo, 25mar16
            """
            def auto_refresher():
                global refresh_next
                # global auto_refresh_var
                global update_counter
                global update_delay
                global refresh_counter
                global refresh_delay
                global first_check_complete
                global first_tab_switch
                global updating

                update_counter+=1
                refresh_counter+=1
                #if (tabgui.index("current")) == 0:
                if update_counter >= update_delay or first_check_complete == False:
                    first_check_complete = True
                    update_counter = 0
                    print("checking for honfigurator update")
                    self.update_repository(NULL,NULL,NULL)
                    print("checking for hon update")
                    if not updating:
                        Thread(target=self.forceupdate_hon,args=(False,"all",self.tab3_hosterd.get(),self.tab3_regionsd.get(),self.tab1_from_svr.get(),self.tab1_servertd.get(),self.tab3_hondird.get(),self.tab3_honreplay.get(),self.tab3_user.get(),self.tab3_pass.get(),self.tab3_ip.get(),self.tab3_bottokd.get(),self.tab3_discordadmin.get(),self.tab3_masterserver.get(),True,self.enablebot.get(),self.alert_on_crash.get(),self.alert_on_lag.get(),self.tab1_alertlist_limit.get(),self.tab1_eventlist_limit.get(),self.autoupdate.get(),self.console.get(),self.useproxy.get(),self.restart_proxy.get(),self.tab3_game_port.get(),self.tab3_voice_port.get(),self.core_assign.get(),self.priority.get(),self.botmatches.get(),self.debugmode.get(),self.git_branch.get(),self.increment_port.get())).start()
                    current_version=dmgr.mData.check_hon_version(self,f"{self.dataDict['hon_directory']}hon_x64.exe")
                    latest_version=svrcmd.honCMD().check_upstream_patch()
                    if latest_version != False:
                        latest_version_list = latest_version.split('.')
                        if len(latest_version_list) == 3:
                            latest_version = f"{'.'.join(latest_version_list)}.0"

                    if (self.dataDict['svr_hoster'] != "eg. T4NK" and self.autoupdate.get()==True and current_version == latest_version):
                        Thread(target=honfigurator.check_deployed_update,args=[self]).start()
                if refresh_next==True:
                    if server_admin_loading: refresh_counter = 0
                    if ((refresh_counter >= int(refresh_delay)) or first_tab_switch):
                            refresh_counter=0
                            try:
                                viewButton.refresh(int(stretch.get())+3)
                            except NameError:
                                viewButton.refresh(mod_by)
                            except Exception:
                                print(traceback.format_exc())
                refresh_next=True
                app.after(int(f"{auto_refresh_delay}000"),auto_refresher)
                return
            # create a Scrollbar and associate it with txt
            combo = TextScrollCombo(self.app)
            combo.config(width=600, height=600)
            self.update_repository(NULL,NULL,NULL)
            #tabgui.bind('<<NotebookTabChanged>>',viewButton.refresh)
            #tabgui2.bind('<<NotebookTabChanged>>',viewButton.load_log)

            global refresh_next
            refresh_next = True
            auto_refresher()
            # TODO: re-implement below for systray icon
            #self.app.protocol('WM_DELETE_WINDOW', hide_window)
            #self.app.mainloop()
    app = tk.Tk()
    honfigurator(app)
    app.mainloop()
    #test.creategui()
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 5)
