import pkg_resources
import sys
import subprocess as sp
required = {'discord.py==1.7.3','psutil','wmi','getmac','pygit2','gitpython','python-hosts','pillow'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    python = sys.executable
    sp.check_call([python, '-m', 'pip', 'install', *missing], stdout=sp.DEVNULL)
# determine if application is a script file or frozen exe

from asyncio.subprocess import DEVNULL
import tkinter as tk
from tkinter import *
from tkinter import getboolean, ttk
import configparser
import psutil
import socket
import os
from asyncio.windows_events import NULL
import time
from os.path import exists
import shutil
from tkinter import PhotoImage
import ctypes
from tkinter import END
import distutils
from distutils import dir_util
import subprocess
import traceback
# task scheduler component, didn't quite work as I intended
#import win32com.client
import datetime
from pygit2 import Repository
import git
from python_hosts import Hosts, HostsEntry
from functools import partial

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)
if is_admin():
    config_global = os.path.abspath(application_path)+"\\config\\global_config.ini"
    config_default = f"{os.path.abspath(application_path)}\\config\\default_config.ini"
    config_local = os.path.abspath(application_path)+"\\config\\local_config.ini"
    if not exists(config_local):
        shutil.copy(config_default,config_local)

    import cogs.server_status as svrcmd
    import cogs.dataManager as dmgr

    global hon_api_updated
    #
    #   This changes the taskbar icon by telling windows that python is not an app but an app hoster
    #   Otherwise taskbar icon will be python shell icon
    myappid = 'honfiguratoricon.1.0' # arbitrary string
    mod_by=13
    bot_tab=0
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    hon_api_updated = False
    players_connected = False

    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
    #
    #
    class initialise():
        global config_global
        global config_local
        global deployed_status
        #global deployed_status
        def __init__(self):
            global app_name
            self.data = dmgr.mData()
            self.dataDict = self.data.returnDict()
            self.startup = initialise.get_startupcfg(self)
            self.nssm = self.dataDict['nssm_exe']
            self.hon_directory = self.dataDict['hon_directory']
            self.hon_game_dir = self.dataDict['hon_game_dir']
            self.sdc_home_dir = self.dataDict['sdc_home_dir']
            self.hon_logs_dir = self.dataDict['hon_logs_dir']
            self.bot_version = self.dataDict['bot_version']
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
                except: pass
            else:
                self.ver_existing = 0
            #app_name=f"adminbot{self.dataDict['svr_id']}"
            app_name=f"adminbot"
            # if exists(f"{self.sdc_home_dir}\\config\\local_config.ini"):
            #     config = configparser.ConfigParser()
            #     config.read(f"{self.sdc_home_dir}\\config\\local_config.ini")
            # return
        def start_bot(self,deployed):
            #start_bot = subprocess.Popen(['cmd',"python",f"{self.dataDict['sdc_home_dir']}\\sdc.py"])
            if deployed:
                try:
                    os.chdir(deployed_status['sdc_home_dir'])
                    os.startfile(f"adminbot{deployed_status['svr_id']}-launch.exe")
                    os.chdir(application_path)
                    return True
                except Exception as e:
                    print(e)
                    return False
            else:
                try:
                    os.chdir(self.dataDict['sdc_home_dir'])
                    os.startfile(f"adminbot{self.dataDict['svr_id']}-launch.exe")
                    os.chdir(application_path)
                    return True
                except Exception as e:
                    print(e)
                    return False
        def check_proc(proc_name):
            for proc in psutil.process_iter():
                if proc.name() == proc_name:
                    return True
            return False
        def stop_bot(self,proc_name):
            for proc in psutil.process_iter():
                if proc.name() == proc_name:
                    proc.kill()
        def add_hosts_entry(self):
            hosts = Hosts(path='c:\\windows\\system32\\drivers\\etc\\hosts')
            mserver = self.dataDict['master_server']
            add_mserver=False
            ip_addr = None
            if ":" in mserver:
                mserver = mserver.split(":")
                mserver = mserver[0]
            try:
                ip_addr = socket.gethostbyname(mserver)
            except Exception as e:
                print(e)
                import wmi
                c = wmi.WMI()
                x = c.Win32_PingStatus(Address=mserver)
                ip_addr = (x[0].ProtocolAddress)
                print(ip_addr)
            try:
                process = subprocess.run(["nslookup", mserver], stdout=subprocess.PIPE, text=True)
                output = process.stdout
                output = output.split('\n')
                ip_arr = []
                for data in output:
                    if 'Address' in data:
                        ip_arr.append(data.replace('Address: ',''))
                ip_arr.pop(0)
                if len(ip_addr) == 0:
                    add_mserver=True
                print (ip_arr)
            except Exception as e:
                print(e)
            if ip_addr == None or ip_addr == '':
                if 'kongor.online' in mserver:
                    ip_addr = "73.185.77.188"
                else: return False
                print(f"Problem obtaining IP. Adding last known IP to hosts file {ip_addr}")
            if add_mserver:
                hosts.remove_all_matching(name='client.sea.heroesofnewerth.com')
                hosts.write()
                add_entry = HostsEntry(entry_type='ipv4', address=ip_addr, names=[f'client.sea.heroesofnewerth.com  {mserver}   #required by hon as this address is frequently used to poll for match stats'])
            else:
                hosts.remove_all_matching(name='client.sea.heroesofnewerth.com')
                hosts.write()
                add_entry = HostsEntry(entry_type='ipv4', address=ip_addr, names=['client.sea.heroesofnewerth.com    #required by hon as this address is frequently used to poll for match stats'])
            hosts.add([add_entry])
            hosts.write()
        def KOTF(self):
            app_svr_desc = subprocess.run([f'{application_path}\\cogs\\keeper.exe'],stdout=subprocess.PIPE, text=True)
            rc = app_svr_desc.returncode
            result = str(app_svr_desc.stdout)
            if rc == 0:
                print("hashes checked OK")
                return result
            elif rc == 1:
                print(bcolors.FAIL +"ERROR CHECKING HASHES, please obtain correct server binaries" + bcolors.ENDC)
                tex.insert(END,"ERROR CHECKING HASHES, please obtain correct server binaries\n",'warning')
                tex.insert(END,"continuing anyway")
                # returning true as I have no idea what the right hashes should be anymore
                return True
            elif rc == 3:
                print(bcolors.FAIL +"ERROR GETTING MAC ADDR" + bcolors.ENDC)
                tex.insert(END,"ERROR GETTING MAC ADDR\n",'warning')
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
        #                     p = subprocess.Popen(['SCHTASKS', '/CHANGE', '/TN', task.Path,"/DISABLE"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #                     return True
        #                 elif TASK_STATE[task.State] == "Disabled" and auto_update == True:
        #                     p = subprocess.Popen(['SCHTASKS', '/CHANGE', '/TN', task.Path,"/ENABLE"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #                     return False
        #                 return
        #         else: 
        #             if auto_update == True:
        #                 initialise.register_updater(self,selected_branch)
        #                 return True
        #             else:
        #                 return False
        def update_repository(self,selected_branch):
            current_branch = Repository('.').head.shorthand  # 'master'
            if selected_branch != current_branch:
                checkout = subprocess.run(["git","checkout",selected_branch],stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True)
                if checkout.returncode == 0:
                    print(f"Repository: {selected_branch}\nCheckout status: {checkout.stdout}")
                    tex.insert(END,f"Repository: {selected_branch}\nCheckout Status: {checkout.stdout}")
                    print(f"Updating selected repository: {selected_branch} branch")
                    output = subprocess.run(["git", "pull"],stdout=subprocess.PIPE, text=True)
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
                output = subprocess.run(["git", "pull"],stdout=subprocess.PIPE, text=True)
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
            except Exception as ex:
                # raise psutil.NoSuchProcess if no service with such name exists
                print(f"{service_name} does not exist")
                return False
                #print(str(ex))
            return service
        def disable_service(service_name):
            #doesnt work
            os.system(f'net disable "{service_name}"')
        def playerCount(self):
            check = subprocess.Popen([self.dataDict['player_count_exe_loc'],self.dataDict['hon_file_name']],stdout=subprocess.PIPE, text=True)
            i = int(check.stdout.read())
            if i == -3 and self.dataDict['master_server'] == "honmasterserver.com":
                try:
                    check = subprocess.Popen([self.dataDict['player_count_exe_loc'],f"KONGOR_ARENA_{self.svr_id}.exe"],stdout=subprocess.PIPE, text=True)
                    i = int(check.stdout.read())
                except: pass
            elif i == -3 and 'kongor.online' in self.dataDict['master_server']:
                try:
                    check = subprocess.Popen([self.dataDict['player_count_exe_loc'],f"HON_SERVER_{self.svr_id}.exe"],stdout=subprocess.PIPE, text=True)
                    i = int(check.stdout.read())
                except: pass
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
                return False

        def playerCountX(self,svr_id):
            if self.dataDict['master_server'] == "honmasterserver.com":
                check = subprocess.Popen([self.dataDict['player_count_exe_loc'],f"HON_SERVER_{svr_id}.exe"],stdout=subprocess.PIPE, text=True)
            else:
                check = subprocess.Popen([self.dataDict['player_count_exe_loc'],f"KONGOR_ARENA_{svr_id}.exe"],stdout=subprocess.PIPE, text=True)
            i = int(check.stdout.read())
            if i == -3 and self.dataDict['master_server'] == "honmasterserver.com":
                try:
                    check = subprocess.Popen([self.dataDict['player_count_exe_loc'],f"KONGOR_ARENA_{svr_id}.exe"],stdout=subprocess.PIPE, text=True)
                    i = int(check.stdout.read())
                except: pass
            elif i == -3 and 'kongor.online' in self.dataDict['master_server']:
                try:
                    check = subprocess.Popen([self.dataDict['player_count_exe_loc'],f"HON_SERVER_{svr_id}.exe"],stdout=subprocess.PIPE, text=True)
                    i = int(check.stdout.read())
                except: pass
            check.terminate()
            return i
        def start_service(self,service_name,deployed):
            try:
                #os.system(f'net start "{service_name}"')
                if deployed:
                    subprocess.Popen(['net','start',f'{service_name}'])
                else:
                    subprocess.run(['net','start',f'{service_name}'])
                # waiting = True
                # threshold = 15
                # o=0
                # while waiting:
                #     o+=1
                #     service = initialise.get_service(service_name)
                #     print(f"\nwaiting for service to start.. {o}/{threshold}secs remaining")
                #     if service['status'] == 'running' or service['status'] == 'start_pending':
                #         print(f"{service_name} started")
                #         return True
                #     time.sleep(1)
                #     if o == threshold:
                #         return False
            except:
                print ('could not start service {}'.format(service_name))
                return False
            return True
        def stop_service(self,service_name,deployed):
            try:
                #os.system(f'net stop "{service_name}"')
                if deployed:
                    subprocess.Popen(['net','stop',f'{service_name}'])
                else:
                    subprocess.run(['net','stop',f'{service_name}'])
                # waiting = True
                # threshold = 15
                # o=0
                # while waiting:
                #     o+=1
                #     service = initialise.get_service(service_name)
                #     print(f"\nwaiting for service to stop.. {o}/{threshold}secs remaining")
                #     if service['status'] == 'stopped':
                #         print(f"{service_name} stopped")
                #         return True
                #     time.sleep(1)
                #     if o == threshold:
                #         return False
            except:
                print ('could not stop service {}'.format(service_name))
                return False
            return True

        def create_service_bot(self,service_name):
            if not exists(f"{self.dataDict['hon_directory']}\\nssm.exe"):
                shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\nssm.exe",f"{self.dataDict['hon_directory']}\\nssm.exe")
            sp.run([self.dataDict['nssm_exe'], "install",service_name,f"{self.sdc_home_dir}\\adminbot{self.dataDict['svr_id']}.exe"])
            return True
        def create_service_generic(self,service_name,application):
            if not exists(f"{self.dataDict['hon_directory']}\\nssm.exe"):
                shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\nssm.exe",f"{self.dataDict['hon_directory']}\\nssm.exe")
            sp.run([self.dataDict['nssm_exe'], "install",service_name,f"{self.dataDict['hon_directory']}{application}"])
            return True
        def configure_service_generic(self,service_name,application,arguments):
            if not exists(f"{self.dataDict['hon_directory']}\\nssm.exe"):
                shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\nssm.exe",f"{self.dataDict['hon_directory']}\\nssm.exe")
            sp.run([self.dataDict['nssm_exe'], "set",service_name,"Application",f"{self.dataDict['hon_directory']}{application}"])
            #time.sleep
            if arguments is not None:
                sp.run([self.dataDict['nssm_exe'], "set",service_name,"AppParameters",arguments])
                #time.sleep(1)
            sp.run([self.dataDict['nssm_exe'], "set",service_name,f"AppDirectory",f"{self.dataDict['hon_directory']}"])
            #time.sleep(1)
            sp.run([self.dataDict['nssm_exe'], "set",service_name,"Start","SERVICE_DEMAND_START"])
            #time.sleep(1)
            sp.run([self.dataDict['nssm_exe'], "set",service_name,f"AppExit","Default","Restart"])
            #time.sleep(1)
            if service_name == "HoN Server Manager":
                sp.run([self.dataDict['nssm_exe'], "set",service_name,"AppEnvironmentExtra",f"USERPROFILE={self.dataDict['hon_manager_dir']}"])
            elif service_name == "HoN Proxy Manager":
                sp.run([self.dataDict['nssm_exe'], "set",service_name,"AppEnvironmentExtra",f"APPDATA={self.dataDict['hon_root_dir']}"])
            return True
        def configure_service_api(self,service_name):
            if not exists(f"{self.dataDict['hon_directory']}\\nssm.exe"):
                shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\nssm.exe",f"{self.dataDict['hon_directory']}\\nssm.exe")
            sp.run([self.dataDict['nssm_exe'], "set",service_name,f"Application",f"{self.dataDict['hon_directory']}API_HON_SERVER.exe"])
            return True
        def configure_service_bot(self,service_name):
            if not exists(f"{self.dataDict['hon_directory']}\\nssm.exe"):
                shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\nssm.exe",f"{self.dataDict['hon_directory']}\\nssm.exe")
            sp.run([self.dataDict['nssm_exe'], "set",service_name,"Application",f"{self.sdc_home_dir}\\adminbot{self.dataDict['svr_id']}.exe"])
            #time.sleep(1)
            sp.run([self.dataDict['nssm_exe'], "set",service_name,f"AppDirectory",f"{self.sdc_home_dir}"])
            #time.sleep(1)
            sp.run([self.dataDict['nssm_exe'], "set",service_name,f"AppStderr",f"{self.sdc_home_dir}\\{self.service_name_bot}.log"])
            #time.sleep(1)
            sp.run([self.dataDict['nssm_exe'], "set",service_name,"Start","SERVICE_DEMAND_START"])
            #time.sleep(1)
            sp.run([self.dataDict['nssm_exe'], "set",service_name,f"AppExit","Default","Restart"])
            #time.sleep(1)
            sp.run([self.dataDict['nssm_exe'], "set",service_name,"AppParameters",f"adminbot.py"])
            return True

        def restart_service(self,service_name):
            try:
                #os.system(f'net stop "{service_name}"')
                sp.run(['net','stop',f'{service_name}'])
                # waiting = True
                # threshold = 15
                # o=0
                # while waiting:
                #     o+=1
                #     service = initialise.get_service(service_name)
                #     print(f"waiting for service to start.. {o}/{threshold}secs remaining")
                #     if service['status'] == 'stopped':
                #         print(f"{service_name} started")
                #         waiting=False
                #     time.sleep(1)
                #     if o == threshold:
                #         return False
            except:
                print ('could not stop service {}'.format(service_name))
                return False
            try:
                #os.system(f'net start "{service_name}"')
                sp.run(['net','start',f'{service_name}'])
                # waiting = True
                # threshold = 15
                # o=0
                # while waiting:
                #     o+=1
                #     service = initialise.get_service(service_name)
                #     print(f"waiting for service to start.. {o}/{threshold}secs remaining")
                #     if service['status'] == 'running' or service['status'] == 'start_pending':
                #         print(f"{service_name} started")
                #         waiting=False
                #     time.sleep(1)
                #     if o == threshold:
                #         return False
            except:
                print ('could not start service {}'.format(service_name))
                return False
            return True
        def schedule_restart(self):
            temFile = f"{self.sdc_home_dir}\\pending_restart"
            with open(temFile, "w") as f:
                f.write("True")
        def schedule_shutdown(deployed_status):
            temFile = f"{deployed_status['sdc_home_dir']}\\pending_shutdown"
            with open(temFile, "w") as f:
                f.write("True")
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

        def create_config(self,filename,type,svr_port,voicelocal,svr_proxyport,voiceremote,serverID,serverHoster,location,svr_total,svr_ip,master_user,master_pass,svr_desc):
            self.proxy = {}
            self.base = dmgr.mData.parse_config(self,os.path.abspath(application_path)+"\\config\\honfig.ini")
            iter = self.dataDict['incr_port']
            svr_identifier = self.dataDict['svrid_total']
            svr_ip = dmgr.mData.getData(self,"svr_ip")
            # networking = ["svr_proxyPort","svr_proxyRemoteVoicePort"]
            # for i in networking:
            #     temp_port = self.base[i]
            #     temp_port = temp_port.strip('"')
            #     temp_port = int(temp_port)
            #     temp_port = temp_port + iter
            #     self.startup.update({i:f'"{temp_port}"'})
            if type == "startup":
                print("customising startup.cfg with the following values")
                print("svr_id: " + str(serverID))
                print("svr_host: " + str(serverHoster))
                print("svr_location: " + str(location))
                print("svr_total: " + str(svr_total))
                print("svr_ip: " + str(svr_ip))
                #self.startup = dmgr.mData.parse_config(self,os.path.abspath(application_path)+"\\config\\honfig.ini")
                    # if i == "svr_port":
                    #     print("svr_port: "+str(temp_port))
                    # if i == "svr_proxyPort" and self.dataDict['use_proxy'] == True:
                    #     print("svr_proxyPort: "+str(temp_port))
                    # if i == "svr_proxyLocalVoicePort" and self.dataDict['use_proxy'] == True:
                    #     print("voice_port"+str(temp_port))
                # if self.dataDict['use_proxy'] == True:
                #     tem_game_port_proxy = int(game_port_proxy)
                #     tem_voice_port_proxy = int(voice_port_proxy)
                #     tem_game_port_proxy = tem_game_port_proxy + iter
                #     tem_voice_port_proxy = tem_voice_port_proxy + iter
                #     self.startup.update({'svr_proxyPort':f'"{tem_game_port_proxy}"'})
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
                    # tem_game_port +=10000
                    # tem_voice_port +=10000
                else:
                    self.startup.update({"man_enableProxy":f'"false"'})
                    # tem_game_port_proxy +=10000
                    # tem_voice_port_proxy +=10000
                self.startup.update({"svr_name":f'"{serverHoster} {str(svr_identifier)}"'})
                self.startup.update({"svr_location":f'"{location}"'})
                self.startup.update({"svr_ip":f'"{svr_ip}"'})
                self.startup.update({"svr_login":f'"{master_user}"'})
                self.startup.update({"svr_password":f'"{master_pass}"'})
                self.startup.update({"svr_desc":f'"{svr_desc}"'})
            elif type == "proxy":
                self.proxy.update({'redirectIP':'127.0.0.1'})
                self.proxy.update({'publicip':svr_ip})
                self.proxy.update({'publicPort':svr_proxyport})
                self.proxy.update({'redirectPort':svr_port})
                self.proxy.update({'voiceRedirectPort':voicelocal})
                self.proxy.update({'voicePublicPort':voiceremote})
                self.proxy.update({'region':'naeu'})
            dmgr.mData.setData(NULL,filename,type,self.startup,self.proxy)
            return True
        def configure_firewall(self,name,application):
            try:
                check_rule = os.system(f"netsh advfirewall firewall show rule name=\"{name}\"")
                if check_rule == 0:
                    add_rule = os.system(f"netsh advfirewall firewall set rule name=\"{name}\" new program=\"{application}\" dir=in action=allow")
                    print("firewall rule modified.")
                    tex.insert(END,f"Windows firewall configured for application: {application}\n")
                    return True
                elif check_rule == 1:
                    add_rule = os.system(f"netsh advfirewall firewall add rule name=\"{name}\" program=\"{application}\" dir=in action=allow")
                    print("firewall rule added.")
                    tex.insert(END,f"Windows firewall configured for application: {application}\n")
                    return True
            except: 
                print(traceback.format_exc())
                return False
        def remove_firewall(self,name,application):
            try:
                check_rule = os.system(f"netsh advfirewall firewall show rule name=\"{name}\"")
                if check_rule == 0:
                    remove_rule = os.system(f"netsh advfirewall firewall delete rule name=\"{name}\"")
            except: 
                print(traceback.format_exc())
                return False
        def build(self,name):
            os.environ["PYTHONHASHSEED"] = "1"
            os.system(f'pyinstaller --noconfirm --onefile --console --icon .\\icons\\botico.png --uac-admin --add-data "cogs;cogs/" --add-data "config;config/"  "adminbot.py" --name {name} -y')
            return True
        def configureEnvironment(self,configLoc,force_update,use_console):
            global hon_api_updated
            global players_connected
            global tex

            self.bot_version = float(self.bot_version)
            bot_needs_update = False
            bot_first_launch = False
            exe_force_copy = False
            
            os.environ["USERPROFILE"] = self.dataDict['hon_home_dir']
            os.environ["APPDATA"] = self.dataDict['hon_root_dir']


            #self.ver_existing = float(self.ver_existing)
            if self.bot_version > self.ver_existing: # or checkbox force is on:
                bot_needs_update = True
            
            print()
            print("==========================================")
            print("CHECKING EXISTING HON ENVIRONMENT")
            print("==========================================")
            tex.insert(END,f"================= {self.service_name_bot} ===================\n")

            if exists(f"{self.hon_home_dir}\\Documents"):
                #os.environ["USERPROFILE"] = self.hon_home_dir
                print(f"Environment EXISTS for {self.service_name_bot}: " + (os.environ["USERPROFILE"] + "!"))

            else:
                os.makedirs(f"{self.hon_home_dir}\\Documents")
                #os.environ["USERPROFILE"] = self.hon_home_dir
                print(f"Environment requires creating for new server {self.service_name_bot}...")
                print("Created & Configured HoN environment: " + (os.environ["USERPROFILE"] + "!"))
                bot_first_launch = True
            if not exists(f"{self.dataDict['hon_root_dir']}\\Documents"):
                os.makedirs(f"{self.dataDict['hon_root_dir']}\\Documents")

            if exists(f"{self.dataDict['sdc_home_dir']}\\config\\local_config.ini"):
                try:
                    if self.deployed_status['hon_directory'] != self.dataDict['hon_directory']:
                        # think about migrating here, like
                        #distutils.dir_util.copy_tree(os.path.abspath(application_path)+"\\oldSDC\\", f'{self.sdc_home_dir}\\newSDC\\')
                        try:
                            shutil.copy(f"{self.deployed_status['sdc_home_dir']}\\messages\\message{self.dataDict['svr_identifier']}",f"{self.dataDict['sdc_home_dir']}\\messages\message{self.dataDict['svr_identifier']}.txt")
                            shutil.copy(f"{self.deployed_status['sdc_home_dir']}\\cogs\\total_games_played",f"{self.dataDict['sdc_home_dir']}\\cogs\\total_games_played")
                        except Exception as e:
                            print(e)
                    if self.deployed_status['svr_hoster'] != self.dataDict['svr_hoster']:
                        try:
                            shutil.copy(f"{self.deployed_status['sdc_home_dir']}\\messages\\message{self.dataDict['svr_identifier']}",f"{self.dataDict['sdc_home_dir']}\\messages\message{self.dataDict['svr_identifier']}.txt")
                        except Exception as e:
                            print(e)
                except Exception as e:
                                print(e)

            if not exists(self.hon_logs_dir):
                print("creating: " + self.hon_logs_dir)
                os.makedirs(self.hon_logs_dir)
                print(f"creating: {self.hon_logs_dir} ...")
                #   os.chdir(self.hon_logs_dir)     # not required as we're honfigurator not a bot.

            if not exists(self.sdc_home_dir):
                print(f"creating: {self.sdc_home_dir} ...")
                os.makedirs(self.sdc_home_dir)
            
            if not exists(f"{self.dataDict['hon_manager_dir']}\\Documents\\Heroes of Newerth x64\\game\\replays"):
                print(f"creating {self.dataDict['hon_manager_dir']}\\Documents\\Heroes of Newerth x64\\game\\replays")
                os.makedirs(f"{self.dataDict['hon_manager_dir']}\\Documents\\Heroes of Newerth x64\\game\\replays")
            # fix this - need a way to know wwhether to copy the old bot directory files
            # if (self.deployed_status['sdc_home_dir'] != self.dataDict['sdc_home_dir']):
            #     # copy older metadata files
            #     try:
            #         shutil.copy(f"{self.deployed_status['sdc_home_dir']}\\..\\sdc\\messages\\message{self.dataDict['svr_identifier']}",f"{self.sdc_home_dir}\\messages\message{self.dataDict['svr_identifier']}.txt")
            #         shutil.copy(f"{self.deployed_status['sdc_home_dir']}\\..\\sdc\\cogs\\total_games_played",f"{self.sdc_home_dir}\\cogs\\total_games_played")
            #     except Exception as e:
            #         print(e)


            if not exists(f"{self.sdc_home_dir}\\messages"):
                print(f"creating: {self.sdc_home_dir}\\messages ...")
                os.makedirs(f"{self.sdc_home_dir}\\messages")
            if not exists(f"{self.sdc_home_dir}\\suspicious"):
                print(f"creating: {self.sdc_home_dir}\\suspicious ...")
                os.makedirs(f"{self.sdc_home_dir}\\suspicious")
            if not exists(f"{self.sdc_home_dir}\\config"):
                print(f"creating: {self.sdc_home_dir}\\config ...")
                os.makedirs(f"{self.sdc_home_dir}\\config")
            if not exists(f"{self.sdc_home_dir}\\icons"):
                print(f"creating: {self.sdc_home_dir}\\icons ...")
                os.makedirs(f"{self.sdc_home_dir}\\icons")
            if not exists(f"{self.sdc_home_dir}\\cogs"):
                print(f"creating: {self.sdc_home_dir}\\cogs ...")
                os.makedirs(f"{self.sdc_home_dir}\\cogs")
            if not exists(f"{self.hon_directory}game_shared_x64.dll"):
                shutil.copy(f"{self.hon_directory}game\\game_shared_x64.dll",f"{self.hon_directory}game_shared_x64.dll")
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
                    print(f"{self.hon_directory}game\\game_shared_x64.dll needs to be copied into {self.hon_directory}")

            ## global networking settings ##
            iter = int(self.dataDict['incr_port'])
            self.game_port = int(self.dataDict['game_starting_port']) + iter
            self.voice_port = int(self.dataDict['voice_starting_port']) + iter
            self.game_port_proxy = self.game_port + 10000
            self.voice_port_proxy = self.voice_port + 10000
            self.secrets = initialise.KOTF(self)
            if self.secrets:
                self.svr_desc = self.secrets.split(',')[0]
                self.svr_desc = self.svr_desc.replace('\n','')
                self.master_user = self.secrets.split(',')[1]
                self.master_user = self.master_user.replace('\n','')
                self.master_pass = self.secrets.split(',')[2]
                self.master_pass = self.master_pass.replace('\n','')
            else:
                bot_needs_update = False
                force_update = False
                bot_first_launch = False
            #
            #   Check if startup.cfg exists.
            if exists(f"{self.hon_game_dir}\\startup.cfg") and bot_first_launch != True and bot_needs_update != True and force_update != True:
                print(f"Server is already configured, checking values for {self.service_name_bot}...")
                dmgr.mData.parse_config(self,f"{self.hon_game_dir}\\startup.cfg")
            if self.dataDict['use_proxy'] == "True":
                firewall = initialise.remove_firewall(self,self.dataDict['hon_file_name'],self.dataDict['hon_exe'])
            else:
                firewall = initialise.configure_firewall(self,self.dataDict['hon_file_name'],self.dataDict['hon_exe'])
            if not exists(f"{self.hon_game_dir}\\startup.cfg") or bot_first_launch == True or bot_needs_update == True or force_update == True:
                if bot_needs_update or force_update == True:
                    tex.insert(END,f"FORCE or UPDATE DETECTED, APPLIED v{self.bot_version}\n")
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
                        print("copying server exe...")
                    except: 
                        shutil.move(exe_path,f"{exe_path_cut}_old.exe")
                        shutil.copy(f"{self.dataDict['hon_directory']}hon_x64.exe",exe_path)
                        exe_force_copy=True
                if not exists(f"{self.hon_game_dir}\\startup.cfg"):
                    print(f"Server {self.service_name_bot} requires full configuration. No existing startup.cfg or game_settings_local.cfg. Configuring...")
                initialise.create_config(self,f"{self.hon_game_dir}\\startup.cfg","startup",self.game_port,self.voice_port,self.game_port_proxy,self.voice_port_proxy,self.svr_id,self.svr_hoster,self.svr_region_short,self.svr_total,self.svr_ip,self.master_user,self.master_pass,self.svr_desc)
                initialise.create_config(self,f"{self.hon_game_dir}\\proxy_config.cfg","proxy",self.game_port,self.voice_port,self.game_port_proxy,self.voice_port_proxy,self.svr_id,self.svr_hoster,self.svr_region_short,self.svr_total,self.svr_ip,self.master_user,self.master_pass,self.svr_desc)
                print(f"copying {self.service_name_bot} script and related configuration files to HoN environment: "+ self.hon_home_dir + "..")
                try:
                    shutil.copy(os.path.abspath(application_path)+"\\dependencies\\adminbot-launch.exe", f'{self.sdc_home_dir}\\{self.service_name_bot}-launch.exe')
                except PermissionError:
                    os.rename(f'{self.sdc_home_dir}\\{self.service_name_bot}.exe',f'{self.sdc_home_dir}\\{self.service_name_bot}_old.exe')
                    shutil.copy(os.path.abspath(application_path)+"\\dependencies\\adminbot-launch.exe", f'{self.sdc_home_dir}\\{self.service_name_bot}.exe')
                try:
                    shutil.copy(f"{application_path}\\dependencies\\python310.dll",self.dataDict['sdc_home_dir'])
                    shutil.copy(f"{application_path}\\dependencies\\vcruntime140.dll",self.dataDict['sdc_home_dir'])
                except Exception as e:
                    print(e)
                if not exists(f'{self.sdc_home_dir}\\{self.service_name_bot}.exe'):
                    try:
                        shutil.copy(f"{self.dataDict['python_location']}", f'{self.sdc_home_dir}\\{self.service_name_bot}.exe')
                    except PermissionError:
                        os.rename(f'{self.sdc_home_dir}\\{self.service_name_bot}.exe',f'{self.sdc_home_dir}\\{self.service_name_bot}_old.exe')
                        shutil.copy(f"{self.dataDict['python_location']}", f'{self.sdc_home_dir}\\{self.service_name_bot}.exe')

                shutil.copy(os.path.abspath(application_path)+"\\dependencies\\adminbot.py", f'{self.sdc_home_dir}\\adminbot.py')
                src_folder = os.path.abspath(application_path)+"\\cogs\\"
                dst_folder = f'{self.sdc_home_dir}\\cogs\\'
                for file_name in os.listdir(src_folder):
                    src_file = src_folder+file_name
                    dst_file = dst_folder+file_name
                    if os.path.isfile(src_file):
                        shutil.copy(src_file, dst_file)
                        print('copied', file_name)

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
                print("Done!")
                print("Checking and creating required dependencies...")
                #
                #
                # if not exists(f"{self.dataDict['hon_directory']}{self.dataDict['player_count_exe']}" or force_update == True or bot_needs_update == True):
                try:
                    shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\{self.dataDict['player_count_exe']}",f"{self.dataDict['hon_directory']}{self.dataDict['player_count_exe']}")
                except Exception as e: print(e)
                print("copying other dependencies...")
                print("Done!")
            
            if self.dataDict['master_server'] == "honmasterserver.com":
                service_api = initialise.get_service(self.service_name_api)
                if service_api:
                    #print("HON Registration API STATUS: " + self.service_name_api)
                    if service_api['status'] == 'running' or service_api['status'] == 'paused':
                        if force_update != True and bot_needs_update != True:
                            tex.insert(END,"HON Registration API STATUS: RUNNING\n")
                        elif (force_update == True or bot_needs_update == True) and hon_api_updated !=True:
                            initialise.stop_service(self,self.service_name_api,False)
                            #time.sleep(1)
                            service_api = initialise.get_service(self.service_name_api)
                            if service_api['status'] == 'stopped':
                                try:
                                    shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\API_HON_SERVER.exe",f"{self.dataDict['hon_directory']}API_HON_SERVER.exe")
                                except PermissionError:
                                    tex.insert(END,"COULD NOT UPGRADE SERVICE: " + self.service_name_api +" The service is currently runing so we cannot replace this file. We'll try again later\n",'warning')
                                    print(bcolors.FAIL +"COULD NOT UPGRADE SERVICE: " + self.service_name_api +" The service is currently runing so we cannot replace this file. We'll try again later\n" + bcolors.ENDC)
                                except: print(traceback.format_exc())
                            if initialise.configure_service_api(self,self.service_name_api):
                                hon_api_updated = True
                            #time.sleep(1)
                            initialise.start_service(self,self.service_name_api,False)
                    else:
                        if (force_update ==True or bot_needs_update == True) and hon_api_updated !=True:
                            try:
                                shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\API_HON_SERVER.exe",f"{self.dataDict['hon_directory']}API_HON_SERVER.exe")
                            except PermissionError:
                                tex.insert(END,"COULD NOT UPGRADE SERVICE: " + self.service_name_api +" The service is currently in use so we cannot replace this file. We'll try again later\n",'warning')
                                print(bcolors.FAIL +"COULD NOT UPGRADE SERVICE: " + self.service_name_api +" The service is currently runing so we cannot replace this file. We'll try again later\n") + bcolors.ENDC
                            except: print(traceback.format_exc())
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
                            tex.insert(END,"HON Registration API STATUS: " + self.service_name_api +": RUNNING\n")
                        else:
                            tex.insert(END,"HON Registration API STATUS: " + self.service_name_api +":  FAILED TO START!\n",'warning')
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
                        tex.insert(END,"HON Registration API STATUS: " + self.service_name_api +": RUNNING\n")
                    else:
                        tex.insert(END,"HON Registration API STATUS: " + self.service_name_api +":  FAILED TO START!\n",'warning')
                    print("==========================================")
            # if force_update or bot_needs_update or bot_first_launch:
            #     #Compile bot code into exe
            #     initialise.build(self,app_name)
            service_bot = initialise.get_service(self.service_name_bot)
            if service_bot:
                print(f"HONSERVER STATUS: {self.service_name_bot}")
                if use_console == False:
                    initialise.configure_service_bot(self,self.service_name_bot)
                if service_bot['status'] == 'running' or service_bot['status'] == 'paused':
                    tex.insert(END,f"HONSERVER STATUS: {self.service_name_bot}: RUNNING\n")
                    if force_update == True or bot_needs_update == True:
                        svr_state = svrcmd.honCMD()
                        svr_state.getDataDict()
                        playercount = initialise.playerCount(self)
                        if playercount <= 0:
                            print("No players connected, safe to restart...")
                            initialise.stop_service(self,self.service_name_bot,False)
                            if self.dataDict['use_proxy']=='True':
                                if initialise.check_port(self.game_port_proxy):
                                    pass
                                else:
                                    tex.insert(END,"Proxy is not running. You may not start the server without the proxy first running.\n",'warning')
                                    tex.see(tk.END)
                                    return
                            initialise.start_bot(self,False)
                        else:
                            players_connected = True
                            bot_running=initialise.check_proc(f"{self.service_name_bot}.exe")
                            if use_console and bot_running:
                                tex.insert(END,"Players are connected. A scheduled shutdown is being performed. HoNfigurator is unable to automatically reconfigure windows services to start in console mode, due to system limitation.\nPlease start your services manually in the admin tab once the scheduled shutdown is complete.",'warning')
                                initialise.schedule_shutdown(self)
                            elif use_console and bot_running == False:
                                initialise.start_bot(self,False)
                            else:
                                initialise.schedule_restart(self)
                else:
                    bot_running=initialise.check_proc(f"{self.service_name_bot}.exe")
                    server_running=initialise.check_proc(f"{self.dataDict['hon_file_name']}")
                    if force_update == True or bot_needs_update == True:
                        #reconfigure service + restart
                        if bot_running or server_running:
                            playercount = initialise.playerCount(self)
                            # if self.deployed_status['use_console'] == 'True':
                            #if playercount <=0:
                            initialise.stop_bot(self,f"{self.service_name_bot}.exe")
                                # can we hook onto existing EXEs here instead?
                            old_ip=self.dataDict['svr_ip']
                            new_ip=dmgr.mData.getData(self,"svr_ip")
                            if use_console == False or (old_ip != new_ip):
                                initialise.stop_bot(self,f"KONGOR_ARENA_{self.dataDict['svr_id']}.exe")
                                initialise.stop_bot(self,f"HON_SERVER_{self.dataDict['svr_id']}.exe")
                            # else:
                            #     # copy files to _old
                            #     players_connected=True
                            if exe_force_copy:
                                initialise.schedule_restart(self)
                    bot_running=initialise.check_proc(f"{self.service_name_bot}.exe")
                    server_running=initialise.check_proc(f"{self.dataDict['hon_file_name']}")
                    if bot_running == False:
                        if self.dataDict['use_proxy']=='True':
                            if initialise.check_port(self.game_port_proxy):
                                pass
                            else:
                                tex.insert(END,"Proxy is not running. You may not start the server without the proxy first running.\n",'warning')
                                tex.see(tk.END)
                                return
                        initialise.start_bot(self,False)
                    if use_console == False:
                        waiting = True
                        threshold = 15
                        o=0
                        while waiting:
                            o+=1
                            time.sleep(1)
                            service_bot = initialise.get_service(self.service_name_bot)
                            print(f"waiting for service to start.. {o}/{threshold}secs remaining")
                            if service_bot['status'] == 'running':
                                waiting=False
                            if o == threshold:
                                waiting=False
                        if service_bot['status'] == 'running' or service_bot['status'] == 'start_pending':
                            tex.insert(END,f"HONSERVER STATUS: {self.service_name_bot} {service_bot['status']}\n")
                        else:
                            tex.insert(END,f"HONSERVER STATUS: {self.service_name_bot} FAILED TO START!\n",'warning')
                        print("==========================================")
                    print(self.service_name_bot)
            else:
                bot_needs_update = True
                print("==========================================")
                print(f"Creating adminbot: {self.service_name_bot}..")
                print("==========================================")
                initialise.create_service_bot(self,self.service_name_bot)
                if self.dataDict['use_proxy']=='True':
                    if initialise.check_port(self.game_port_proxy):
                        pass
                    else:
                        tex.insert(END,"Proxy is not running. You may not start the server without the proxy first running.\n",'warning')
                        tex.see(tk.END)
                if use_console == False:
                    initialise.configure_service_bot(self,self.service_name_bot)
                initialise.start_bot(self,False)
                print("==========================================")
                print(f"HONSERVER STATUS: {self.service_name_bot}")

            if force_update == True or bot_first_launch == True or bot_needs_update == True:
                if players_connected == True:
                    tex.insert(END,f"{self.service_name_bot}: {playercount} Players are connected, scheduling restart for after the current match finishes..\n",'warning')
                    print(f"{self.service_name_bot}: {playercount} Players are connected, scheduling restart for after the current match finishes..\n")
                if self.dataDict['use_proxy'] == 'False':
                    tex.insert(END,f"Server ports: Game ({self.startup['svr_port']}), Voice ({self.startup['svr_proxyLocalVoicePort']})\n")
                    ports_to_forward_game.append(self.startup['svr_port'])
                    ports_to_forward_voice.append(self.startup['svr_proxyLocalVoicePort'])
                    tex.see(tk.END)
                elif self.dataDict['use_proxy'] == 'True':
                    tex.insert(END,f"Server ports (PROXY): Game ({self.startup['svr_proxyPort']}), Voice ({self.startup['svr_proxyRemoteVoicePort']})\n")
                    ports_to_forward_game.append(self.startup['svr_proxyPort'])
                    ports_to_forward_voice.append(self.startup['svr_proxyRemoteVoicePort'])
                    tex.see(tk.END)           
                print("==========================================")
            else:
                print("==========================================")
                tex.insert(END,f"ADMINBOT{self.svr_id} v{self.bot_version}\n")
                tex.insert(END,"NO UPDATES OR CONFIGURATION CHANGES MADE\n")
                tex.see(tk.END)
                #tex.insert(END,"==============================================\n")
            bot_needs_update = False
            players_connected = False
    class honfigurator():
        global tex
        def __init__(self):
            # global self.dataDict
            self.initdict = dmgr.mData()
            self.dataDict = self.initdict.returnDict()
            print (self.dataDict)
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
            os.chdir(application_path)
            current_branch = Repository('.').head.shorthand  # 'master'
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
            return ["one","two","two servers/core"]
        def incrementport(self):
            return["1","10","100","200","500","1000"]
        def priorityassign(self):
            return ["normal","high","realtime"]
        def coreadjust(self,var,index,mode):
            cores = []
            total_cores = psutil.cpu_count(logical = True)
            half_core_count = total_cores / 2
            half_core_count = int(half_core_count)
            two_servers_core = total_cores * 2
            core_assignment = str(self.core_assign.get()).lower()
            selected_id = str(self.svr_id_var.get())
            if core_assignment == "one":
                if int(self.svr_total_var.get()) > total_cores:
                    self.svr_total_var.set(total_cores)
                if int(selected_id) > int(self.svr_total_var.get()):
                    self.svr_id_var.set(total_cores)
                for i in range(total_cores):
                    cores.append(i+1)
                self.tab1_servertd['values']=cores
                self.tab1_serveridd['values']=cores
                return
            elif core_assignment == "two":
                #if int(self.svr_total_var.get()) > half_core_count:
                self.svr_total_var.set(half_core_count)
                if int(selected_id) > int(self.svr_total_var.get()):
                    self.svr_id_var.set(half_core_count)
                for i in range(half_core_count):
                    cores.append(i+1)
                self.tab1_servertd['values']=cores
                self.tab1_serveridd['values']=cores
                return
            elif core_assignment == "two servers/core":
                #if int(self.svr_total_var.get()) > two_servers_core:
                self.svr_total_var.set(two_servers_core)
                if int(selected_id) > int(self.svr_total_var.get()):
                    self.svr_id_var.set(two_servers_core)
                for i in range(two_servers_core):
                    cores.append(i+1)
                self.tab1_servertd['values']=cores
                self.tab1_serveridd['values']=cores
                return
        def corecount(self):
            cores = []
            total_cores = psutil.cpu_count(logical = True)
            half_core_count = total_cores / 2
            half_core_count = int(half_core_count)
            if self.dataDict['core_assignment'] == "two":
                total_cores = half_core_count
                #for i in range(half_core_count):
                    #cores.append(i+1)
                #self.svr_total_var.set(half_core_count)
            elif self.dataDict['core_assignment'] == "two servers/core":
                total_cores = total_cores * 2
            for i in range(total_cores):
                cores.append(i+1)
                
            return cores
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
            return ["kongor.online:666","api.kongor.online","honmasterserver.com"]
        # def reg_def_link(self,var,index,mode):
        #     reglist = self.regions()
        #     svrloc = str(self.svr_loc.get()).lower()
        #     for reg in reglist[0]:
        #         if svrloc == reg.lower():
        #             self.svr_loc.set(reglist[0][reglist[0].index(reg)])
        #             self.svr_reg_code.set(reglist[1][reglist[0].index(reg)])
        def svr_num_link(self,var,index,mode):
            if self.svr_id_var.get() == "(for single server)":
                return
            elif int(self.svr_id_var.get()) > int(self.svr_total_var.get()):
                self.svr_id_var.set(self.svr_total_var.get())
            # elif str(self.core_assign.get()).lower() == "two":
            #     self.svr_total_var.set()
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
            os.chdir(application_path)
            selected_branch = self.git_branch.get()
            current_branch = Repository('.').head.shorthand  # 'master'
            # if selected_branch != current_branch:
            checkout = subprocess.run(["git","checkout",selected_branch],stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True)
            if checkout.returncode == 0:
                # print(f"Repository: {selected_branch}\nCheckout status: {checkout.stdout}")
                #tex.insert(END,f"Repository: {selected_branch}\nCheckout Status: {checkout.stdout}")
                print(f"Updating selected repository: {selected_branch} branch")
                output = subprocess.run(["git", "pull"],stdout=subprocess.PIPE, text=True)
                print(f"Repository: {selected_branch}\nUpdate Status: {output.stdout}")
                tex.insert(END,f"Repository: {selected_branch}\nUpdate Status: {output.stdout}")
                tex.insert(END,"==========================================\n")
                #os.execv(sys.argv[0], sys.argv)
                try:
                    if 'Updating' in output.stdout or 'Switched to branch' in checkout.stderr:
                        if honfigurator.popup_bonus():
                            #test
                            path=os.path.abspath(__file__)
                            path=f"\"{path}\""
                            os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
                except Exception as e: print(e)
                return True
            else:
                print(f"Repository: {selected_branch}\nCheckout status: {checkout.stderr}")
                tex.insert(END,f"Repository: {selected_branch}\nCheckout Status ({checkout.returncode}): {checkout.stderr}")
                if 'Please commit your changes or stash them before you switch branches.' in checkout.stderr:
                    print()
                tex.insert(END,"==========================================\n")
                self.git_branch.set(current_branch)
                return False
        def forceupdate_hon(self,hon_dir,master_server):
            os.chdir(hon_dir)
            subprocess.Popen(["hon_x64.exe","-update","-masterserver",master_server])
            os.chdir(application_path)
            #honfigurator.creategui(self)
            
        def return_currentver(self):
            manifest=f"{self.dataDict['hon_directory']}Update\\manifest.xml"
            if exists(manifest):
                with open(manifest,'r') as f:
                    for line in f:
                        if "manifest version=" in line:
                            ver=line.split(" ")
                            return ver
            return "couldn't find version number."
        def sendData(self,identifier,hoster, regionshort, serverid, servertotal,hondirectory,honreplay,svr_login,svr_password,static_ip, bottoken,discordadmin,master_server,force_update,disable_bot,use_console,use_proxy,restart_proxy,game_port,voice_port,core_assignment,process_priority,botmatches,debug_mode,selected_branch,increment_port):
            global config_local
            global config_global
            global ports_to_forward_game
            global ports_to_forward_voice

            self.dataDict = self.initdict.returnDict()
            checks=True
            if " " in hoster:
                checks=False
                tex.insert(END,"FIXME: Please ensure there are no spaces in the server name field.\n",'warning')
                tex.see(tk.END)
            if " " not in hondirectory:
                checks=False
                tex.insert(END,"FIXME: Please ensure there is a space in the HoN Directory path.\n",'warning')
                tex.see(tk.END)
            if bottoken=='':
                checks=False
                tex.insert(END,"FIXME: Please provide a bot token.\n",'warning')
                tex.see(tk.END)
            if discordadmin=='':
                checks=False
                tex.insert(END,"FIXME: Please provide a discord user ID (10 digit number).\n",'warning')
                tex.see(tk.END)
            if static_ip != '':
                try:
                    # legal
                    socket.inet_aton(static_ip)
                    tex.insert(END,f"{static_ip} will be used to start your servers.\n")
                    tex.see(tk.END)
                    self.dataDict.update({'static_ip':static_ip})
                except socket.error:
                    # Not legal
                    checks=False
                    tex.insert(END,"FIXME: Please provide a valid IPv4 address.\n",'warning')
                    tex.see(tk.END)
            if checks==True:
                conf_local = configparser.ConfigParser()
                conf_global = configparser.ConfigParser()
                #   adds a trailing slash to the end of the path if there isn't one. Required because the code breaks if a slash isn't provided
                hondirectory = os.path.join(hondirectory, '')
                honreplay = os.path.join(honreplay,'')
                ports_to_forward_game=[]
                ports_to_forward_voice=[]
                #if use_console == False:
                if hondirectory != self.dataDict['hon_directory']:
                    self.dataDict.update({'hon_directory':hondirectory})
                if master_server != self.dataDict['master_server']:
                    self.dataDict.update({'master_server':master_server})
                initialise.add_hosts_entry(self)
                if honreplay != self.dataDict['hon_manager_dir']:
                    force_update = True
                    if not exists(honreplay):
                        try:
                            os.makedirs(honreplay)
                            tex.insert(END,f"CHECKME: Base directory {honreplay} has been created. Continuing on\n",'warning')
                        except Exception as e:
                            print(e)
                            tex.insert(END,f"FIXME: Unable to create directory: {honreplay} is it a valid path?\n",'warning')
                            return
                    if exists(honreplay):
                        print("migrating data")
                        if not exists(honreplay+"\\Documents\\Heroes of Newerth x64\\game\\replays"):
                            try:
                                os.makedirs(honreplay+"\\Documents\\Heroes of Newerth x64\\game\\replays")
                            except Exception as e:
                                print(e)
                            tex.insert(END,f"FIXME: Failed to create directory {honreplay}\\Documents\\Heroes of Newerth x64\\game\\replays\nIs it a valid path?\n",'warning')    
                        try:
                            distutils.dir_util.copy_tree(f"{self.dataDict['hon_manager_dir']}\\Documents\\Heroes of Newerth x64\\game\\replays",f"{honreplay}\\Documents\\Heroes of Newerth x64\\game\\replays",update=1)
                            tex.insert(END,"You have changed the hon replays directory. Please ensure you configure all servers.\n",'interest')
                            tex.insert(END,f"All replays migrated to {honreplay}\\Documents\\Heroes of Newerth x64\\game\\replays.\nYou may want to manually clean up the old directory: {self.dataDict['hon_manager_dir']} to free up disk space.\n",'interest')
                            self.dataDict.update({'hon_manager_dir':honreplay})
                        except Exception as e:
                            print(e)
                            tex.insert(END,f"FIXME: Failed to migrate data from {self.dataDict['hon_manager_dir']} to {honreplay}\n",'warning')
                # stop services that sit outside the total server range
                if int(servertotal) < int(self.dataDict['svr_total']):
                    x=int(self.dataDict['svr_total']) - int(servertotal)
                    for i in range (1,x+1):
                        o=int(servertotal)+i
                        temp_dict = dmgr.mData.returnDict_basic(self,o)
                        print("disable "+str(o))
                        playercount=initialise.playerCountX(self,o)
                        service_state = initialise.get_service(f"{app_name}{o}")
                        if playercount == 0:
                            if service_state:
                                if service_state['status'] == 'running':
                                    initialise.stop_service(self,f"{app_name}{o}",False)
                            initialise.stop_bot(self,f"{app_name}{o}.exe")
                            initialise.stop_bot(self,f"KONGOR_ARENA_{o}.exe")
                            initialise.stop_bot(self,f"HON_SERVER_{o}.exe")
                        elif playercount > 0:
                            print("scheduled shutdown of no longer required service as it sits outside the total servers range")
                            initialise.schedule_shutdown(temp_dict)
                if use_proxy:
                    if not exists(hondirectory+'proxy.exe'):
                        tex.insert(END,f"FIXME: NO PROXY.EXE FOUND. Please obtain this and place it into {hondirectory} and try again.\nContinuing with proxy disabled..\n",'warning')
                        use_proxy=False
                    if not exists(hondirectory+'proxymanager.exe'):
                        tex.insert(END,f"FIXME: NO PROXYMANAGER.EXE FOUND. Please obtain this and place it into {hondirectory} and try again.\nContinuing with proxy disabled..\n",'warning')
                        use_proxy=False
                    else:
                        firewall = initialise.configure_firewall(self,"HoN Proxy",hondirectory+'proxy.exe')
                #service_proxy_name="HoN Proxy Manager"
                service_manager_name="HoN Server Manager"
                #service_proxy = initialise.get_service(service_proxy_name)
                service_manager = initialise.get_service(service_manager_name)
                default_voice_port=11435
                manager_application=f"KONGOR ARENA MANAGER.exe"
                manager_arguments=f"-manager -noconfig -execute \"Set man_masterLogin {self.dataDict['svr_login']}:;Set man_masterPassword {self.dataDict['svr_password']};Set man_numSlaveAccounts 0;Set man_startServerPort {self.dataDict['game_starting_port']};Set man_endServerPort {int(self.dataDict['game_starting_port'])+(int(self.dataDict['svr_total'])-1)};Set man_voiceProxyStartPort {self.dataDict['voice_starting_port']};Set man_voiceProxyEndPort {int(self.dataDict['voice_starting_port'])+(int(self.dataDict['svr_total'])-1)};Set man_maxServers {self.dataDict['svr_id']};Set man_enableProxy {self.dataDict['use_proxy']};Set man_broadcastSlaves true;Set http_useCompression false;Set man_autoServersPerCPU 1;Set man_allowCPUs 0;Set host_affinity -1;Set man_uploadToS3OnDemand 1;Set man_uploadToCDNOnDemand 0;Set svr_name {self.dataDict['svr_hoster']} 0 0;Set svr_location {self.dataDict['svr_region_short']};Set svr_ip {self.dataDict['svr_ip']}\" -masterserver {master_server}"
                manager_arguments_console=f"Set man_masterLogin {self.dataDict['svr_login']}:;Set man_masterPassword {self.dataDict['svr_password']};Set man_numSlaveAccounts 0;Set man_startServerPort {self.dataDict['game_starting_port']};Set man_endServerPort {int(self.dataDict['game_starting_port'])+(int(self.dataDict['svr_total'])-1)};Set man_voiceProxyStartPort {self.dataDict['voice_starting_port']};Set man_voiceProxyEndPort {int(self.dataDict['voice_starting_port'])+(int(self.dataDict['svr_total'])-1)};Set man_maxServers {self.dataDict['svr_id']};Set man_enableProxy {self.dataDict['use_proxy']};Set man_broadcastSlaves true;Set http_useCompression false;Set man_autoServersPerCPU 1;Set man_allowCPUs 0;Set host_affinity -1;Set man_uploadToS3OnDemand 1;Set man_uploadToCDNOnDemand 0;Set svr_name {self.dataDict['svr_hoster']} 0 0;Set svr_location {self.dataDict['svr_region_short']};Set svr_ip {self.dataDict['svr_ip']}"
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
                    if service_manager:
                        if use_console == False:
                            initialise.configure_service_generic(self,service_manager_name,manager_application,None)
                        if service_manager['status'] == 'running' or service_manager['status'] == 'paused':
                            initialise.stop_service(self,service_manager_name,False)
                        else:
                            if svrcmd.honCMD.check_proc(manager_application):
                                svrcmd.honCMD.stop_proc(manager_application)
                        if copy_retry:
                            shutil.copy(f"{hondirectory}hon_x64.exe",f"{hondirectory}{manager_application}")
                        if use_console == False:
                            initialise.start_service(self,service_manager_name,False)
                        else:
                            subprocess.Popen([hondirectory+manager_application,"-manager","-noconfig","-execute",manager_arguments_console,"-masterserver",master_server])
                    else:
                        if svrcmd.honCMD.check_proc(manager_application):
                            svrcmd.honCMD.stop_proc(manager_application)
                        if use_console == False:
                            initialise.create_service_generic(self,service_manager_name,manager_application)
                            initialise.configure_service_generic(self,service_manager_name,manager_application,manager_arguments)
                            initialise.start_service(self,service_manager_name,False)
                        else:
                            subprocess.Popen([hondirectory+manager_application,"-manager","-noconfig","-execute",manager_arguments_console,"-masterserver",master_server])
                if use_proxy:
                    proxy_running=False
                    os.environ["APPDATA"] = self.dataDict['hon_root_dir']
                    application="proxymanager.exe"
                    service_proxy_name="HoN Proxy Manager"
                    service_proxy = initialise.get_service(service_proxy_name)
                    if svrcmd.honCMD.check_proc(application):
                        proxy_running=True
                    # if service_proxy:
                    print("proxy exists")
                    proxy_config=[f"count={servertotal}",f"ip={self.dataDict['svr_ip']}",f"startport={game_port}",f"startvoicePort={voice_port}","region=naeu"]
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
                                svrcmd.honCMD.stop_proc(application)
                            if svrcmd.honCMD.check_proc("proxy.exe"):
                                svrcmd.honCMD.stop_proc("proxy.exe")
                            initialise.start_service(self,service_proxy_name,False)
                        else:
                            if svrcmd.honCMD.check_proc(application):
                                svrcmd.honCMD.stop_proc(application)
                            initialise.create_service_generic(self,service_proxy_name,application)
                            initialise.configure_service_generic(self,service_proxy_name,application,None)
                            initialise.start_service(self,service_proxy_name,False)
                        print("waiting 30 seconds for proxy to finish setting up ports...")
                        time.sleep(30)
                        # else:
                        #     if service_proxy:
                        #         if service_proxy['status'] == 'running' or service_proxy['status'] == 'paused':
                        #             initialise.stop_service(self,service_proxy_name,False)
                        #     if svrcmd.honCMD.check_proc(application):
                        #         svrcmd.honCMD.stop_proc(application)
                        #     os.chdir(self.dataDict['hon_directory'])
                        #     os.startfile(f"proxymanager.exe")
                        #     os.chdir(application_path)
                        #     print("waiting 30 seconds for proxy to finish setting up ports...")
                        #     time.sleep(30)
                        self.restart_proxy.set(False)
                if identifier == "single":
                    self.basic_dict = dmgr.mData.returnDict_basic(self,serverid)
                    print()
                    print(f"Selected option to configure adminbot-server{serverid}\n")
                    print("==========================================")
                    #
                    #   local config
                    if not conf_local.has_section("OPTIONS"):
                        conf_local.add_section("OPTIONS")
                    conf_local.set("OPTIONS","svr_hoster",hoster)
                    #conf_local.set("OPTIONS","svr_region",region)
                    conf_local.set("OPTIONS","svr_region_short",regionshort)
                    conf_local.set("OPTIONS","svr_id",serverid)
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
                    conf_local.set("OPTIONS","game_starting_port",game_port)
                    conf_local.set("OPTIONS","voice_starting_port",voice_port)
                    conf_local.set("OPTIONS","github_branch",str(selected_branch))
                    conf_local.set("OPTIONS","debug_mode",str(debug_mode))
                    conf_local.set("OPTIONS","use_proxy",str(use_proxy))
                    conf_local.set("OPTIONS","svr_login",svr_login)
                    conf_local.set("OPTIONS","svr_password",svr_password)
                    conf_local.set("OPTIONS","use_console",str(use_console))
                    conf_local.set("OPTIONS","sdc_home_dir",self.basic_dict['sdc_home_dir'])
                    conf_local.set("OPTIONS","disable_bot",str(disable_bot))
                    with open(config_local, "w") as a:
                        conf_local.write(a)
                    a.close()
                    #
                    #   global values
                    # if not conf_global.has_section("OPTIONS"):
                    #     conf_global.add_section("OPTIONS")
                    # conf_global.set("OPTIONS","bot_version",self.dataDict['bot_version'])

                    # with open(config_global, "w") as b:
                    #     conf_global.write(b)
                    # b.close()
                    

                    initialise().configureEnvironment(self,force_update,use_console)
                    hon_api_updated = False
                if identifier == "all":
                    #tex.insert(END,"==========================================\n")
                    print("Selected option to configure ALL servers\n")
                    for i in range(0,int(servertotal)):
                        serverid = i + 1
                        self.basic_dict = dmgr.mData.returnDict_basic(self,serverid)
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
                        conf_local.set("OPTIONS","game_starting_port",game_port)
                        conf_local.set("OPTIONS","voice_starting_port",voice_port)
                        conf_local.set("OPTIONS","github_branch",str(selected_branch))
                        conf_local.set("OPTIONS","debug_mode",str(debug_mode))
                        conf_local.set("OPTIONS","use_proxy",str(use_proxy))
                        conf_local.set("OPTIONS","svr_login",svr_login)
                        conf_local.set("OPTIONS","svr_password",svr_password)
                        conf_local.set("OPTIONS","use_console",str(use_console))
                        conf_local.set("OPTIONS","sdc_home_dir",self.basic_dict['sdc_home_dir'])
                        conf_local.set("OPTIONS","disable_bot",str(disable_bot))
                        with open(config_local, "w") as c:
                            conf_local.write(c)
                        c.close()
                        # #
                        # #   global values
                        # if not conf_global.has_section("OPTIONS"):
                        #     conf_global.add_section("OPTIONS")
                        # conf_global.set("OPTIONS","bot_version",self.dataDict['bot_version'])
                        # with open(config_global, "w") as d:
                        #     conf_global.write(d)
                        # d.close()
                        hon_api_updated = False
                        initialise().configureEnvironment(self,force_update,use_console)
                #tex.insert(END,f"Updated {self.service_name_bot} to version v{self.bot_version}.\n")
                tex.insert(END,("\nPORTS TO FORWARD (Game): "+', '.join(ports_to_forward_game)))
                tex.insert(END,("\nPORTS TO FORWARD (Voice): "+', '.join(ports_to_forward_voice))+'\n')
                tex.see(tk.END)
                return

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
            global tex
            app = tk.Tk()
            applet = ttk
            app.title(f"HoNfigurator v{self.dataDict['bot_version']} by @{self.dataDict['bot_author']}")
            #   importing icon
            honico = PhotoImage(file = os.path.abspath(application_path)+f"\\icons\\honico.png")
            app.iconphoto(False, honico) 
            honlogo = PhotoImage(file = os.path.abspath(application_path)+f"\\icons\\logo.png")
            config_startup = initialise.get_startupcfg(self)
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
            gui = tk.Frame(app,bg=maincolor,padx=10,pady=10)
            app.configure(bg=maincolor)
            gui.grid()

            tabgui = ttk.Notebook(gui)
            tabgui.grid(column=0,row=0)
            tab1 = ttk.Frame(tabgui)
            tab2 = ttk.Frame(tabgui)
            #tab3 = ttk.Frame(tabgui)
            tabgui.add(tab1,text="Server Setup")
            tabgui.add(tab2,text="Server Administration")
            #tabgui.add(tab3,text="Discord Integration")
            
            """
            creating tooltips
            """

            
            """
            simple server setup tab
            """
            #   title
            logolabel_tab1 = applet.Label(tab1,text=f"HoNfigurator",background=maincolor,foreground='white',image=honlogo)
            logolabel_tab1.grid(columnspan=5,column=0, row=0,sticky="n",pady=[10,0],padx=[40,0])
            #   server total    
            self.svr_total_var = tk.StringVar(app,self.dataDict['svr_total'])
            applet.Label(tab1, text="Total Servers:",background=maincolor,foreground='white').grid(column=1, row=5,sticky="e")
            self.tab1_servertd = applet.Combobox(tab1,foreground=textcolor,value=self.corecount(),textvariable=self.svr_total_var,width=5)
            labl_ttp = honfigurator.CreateToolTip(self.tab1_servertd, \
                    f"The total servers allowed by your CPU core count.")
            self.tab1_servertd.grid(column= 2 , row = 5,sticky="w",pady=4)
            self.svr_total_var.trace_add('write', self.svr_num_link)
            #  one or two cores
            self.core_assign = tk.StringVar(app,self.dataDict['core_assignment'])
            applet.Label(tab1, text="CPU cores assigned per server:",background=maincolor,foreground='white').grid(column=0, row=8,sticky="e",padx=[20,0])
            tab1_core_assign = applet.Combobox(tab1,foreground=textcolor,value=self.coreassign(),textvariable=self.core_assign,width=16)
            labl_ttp = honfigurator.CreateToolTip(tab1_core_assign, \
                    f"Multiple servers can be started on a single CPU core.\nThe recommended value is 1 core per server.\nIf you have reports of lag, try 2 cores per server\nIf you have a very strong CPU, try 2 servers per core.")
            tab1_core_assign.grid(column= 1, row = 8,sticky="w",pady=4,padx=[0,130])
            self.core_assign.trace_add('write', self.coreadjust)
            #   
            #   Simple Server data
            applet.Label(tab1, text="Hon Server Data",background=maincolor,foreground='white').grid(columnspan=1,column=1, row=1,sticky="w")
            #   hoster
            applet.Label(tab1, text="Server Name:",background=maincolor,foreground='white').grid(column=0,row=2,sticky="e")
            tab1_hosterd = applet.Entry(tab1,foreground=textcolor,width=16)
            labl_ttp = honfigurator.CreateToolTip(tab1_hosterd, \
                    f"The server name which will appear in HoN. Also the name which the Discord bots will be called by.\nCannot contain spaces.")
            tab1_hosterd.insert(0,self.dataDict['svr_hoster'])
            tab1_hosterd.grid(column= 1 , row = 2,sticky="w",pady=4,padx=[0,130])
            #   server name
            applet.Label(tab1, text="HoN Username:",background=maincolor,foreground='white').grid(column=0,row=3,sticky="e")
            tab1_user = applet.Entry(tab1,foreground=textcolor,width=16)
            labl_ttp = honfigurator.CreateToolTip(tab1_user, \
                    f"This must be a unique username per VM / Dedicated Host.\nUsing the same user on multiple server hosting infrastructures will cause the inability for players to download replays.")
            tab1_user.insert(0,self.dataDict['svr_login'])
            tab1_user.grid(column= 1 , row = 3,sticky="w",pady=4,padx=[0,130])
            #   server password
            applet.Label(tab1, text="HoN Password:",background=maincolor,foreground='white').grid(column=1,row=3,sticky="e")
            tab1_pass = applet.Entry(tab1,foreground=textcolor,width=16,show="*")
            tab1_pass.insert(0,self.dataDict['svr_password'])
            tab1_pass.grid(column= 2 , row = 3,sticky="w",pady=4)
            #   optional static IP
            applet.Label(tab1, text="Static IP (optional):",background=maincolor,foreground='white').grid(column=1,row=4,sticky="e")
            tab1_ip = applet.Entry(tab1,foreground=textcolor,width=16)
            labl_ttp = honfigurator.CreateToolTip(tab1_ip, \
                    f"An optional static IP. Otherwise, your IP will be set to {self.dataDict['svr_ip']}")
            if 'static_ip' in self.dataDict:
                tab1_ip.insert(0,self.dataDict['svr_ip'])
            tab1_ip.grid(column= 2 , row = 4,sticky="w",pady=4)
            #
            #   region
            # self.svr_loc = tk.StringVar(app,self.dataDict["svr_region"])
            # applet.Label(tab1, text="Location:",background=maincolor,foreground='white').grid(column=0, row=4,sticky="e")
            # tab1_regiond = applet.Combobox(tab1,foreground=textcolor,value=self.regions()[0],textvariable=self.svr_loc,width=16)
            # tab1_regiond.grid(column= 1 , row = 4,sticky="w",pady=4,padx=[0,130])
            # self.svr_loc.trace_add('write', self.reg_def_link)
            #   regionId
            self.svr_reg_code = tk.StringVar(app,self.dataDict["svr_region_short"])
            applet.Label(tab1, text="Region:",background=maincolor,foreground='white').grid(column=0, row=4,sticky="e")
            tab1_regionsd = applet.Combobox(tab1,foreground=textcolor,value=self.regions(),textvariable=self.svr_reg_code,width=6)
            labl_ttp = honfigurator.CreateToolTip(tab1_regionsd, \
                    f"These are the only valid region codes. Any others will not show up in-game.")
            tab1_regionsd.grid(column= 1 , row = 4,sticky="w",pady=4)
            #self.svr_reg_code.trace_add('write', self.reg_def_link)
            #   server id
            self.svr_id_var = tk.StringVar(app,self.dataDict['svr_id'])
            applet.Label(tab1, text="Server ID:",background=maincolor,foreground='white').grid(column=0, row=5,sticky="e")
            self.tab1_serveridd = applet.Combobox(tab1,foreground=textcolor,value=self.corecount(),textvariable=self.svr_id_var,width=5)
            self.tab1_serveridd.grid(column= 1 , row = 5,sticky="w",pady=4,padx=[0,130])
            self.svr_id_var.trace_add('write', self.svr_num_link)
            
            #   HoN Directory
            applet.Label(tab1, text="HoN Directory:",background=maincolor,foreground='white').grid(column=0, row=12,sticky="e",padx=[20,0])
            tab1_hondird = applet.Entry(tab1,foreground=textcolor,width=70)
            tab1_hondird.insert(0,self.dataDict['hon_directory'])
            tab1_hondird.grid(columnspan=3,column= 1, row = 12,sticky="w",pady=4)
            #   HoN Home
            applet.Label(tab1, text="HoN Storage Folder\n(replays, long term storage):",background=maincolor,foreground='white').grid(column=0, row=13,sticky="e",padx=[20,0])
            tab1_honreplay = applet.Entry(tab1,foreground=textcolor,width=70)
            labl_ttp = honfigurator.CreateToolTip(tab1_honreplay, \
                    f"Use to store HoN replays.")
            tab1_honreplay.insert(0,self.dataDict['hon_manager_dir'])
            tab1_honreplay.grid(columnspan=3,column= 1, row = 13,sticky="w",pady=4)
            # HoN master server
            self.master_server = tk.StringVar(app,self.dataDict['master_server'])
            applet.Label(tab1, text="HoN Master Server:",background=maincolor,foreground='white').grid(column=0, row=6,sticky="e",padx=[20,0])
            tab1_masterserver = applet.Combobox(tab1,foreground=textcolor,value=self.masterserver(),textvariable=self.master_server,width=16)
            tab1_masterserver.grid(column= 1, row = 6,sticky="w",pady=4,padx=[0,130])
            
            #  one or two cores
            self.priority = tk.StringVar(app,self.dataDict['process_priority'])
            applet.Label(tab1, text="In-game CPU process priority:",background=maincolor,foreground='white').grid(column=0, row=7,sticky="e",padx=[20,0])
            tab1_priority = applet.Combobox(tab1,foreground=textcolor,value=self.priorityassign(),textvariable=self.priority,width=16)
            labl_ttp = honfigurator.CreateToolTip(tab1_priority, \
                    f"Default option: Realtime. There is no need to change this unless you are being experimental.")
            tab1_priority.grid(column= 1, row = 7,sticky="w",pady=4,padx=[0,130])
            #  increment ports
            self.increment_port = tk.StringVar(app,self.dataDict['incr_port_by'])
            applet.Label(tab1, text="Increment ports by:",background=maincolor,foreground='white').grid(column=1, row=6,sticky="e",padx=[20,0])
            tab1_increment_port = applet.Combobox(tab1,foreground=textcolor,value=self.incrementport(),textvariable=self.increment_port,width=5)
            tab1_increment_port.grid(column= 2, row = 6,sticky="w",pady=4)
            #
            #   use proxy
            applet.Label(tab1, text="Use proxy (anti-DDOS):",background=maincolor,foreground='white').grid(column=1, row=10,sticky="e",padx=[20,0])
            self.useproxy = tk.BooleanVar(app)
            if self.dataDict['use_proxy'] == 'True':
                self.useproxy.set(True)
            tab1_useproxy_btn = applet.Checkbutton(tab1,variable=self.useproxy)
            labl_ttp = honfigurator.CreateToolTip(tab1_useproxy_btn, \
                    f"Enable this option to use the HoN Proxy service.\nThis creates a layer of protection by ensuring all game server data is dealt with by the proxy first, eliminating malicious DoS attempts.\nIf using the proxy. Observe carefully the HoNfigurator output, and only port forward the Proxy ports on your router.")
            tab1_useproxy_btn.grid(column= 2, row = 10,sticky="w",pady=4)
            #
            #   force proxy restart
            applet.Label(tab1, text="Restart Proxy (in next configure)",background=maincolor,foreground='white').grid(column=1, row=11,sticky="e",padx=[20,0])
            self.restart_proxy = tk.BooleanVar(app)
            tab1_restart_proxy = applet.Checkbutton(tab1,variable=self.restart_proxy)
            labl_ttp = honfigurator.CreateToolTip(tab1_restart_proxy, \
                    f"Enable this option to ensure the proxy is restarted on the next configure. This may disrupt games in progress.")
            tab1_restart_proxy.grid(column= 2, row = 11,sticky="w",pady=4)
            # self.useproxy.trace_add('write',self.change_to_proxy2)
            #  starting gameport
            applet.Label(tab1, text="Starting game port:",background=maincolor,foreground='white').grid(column=1,row=7,sticky="e")
            tab1_game_port = applet.Entry(tab1,foreground=textcolor,width=5)
            labl_ttp = honfigurator.CreateToolTip(tab1_game_port, \
                    f"The starting voice port defaults to 10000.\nEach server is started on the starting voice port + the nth server\nif using the proxy, the public ports will be an additional 10000 ontop of this.\nHoNfigurator will output the required ports to forward after configuring a server.")
            tab1_game_port.insert(0,self.dataDict['game_starting_port'])
            # self.tab1_game_port.insert(0,self.change_to_proxy())
            tab1_game_port.grid(column=2,row = 7,sticky="w",pady=4)
            #  starting gameport
            applet.Label(tab1, text="Starting voice port:",background=maincolor,foreground='white').grid(column=1,row=8,sticky="e")
            tab1_voice_port = applet.Entry(tab1,foreground=textcolor,width=5)
            labl_ttp = honfigurator.CreateToolTip(tab1_voice_port, \
                    f"The starting game port defaults to 10000.\nEach server is started on the starting game port + the nth server\nif using the proxy, the public ports will be an additional 10000 ontop of this.\nHoNfigurator will output the required ports to forward after configuring a server.")
            tab1_voice_port.insert(0,self.dataDict['voice_starting_port'])
            tab1_voice_port.grid(column=2,row = 8,sticky="w",pady=4)
            #   force update
            applet.Label(tab1, text="Force Update:",background=maincolor,foreground='white').grid(column=0, row=10,sticky="e",padx=[20,0])
            self.forceupdate = tk.BooleanVar(app)
            tab1_forceupdate_btn = applet.Checkbutton(tab1,variable=self.forceupdate)
            tab1_forceupdate_btn.grid(column= 1, row = 10,sticky="w")
            #   console windows, for launching servers locally (not as windows services)
            applet.Label(tab1, text="Launch as Console (BETA):",background=maincolor,foreground='white').grid(column=0, row=11,sticky="e",padx=[20,0])
            self.console = tk.BooleanVar(app)
            if self.dataDict['use_console'] == 'True':
                self.console.set(True)
            else:
                self.console.set(False)
            tab1_console_btn = applet.Checkbutton(tab1,variable=self.console)
            labl_ttp = honfigurator.CreateToolTip(tab1_console_btn, \
                    f"Use this option to run servers in console app mode. This is more CPU intensive, and you must remain logged in.")
            tab1_console_btn.grid(column= 1, row = 11,sticky="w",pady=2)
            # self.useproxy.trace_add('write', self.change_to_proxy(NULL,NULL,NULL))
            #
            
            #    Setup Info
            applet.Label(tab1, text="Discord Data",background=maincolor,foreground='white').grid(columnspan=1,column=4, row=1,sticky="w")
            #   discord admin
            applet.Label(tab1, text="Bot Owner (discord ID):",background=maincolor,foreground='white').grid(column=3, row=2,sticky="e",padx=[20,0])
            tab1_discordadmin = applet.Entry(tab1,foreground=textcolor,width=45)
            labl_ttp = honfigurator.CreateToolTip(tab1_discordadmin, \
                    f"YOUR Discord user ID.\nObtainable by enabling developer options in Discord advanced settings, then right clicking your name in the members list on any Discord guild, and selecting \"Copy ID\".")
            tab1_discordadmin.insert(0,self.dataDict['discord_admin'])
            tab1_discordadmin.grid(column= 4, row = 2,sticky="w",pady=4)
            #   token
            applet.Label(tab1, text="Bot Token (SECRET):",background=maincolor,foreground='white').grid(column=3, row=3,sticky="e",padx=[20,0])
            tab1_bottokd = applet.Entry(tab1,foreground=textcolor,width=45)
            labl_ttp = honfigurator.CreateToolTip(tab1_bottokd, \
                    f"The secret token which your bot uses to authenticate to Discord. This is provide when your bot is made\nContact @FrankTheGodDamnMotherFuckenTank#8426\nOR, create your own Discord bot.\nPermissions integer: 533650040896.\nRequires message content intent.")
            tab1_bottokd.insert(0,self.dataDict['token'])
            tab1_bottokd.grid(column= 4, row = 3,sticky="w",pady=4,padx=[0,20])
            #  allow bot matches 
            applet.Label(tab1, text="Allow bot matches:",background=maincolor,foreground='white').grid(column=3, row=4,sticky="e",padx=[20,0])
            self.botmatches = tk.BooleanVar(app)
            tab1_botmatches_btn = applet.Checkbutton(tab1,variable=self.botmatches)
            labl_ttp = honfigurator.CreateToolTip(tab1_botmatches_btn, \
                    f"Bot matches are disabled by default. Check this box to enable bot matches to be played.")
            tab1_botmatches_btn.grid(column= 4, row = 4,sticky="w",pady=4)
            #  Debug mode 
            applet.Label(tab1, text="Debug mode:",background=maincolor,foreground='white').grid(column=3, row=5,sticky="e",padx=[20,0])
            self.debugmode = tk.BooleanVar(app)
            if self.dataDict['debug_mode'] == 'True':
                self.debugmode.set(True)
            tab1_debugmode_btn = applet.Checkbutton(tab1,variable=self.debugmode)
            labl_ttp = honfigurator.CreateToolTip(tab1_debugmode_btn, \
                    f"Enhanced logging, specifically in eventlog sent to Discord DM by bot.")
            tab1_debugmode_btn.grid(column= 4, row = 5,sticky="w",pady=4)
            #  Run without bots 
            applet.Label(tab1, text="Run without bots:",background=maincolor,foreground='white').grid(column=3, row=6,sticky="e",padx=[20,0])
            self.disablebot = tk.BooleanVar(app)
            if self.dataDict['disable_bot'] == 'True':
                self.disablebot.set(True)
            tab1_disablebot_btn = applet.Checkbutton(tab1,variable=self.disablebot)
            labl_ttp = honfigurator.CreateToolTip(tab1_disablebot_btn, \
                    f"An experimental feature, allowing you to run the app without a reliance on Discord bots.")
            tab1_disablebot_btn.grid(column= 4, row = 6,sticky="w",pady=4)
            # #   auto update
            # applet.Label(tab1, text="Auto update HoNfigurator:",background=maincolor,foreground='white').grid(column=3, row=5,sticky="e",padx=[20,0])
            # self.autoupdate = tk.BooleanVar(app)
            # if self.dataDict['auto_update'] == 'True':
            #     self.autoupdate.set(True)
            # tab1_autoupdate_btn = applet.Checkbutton(tab1,variable=self.autoupdate)
            # tab1_autoupdate_btn.grid(column= 4, row = 5,sticky="w",pady=4)
            #   branch select
            self.git_branch = tk.StringVar(app,self.git_current_branch())
            applet.Label(tab1, text="Currently selected branch:",background=maincolor,foreground='white').grid(column=3, row=7,sticky="e",padx=[20,0])
            tab1_git_branch = applet.Combobox(tab1,foreground=textcolor,value=self.git_all_branches(),textvariable=self.git_branch)
            tab1_git_branch.grid(column= 4, row = 7,sticky="w",pady=4)
            self.git_branch.trace_add('write', self.update_repository)

            #   bot version
            applet.Label(tab1, text="Bot Version:",background=maincolor,foreground='white').grid(column=3, row=8,sticky="e",padx=[20,0])
            applet.Label(tab1,text=f"{self.dataDict['bot_version']}-{self.dataDict['environment']}",background=maincolor,foreground='white').grid(column= 4, row = 8,sticky="w",pady=4)
            print(self.forceupdate.get())

            # tex = tk.Text(tab1,foreground=textcolor,width=70,height=10,background=textbox)
            # tex.grid(columnspan=6,column=0,row=15,sticky="n")
            #   button
            tab1_singlebutton = applet.Button(tab1, text="Configure Single Server",command=lambda: self.sendData("single",tab1_hosterd.get(),tab1_regionsd.get(),self.tab1_serveridd.get(),self.tab1_servertd.get(),tab1_hondird.get(),tab1_honreplay.get(),tab1_user.get(),tab1_pass.get(),tab1_ip.get(),tab1_bottokd.get(),tab1_discordadmin.get(),tab1_masterserver.get(),self.forceupdate.get(),self.disablebot.get(),self.console.get(),self.useproxy.get(),self.restart_proxy.get(),tab1_game_port.get(),tab1_voice_port.get(),self.core_assign.get(),self.priority.get(),self.botmatches.get(),self.debugmode.get(),self.git_branch.get(),self.increment_port.get()))
            tab1_singlebutton.grid(columnspan=5,column=0, row=14,stick='n',padx=[0,400],pady=[20,10])
            labl_ttp = honfigurator.CreateToolTip(tab1_singlebutton, \
                    f"Configure the currently selected server ID only.")
            tab1_allbutton = applet.Button(tab1, text="Configure All Servers",command=lambda: self.sendData("all",tab1_hosterd.get(),tab1_regionsd.get(),self.tab1_serveridd.get(),self.tab1_servertd.get(),tab1_hondird.get(),tab1_honreplay.get(),tab1_user.get(),tab1_pass.get(),tab1_ip.get(),tab1_bottokd.get(),tab1_discordadmin.get(),tab1_masterserver.get(),self.forceupdate.get(),self.disablebot.get(),self.console.get(),self.useproxy.get(),self.restart_proxy.get(),tab1_game_port.get(),tab1_voice_port.get(),self.core_assign.get(),self.priority.get(),self.botmatches.get(),self.debugmode.get(),self.git_branch.get(),self.increment_port.get()))
            tab1_allbutton.grid(columnspan=5,column=0, row=14,stick='n',padx=[0,110],pady=[20,10])
            labl_ttp = honfigurator.CreateToolTip(tab1_allbutton, \
                    f"Configure ALL total servers.")
            tab1_updatebutton = applet.Button(tab1, text="Update HoNfigurator",command=lambda: self.update_repository(NULL,NULL,NULL))
            tab1_updatebutton.grid(columnspan=5,column=0, row=14,stick='n',padx=[180,0],pady=[20,10])
            labl_ttp = honfigurator.CreateToolTip(tab1_updatebutton, \
                    f"Update this application. Pulls latest commits from GitHub.")
            tab1_updatehon = applet.Button(tab1, text="Force Update HoN",command=lambda: self.forceupdate_hon(tab1_hondird.get(),tab1_masterserver.get()))
            tab1_updatehon.grid(columnspan=5,column=0, row=14,stick='n',padx=[450,0],pady=[20,10])
            labl_ttp = honfigurator.CreateToolTip(tab1_updatehon, \
                    f"Used when there is a HoN server udpate available. All servers must first be stopped for this to work.")
            app.rowconfigure(14,weight=1)
            app.rowconfigure(15,weight=1)
            app.columnconfigure(0,weight=1)
            """
            
            This is the advanced server setup tab
            ui
            """
            # logolabel_tab2 = applet.Label(tab2,text="HoNfigurator",background=maincolor,foreground='white',image=honlogo)
            # logolabel_tab2.grid(columnspan=2,column=, row=0,sticky="n",pady=[10,0])
            
            """
            
            This is the bot command center tab
            
            """
            # status = Entry(app,background=maincolor,foreground='white',width="200")
            # status.insert(0,ver)
            # status.grid(row=21,column=0,sticky='w')
            class TextScrollCombo(ttk.Frame):

                def __init__(self, *args, **kwargs):
                    global tex
                    super().__init__(*args, **kwargs)

                # # ensure a consistent GUI size
                #     self.grid_propagate(False)
                # # implement stretchability
                #     self.grid_rowconfigure(0, weight=1)
                #     self.grid_columnconfigure(0, weight=1)

                # create a Text widget
                    tex = tk.Text(app,foreground=textcolor,background=textbox,height=10)
                    tex.grid(row=16, column=0, sticky="nsew", padx=2, pady=2)
                    tex.tag_config('warning', background="yellow", foreground="red")
                    tex.tag_config('interest', background="green")
                # create a Scrollbar and associate it with txt
                    scrollb = ttk.Scrollbar(app, command=tex.yview)
                    scrollb.grid(row=16, column=1, sticky='nsew')
                    tex['yscrollcommand'] = scrollb.set

            ButtonString = ['View Log', 'Start', 'Stop', 'Clean', 'Uninstall']
            LablString = ['hon_server_','test','space']
            LablStringTop = ['Manager','test']

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
                    except Exception as e:
                        print(e)
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
                    bot_running=initialise.check_proc(f"{service_name}.exe")
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
                #app.after(15000,viewButton.refresh())
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
                        bot_running=initialise.check_proc(f"{service_name}.exe")
                        if bot_running:
                            # if deployed_status['use_console'] == 'False':
                                # if initialise.stop_service(self,service_name,True):
                                #     tex.insert(END,f"{service_name} stopped successfully.\n")
                                # else:
                                #     tex.insert(END,f"{service_name} failed to stop.\n")
                            #else:
                                initialise.stop_bot(self,f"{service_name}.exe")
                                initialise.stop_bot(self,f"KONGOR_ARENA_{i}.exe")
                                initialise.stop_bot(self,f"HON_SERVER_{i}.exe")
                            #viewButton.refresh()
                    else:
                        print("[ABORT] players are connected. Scheduling shutdown instead..")
                        initialise.schedule_shutdown(deployed_status)
                viewButton.refresh()

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
            class viewButton():
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
                        viewButton.ViewLog(self)
                    elif btn == "Stop":
                        viewButton.Stop(self)
                    elif btn == "Start":
                        viewButton.Start(self)
                    elif btn == "Clean":
                        viewButton.Clean(self)
                    elif btn == "Uninstall":
                        viewButton.Uninstall(self,id)
                def clear_frame():
                    list = tab2.grid_slaves()
                    for l in list:
                        l.destroy()
                def refresh(*args):
                    global mod_by
                    global refresh_next
                    refresh_next=False
                    if (tabgui.index("current")) == 0:
                        ver=honfigurator.return_currentver(self)
                        ver=ver[1]
                        status = Entry(app,background=maincolor,foreground='white',width="200")
                        status.insert(0,ver)
                        status.grid(row=21,column=0,sticky='w')
                    if (tabgui.index("current")) == 1:
                        if len(args) >= 1 and type(args[0]) is int:
                            mod_by = args[0]
                        viewButton.clear_frame()
                        viewButton.load_server_mgr(self)
                        # else:
                        #     viewButton.clear_frame()
                        #     viewButton.load_server_mgr(self)
                        # try:
                        #     status = Entry(app,background=maincolor,foreground='white',width="200")
                        #     status.insert(0,f"Viewing hon_server_{deployed_status['svr_id']}: {latest_file}")
                        #     status.grid(row=21,column=0,sticky='w')
                        # except:pass
                def load_log(self,*args):
                    global bot_tab
                    if (tabgui.index("current")) == 1:
                        if bot_tab !=tabgui2.index("current"):
                            viewButton.ViewLog(self)
                        bot_tab=tabgui2.index("current")
                        #viewButton.ViewLog(self)

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
                    if (tabgui2.index("current")) == 0:
                        if pcount <=0:
                            log_File = f"Slave*.log"
                        else:
                            log_File = f"Slave*{id}*.clog"
                        list_of_files = glob.glob(logs_dir + log_File) # * means all if need specific format then *.csv
                        latest_file = max(list_of_files, key=os.path.getctime)
                        info=["New session cookie "," Connected","[ALL]","lag","spike","ddos"]
                        warnings=["Skipped","Session cookie request failed!","No session cookie returned!","Timeout","Disconnected"]
                        with open(latest_file,'r',encoding='utf-16-le') as file:
                            for line in file:
                                tem=line.lower()
                                if any(x.lower() in tem for x in warnings):
                                    tex.insert(tk.END,line,'warning')
                                elif any(x.lower() in tem for x in info):
                                    tex.insert(tk.END,line,'interest')
                                else:
                                    tex.insert(tk.END,line)
                    if (tabgui2.index("current")) == 1:
                        if pcount > 0:
                            logs_dir = f"{deployed_status['hon_logs_dir']}\\"
                            log_File = "M*.log"
                        else:
                            tex.insert(END,'No match in progress.')
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
                    if (tabgui2.index("current")) == 2:
                        logs_dir = f"{deployed_status['sdc_home_dir']}\\"
                        log_File = f"adminbot{id}.log"
                        list_of_files = glob.glob(logs_dir + log_File) # * means all if need specific format then *.csv
                        latest_file = max(list_of_files, key=os.path.getctime)
                        with open(latest_file,'r') as file:
                            for line in file:
                                tem=line.lower()
                                tex.insert(tk.END,line)
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
                    status = Entry(app,background=maincolor,foreground='white',width="200")
                    status.insert(0,f"Viewing hon_server_{id}: {latest_file}")
                    status.grid(columnspan=total_columns,row=21,column=0,sticky='w')
                    print(latest_file)                   
                    tex.see(tk.END)

                def Start(self):
                    pcount = initialise.playerCountX(self,id)
                    deployed_status = dmgr.mData.returnDict_deployed(self,id)
                    if pcount == -3:
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
                        viewButton.refresh()
                def StartProxy(self):
                    if svrcmd.honCMD.check_proc("HoN Proxy Manager") == False:
                        if self.dataDict['use_proxy']=='True':
                            # if self.dataDict['use_console']=='False':
                                if initialise.start_service(self,"HoN Proxy Manager",True):
                                    tex.insert(END,"Proxy started.")
                                    tex.see(tk.END)
                                    viewButton.refresh()
                                else:
                                    tex.insert(END,"Failed to start the proxy service.")
                                    tex.see(tk.END)
                            # else:
                            #     os.chdir(self.dataDict['hon_directory'])
                            #     os.startfile(f"proxymanager.exe")
                            #     os.chdir(application_path)
                            #     app.after(5000,viewButton.load_server_mgr(self))
                        else:
                            tex.insert(END,"Proxy not enabled. Please configure some servers using the proxy.")
                            tex.see(tk.END)
                def StartManager(self):
                    if svrcmd.honCMD.check_proc("KONGOR ARENA MANAGER.exe") == False:
                        if initialise.start_service(self,"HoN Server Manager",True):
                            tex.insert(END,"HoN Server Manager started.")
                            tex.see(tk.END)
                            viewButton.refresh()
                        else:
                            tex.insert(END,"Failed to start the server manager service. This is required for replays.")
                            tex.see(tk.END)
                def Stop(self):
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
                        bot_running=initialise.check_proc(f"{service_name}.exe")
                        if bot_running:
                                # if deployed_status['use_console'] == 'False':
                                    # if initialise.stop_service(self,service_name,True):
                                    #     tex.insert(END,f"{service_name} stopped successfully.\n")
                                    # else:
                                    #     tex.insert(END,f"{service_name} failed to stop.\n")
                                #else:
                                    initialise.stop_bot(self,f"{service_name}.exe")
                                    initialise.stop_bot(self,f"KONGOR_ARENA_{id}.exe")
                                    initialise.stop_bot(self,f"HON_SERVER_{id}.exe")
                                #viewButton.refresh()
                    else:
                        print("[ABORT] players are connected. Scheduling shutdown instead..")
                        initialise.schedule_shutdown(deployed_status)
                    viewButton.refresh()
                def Clean(self):
                    paths = [f"{deployed_status['hon_logs_dir']}",f"{deployed_status['hon_logs_dir']}\\diagnostics",f"{deployed_status['hon_home_dir']}\\HoNProxyManager"]
                    now = time.time()
                    count=0
                    for path in paths:
                        for f in os.listdir(path):
                            f = os.path.join(path, f)
                            if os.stat(f).st_mtime < now - 7 * 86400:
                                if os.path.isfile(f):
                                    os.remove(os.path.join(path, f))
                                    count+=1
                                    print("removed "+f)
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
                def Uninstall(self,x):
                    pcount = initialise.playerCountX(self,id)
                    if pcount <= 0:
                        service_state = initialise.get_service(service_name)
                        if service_state != False and service_state['status'] != 'stopped':
                            if initialise.stop_service(self,service_name,True):
                                tex.insert(END,f"{service_name} stopped successfully.\n")
                                viewButton.load_server_mgr(self)
                            else:
                                tex.insert(END,f"{service_name} failed to stop.\n")
                        service_state = initialise.get_service(service_name)
                        if service_state == False or service_state['status'] == 'stopped':
                            try:
                                #shutil.copy(f"{deployed_status['sdc_home_dir']}\\cogs\\total_games_played")
                                rem = shutil.rmtree(deployed_status['hon_home_dir'],onerror=honfigurator.onerror)
                                tex.insert(END,f"removed files: {deployed_status['hon_home_dir']}")
                            except Exception as e:
                                print(e)
                            try:
                                remove_service = subprocess.run(['sc.exe','delete',f'adminbot{x}'])
                            except Exception as e:
                                print(e)
                    else:
                        print("[ABORT] players are connected. You must stop the service before uninstalling..")
                        tex.insert(END,"[ABORT] players are connected. You must stop the service before uninstalling..\n")
                        initialise.schedule_shutdown(deployed_status)
            #app.attributes("-topmost",True)
                def load_server_mgr(self,*args):
                    global total_columns
                    global mod_by
                    global bot_tab
                    global logolabel_tab2
                    global tab2_cleanall
                    global tab2_refresh
                    global tab2_stopall
                    global tab2_startall
                    global tabgui2
                    global stretch

                    app.lift()
                    i=2
                    c=0
                    c_len = len(ButtonString)+len(LablString)

                    svc_or_con="svc"
                    cookie=True
                    # create a grid of 2x6
                    for t in range(20):
                        tab2.rowconfigure(t, weight=1,pad=0)
                    for o in range(100):
                        tab2.columnconfigure(o, weight=1,pad=0)
                    for x in range(0,(int(self.dataDict['svr_total']))):
                        x+=1
                        i+=1
                        service_name = f"adminbot{x}"
                        deployed_status = dmgr.mData.returnDict_deployed(self,x)
                        dir_name = f"{deployed_status['hon_logs_dir']}\\"
                        file = "Slave*.log"
                        log = False
                        try:
                            list_of_files = glob.glob(dir_name + file) # * means all if need specific format then *.csv
                            log = max(list_of_files, key=os.path.getctime)
                        except Exception as e:
                            print(e)
                        if log != False:
                            cookie = svrcmd.honCMD.check_cookie(deployed_status,log,"honfigurator_log_check")
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
                        LablString[0]=f"hon_server_{x}"
                        for index1, labl_name in enumerate(LablString):
                            if cookie:
                                if pcount < 0:
                                    colour = 'OrangeRed4'
                                    LablString[1]="Offline"
                                elif pcount == 0:
                                    colour = 'MediumPurple3'
                                    LablString[1]="Available"
                                elif pcount >0:
                                    colour = 'SpringGreen4'
                                    LablString[1]=f"In-game ({pcount})"
                                if pcount >=0:
                                    if schd_restart:
                                        colour='indian red'
                                        LablString[1]='schd-restart'
                                    if schd_shutdown:
                                        LablString[1]='schd-shutdown'
                            else:
                                if pcount < 0:
                                    colour = 'OrangeRed4'
                                    LablString[1]="Offline"
                                elif pcount == 0:
                                    colour = 'MediumPurple3'
                                    LablString[1]="connect error"
                                elif pcount >0:
                                    colour = 'SpringGreen4'
                                    LablString[1]=f"In-game ({pcount})"
                            if service_state is not None and deployed_status['use_console'] == 'False':
                                if service_state == False or service_state['status'] == 'stopped':
                                    colour = 'OrangeRed4'
                                    svc_or_con="svc"
                                    #LablString[1]=f"svc-Stopped"
                            elif deployed_status['use_console'] == 'True':
                                #colour = 'OrangeRed4'
                                svc_or_con="con"
                                #LablString[1]=f"con-Stopped"
                            c_pos1 = index1 + c
                            if index1==0:
                                labl = Label(tab2,width=12,text=f"{labl_name}", background=colour, foreground='white')
                                try:
                                    labl_ttp = honfigurator.CreateToolTip(labl, \
                                    f"version {deployed_status['bot_version']}")
                                except: pass
                            elif index1==1:
                                labl = Label(tab2,width=14,text=f"{svc_or_con}-{labl_name}", background=colour, foreground='white')
                                if 'available' in labl_name.lower():
                                    labl_ttp = honfigurator.CreateToolTip(labl, \
                                        f"Server is available and connected to the master server.")
                                elif 'cookie' in labl_name.lower():
                                    labl_ttp = honfigurator.CreateToolTip(labl, \
                                        f"Potential outage.\nServer does not have a session cookie. Not connected to masterserver.\nRun in console mode, or view server logs to debug further.")
                                if pcount > 0:
                                    logs_dir = f"{deployed_status['hon_logs_dir']}\\"
                                    log_File = f"Slave*{x}*.clog"
                                    list_of_files = glob.glob(logs_dir + log_File) # * means all if need specific format then *.csv
                                    latest_file = max(list_of_files, key=os.path.getctime)
                                    match_status = svrcmd.honCMD.simple_match_data(latest_file,"match")
                                    labl_ttp = honfigurator.CreateToolTip(labl, \
                                        f"Game in progress,\n{pcount} players connected\nMatch time: {match_status['match_time']}\nSkipped server frames: {match_status['skipped_frames']}\nLargest skipped frame: {match_status['largest_skipped_frame']}")
                            labl.grid(row=i, column=c_pos1)
                            for index2, btn_name in enumerate(ButtonString):
                                index2 +=len(LablString)
                                c_pos2 = index2 + c
                                btn = Button(tab2,text=btn_name, command=partial(viewButton,btn_name,x,pcount))
                                if btn_name == "View Log":
                                    btn_ttp = honfigurator.CreateToolTip(btn, \
                                        "View the server logs")
                                elif btn_name == "Start":
                                    btn_ttp = honfigurator.CreateToolTip(btn, \
                                        "Start the server with the current configuration.")
                                elif btn_name == "Stop":
                                    btn_ttp = honfigurator.CreateToolTip(btn, \
                                        "Schedule a shutdown of this server. Does NOT disconnect current games.")
                                elif btn_name == "Clean":
                                    btn_ttp = honfigurator.CreateToolTip(btn, \
                                        "Remove unnecessary files (7 days or older), such as old log files.")
                                elif btn_name == "Uninstall":
                                    btn_ttp = honfigurator.CreateToolTip(btn, \
                                        "Remove this server and bot, also removes folders and files.")
                                btn.grid(row=i, column=c_pos2)
                    column_rows=(tab2.grid_size())
                    total_columns=column_rows[0]
                    total_rows=column_rows[1]
                    print(column_rows)
                    #Proxy and Manager
                    if svrcmd.honCMD.check_proc("proxymanager.exe"):
                        labl = Label(tab2,width=25,text=f"Proxy Manager - UP", background="green", foreground='white')
                    else:
                        labl = Label(tab2,width=25,text=f"Proxy Manager - Down", background="red", foreground='white')
                        btn = Button(tab2, text="Start",command=lambda: viewButton.StartProxy(self))
                        btn.grid(columnspan=total_columns,column=0, row=1,sticky='n',padx=[430,0])
                    labl.grid(row=1, column=0,columnspan=total_columns,padx=[200,0],sticky='n',pady=[2,4])
                    if svrcmd.honCMD.check_proc("KONGOR ARENA MANAGER.exe"):
                        labl = Label(tab2,width=25,text=f"Server Manager - UP", background="green", foreground='white')
                    else:
                        labl = Label(tab2,width=25,text=f"Server Manager - Down", background="red", foreground='white')
                        btn = Button(tab2, text="Start",command=lambda: viewButton.StartManager(self))
                        btn.grid(columnspan=total_columns,column=0, row=1,sticky='n',padx=[0,430])
                    labl.grid(row=1, column=0,columnspan=total_columns,padx=[0,200],sticky='n',pady=[2,4])

                    stretch_lbl = Label(tab2,width=15,text="servers per row",background=maincolor,foreground='white')
                    stretch_lbl.grid(row=1, column=0,columnspan=total_columns,padx=[5,0],sticky='w',pady=[2,4])
                    stretch = Entry(tab2,width=5)
                    stretch.insert(0,mod_by-3)
                    stretch.grid(row=1, column=0,columnspan=total_columns,padx=[120,0],sticky='w',pady=[2,4])
                    
                    tabgui2 = ttk.Notebook(tab2)
                    tab11 = ttk.Frame(tabgui2)
                    tab22 = ttk.Frame(tabgui2)
                    tab23 = ttk.Frame(tabgui2)
                    tab24 = ttk.Frame(tabgui2)
                    tabgui2.add(tab11,text="Server Log")
                    tabgui2.add(tab22,text="Match Log")
                    tabgui2.add(tab23,text="Bot Log")
                    tabgui2.add(tab24,text="Proxy Log")
                    tabgui2.grid(column=0,row=total_rows+2,sticky='ew',columnspan=total_columns)
                    tabgui2.select(bot_tab)
                    tabgui2.bind('<<NotebookTabChanged>>',viewButton.load_log)

                    #tab2.grid_rowconfigure(1,weight=1)
                    logolabel_tab2 = applet.Label(tab2,text="HoNfigurator",background=maincolor,foreground='white',image=honlogo)
                    logolabel_tab2.grid(columnspan=total_columns,column=0, row=0,pady=[10,0],sticky='n')
                    tab2_cleanall = applet.Button(tab2, text="Clean All",command=lambda: clean_all())
                    tab2_cleanall.grid(columnspan=total_columns,column=0, row=mod_by+1,sticky='n',padx=[200,0],pady=[20,10])
                    tab2_cleanall_ttp = honfigurator.CreateToolTip(tab2_cleanall, \
                                    f"Remove ALL unnecessary files (7 days or older), such as old log files.")
                    # tab2_refresh = applet.Button(tab2, text="Refresh",command=lambda: viewButton.refresh(int(stretch.get())+3))
                    # tab2_refresh.grid(columnspan=total_columns,column=0, row=mod_by+1,sticky='n',padx=[100,0],pady=[20,10])
                    # tab2_refresh_ttp = honfigurator.CreateToolTip(tab2_refresh, \
                    #                 f"Refresh this page, reloads server status and shows the most recent data.")
                    tab2_stopall = applet.Button(tab2, text="Stop All",command=lambda: stop_all())
                    tab2_stopall.grid(columnspan=total_columns,column=0, row=mod_by+1,sticky='n',padx=[0,0],pady=[20,10])
                    tab2_refresh_ttp = honfigurator.CreateToolTip(tab2_stopall, \
                                    f"Schedule a shut down of all servers. Does NOT disconnect games in progress.")
                    tab2_startall = applet.Button(tab2, text="Start All",command=lambda: start_all())
                    tab2_startall.grid(columnspan=total_columns,column=0, row=mod_by+1,sticky='n',padx=[0,200],pady=[20,10])
                    tab2_startall_ttp = honfigurator.CreateToolTip(tab2_startall, \
                                    f"Start all stopped servers with their current configuration.")
                def Tools():
                    pass
            def auto_refresher():
                global refresh_next
                if refresh_next==True:
                    if (tabgui.index("current")) == 1:
                        viewButton.refresh(int(stretch.get())+3)
                refresh_next=True
                app.after(10000,auto_refresher)
            # create a Scrollbar and associate it with txt
            combo = TextScrollCombo(app)
            combo.config(width=600, height=600)
            self.update_repository(NULL,NULL,NULL)
            tabgui.bind('<<NotebookTabChanged>>',viewButton.refresh)
            #tabgui2.bind('<<NotebookTabChanged>>',viewButton.load_log)

            global refresh_next
            refresh_next = True
            auto_refresher()
            app.mainloop()
    test = honfigurator()
    test.creategui()
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 5)
