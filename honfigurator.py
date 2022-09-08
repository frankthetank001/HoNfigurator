
from asyncio.subprocess import DEVNULL
import tkinter as tk
from tkinter import *
from tkinter import getboolean, ttk
import multiprocessing
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
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)


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
            print("ERROR CHECKING HASHES, you may have issues connecting to the masterserver")
            tex.insert(END,"ERROR CHECKING HASHES, you may have issues connecting to the masterserver\n")
            return False
        elif rc == 3:
            print("ERROR GETTING MAC ADDR")
            tex.insert(END,"ERROR GETTING MAC ADDR\n")
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
                return True
            else:
                print(f"Repository: {selected_branch}\nCheckout status: {checkout.stderr}")
                tex.insert(END,f"Repository: {selected_branch}\nCheckout Status ({checkout.returncode}): {checkout.stderr}")
                if 'Please commit your changes or stash them before you switch branches.' in checkout.stderr:
                    print()
                return False
        else:
            print(f"Updating selected repository: {selected_branch} branch")
            output = subprocess.run(["git", "pull"],stdout=subprocess.PIPE, text=True)
            print(f"Repository: {selected_branch}\nUpdate Status: {output.stdout}")
            tex.insert(END,f"Repository: {selected_branch}\nUpdate Status: {output.stdout}")
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
            os.system(f'net start {service_name}')
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
        sp.Popen([self.nssm, "install",service_name,"python.exe",f"sdc.py"])
        return True

    def create_service_api(self,service_name):
        sp.Popen([self.nssm, "install",service_name,f"{self.hon_directory}API_HON_SERVER.exe"])
        return True

    def configure_service_api(self,service_name):
        sp.Popen([self.nssm, "set",service_name,f"Application",f"{self.hon_directory}API_HON_SERVER.exe"])
        return True
        
    def configure_service_bot(self,service_name):
        sp.Popen([self.nssm, "set",service_name,"Application","python.exe"])
        time.sleep(1)
        sp.Popen([self.nssm, "set",service_name,f"AppDirectory",f"{self.sdc_home_dir}"])
        time.sleep(1)
        sp.Popen([self.nssm, "set",service_name,f"AppStderr",f"{self.sdc_home_dir}\\sdc.log"])
        time.sleep(1)
        sp.Popen([self.nssm, "set",service_name,"Start","SERVICE_DEMAND_START"])
        time.sleep(1)
        sp.Popen([self.nssm, "set",service_name,f"AppExit","Default","Restart"])
        time.sleep(1)
        sp.Popen([self.nssm, "set",service_name,"AppParameters","sdc.py"])
        return True

    def restart_service(self,service_name):
        try:
            os.system(f'net stop {service_name}')
        except:
            print ('could not stop service {}'.format(service_name))
        try:
            os.system(f'net start {service_name}')
        except:
            print ('could not start service {}'.format(service_name))
        return True
    def schedule_restart(self):
        temFile = f"{self.sdc_home_dir}\\pending_restart"
        with open(temFile, "w") as f:
            f.write("True")
    def schedule_shutdown(server_status):
        temFile = f"{server_status['sdc_home_dir']}\\pending_shutdown"
        with open(temFile, "w") as f:
            f.write("True")
    def check_schd_restart(server_status):
        temFile = server_status['sdc_home_dir']+"\\pending_restart"
        if exists(temFile):
            return True
        else:
            return False
    def check_schd_shutdown(server_status):
        temFile = server_status['sdc_home_dir']+"\\pending_shutdown"
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
        networking = ["svr_proxyPort","svr_proxyRemoteVoicePort"]
        for i in networking:
            temp_port = self.base[i]
            temp_port = temp_port.strip('"')
            temp_port = int(temp_port)
            temp_port = temp_port + iter
            self.startup.update({i:f'"{temp_port}"'})
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
            self.startup.update({'svr_proxyLocalVoicePort':f'"{tem_voice_port}"'})
            self.startup.update({'svr_voicePortEnd':f'"{tem_voice_port}"'})
            self.startup.update({'svr_voicePortStart':f'"{tem_voice_port}"'})
            print("svr_port: " + str(tem_game_port))
            print("voice_port: " + str(tem_voice_port))
            if self.dataDict['use_proxy']=='True':
                self.startup.update({"man_enableProxy":f'"true"'})
            else:
                self.startup.update({"man_enableProxy":f'"false"'})
            self.startup.update({"svr_name":f'"{serverHoster} {str(svr_identifier)}"'})
            self.startup.update({"svr_location":f'"{location}"'})
            self.startup.update({"svr_ip":f'"{svr_ip}"'})
            self.startup.update({"svr_login":f'"{master_user}"'})
            self.startup.update({"svr_password":f'"{master_pass}"'})
            self.startup.update({"svr_desc":f'"{svr_desc}"'})
        elif type == "proxy":
            self.proxy.update({'redirectIP':'127.0.0.1'})
            self.proxy.update({'publicip':svr_ip})
            self.proxy.update({'publicPort':self.startup['svr_proxyPort']})
            self.proxy.update({'redirectPort':self.startup['svr_port']})
            self.proxy.update({'voiceRedirectPort':self.startup['svr_proxyLocalVoicePort']})
            self.proxy.update({'voicePublicPort':self.startup['svr_proxyRemoteVoicePort']})
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
    def configureEnvironment(self,configLoc,force_update):
        global hon_api_updated
        global players_connected
        global tex
        self.bot_version = float(self.bot_version)
        bot_needs_update = False
        bot_first_launch = False
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
                if not exists(f"{self.hon_directory}\\HON_SERVER_{self.svr_id}.exe") or force_update == True or bot_needs_update == True:
                    try:
                        shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\kongor.exe",f"{self.hon_directory}HON_SERVER_{self.svr_id}.exe")
                        shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\hon_x64.exe",f"{self.hon_directory}hon_x64.exe")
                        print("copying server exe...")
                    except: print("server in use, can't replace exe, will try again when server is stopped.")
            if self.dataDict['master_server'] == "kongor.online:666":
                if not exists(f"{self.hon_directory}\\KONGOR_ARENA_{self.svr_id}.exe") or force_update == True or bot_needs_update == True:
                    try:
                        shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\kongor.exe",f"{self.hon_directory}KONGOR_ARENA_{self.svr_id}.exe")
                        shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\hon_x64.exe",f"{self.hon_directory}hon_x64.exe")
                        print("copying server exe...")
                    except: print("server in use, can't replace exe, will try again when server is stopped.")
            self.secrets = initialise.KOTF(self)
            if self.secrets:
                self.svr_desc = self.secrets.split(',')[0]
                self.svr_desc = self.svr_desc.replace('\n','')
                self.master_user = self.secrets.split(',')[1]
                self.master_user = self.master_user.replace('\n','')
                self.master_pass = self.secrets.split(',')[2]
                self.master_pass = self.master_pass.replace('\n','')
            if not exists(f"{self.hon_game_dir}\\startup.cfg"):
            #   below commented as we are no longer using game_settings_local.cfg
            # if not exists(f"{self.hon_logs_dir}\\..\\startup.cfg") or not exists(f"{self.hon_logs_dir}\\..\\game_settings_local.cfg"):
                print(f"Server {self.service_name_bot} requires full configuration. No existing startup.cfg or game_settings_local.cfg. Configuring...")
            #   below commented as we are no longer using game_settings_local.cfg
            #initialise.create_config(self,f"{self.hon_logs_dir}\\..\\startup.cfg",f"{self.hon_logs_dir}\\..\\game_settings_local.cfg",self.svr_id,self.svr_hoster,self.svr_region,self.svr_total,self.svr_ip)
            initialise.create_config(self,f"{self.hon_game_dir}\\startup.cfg","startup",self.dataDict['game_starting_port'],self.dataDict['voice_starting_port'],self.svr_id,self.svr_hoster,self.svr_region_short,self.svr_total,self.svr_ip,self.master_user,self.master_pass,self.svr_desc)
            initialise.create_config(self,f"{self.hon_game_dir}\\proxy_config.cfg","proxy",self.dataDict['game_starting_port'],self.dataDict['voice_starting_port'],self.svr_id,self.svr_hoster,self.svr_region_short,self.svr_total,self.svr_ip,self.master_user,self.master_pass,self.svr_desc)
            print(f"copying {self.service_name_bot} script and related configuration files to HoN environment: "+ self.hon_home_dir + "..")
            #config = ["sdc.py","multiguild.py"]
            # for i in config:
            #     if exists(os.path.abspath(application_path)+"\\"+i):
            #         shutil.copy(os.path.abspath(application_path)+"\\"+i,self.sdc_home_dir+"\\"+i)
            shutil.copy(os.path.abspath(application_path)+"\\sdc.py", f'{self.sdc_home_dir}\\sdc.py')
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
            # if not exists(f"{self.hon_directory}{self.dataDict['player_count_exe']}" or force_update == True or bot_needs_update == True):
            try:
                shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\{self.dataDict['player_count_exe']}",f"{self.hon_directory}{self.dataDict['player_count_exe']}")
            except Exception as e: print(e)
            print("copying other dependencies...")
            if not exists(f"{self.hon_directory}\\nssm.exe"):
                shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\nssm.exe",f"{self.hon_directory}\\nssm.exe")
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
                                shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\API_HON_SERVER.exe",f"{self.hon_directory}API_HON_SERVER.exe")
                            except PermissionError:
                                tex.insert(END,"COULD NOT UPGRADE SERVICE: " + self.service_name_api +" The service is currently runing so we cannot replace this file. We'll try again later\n")
                                print("COULD NOT UPGRADE SERVICE: " + self.service_name_api +" The service is currently runing so we cannot replace this file. We'll try again later\n")
                            except: print(traceback.format_exc())
                        if initialise.configure_service_api(self,self.service_name_api):
                            hon_api_updated = True
                        time.sleep(1)
                        initialise.start_service(self,self.service_name_api)
                else:
                    if (force_update ==True or bot_needs_update == True) and hon_api_updated !=True:
                        try:
                            shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\API_HON_SERVER.exe",f"{self.hon_directory}API_HON_SERVER.exe")
                        except PermissionError:
                            tex.insert(END,"COULD NOT UPGRADE SERVICE: " + self.service_name_api +" The service is currently in use so we cannot replace this file. We'll try again later\n")
                            print("COULD NOT UPGRADE SERVICE: " + self.service_name_api +" The service is currently runing so we cannot replace this file. We'll try again later\n")
                        except: print(traceback.format_exc())
                        #shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\API_HON_SERVER.exe",f"{self.hon_directory}API_HON_SERVER.exe")
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
                        tex.insert(END,"HON Registration API STATUS: " + self.service_name_api +":  FAILED TO START!\n")
                    print("==========================================")
            else:
                bot_needs_update = True
                print("==========================================")
                print(f"Creating hon server registration API: {self.service_name_api}..")
                print("==========================================")
                initialise.create_service_api(self,self.service_name_api)
                print("starting service.. " + self.service_name_api)
                initialise.start_service(self,self.service_name_api)
                print("==========================================")
                print("HON Registration API STATUS: " + self.service_name_api)
                service_api = initialise.get_service(self.service_name_api)
                if service_api['status'] == 'running':
                    tex.insert(END,"HON Registration API STATUS: " + self.service_name_api +": RUNNING\n")
                else:
                    tex.insert(END,"HON Registration API STATUS: " + self.service_name_api +":  FAILED TO START!\n")
                print("==========================================")
        
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
                    if playercount == 0 or playercount == -3:
                        print("No players connected, safe to restart...")
                        initialise.stop_service(self,self.service_name_bot)
                        if self.dataDict['master_server'] == "honmasterserver.com":
                            try:
                                shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\kongor.exe",f"{self.hon_directory}HON_SERVER_{self.svr_id}.exe")
                                print("copying server exe...")
                            except Exception as e: print(e + "can't replace exe.")
                        if self.dataDict['master_server'] == "kongor.online:666":
                            try:
                                shutil.copy(os.path.abspath(application_path)+f"\\dependencies\\server_exe\\kongor.exe",f"{self.hon_directory}KONGOR_ARENA_{self.svr_id}.exe")
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
                    tex.insert(END,f"HONSERVER STATUS: {self.service_name_bot} FAILED TO START!\n")
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
                tex.insert(END,f"{self.service_name_bot}: {playercount} Players are connected, scheduling restart for after the current match finishes..\n")
                print(f"{self.service_name_bot}: {playercount} Players are connected, scheduling restart for after the current match finishes..\n")
            if self.dataDict['use_proxy'] == 'False':
                tex.insert(END,f"Server ports: Game ({self.startup['svr_port']}), Voice ({self.startup['svr_proxyLocalVoicePort']})\n")
            elif self.dataDict['use_proxy'] == 'True':
                tex.insert(END,f"Server ports (PROXY): Game ({self.startup['svr_proxyPort']}), Voice ({self.startup['svr_proxyRemoteVoicePort']})\n")
            print("==========================================")
        else:
            print("==========================================")
            tex.insert(END,f"ADMINBOT{self.svr_id} v{self.bot_version}\n")
            tex.insert(END,"NO UPDATES OR CONFIGURATION CHANGES MADE\n")
            #tex.insert(END,"==============================================\n")
        bot_needs_update = False
        players_connected = False

