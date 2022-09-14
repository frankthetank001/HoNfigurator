from asyncio.subprocess import DEVNULL
import tkinter as tk
from tkinter import *
from tkinter import getboolean, ttk
import configparser
import psutil
import os
import subprocess as sp
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
import sys
import win32com.client
import datetime
from pygit2 import Repository
import git
from python_hosts import Hosts, HostsEntry
from functools import partial
# determine if application is a script file or frozen exe

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
        def __init__(self):
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
            self.svr_region = self.dataDict['svr_region']
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
            if exists(deployed_config):
                config = configparser.ConfigParser()
                config.read(deployed_config)
                self.ver_existing = config['OPTIONS']['bot_version']
                try:
                    self.ver_existing = float(self.ver_existing)
                except: pass
            else:
                self.ver_existing = 0
            # if exists(f"{self.sdc_home_dir}\\config\\local_config.ini"):
            #     config = configparser.ConfigParser()
            #     config.read(f"{self.sdc_home_dir}\\config\\local_config.ini")
            # return
        def start_bot(self,deployed):
            #start_bot = subprocess.Popen(['cmd',"python",f"{self.dataDict['sdc_home_dir']}\\sdc.py"])
            if deployed:
                os.system(f"start cmd /k \"{deployed_status['sdc_home_dir']}\\sdc.py\"")
            else:
                os.system(f"start cmd /k \"{self.dataDict['sdc_home_dir']}\\sdc.py\"")
            #os.spawnl(os.P_DETACH, f"cmd /k \"{self.dataDict['sdc_home_dir']}\\sdc.py\"")
        def add_hosts_entry(self):
            hosts = Hosts(path='c:\\windows\\system32\\drivers\\etc\\hosts')
            hosts.remove_all_matching(name='client.sea.heroesofnewerth.com')
            hosts.write()
            add_entry = HostsEntry(entry_type='ipv4', address='73.185.77.188', names=['client.sea.heroesofnewerth.com    #required by hon as this address is frequently used to poll for match stats'])
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
                return False
            elif rc == 3:
                print(bcolors.FAIL +"ERROR GETTING MAC ADDR" + bcolors.ENDC)
                tex.insert(END,"ERROR GETTING MAC ADDR\n",'warning')
                return False
        def getstatus_updater(self,auto_update,selected_branch):
            TASK_ENUM_HIDDEN = 1
            TASK_STATE = {0: 'Unknown',
                        1: 'Disabled',
                        2: 'Queued',
                        3: 'Ready',
                        4: 'Running'}

            scheduler = win32com.client.Dispatch('Schedule.Service')
            scheduler.Connect()

            n = 0
            folders = [scheduler.GetFolder('\\')]
            while folders:
                folder = folders.pop(0)
                folders += list(folder.GetFolders(0))
                tasks = list(folder.GetTasks(TASK_ENUM_HIDDEN))
                for task in tasks:
                    if task.name == "HoNfigurator Updater":
                        # settings = task.Definition.Settings
                        # print('Path       : %s' % task.Path)
                        # print('Hidden     : %s' % settings.Hidden)
                        # print('State      : %s' % TASK_STATE[task.State])
                        # print('Last Run   : %s' % task.LastRunTime)
                        # print('Last Result: %s\n' % task.LastTaskResult)
                        if TASK_STATE[task.State] == "Ready" and auto_update == False:
                            p = subprocess.Popen(['SCHTASKS', '/CHANGE', '/TN', task.Path,"/DISABLE"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            return True
                        elif TASK_STATE[task.State] == "Disabled" and auto_update == True:
                            p = subprocess.Popen(['SCHTASKS', '/CHANGE', '/TN', task.Path,"/ENABLE"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            return False
                        return
                else: 
                    if auto_update == True:
                        initialise.register_updater(self,selected_branch)
                        return True
                    else:
                        return False
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
        def playerCount(self):
            check = subprocess.Popen([self.dataDict['player_count_exe_loc'],self.dataDict['hon_file_name']],stdout=subprocess.PIPE, text=True)
            i = int(check.stdout.read())
            if i == -3 and self.dataDict['master_server'] == "honmasterserver.com":
                try:
                    check = subprocess.Popen([self.dataDict['player_count_exe_loc'],f"KONGOR_ARENA_{self.svr_id}.exe"],stdout=subprocess.PIPE, text=True)
                    i = int(check.stdout.read())
                except: pass
            elif i == -3 and self.dataDict['master_server'] == "kongor.online:666":
                try:
                    check = subprocess.Popen([self.dataDict['player_count_exe_loc'],f"HON_SERVER_{self.svr_id}.exe"],stdout=subprocess.PIPE, text=True)
                    i = int(check.stdout.read())
                except: pass
            check.terminate()
            return i
        def playerCountX(self,svr_id):
            if self.dataDict['master_server'] == "honmasterserver.com":
                check = subprocess.Popen([self.dataDict['player_count_exe_loc'],f"HON_SERVER_{svr_id}.exe"],stdout=subprocess.PIPE, text=True)
            elif self.dataDict['master_server'] == "kongor.online:666":
                check = subprocess.Popen([self.dataDict['player_count_exe_loc'],f"KONGOR_ARENA_{svr_id}.exe"],stdout=subprocess.PIPE, text=True)
            i = int(check.stdout.read())
            if i == -3 and self.dataDict['master_server'] == "honmasterserver.com":
                try:
                    check = subprocess.Popen([self.dataDict['player_count_exe_loc'],f"KONGOR_ARENA_{svr_id}.exe"],stdout=subprocess.PIPE, text=True)
                    i = int(check.stdout.read())
                except: pass
            elif i == -3 and self.dataDict['master_server'] == "kongor.online:666":
                try:
                    check = subprocess.Popen([self.dataDict['player_count_exe_loc'],f"HON_SERVER_{svr_id}.exe"],stdout=subprocess.PIPE, text=True)
                    i = int(check.stdout.read())
                except: pass
            check.terminate()
            return i
        def start_service(self,service_name):
            try:
                os.system(f'net start "{service_name}"')
            except:
                print ('could not start service {}'.format(service_name))
            return True
        def stop_service(self,service_name):
            try:
                os.system(f'net stop {service_name}')
            except:
                print ('could not stop service {}'.format(service_name))
            return True

        def create_service_bot(self,service_name):
            sp.Popen([self.dataDict['nssm_exe'], "install",service_name,"python.exe",f"sdc.py"])
            return True
        def create_service_generic(self,service_name,application):
            sp.Popen([self.dataDict['nssm_exe'], "install",service_name,f"{self.dataDict['hon_directory']}{application}"])
            return True
        def configure_service_generic(self,service_name,application,arguments):
            sp.Popen([self.dataDict['nssm_exe'], "set",service_name,"Application",f"{self.dataDict['hon_directory']}{application}"])
            time.sleep
            if arguments is not None:
                sp.Popen([self.dataDict['nssm_exe'], "set",service_name,"AppParameters",arguments])
                time.sleep(1)
            sp.Popen([self.dataDict['nssm_exe'], "set",service_name,"Start","SERVICE_DEMAND_START"])
            time.sleep(1)
            sp.Popen([self.dataDict['nssm_exe'], "set",service_name,f"AppExit","Default","Restart"])
            time.sleep(1)
            if service_name == "HoN Server Manager":
                sp.Popen([self.dataDict['nssm_exe'], "set",service_name,"AppEnvironmentExtra",f"USERPROFILE={self.dataDict['hon_root_dir']}"])
            elif service_name == "HoN Proxy Manager":
                sp.Popen([self.dataDict['nssm_exe'], "set",service_name,"AppEnvironmentExtra",f"APPDATA={self.dataDict['hon_root_dir']}"])
            return True
        def configure_service_api(self,service_name):
            sp.Popen([self.dataDict['nssm_exe'], "set",service_name,f"Application",f"{self.dataDict['hon_directory']}API_HON_SERVER.exe"])
            return True
        def configure_service_bot(self,service_name):
            sp.Popen([self.dataDict['nssm_exe'], "set",service_name,"Application","python.exe"])
            time.sleep(1)
            sp.Popen([self.dataDict['nssm_exe'], "set",service_name,f"AppDirectory",f"{self.sdc_home_dir}"])
            time.sleep(1)
            sp.Popen([self.dataDict['nssm_exe'], "set",service_name,f"AppStderr",f"{self.sdc_home_dir}\\sdc.log"])
            time.sleep(1)
            sp.Popen([self.dataDict['nssm_exe'], "set",service_name,"Start","SERVICE_DEMAND_START"])
            time.sleep(1)
            sp.Popen([self.dataDict['nssm_exe'], "set",service_name,f"AppExit","Default","Restart"])
            time.sleep(1)
            sp.Popen([self.dataDict['nssm_exe'], "set",service_name,"AppParameters","sdc.py"])
            return True

        def restart_service(self,service_name):
            try:
                os.system(f'net stop "{service_name}"')
            except:
                print ('could not stop service {}'.format(service_name))
            try:
                os.system(f'net start "{service_name}"')
            except:
                print ('could not start service {}'.format(service_name))
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

        def create_config(self,filename,type,game_port,voice_port,serverID,serverHoster,location,svr_total,svr_ip,master_user,master_pass,svr_desc):
            self.proxy = {}
            self.base = dmgr.mData.parse_config(self,os.path.abspath(application_path)+"\\config\\honfig.ini")
            iter = self.dataDict['incr_port']
            svr_identifier = self.dataDict['svrid_total']

            tem_game_port = int(game_port)
            tem_voice_port = int(voice_port)
            tem_game_port = tem_game_port + iter
            tem_voice_port = tem_voice_port + iter

            tem_game_port_proxy = self.base['svr_proxyPort']
            tem_game_port_proxy = tem_game_port_proxy.replace('"','')
            tem_game_port_proxy = int(tem_game_port_proxy) + (int(serverID) - 1)
            tem_voice_port_proxy = self.base['svr_proxyRemoteVoicePort']
            tem_voice_port_proxy = tem_voice_port_proxy.replace('"','')
            tem_voice_port_proxy = int(tem_voice_port_proxy) + (int(serverID) - 1)

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
                self.startup.update({'svr_port':f'"{tem_game_port}"'})
                self.startup.update({'svr_proxyPort':f'"{tem_game_port_proxy}"'})
                self.startup.update({'svr_proxyLocalVoicePort':f'"{tem_voice_port}"'})
                self.startup.update({'svr_proxyRemoteVoicePort':f'"{tem_voice_port_proxy}"'})
                self.startup.update({'svr_voicePortEnd':f'"{tem_voice_port}"'})
                self.startup.update({'svr_voicePortStart':f'"{tem_voice_port}"'})
                print("svr_port: " + str(tem_game_port))
                print("voice_port: " + str(tem_voice_port))
                if self.dataDict['use_proxy']=='True':
                    self.startup.update({"man_enableProxy":f'"true"'})
                    print("===============PROXY ACTIVE===================")
                    print("svr_proxyPort: " + str(tem_game_port_proxy))
                    print("svr_voiceProxyPort: " + str(tem_voice_port_proxy))
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
                self.proxy.update({'publicPort':tem_game_port_proxy})
                self.proxy.update({'redirectPort':tem_game_port})
                self.proxy.update({'voiceRedirectPort':tem_voice_port})
                self.proxy.update({'voicePublicPort':tem_voice_port_proxy})
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
        def configureEnvironment(self,configLoc,force_update,use_console):
            global hon_api_updated
            global players_connected
            global tex

            self.bot_version = float(self.bot_version)
            bot_needs_update = False
            bot_first_launch = False

            os.environ["USERPROFILE"] = self.dataDict['hon_root_dir']
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

            try:
                deployed_status=dmgr.mData.returnDict_basic(self,self.dataDict['svr_id'])
                if deployed_status['hon_directory'] != self.dataDict['hon_directory']:
                    # think about migrating here, like
                    #distutils.dir_util.copy_tree(os.path.abspath(application_path)+"\\oldSDC\\", f'{self.sdc_home_dir}\\newSDC\\')
                    try:
                        shutil.copy(f"{deployed_status['sdc_home_dir']}\\messages\\message{self.dataDict['svr_identifier']}",f"{self.dataDict['sdc_home_dir']}\\cogs\\messages\message{self.dataDict['svr_identifier']}.txt")
                        shutil.copy(f"{deployed_status['sdc_home_dir']}\\cogs\\total_games_played",f"{self.dataDict['sdc_home_dir']}\\cogs\\total_games_played")
                    except Exception as e:
                        print(e)
                if deployed_status['svr_hoster'] != self.dataDict['svr_hoster']:
                    try:
                        shutil.copy(f"{deployed_status['sdc_home_dir']}\\messages\\message{self.dataDict['svr_identifier']}",f"{self.dataDict['sdc_home_dir']}\\cogs\\messages\message{self.dataDict['svr_identifier']}.txt")
                    except Exception as e:
                        print(e)
            except Exception as e:
                            print(e)

            if exists(self.hon_logs_dir):
                print("exists: " + self.hon_logs_dir)
                #   os.chdir(self.hon_logs_dir)     # not required as we're honfigurator not a bot.
            else:
                os.makedirs(self.hon_logs_dir)
                print(f"creating: {self.hon_logs_dir} ...")
                #   os.chdir(self.hon_logs_dir)     # not required as we're honfigurator not a bot.

            if not exists(self.sdc_home_dir):
                print(f"creating: {self.sdc_home_dir} ...")
                os.makedirs(self.sdc_home_dir)

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
            firewall = initialise.configure_firewall(self,self.dataDict['hon_file_name'],self.dataDict['hon_exe'])
            if not exists(f"{self.hon_game_dir}\\startup.cfg") or bot_first_launch == True or bot_needs_update == True or force_update == True:
            #   below commented as we are no longer using game_settings_local.cfg
            #if not exists(f"{{hon_game_dir}\\startup.cfg") or not exists(f"{self.hon_logs_dir}\\..\\game_settings_local.cfg") or bot_first_launch == True or bot_needs_update == True or force_update == True:
                if bot_needs_update or force_update == True:
                    #tex.insert(END,"==========================================\n")
                    tex.insert(END,f"FORCE or UPDATE DETECTED, APPLIED v{self.bot_version}\n")
                    #tex.insert(END,"==========================================\n")
                #
                #    Kongor testing
                if self.dataDict['master_server'] == "honmasterserver.com":
                    if not exists(f"{self.dataDict['hon_directory']}\\HON_SERVER_{self.svr_id}.exe") or force_update == True or bot_needs_update == True:
                        try:
                            shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\kongor.exe",f"{self.dataDict['hon_directory']}HON_SERVER_{self.svr_id}.exe")
                            shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\hon_x64.exe",f"{self.dataDict['hon_directory']}hon_x64.exe")
                            print("copying server exe...")
                        except: print("server in use, can't replace exe, will try again when server is stopped.")
                if self.dataDict['master_server'] == "kongor.online:666":
                    if not exists(f"{self.dataDict['hon_directory']}\\KONGOR_ARENA_{self.svr_id}.exe") or force_update == True or bot_needs_update == True:
                        try:
                            shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\kongor.exe",f"{self.dataDict['hon_directory']}KONGOR_ARENA_{self.svr_id}.exe")
                            shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\hon_x64.exe",f"{self.dataDict['hon_directory']}hon_x64.exe")
                            print("copying server exe...")
                        except: print("server in use, can't replace exe, will try again when server is stopped.")
                if not exists(f"{self.hon_game_dir}\\startup.cfg"):
                #   below commented as we are no longer using game_settings_local.cfg
                # if not exists(f"{self.hon_logs_dir}\\..\\startup.cfg") or not exists(f"{self.hon_logs_dir}\\..\\game_settings_local.cfg"):
                    print(f"Server {self.service_name_bot} requires full configuration. No existing startup.cfg or game_settings_local.cfg. Configuring...")
                #   below commented as we are no longer using game_settings_local.cfg
                # COMMENTED OUT DUE TO TESTING LAUNCHING WITH COMMANDLINE ARGUMENTS
                #initialise.create_config(self,f"{self.hon_logs_dir}\\..\\startup.cfg",f"{self.hon_logs_dir}\\..\\game_settings_local.cfg",self.svr_id,self.svr_hoster,self.svr_region,self.svr_total,self.svr_ip)
                initialise.create_config(self,f"{self.hon_game_dir}\\startup.cfg","startup",self.dataDict['game_starting_port'],self.dataDict['voice_starting_port'],self.svr_id,self.svr_hoster,self.svr_region_short,self.svr_total,self.svr_ip,self.master_user,self.master_pass,self.svr_desc)
                initialise.create_config(self,f"{self.hon_game_dir}\\proxy_config.cfg","proxy",self.dataDict['game_starting_port'],self.dataDict['voice_starting_port'],self.svr_id,self.svr_hoster,self.svr_region_short,self.svr_total,self.svr_ip,self.master_user,self.master_pass,self.svr_desc)
                print(f"copying {self.service_name_bot} script and related configuration files to HoN environment: "+ self.hon_home_dir + "..")
                #config = ["sdc.py","multiguild.py"]
                # for i in config:
                #     if exists(os.path.abspath(application_path)+"\\"+i):
                #         shutil.copy(os.path.abspath(application_path)+"\\"+i,self.sdc_home_dir+"\\"+i)
                shutil.copy(os.path.abspath(application_path)+"\\sdc.py", f'{self.sdc_home_dir}\\sdc.py')
                shutil.copy(os.path.abspath(application_path)+"\\sdc.bat", f'{self.sdc_home_dir}\\sdc.bat')
                #shutil.copy(os.path.abspath(application_path)+"\\sdc.py", f'{self.sdc_home_dir}\\sdc.py')
                src_folder = os.path.abspath(application_path)+"\\cogs\\"
                dst_folder = f'{self.sdc_home_dir}\\cogs\\'
                for file_name in os.listdir(src_folder):
                    src_file = src_folder+file_name
                    dst_file = dst_folder+file_name
                    if os.path.isfile(src_file):
                        shutil.copy(src_file, dst_file)
                        print('copied', file_name)
                #shutil.copy(os.path.abspath(application_path)+"\\cogs\\*", f'{self.sdc_home_dir}\\cogs\\')
                distutils.dir_util.copy_tree(os.path.abspath(application_path)+"\\config\\", f'{self.sdc_home_dir}\\config\\')
                #
                #   FIX BELOW
                distutils.dir_util.copy_tree(os.path.abspath(application_path)+"\\icons\\", f'{self.sdc_home_dir}\\icons\\')
                #shutil.copy(os.path.abspath(application_path)+"\\multiguild.py", f'{self.sdc_home_dir}\\multiguild.py')
                #shutil.copy(configLoc,f"{self.sdc_home_dir}\\config\\sdc.ini")
                #shutil.copy(os.path.abspath(application_path)+"\\config\\honfig.py",f"{self.sdc_home_dir}\\config\\honfig.py")
                print("Done!")
                print("Checking and creating required dependencies...")
                #
                #
                # if not exists(f"{self.dataDict['hon_directory']}{self.dataDict['player_count_exe']}" or force_update == True or bot_needs_update == True):
                try:
                    shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\{self.dataDict['player_count_exe']}",f"{self.dataDict['hon_directory']}{self.dataDict['player_count_exe']}")
                except Exception as e: print(e)
                print("copying other dependencies...")
                if not exists(f"{self.dataDict['hon_directory']}\\nssm.exe"):
                    shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\nssm.exe",f"{self.dataDict['hon_directory']}\\nssm.exe")
                print("Done!")
            if self.dataDict['master_server'] == "honmasterserver.com":
                service_api = initialise.get_service(self.service_name_api)
                if service_api:
                    #print("HON Registration API STATUS: " + self.service_name_api)
                    if service_api['status'] == 'running' or service_api['status'] == 'paused':
                        if force_update != True and bot_needs_update != True:
                            tex.insert(END,"HON Registration API STATUS: RUNNING\n")
                        elif (force_update == True or bot_needs_update == True) and hon_api_updated !=True:
                            initialise.stop_service(self,self.service_name_api)
                            time.sleep(1)
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
                            time.sleep(1)
                            initialise.start_service(self,self.service_name_api)
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
                            time.sleep(1)
                            initialise.start_service(self,self.service_name_api)
                        else:
                            print("Windows Service STARTING...")
                            initialise.start_service(self,self.service_name_api)
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
                    initialise.start_service(self,self.service_name_api)
                    print("==========================================")
                    print("HON Registration API STATUS: " + self.service_name_api)
                    service_api = initialise.get_service(self.service_name_api)
                    if service_api['status'] == 'running':
                        tex.insert(END,"HON Registration API STATUS: " + self.service_name_api +": RUNNING\n")
                    else:
                        tex.insert(END,"HON Registration API STATUS: " + self.service_name_api +":  FAILED TO START!\n",'warning')
                    print("==========================================")
            if use_console == False:
                service_bot = initialise.get_service(self.service_name_bot)
                if service_bot:
                    print(f"HONSERVER STATUS: {self.service_name_bot}")
                    if service_bot['status'] == 'running' or service_bot['status'] == 'paused':
                        tex.insert(END,f"HONSERVER STATUS: {self.service_name_bot}: RUNNING\n")
                        if force_update == True or bot_needs_update == True:
                            #reconfigure service + restart
                            initialise.configure_service_bot(self,self.service_name_bot)
                            time.sleep(1)
                            svr_state = svrcmd.honCMD()
                            svr_state.getDataDict()
                            playercount = initialise.playerCount(self)
                            if playercount <= 0:
                                print("No players connected, safe to restart...")
                                initialise.stop_service(self,self.service_name_bot)
                                if self.dataDict['master_server'] == "honmasterserver.com":
                                    try:
                                        shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\kongor.exe",f"{self.dataDict['hon_directory']}HON_SERVER_{self.svr_id}.exe")
                                        print("copying server exe...")
                                    except Exception as e: print(e + "can't replace exe.")
                                if self.dataDict['master_server'] == "kongor.online:666":
                                    try:
                                        shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\kongor.exe",f"{self.dataDict['hon_directory']}KONGOR_ARENA_{self.svr_id}.exe")
                                        print("copying server exe...")
                                    except Exception as e: print(e + "can't replace exe.")
                                initialise.start_service(self,self.service_name_bot)
                            else:
                                players_connected = True
                                initialise.schedule_restart(self)
                    else:
                        if force_update == True or bot_needs_update == True:
                            #reconfigure service + restart
                            initialise.configure_service_bot(self,self.service_name_bot)
                            time.sleep(1)
                        print(f"HONSERVER STATUS: {self.service_name_bot}")
                        initialise.start_service(self,self.service_name_bot)
                        service_bot = initialise.get_service(self.service_name_bot)
                        if service_bot['status'] == 'running':
                            tex.insert(END,f"HONSERVER STATUS: {self.service_name_bot} RUNNING\n")
                        else:
                            tex.insert(END,f"HONSERVER STATUS: {self.service_name_bot} FAILED TO START!\n",'warning')
                        print("==========================================")
                else:
                    bot_needs_update = True
                    print("==========================================")
                    print(f"Creating adminbot: {self.service_name_bot}..")
                    print("==========================================")
                    initialise.create_service_bot(self,self.service_name_bot)
                    time.sleep(1)
                    initialise.configure_service_bot(self,self.service_name_bot)
                    initialise.start_service(self,self.service_name_bot)
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
            else:
                playercount = initialise.playerCount(self)
                if playercount == -3:
                    initialise.start_bot(self,False)
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
        def regions(self):
            return [["US - West","US - East","Thailand","Australia","Malaysia","Russia","Europe","Brazil"],["USW","USE","SEA","AU","SEA","RU","EU","BR"]]
        def masterserver(self):
            return ["kongor.online:666","honmasterserver.com"]
        def reg_def_link(self,var,index,mode):
            reglist = self.regions()
            svrloc = str(self.svr_loc.get()).lower()
            for reg in reglist[0]:
                if svrloc == reg.lower():
                    self.svr_loc.set(reglist[0][reglist[0].index(reg)])
                    self.svr_reg_code.set(reglist[1][reglist[0].index(reg)])
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
            
        def sendData(self,identifier,hoster, region, regionshort, serverid, servertotal,hondirectory,svr_login,svr_password, bottoken,discordadmin,master_server,force_update,use_console,use_proxy,game_port,voice_port,core_assignment,process_priority,botmatches,debug_mode,selected_branch,increment_port):
            global config_local
            global config_global
            global ports_to_forward_game
            global ports_to_forward_voice
            
            conf_local = configparser.ConfigParser()
            conf_global = configparser.ConfigParser()
            #   adds a trailing slash to the end of the path if there isn't one. Required because the code breaks if a slash isn't provided
            hondirectory = os.path.join(hondirectory, '')
            ports_to_forward_game=[]
            ports_to_forward_voice=[]


            # if 'github_branch' not in self.dataDict:
            #     self.dataDict.update({'github_branch':selected_branch})
            # if identifier == "update":
            #     update = initialise.update_repository(self,selected_branch)
            #     tex.insert(END,"==========================================\n")
            #     # if update:
            #     #     gui.popup_bonus()
            #     #     os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 
            # # update hosts file to fix an issue where hon requires resolving to name client.sea.heroesofnewerth.com
            #initialise.add_hosts_entry(self)
            if use_proxy:
                if not exists(hondirectory+'proxy.exe'):
                    tex.insert(END,f"NO PROXY.EXE FOUND. Please obtain this and place it into {hondirectory} and try again. Continuing with proxy disabled..\n",'warning')
                    use_proxy=False
                else:
                    firewall = initialise.configure_firewall(self,"HoN Proxy",hondirectory+'proxy.exe')
            if use_console == False:
                service_proxy_name="HoN Proxy Manager"
                service_manager_name="HoN Server Manager"
                service_proxy = initialise.get_service(service_proxy_name)
                service_manager = initialise.get_service(service_manager_name)
                default_voice_port=11435
                manger_application=f"KONGOR ARENA MANAGER.exe"
                manager_arguments=f"-manager -noconfig -execute \"Set man_masterLogin {self.dataDict['svr_login']}:;Set man_masterPassword {self.dataDict['svr_password']};Set man_numSlaveAccounts 0;Set man_startServerPort {self.dataDict['game_starting_port']};Set man_endServerPort {int(self.dataDict['game_starting_port'])+(int(self.dataDict['svr_total'])-1)};Set man_voiceProxyStartPort {self.dataDict['voice_starting_port']};Set man_voiceProxyEndPort {int(self.dataDict['voice_starting_port'])+(int(self.dataDict['svr_total'])-1)};Set man_maxServers {self.dataDict['svr_id']};Set man_enableProxy {self.dataDict['use_proxy']};Set man_broadcastSlaves true;Set man_autoServersPerCPU 1;Set man_allowCPUs 0;Set host_affinity -1;Set man_uploadToS3OnDemand 1;Set man_uploadToCDNOnDemand 0;Set svr_name {self.dataDict['svr_hoster']} 0 0;Set svr_location {self.dataDict['svr_region_short']};Set svr_ip {self.dataDict['svr_ip']}\" -masterserver {self.dataDict['master_server']}"
                if service_manager:
                    print("Manager exists")
                    #if force_update or bot_needs_update or bot_first_launch:
                    if force_update:
                        if not exists(f"{hondirectory}KONGOR ARENA MANAGER.exe"):
                            shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\kongor.exe",f"{hondirectory}{manger_application}")
                        initialise.configure_service_generic(self,service_manager_name,manger_application,manager_arguments)
                        if service_manager['status'] == 'running' or service_manager['status'] == 'paused':
                            initialise.restart_service(self,service_manager_name)
                        else:
                            initialise.start_service(self,service_manager_name)
                        service_manager = initialise.get_service(service_manager_name)
                else:
                    if not exists(f"{hondirectory}KONGOR ARENA MANAGER.exe"):
                        shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\kongor.exe",f"{hondirectory}{manger_application}")
                    initialise.create_service_generic(self,service_manager_name,manger_application)
                    initialise.start_service(self,service_manager_name)
                    service_manager = initialise.get_service(service_manager_name)
                    if service_manager:
                        print("Manager started")
                if use_proxy:
                    if service_proxy:
                        print("proxy exists")
                        #if force_update or bot_needs_update or bot_first_launch:
                        if force_update:
                            proxy_config=[f"count={self.dataDict['svr_total']}",f"ip={self.dataDict['svr_ip']}",f"startport={self.dataDict['game_starting_port']}",f"startvoicePort={default_voice_port}","region=naeu"]
                            proxy_config_location=f"{self.dataDict['hon_root_dir']}\\HoNProxyManager"
                            if not exists(proxy_config_location):
                                os.mkdir(proxy_config_location)
                            proxy_config_location=f"{self.dataDict['hon_root_dir']}\\HoNProxyManager\\config.cfg"
                            with open(proxy_config_location,"w") as f:
                                for items in proxy_config:
                                    f.write(f"{items}\n")
                            initialise.configure_service_generic(self,service_proxy_name,"proxymanager.exe",None)
                            if service_proxy['status'] == 'running' or service_proxy['status'] == 'paused':
                                initialise.restart_service(self,service_proxy_name)
                            else:
                                initialise.start_service(self,service_proxy_name)
                            #service_manager = initialise.get_service(service_proxy)
                    else:
                        proxy_config=[f"count={self.dataDict['svr_total']}",f"ip={self.dataDict['svr_ip']}",f"startport={self.dataDict['game_starting_port']}",f"startvoicePort={default_voice_port}","region=naeu"]
                        proxy_config_location=f"{self.dataDict['hon_root_dir']}\\HoNProxyManager"
                        if not exists(proxy_config_location):
                            os.mkdir(proxy_config_location)
                        proxy_config_location=f"{self.dataDict['hon_root_dir']}\\HoNProxyManager\\config.cfg"
                        with open(proxy_config_location,"w") as f:
                            for items in proxy_config:
                                f.writelines([items])
                        application="proxymanager.exe"
                        initialise.create_service_generic(self,service_proxy_name,application)
                        time.sleep(1)
                        initialise.start_service(self,service_proxy_name)
                        #service_manager = initialise.get_service(service_manager_name)
            if identifier == "single":
                print()
                print(f"Selected option to configure adminbot-server{serverid}\n")
                print("==========================================")
                #
                #   local config
                if not conf_local.has_section("OPTIONS"):
                    conf_local.add_section("OPTIONS")
                conf_local.set("OPTIONS","svr_hoster",hoster)
                conf_local.set("OPTIONS","svr_region",region)
                conf_local.set("OPTIONS","svr_region_short",regionshort)
                conf_local.set("OPTIONS","svr_id",serverid)
                conf_local.set("OPTIONS","svr_ip",self.dataDict['svr_ip'])
                conf_local.set("OPTIONS","svr_total",servertotal)
                conf_local.set("OPTIONS","token",bottoken)
                conf_local.set("OPTIONS","hon_directory",hondirectory)
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
                    #
                    #   local config
                    if not conf_local.has_section("OPTIONS"):
                        conf_local.add_section("OPTIONS")
                    conf_local.set("OPTIONS","svr_hoster",hoster)
                    conf_local.set("OPTIONS","svr_region",region)
                    conf_local.set("OPTIONS","svr_region_short",regionshort)
                    conf_local.set("OPTIONS","svr_id",str(serverid))
                    conf_local.set("OPTIONS","svr_ip",self.dataDict['svr_ip'])
                    conf_local.set("OPTIONS","svr_total",servertotal)
                    conf_local.set("OPTIONS","token",bottoken)
                    conf_local.set("OPTIONS","hon_directory",hondirectory)
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
            self.tab1_servertd.grid(column= 2 , row = 5,sticky="w",pady=4)
            self.svr_total_var.trace_add('write', self.svr_num_link)
            #  one or two cores
            self.core_assign = tk.StringVar(app,self.dataDict['core_assignment'])
            applet.Label(tab1, text="CPU cores assigned per server:",background=maincolor,foreground='white').grid(column=0, row=8,sticky="e",padx=[20,0])
            tab1_core_assign = applet.Combobox(tab1,foreground=textcolor,value=self.coreassign(),textvariable=self.core_assign,width=16)
            tab1_core_assign.grid(column= 1, row = 8,sticky="w",pady=4,padx=[0,130])
            self.core_assign.trace_add('write', self.coreadjust)
            #   
            #   Simple Server data
            applet.Label(tab1, text="Hon Server Data",background=maincolor,foreground='white').grid(columnspan=1,column=1, row=1,sticky="w")
            #   hoster
            applet.Label(tab1, text="Server Name:",background=maincolor,foreground='white').grid(column=0,row=2,sticky="e")
            tab1_hosterd = applet.Entry(tab1,foreground=textcolor,width=16)
            tab1_hosterd.insert(0,self.dataDict['svr_hoster'])
            tab1_hosterd.grid(column= 1 , row = 2,sticky="w",pady=4,padx=[0,130])
            #   server name
            applet.Label(tab1, text="HoN Username:",background=maincolor,foreground='white').grid(column=0,row=3,sticky="e")
            tab1_user = applet.Entry(tab1,foreground=textcolor,width=16)
            tab1_user.insert(0,self.dataDict['svr_login'])
            tab1_user.grid(column= 1 , row = 3,sticky="w",pady=4,padx=[0,130])
            #   server password
            applet.Label(tab1, text="HoN Password:",background=maincolor,foreground='white').grid(column=1,row=3,sticky="e")
            tab1_pass = applet.Entry(tab1,foreground=textcolor,width=16,show="*")
            tab1_pass.insert(0,self.dataDict['svr_password'])
            tab1_pass.grid(column= 2 , row = 3,sticky="w",pady=4)
            #
            #   region
            self.svr_loc = tk.StringVar(app,self.dataDict["svr_region"])
            applet.Label(tab1, text="Location:",background=maincolor,foreground='white').grid(column=0, row=4,sticky="e")
            tab1_regiond = applet.Combobox(tab1,foreground=textcolor,value=self.regions()[0],textvariable=self.svr_loc,width=16)
            tab1_regiond.grid(column= 1 , row = 4,sticky="w",pady=4,padx=[0,130])
            self.svr_loc.trace_add('write', self.reg_def_link)
            #   regionId
            self.svr_reg_code = tk.StringVar(app,self.dataDict["svr_region_short"])
            applet.Label(tab1, text="Region Code:",background=maincolor,foreground='white').grid(column=1, row=4,sticky="e")
            tab1_regionsd = applet.Combobox(tab1,foreground=textcolor,value=self.regions()[1],textvariable=self.svr_reg_code,width=5)
            tab1_regionsd.grid(column= 2 , row = 4,sticky="w",pady=4)
            self.svr_reg_code.trace_add('write', self.reg_def_link)
            #   server id
            self.svr_id_var = tk.StringVar(app,self.dataDict['svr_id'])
            applet.Label(tab1, text="Server ID:",background=maincolor,foreground='white').grid(column=0, row=5,sticky="e")
            self.tab1_serveridd = applet.Combobox(tab1,foreground=textcolor,value=self.corecount(),textvariable=self.svr_id_var,width=5)
            self.tab1_serveridd.grid(column= 1 , row = 5,sticky="w",pady=4,padx=[0,130])
            self.svr_id_var.trace_add('write', self.svr_num_link)
            
            #   HoN Directory
            applet.Label(tab1, text="HoN Directory:",background=maincolor,foreground='white').grid(column=0, row=12,sticky="e",padx=[20,0])
            tab1_hondird = applet.Entry(tab1,foreground=textcolor,width=45)
            tab1_hondird.insert(0,self.dataDict['hon_directory'])
            tab1_hondird.grid(columnspan=3,column= 1, row = 12,sticky="w",pady=4)
            # #   HoN Home
            # applet.Label(tab1, text="HoN Home Folder (replays, logs):",background=maincolor,foreground='white').grid(column=0, row=13,sticky="e",padx=[20,0])
            # tab1_honroot = applet.Entry(tab1,foreground=textcolor,width=45)
            # tab1_honroot.insert(0,"<default>")
            # tab1_honroot.grid(columnspan=3,column= 1, row = 13,sticky="w",pady=4)
            #  HoN master server
            self.master_server = tk.StringVar(app,self.dataDict['master_server'])
            applet.Label(tab1, text="HoN Master Server:",background=maincolor,foreground='white').grid(column=0, row=6,sticky="e",padx=[20,0])
            tab1_masterserver = applet.Combobox(tab1,foreground=textcolor,value=self.masterserver(),textvariable=self.master_server,width=16)
            tab1_masterserver.grid(column= 1, row = 6,sticky="w",pady=4,padx=[0,130])
            
            #  one or two cores
            self.priority = tk.StringVar(app,self.dataDict['process_priority'])
            applet.Label(tab1, text="In-game CPU process priority:",background=maincolor,foreground='white').grid(column=0, row=7,sticky="e",padx=[20,0])
            tab1_priority = applet.Combobox(tab1,foreground=textcolor,value=self.priorityassign(),textvariable=self.priority,width=16)
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
            tab1_useproxy_btn.grid(column= 2, row = 10,sticky="w",pady=4)
            # self.useproxy.trace_add('write',self.change_to_proxy2)
            #  starting gameport
            applet.Label(tab1, text="Starting game port:",background=maincolor,foreground='white').grid(column=1,row=7,sticky="e")
            tab1_game_port = applet.Entry(tab1,foreground=textcolor,width=5)
            tab1_game_port.insert(0,self.dataDict['game_starting_port'])
            # self.tab1_game_port.insert(0,self.change_to_proxy())
            tab1_game_port.grid(column=2,row = 7,sticky="w",pady=4)
            #  starting gameport
            applet.Label(tab1, text="Starting voice port:",background=maincolor,foreground='white').grid(column=1,row=8,sticky="e")
            tab1_voice_port = applet.Entry(tab1,foreground=textcolor,width=5)
            tab1_voice_port.insert(0,self.dataDict['voice_starting_port'])
            tab1_voice_port.grid(column=2,row = 8,sticky="w",pady=4)
            #   force update
            applet.Label(tab1, text="Force Update:",background=maincolor,foreground='white').grid(column=0, row=10,sticky="e",padx=[20,0])
            self.forceupdate = tk.BooleanVar(app)
            tab1_forceupdate_btn = applet.Checkbutton(tab1,variable=self.forceupdate)
            tab1_forceupdate_btn.grid(column= 1, row = 10,sticky="w",pady=2)
            #   console windows, for launching servers locally (not as windows services)
            applet.Label(tab1, text="Launch as Console (BETA):",background=maincolor,foreground='white').grid(column=0, row=11,sticky="e",padx=[20,0])
            self.console = tk.BooleanVar(app)
            if self.dataDict['use_console'] == 'True':
                self.console.set(True)
            tab1_console_btn = applet.Checkbutton(tab1,variable=self.console)
            tab1_console_btn.grid(column= 1, row = 11,sticky="w",pady=2)
            # self.useproxy.trace_add('write', self.change_to_proxy(NULL,NULL,NULL))
            #
            
            #    Setup Info
            applet.Label(tab1, text="Discord Data",background=maincolor,foreground='white').grid(columnspan=1,column=4, row=1,sticky="w")
            #   discord admin
            applet.Label(tab1, text="Bot Owner (discord ID):",background=maincolor,foreground='white').grid(column=3, row=2,sticky="e",padx=[20,0])
            tab1_discordadmin = applet.Entry(tab1,foreground=textcolor,width=45)
            tab1_discordadmin.insert(0,self.dataDict['discord_admin'])
            tab1_discordadmin.grid(column= 4, row = 2,sticky="w",pady=4)
            #   token
            applet.Label(tab1, text="Bot Token (SECRET):",background=maincolor,foreground='white').grid(column=3, row=3,sticky="e",padx=[20,0])
            tab1_bottokd = applet.Entry(tab1,foreground=textcolor,width=45)
            tab1_bottokd.insert(0,self.dataDict['token'])
            tab1_bottokd.grid(column= 4, row = 3,sticky="w",pady=4,padx=[0,20])
            #  allow bot matches 
            applet.Label(tab1, text="Allow bot matches:",background=maincolor,foreground='white').grid(column=3, row=4,sticky="e",padx=[20,0])
            self.botmatches = tk.BooleanVar(app)
            tab1_botmatches_btn = applet.Checkbutton(tab1,variable=self.botmatches)
            tab1_botmatches_btn.grid(column= 4, row = 4,sticky="w",pady=4)
            #  Debug mode 
            applet.Label(tab1, text="Debug mode:",background=maincolor,foreground='white').grid(column=3, row=5,sticky="e",padx=[20,0])
            self.debugmode = tk.BooleanVar(app)
            if self.dataDict['debug_mode'] == 'True':
                self.debugmode.set(True)
            tab1_debugmode_btn = applet.Checkbutton(tab1,variable=self.debugmode)
            tab1_debugmode_btn.grid(column= 4, row = 5,sticky="w",pady=4)
            # #   auto update
            # applet.Label(tab1, text="Auto update HoNfigurator:",background=maincolor,foreground='white').grid(column=3, row=5,sticky="e",padx=[20,0])
            # self.autoupdate = tk.BooleanVar(app)
            # if self.dataDict['auto_update'] == 'True':
            #     self.autoupdate.set(True)
            # tab1_autoupdate_btn = applet.Checkbutton(tab1,variable=self.autoupdate)
            # tab1_autoupdate_btn.grid(column= 4, row = 5,sticky="w",pady=4)
            #   branch select
            self.git_branch = tk.StringVar(app,self.git_current_branch())
            applet.Label(tab1, text="Currently selected branch:",background=maincolor,foreground='white').grid(column=3, row=6,sticky="e",padx=[20,0])
            tab1_git_branch = applet.Combobox(tab1,foreground=textcolor,value=self.git_all_branches(),textvariable=self.git_branch)
            tab1_git_branch.grid(column= 4, row = 6,sticky="w",pady=4)
            self.git_branch.trace_add('write', self.update_repository)

            #   bot version
            applet.Label(tab1, text="Bot Version:",background=maincolor,foreground='white').grid(column=3, row=7,sticky="e",padx=[20,0])
            applet.Label(tab1,text=f"{self.dataDict['bot_version']}-{self.dataDict['environment']}",background=maincolor,foreground='white').grid(column= 4, row = 7,sticky="w",pady=4)
            print(self.forceupdate.get())
            

            # tex = tk.Text(tab1,foreground=textcolor,width=70,height=10,background=textbox)
            # tex.grid(columnspan=6,column=0,row=15,sticky="n")
            #   button
            tab1_singlebutton = applet.Button(tab1, text="Configure Single Server",command=lambda: self.sendData("single",tab1_hosterd.get(),tab1_regiond.get(),tab1_regionsd.get(),self.tab1_serveridd.get(),self.tab1_servertd.get(),tab1_hondird.get(),tab1_user.get(),tab1_pass.get(),tab1_bottokd.get(),tab1_discordadmin.get(),tab1_masterserver.get(),self.forceupdate.get(),self.console.get(),self.useproxy.get(),tab1_game_port.get(),tab1_voice_port.get(),self.core_assign.get(),self.priority.get(),self.botmatches.get(),self.debugmode.get(),self.git_branch.get(),self.increment_port.get()))
            tab1_singlebutton.grid(columnspan=5,column=0, row=14,stick='n',padx=[0,300],pady=[20,10])
            tab1_allbutton = applet.Button(tab1, text="Configure All Servers",command=lambda: self.sendData("all",tab1_hosterd.get(),tab1_regiond.get(),tab1_regionsd.get(),self.tab1_serveridd.get(),self.tab1_servertd.get(),tab1_hondird.get(),tab1_user.get(),tab1_pass.get(),tab1_bottokd.get(),tab1_discordadmin.get(),tab1_masterserver.get(),self.forceupdate.get(),self.console.get(),self.useproxy.get(),tab1_game_port.get(),tab1_voice_port.get(),self.core_assign.get(),self.priority.get(),self.botmatches.get(),self.debugmode.get(),self.git_branch.get(),self.increment_port.get()))
            tab1_allbutton.grid(columnspan=5,column=0, row=14,stick='n',padx=[30,30],pady=[20,10])
            tab1_updatebutton = applet.Button(tab1, text="Update HoNfigurator",command=lambda: self.update_repository(NULL,NULL,NULL))
            tab1_updatebutton.grid(columnspan=5,column=0, row=14,stick='n',padx=[300,0],pady=[20,10])
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
                    tex = tk.Text(app,foreground=textcolor,background=textbox,height=15)
                    tex.grid(row=15, column=0, sticky="nsew", padx=2, pady=2)
                    tex.tag_config('warning', background="yellow", foreground="red")
                    tex.tag_config('interest', background="green")
                # create a Scrollbar and associate it with txt
                    scrollb = ttk.Scrollbar(app, command=tex.yview)
                    scrollb.grid(row=15, column=1, sticky='nsew')
                    tex['yscrollcommand'] = scrollb.set

            ButtonString = ['View Log', 'Start', 'Stop', 'Clean', 'Uninstall']
            LablString = ['hon_server_','test','space']

            # Calling this function from somewhere else via Queue
            import fnmatch
            import glob
            def clean_all():
                count=0
                for i in range (1,int(self.dataDict['svr_total'])):
                    deployed_status = dmgr.mData.returnDict_basic(self,i)
                    paths = [f"{deployed_status['hon_logs_dir']}",f"{deployed_status['hon_logs_dir']}\\diagnostics",f"{self.dataDict['hon_home_dir']}\\HoNProxyManager"]
                    now = time.time()
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
            def get_size(start_path):
                    total_size = 0
                    for dirpath, dirnames, filenames in os.walk(start_path):
                        for f in filenames:
                            fp = os.path.join(dirpath, f)
                            # skip if it is symbolic link
                            if not os.path.islink(fp):
                                total_size += os.path.getsize(fp)
                    return total_size
            class viewButton():
                # tabgui2 = ttk.Notebook(tab2)
                # tabgui2.grid(column=0,row=14)
                #def __init__(self,btn,i,pcount):
                def __init__(self,btn,i,p):
                    global id
                    global pcount
                    global deployed_status
                    global service_name

                    service_name = f"adminbot{i}"
                    id = i
                    pcount = p
                    self.initdict = dmgr.mData()
                    self.dataDict = self.initdict.returnDict()
                    deployed_status = dmgr.mData.returnDict_basic(self,id)
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
                def refresh(*args):
                    if (tabgui.index("current")) == 1:
                        viewButton.load_server_mgr(self)
                def load_log(self,*args):
                    if (tabgui.index("current")) == 1:
                        viewButton.ViewLog(self)

                def ViewLog(self):
                    tex.delete('1.0', END)
                    logs_dir = f"{deployed_status['hon_logs_dir']}\\"
                    status = Label(tab2,width=14,text=f"testing", background=maincolor,foreground='white')
                    status.grid(row=12,column=0)
                    #print(str(deployed_status))
                    # Server Log
                    if (tabgui2.index("current")) == 0:
                        if pcount <=0:
                            log_File = f"Slave*{deployed_status['svr_id']}*.log"
                        else:
                            log_File = f"Slave*{deployed_status['svr_id']}*.clog"
                        list_of_files = glob.glob(logs_dir + log_File) # * means all if need specific format then *.csv
                        latest_file = max(list_of_files, key=os.path.getctime)
                        info=["New session cookie"," Connected","[ALL]","lag","spike","ddos"]
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
                        log_File = "sdc.log"
                        list_of_files = glob.glob(logs_dir + log_File) # * means all if need specific format then *.csv
                        latest_file = max(list_of_files, key=os.path.getctime)
                        with open(latest_file,'r') as file:
                            for line in file:
                                tem=line.lower()
                                tex.insert(tk.END,line)
                    if (tabgui2.index("current")) == 3:
                        logs_dir = f"{deployed_status['hon_root_dir']}\\HoNProxyManager\\"
                        log_File = f"proxy_{20000 + int(deployed_status['svr_id']) - 1}*.log"
                        list_of_files = glob.glob(logs_dir + log_File) # * means all if need specific format then *.csv
                        latest_file = max(list_of_files, key=os.path.getctime)
                        warnings=["BANNED","BLOCKED","CLOSED"]
                        with open(latest_file,'r') as file:
                            for line in file:
                                tem=line.lower()
                                if any(x.lower() in tem for x in warnings):
                                    tex.insert(tk.END,line,'warning')
                                else:
                                    tex.insert(tk.END,line)
                    print(latest_file)                   
                    tex.see(tk.END)

                def Start(self):
                    if deployed_status['use_console'] == 'True':
                        pcount = initialise.playerCountX(self,id)
                        if pcount == -3:
                            initialise.start_bot(self,True)
                    else:
                        self.service = initialise.get_service(service_name)
                        if self.service['status'] == 'stopped':
                            if initialise.start_service(self,service_name):
                                tex.insert(END,f"{service_name} started successfully.\n")
                                app.after(10000,viewButton.refresh)
                            else:
                                tex.insert(END,f"{service_name} failed to start.\n")
                def Stop(self):
                    pcount = initialise.playerCountX(self,id)
                    if pcount <= 0:
                        if deployed_status['use_console'] == 'False':
                            if initialise.stop_service(self,service_name):
                                tex.insert(END,f"{service_name} stopped successfully.\n")
                                viewButton.load_server_mgr(self)
                            else:
                                tex.insert(END,f"{service_name} failed to stop.\n")
                        # else:

                    else:
                        print("[ABORT] players are connected. Scheduling shutdown instead..")
                        initialise.schedule_shutdown(deployed_status)
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
                            if initialise.stop_service(self,service_name):
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
                    # if (tabgui.index("current")) == 1:
                    app.lift()
                    i=0
                    c=0
                    c_len = len(ButtonString)+len(LablString)
                    mod=11
                    svc_or_con="svc"
                    # create a grid of 2x6
                    for t in range(20):
                        tab2.rowconfigure(t, weight=1,pad=0)
                    for o in range(100):
                        tab2.columnconfigure(o, weight=1,pad=0)
                    for x in range(0,int(self.dataDict['svr_total'])):
                        x+=1
                        i+=1
                        service_name = f"adminbot{x}"
                        deployed_status = dmgr.mData.returnDict_basic(self,x)
                        dir_name = f"{deployed_status['hon_logs_dir']}\\"
                        file = "Slave*.log"
                        log = False
                        try:
                            list_of_files = glob.glob(dir_name + file) # * means all if need specific format then *.csv
                            log = max(list_of_files, key=os.path.getctime)
                        except Exception as e:
                            print(e)
                        cookie = True
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
                        if i%mod==0:
                            c+=c_len
                            i=1
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
                                    LablString[1]="cookie error"
                                elif pcount >0:
                                    colour = 'SpringGreen4'
                                    LablString[1]=f"In-game ({pcount})"
                            if service_state is not None and deployed_status['use_console'] == 'False':
                                if service_state == False or service_state['status'] == 'stopped':
                                    colour = 'OrangeRed4'
                                    svc_or_con="svc"
                                    #LablString[1]=f"svc-Stopped"
                            elif deployed_status['use_console'] == 'True' and pcount <0:
                                colour = 'OrangeRed4'
                                svc_or_con="con"
                                #LablString[1]=f"con-Stopped"
                            c_pos1 = index1 + c
                            if index1==0:
                                labl = Label(tab2,width=12,text=f"{labl_name}", background=colour, foreground='white')
                            elif index1==1:
                                labl = Label(tab2,width=14,text=f"{svc_or_con}-{labl_name}", background=colour, foreground='white')
                            labl.grid(row=i, column=c_pos1)
                            for index2, btn_name in enumerate(ButtonString):
                                index2 +=len(LablString)
                                c_pos2 = index2 + c
                                btn = Button(tab2,text=btn_name, command=partial(viewButton,btn_name,x,pcount))
                                btn.grid(row=i, column=c_pos2)
                    column_rows=(tab2.grid_size())
                    total_columns=column_rows[0]
                    total_rows=column_rows[1]
                    print(column_rows)
                    logolabel_tab2 = applet.Label(tab2,text="HoNfigurator",background=maincolor,foreground='white',image=honlogo)
                    logolabel_tab2.grid(columnspan=total_columns,column=0, row=0,pady=[10,0],sticky='n')
                    
                    tab2_refresh = applet.Button(tab2, text="Refresh",command=lambda: viewButton.refresh())
                    tab2_refresh.grid(columnspan=total_columns,column=0, row=mod+1,sticky='n',padx=[80,0],pady=[20,10])
                    tab2_cleanall = applet.Button(tab2, text="Clean All",command=lambda: clean_all())
                    tab2_cleanall.grid(columnspan=total_columns,column=0, row=mod+1,sticky='n',padx=[0,80],pady=[20,10])
                    tabgui2.grid(column=0,row=13,sticky='ew',columnspan=total_columns)
                def Tools():
                    pass
            # create a Scrollbar and associate it with txt
            combo = TextScrollCombo(app)
            combo.config(width=600, height=600)
            app.grid_rowconfigure(0, weight=1)
            app.grid_columnconfigure(0, weight=1)
            tabgui2 = ttk.Notebook(tab2)
            # app.rowconfigure(15, weight=1)
            tab11 = ttk.Frame(tabgui2)
            tab22 = ttk.Frame(tabgui2)
            tab23 = ttk.Frame(tabgui2)
            tab24 = ttk.Frame(tabgui2)
            tabgui2.add(tab11,text="Server Log")
            tabgui2.add(tab22,text="Match Log")
            tabgui2.add(tab23,text="Bot Log")
            tabgui2.add(tab24,text="Proxy Log")
            tabgui.select(0)
            self.update_repository(NULL,NULL,NULL)
            tabgui.bind('<<NotebookTabChanged>>',viewButton.refresh)
            tabgui2.bind('<<NotebookTabChanged>>',viewButton.load_log)
            app.mainloop()
    test = honfigurator()
    test.creategui()
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 5)