class honfigurator():
    global tex
    def __init__(self):
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
        
    def sendData(self,identifier,hoster, region, regionshort, serverid, servertotal,hondirectory, bottoken,discordadmin,master_server,force_update,use_proxy,game_port,voice_port,core_assignment,process_priority,botmatches,debug_mode,selected_branch,increment_port):
        global config_local
        global config_global
        conf_local = configparser.ConfigParser()
        conf_global = configparser.ConfigParser()
        #   adds a trailing slash to the end of the path if there isn't one. Required because the code breaks if a slash isn't provided
        hondirectory = os.path.join(hondirectory, '')
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
        if use_proxy == True:
            if not exists(self.dataDict['proxy_exe']):
                tex.insert(END,f"NO PROXY.EXE FOUND. Please obtain this and place it into {self.dataDict['hon_directory']} and try again. Continuing with proxy disabled..\n")
                use_proxy=False
            else:
                firewall = initialise.configure_firewall(self,"HoN Proxy",self.dataDict['proxy_exe'])
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
            initialise().configureEnvironment(self,force_update)
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
                initialise().configureEnvironment(self,force_update)
                hon_api_updated = False
        #tex.insert(END,f"Updated {self.service_name_bot} to version v{self.bot_version}.\n")
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
        applet.Label(tab1, text="Total Servers:",background=maincolor,foreground='white').grid(column=1, row=4,sticky="e")
        self.tab1_servertd = applet.Combobox(tab1,foreground=textcolor,value=self.corecount(),textvariable=self.svr_total_var,width=5)
        self.tab1_servertd.grid(column= 2 , row = 4,sticky="w",pady=4)
        self.svr_total_var.trace_add('write', self.svr_num_link)
        #  one or two cores
        self.core_assign = tk.StringVar(app,self.dataDict['core_assignment'])
        applet.Label(tab1, text="CPU cores assigned per server:",background=maincolor,foreground='white').grid(column=0, row=7,sticky="e",padx=[20,0])
        tab1_core_assign = applet.Combobox(tab1,foreground=textcolor,value=self.coreassign(),textvariable=self.core_assign)
        tab1_core_assign.grid(column= 1, row = 7,sticky="w",pady=4)
        self.core_assign.trace_add('write', self.coreadjust)
        #   
        #   Simple Server data
        applet.Label(tab1, text="Hon Server Data",background=maincolor,foreground='white').grid(columnspan=1,column=1, row=1,sticky="w")
        #   hoster
        applet.Label(tab1, text="Server Name:",background=maincolor,foreground='white').grid(column=0,row=2,sticky="e")
        tab1_hosterd = applet.Entry(tab1,foreground=textcolor)
        tab1_hosterd.insert(0,self.dataDict['svr_hoster'])
        tab1_hosterd.grid(column= 1 , row = 2,sticky="w",pady=4)
        #
        #   region
        self.svr_loc = tk.StringVar(app,self.dataDict["svr_region"])
        applet.Label(tab1, text="Location:",background=maincolor,foreground='white').grid(column=0, row=3,sticky="e")
        tab1_regiond = applet.Combobox(tab1,foreground=textcolor,value=self.regions()[0],textvariable=self.svr_loc)
        tab1_regiond.grid(column= 1 , row = 3,sticky="w",pady=4)
        self.svr_loc.trace_add('write', self.reg_def_link)
        #   regionId
        self.svr_reg_code = tk.StringVar(app,self.dataDict["svr_region_short"])
        applet.Label(tab1, text="Region Code:",background=maincolor,foreground='white').grid(column=1, row=3,sticky="e")
        tab1_regionsd = applet.Combobox(tab1,foreground=textcolor,value=self.regions()[1],textvariable=self.svr_reg_code,width=5)
        tab1_regionsd.grid(column= 2 , row = 3,sticky="w",pady=4)
        self.svr_reg_code.trace_add('write', self.reg_def_link)
        #   server id
        self.svr_id_var = tk.StringVar(app,self.dataDict['svr_id'])
        applet.Label(tab1, text="Server ID:",background=maincolor,foreground='white').grid(column=0, row=4,sticky="e")
        self.tab1_serveridd = applet.Combobox(tab1,foreground=textcolor,value=self.corecount(),textvariable=self.svr_id_var)
        self.tab1_serveridd.grid(column= 1 , row = 4,sticky="w",pady=4)
        self.svr_id_var.trace_add('write', self.svr_num_link)
        
        #   HoN Directory
        applet.Label(tab1, text="HoN Directory:",background=maincolor,foreground='white').grid(column=0, row=10,sticky="e",padx=[20,0])
        tab1_hondird = applet.Entry(tab1,foreground=textcolor,width=45)
        tab1_hondird.insert(0,self.dataDict['hon_directory'])
        tab1_hondird.grid(column= 1, row = 10,sticky="w",pady=4)
        #  HoN master server
        self.master_server = tk.StringVar(app,self.dataDict['master_server'])
        applet.Label(tab1, text="HoN Master Server:",background=maincolor,foreground='white').grid(column=0, row=5,sticky="e",padx=[20,0])
        tab1_masterserver = applet.Combobox(tab1,foreground=textcolor,value=self.masterserver(),textvariable=self.master_server)
        tab1_masterserver.grid(column= 1, row = 5,sticky="w",pady=4)
        
        #  one or two cores
        self.priority = tk.StringVar(app,self.dataDict['process_priority'])
        applet.Label(tab1, text="In-game CPU process priority:",background=maincolor,foreground='white').grid(column=0, row=6,sticky="e",padx=[20,0])
        tab1_priority = applet.Combobox(tab1,foreground=textcolor,value=self.priorityassign(),textvariable=self.priority)
        tab1_priority.grid(column= 1, row = 6,sticky="w",pady=4)
        #  increment ports
        self.increment_port = tk.StringVar(app,self.dataDict['incr_port_by'])
        applet.Label(tab1, text="Increment ports by:",background=maincolor,foreground='white').grid(column=1, row=5,sticky="e",padx=[20,0])
        tab1_increment_port = applet.Combobox(tab1,foreground=textcolor,value=self.incrementport(),textvariable=self.increment_port,width=5)
        tab1_increment_port.grid(column= 2, row = 5,sticky="w",pady=4)
        #
        #   use proxy
        applet.Label(tab1, text="Use proxy (anti-DDOS):",background=maincolor,foreground='white').grid(column=1, row=9,sticky="e",padx=[20,0])
        self.useproxy = tk.BooleanVar(app)
        if self.dataDict['use_proxy'] == 'True':
            self.useproxy.set(True)
        tab1_useproxy_btn = applet.Checkbutton(tab1,variable=self.useproxy)
        tab1_useproxy_btn.grid(column= 2, row = 9,sticky="w",pady=4)
        # self.useproxy.trace_add('write',self.change_to_proxy2)
        #  starting gameport
        applet.Label(tab1, text="Starting game port:",background=maincolor,foreground='white').grid(column=1,row=6,sticky="e")
        tab1_game_port = applet.Entry(tab1,foreground=textcolor,width=5)
        tab1_game_port.insert(0,self.dataDict['game_starting_port'])
        # self.tab1_game_port.insert(0,self.change_to_proxy())
        tab1_game_port.grid(column=2,row = 6,sticky="w",pady=4)
        #  starting gameport
        applet.Label(tab1, text="Starting voice port:",background=maincolor,foreground='white').grid(column=1,row=7,sticky="e")
        tab1_voice_port = applet.Entry(tab1,foreground=textcolor,width=5)
        tab1_voice_port.insert(0,self.dataDict['voice_starting_port'])
        tab1_voice_port.grid(column=2,row = 7,sticky="w",pady=4)
        #   force update
        applet.Label(tab1, text="Force Update:",background=maincolor,foreground='white').grid(column=0, row=9,sticky="e",padx=[20,0])
        self.forceupdate = tk.BooleanVar(app)
        tab1_forceupdate_btn = applet.Checkbutton(tab1,variable=self.forceupdate)
        tab1_forceupdate_btn.grid(column= 1, row = 9,sticky="w",pady=4)
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
        tab1_singlebutton = applet.Button(tab1, text="Configure Single Server",command=lambda: self.sendData("single",tab1_hosterd.get(),tab1_regiond.get(),tab1_regionsd.get(),self.tab1_serveridd.get(),self.tab1_servertd.get(),tab1_hondird.get(),tab1_bottokd.get(),tab1_discordadmin.get(),tab1_masterserver.get(),self.forceupdate.get(),self.useproxy.get(),tab1_game_port.get(),tab1_voice_port.get(),self.core_assign.get(),self.priority.get(),self.botmatches.get(),self.debugmode.get(),self.git_branch.get(),self.increment_port.get()))
        tab1_singlebutton.grid(columnspan=1,column=1, row=13,stick='n',padx=[10,0],pady=[20,10])
        tab1_allbutton = applet.Button(tab1, text="Configure All Servers",command=lambda: self.sendData("all",tab1_hosterd.get(),tab1_regiond.get(),tab1_regionsd.get(),self.tab1_serveridd.get(),self.tab1_servertd.get(),tab1_hondird.get(),tab1_bottokd.get(),tab1_discordadmin.get(),tab1_masterserver.get(),self.forceupdate.get(),self.useproxy.get(),tab1_game_port.get(),tab1_voice_port.get(),self.core_assign.get(),self.priority.get(),self.botmatches.get(),self.debugmode.get(),self.git_branch.get(),self.increment_port.get()))
        tab1_allbutton.grid(columnspan=1,column=2, row=13,stick='n',padx=[0,20],pady=[20,10])
        tab1_updatebutton = applet.Button(tab1, text="Update HoNfigurator",command=lambda: self.update_repository(NULL,NULL,NULL))
        tab1_updatebutton.grid(columnspan=1,column=3, row=13,stick='n',padx=[20,0],pady=[20,10])
        
        """
        
        This is the advanced server setup tab
        ui
        """
        # logolabel_tab2 = applet.Label(tab2,text="HoNfigurator",background=maincolor,foreground='white',image=honlogo)
        # logolabel_tab2.grid(columnspan=2,column=, row=0,sticky="n",pady=[10,0])
        
        """
        
        This is the bot command center tab
        
        """

        ButtonString = ['View Log', 'Start', 'Stop', 'Clean', 'Uninstall']
        LablString = ['hon_server_','test','space']

        # Calling this function from somewhere else via Queue
        import fnmatch
        import glob
        
        def get_size(start_path):
                total_size = 0
                for dirpath, dirnames, filenames in os.walk(start_path):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        # skip if it is symbolic link
                        if not os.path.islink(fp):
                            total_size += os.path.getsize(fp)
                return total_size
        def viewButton(btn,i,pcount):
            print(f"{i} {btn}")
            service_name = f"adminbot{i}"
            server_status = dmgr.mData.returnDict_basic(self,i)
            def ViewLog():
                dir_name = f"{server_status['hon_logs_dir']}\\"
                if pcount > 0:
                    log_File = "Slave-1_M*console.clog"
                else:
                    log_File = "Slave*.log"
                list_of_files = glob.glob(dir_name + log_File) # * means all if need specific format then *.csv
                latest_file = max(list_of_files, key=os.path.getctime)
                print(latest_file)
                f = open(latest_file, "r", encoding='utf-16-le')
                text = f.read()
                tex.insert(tk.END, text)
                tex.see(tk.END)
                #app.after(3000,ViewLog)
            def Start():
                service = initialise.get_service(service_name)
                if service['status'] == 'stopped':
                    if initialise.start_service(self,service_name):
                        tex.insert(END,f"{service_name} started successfully.\n")
                        app.after(10000,refresh)
                    else:
                        tex.insert(END,f"{service_name} failed to start.\n")
            def Stop():
                if pcount <= 0:
                    if initialise.stop_service(self,service_name):
                        tex.insert(END,f"{service_name} stopped successfully.\n")
                        load_server_mgr()
                    else:
                        tex.insert(END,f"{service_name} failed to stop.\n")
                else:
                    print("[ABORT] players are connected. Scheduling shutdown instead..")
                    initialise.schedule_shutdown(server_status)
            def Clean():
                paths = [f"{server_status['hon_logs_dir']}",f"{server_status['hon_logs_dir']}\\diagnostics"]
                now = time.time()
                for path in paths:
                    for f in os.listdir(path):
                        f = os.path.join(path, f)
                        if os.stat(f).st_mtime < now - 7 * 86400:
                            if os.path.isfile(f):
                                os.remove(os.path.join(path, f))
                                print("removed "+f)
                replays = f"{server_status['hon_game_dir']}\\replays"
                for f in os.listdir(replays):
                    f = os.path.join(replays, f)
                    if os.stat(f).st_mtime < now - 7 * 86400:
                        if os.path.isfile(f):
                            os.remove(os.path.join(replays, f))
                            print("removed "+f)
                        else:
                            shutil.rmtree(f,onerror=honfigurator.onerror)
                            print("removed "+f)
                print("DONE.")
            def Uninstall(x):
                if pcount <= 0:
                    service_state = initialise.get_service(service_name)
                    if service_state != False and service_state['status'] != 'stopped':
                        if initialise.stop_service(self,service_name):
                            tex.insert(END,f"{service_name} stopped successfully.\n")
                            load_server_mgr()
                        else:
                            tex.insert(END,f"{service_name} failed to stop.\n")
                    service_state = initialise.get_service(service_name)
                    if service_state == False or service_state['status'] == 'stopped':
                        try:
                            #shutil.copy(f"{server_status['sdc_home_dir']}\\cogs\\total_games_played")
                            rem = shutil.rmtree(server_status['hon_home_dir'],onerror=honfigurator.onerror)
                            tex.insert(END,f"removed files: {server_status['hon_home_dir']}")
                        except Exception as e:
                            print(e)
                        try:
                            remove_service = subprocess.run(['sc.exe','delete',f'adminbot{x}'])
                        except Exception as e:
                            print(e)
                else:
                    print("[ABORT] players are connected. You must stop the service before uninstalling..")
                    tex.insert(END,"[ABORT] players are connected. You must stop the service before uninstalling..\n")
                    initialise.schedule_shutdown(server_status)


            def Tools():
                pass
            if btn == "View Log":
                ViewLog()
            elif btn == "Stop":
                Stop()
            elif btn == "Start":
                Start()
            elif btn == "Clean":
                Clean()
            elif btn == "Uninstall":
                Uninstall(i)
        def refresh(*args):
            if (tabgui.index("current")) == 1:
                load_server_mgr()
        tex = tk.Text(app,foreground=textcolor,background=textbox,height=15)
        #app.attributes("-topmost",True)
        def load_server_mgr(*args):
            # if (tabgui.index("current")) == 1:
            app.lift()
            i=0
            c=0
            c_len = len(ButtonString)+len(LablString)
            mod=11
            # create a grid of 2x6
            for t in range(20):
                tab2.rowconfigure(t, weight=1,pad=0)
            for o in range(100):
                tab2.columnconfigure(o, weight=1,pad=0)
            for x in range(0,int(self.dataDict['svr_total'])):
                x+=1
                i+=1
                service_name = f"adminbot{x}"
                server_status = dmgr.mData.returnDict_basic(self,x)
                dir_name = f"{server_status['hon_logs_dir']}\\"
                file = "Slave*.log"
                try:
                    list_of_files = glob.glob(dir_name + file) # * means all if need specific format then *.csv
                    log = max(list_of_files, key=os.path.getctime)
                except Exception as e:
                    print(e)
                cookie = True
                cookie = svrcmd.honCMD.check_cookie(server_status,log,"honfigurator_log_check")
                schd_restart = False
                schd_shutdown = False
                schd_restart=initialise.check_schd_restart(server_status)
                schd_shutdown=initialise.check_schd_shutdown(server_status)
                service_state = initialise.get_service(service_name)
                pcount = initialise.playerCountX(self,x)
                #
                # when total servers goes over <num>, move to the next column, and set row back to 1.
                if i%mod==0:
                    c+=c_len
                    i=1
                LablString[0]=f"hon_server_{x}"
                # LablString[2]=get_size(server_status['hon_home_dir'])
                # LablString[2] = f"{LablString[2]/float(1<<30):,.0f} GB"
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
                    if service_state is not None:
                        if service_state == False or service_state['status'] == 'stopped':
                            colour = 'OrangeRed4'
                            LablString[1]=f"Stopped"
                    c_pos1 = index1 + c
                    if index1==0:
                        labl = Label(tab2,width=12,text=f"{labl_name}", background=colour, foreground='white')
                    elif index1==1:
                        labl = Label(tab2,width=14,text=f"{labl_name}", background=colour, foreground='white')
                    labl.grid(row=i, column=c_pos1)
                    for index2, btn_name in enumerate(ButtonString):
                        index2 +=len(LablString)
                        c_pos2 = index2 + c
                        btn = Button(tab2,text=btn_name, command=partial(viewButton,btn_name,x,pcount))
                        btn.grid(row=i, column=c_pos2)
                    # tab2.grid_columnconfigure(x,weight=0,pad=4)
            # for o in range(1,c_len+c):
            #     tab2.grid_columnconfigure(o,weight=0,pad=4)
            # for o in range(1,mod):
            #     tab2.grid_rowconfigure(o, weight=0,pad=4)
                #print(tabgui.index("current"))
            # if (tabgui.index("current")) == 1:
            #     app.after(10000,load_server_mgr)
            column_rows=(tab2.grid_size())
            total_columns=column_rows[0]
            # for o in range(1,total_columns):
            #     tab2.grid_columnconfigure(o, weight=1,pad=4)
            total_rows=column_rows[1]
            print(column_rows)
            logolabel_tab2 = applet.Label(tab2,text="HoNfigurator",background=maincolor,foreground='white',image=honlogo)
            logolabel_tab2.grid(columnspan=total_columns,column=0, row=0,pady=[10,0],sticky='n')
            
            tab2_refresh = applet.Button(tab2, text="Refresh",command=lambda: refresh())
            tab2_refresh.grid(columnspan=total_columns,column=0, row=mod+1,sticky='n',padx=[10,0],pady=[20,10])
        tex.grid(row=14, column=0, sticky="sew")
        app.grid_rowconfigure(0, weight=1)
        app.grid_columnconfigure(0, weight=1)
        # tab1_startBot.grid(columnspan=3, column=1, row=9,stick='n',padx=[0,10],pady=[20,10])
        # tab1_startall = applet.Button(tab1, text="Configure All Servers",command=lambda: self.sendData("all",tab1_hosterd.get(),tab1_regiond.get(),tab1_regionsd.get(),self.tab1_serveridd.get(),self.tab1_servertd.get(),tab1_hondird.get(),tab1_bottokd.get(),tab1_discordadmin.get(),tab1_masteruser.get(),tab1_masterpass.get(),self.forceupdate.get()))
        # tab1_startall.grid(columnspan=4, column=1, row=9,stick='n',padx=[10,0],pady=[20,10])




        # files = [] #creates list to replace your actual inputs for troubleshooting purposes
        # btn = [] #creates list to store the buttons ins

        # for i in range(50): #this just popultes a list as a replacement for your actual inputs for troubleshooting purposes
        #     files.append("Button"+str(i))

        # for i in range(len(files)): #this says for *counter* in *however many elements there are in the list files*
        #     #the below line creates a button and stores it in an array we can call later, it will print the value of it's own text by referencing itself from the list that the buttons are stored in
        #     btn.append(Button(test, text=files[i], command=lambda c=i: print(btn[c].cget("text"))))
        #    btn[i].pack() #this packs the buttons




        #self.botCount(int(self.dataDict['svr_total']))
        #load_server_mgr()
        tabgui.select(0)
        self.update_repository(NULL,NULL,NULL)
        tabgui.bind('<<NotebookTabChanged>>',refresh)
        app.mainloop()
test = honfigurator()
test.creategui()