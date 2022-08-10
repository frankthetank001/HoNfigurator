
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

config_global = os.path.dirname(os.path.realpath(__file__))+"\\config\\global_config.ini"
config_default = os.path.dirname(os.path.realpath(__file__))+"\\config\\default_config.ini"
config_local = os.path.dirname(os.path.realpath(__file__))+"\\config\\local_config.ini"
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
        self.master_user = self.dataDict['master_user']
        self.master_pass = self.dataDict['master_pass']
        self.service_name_bot = f"adminbot{self.svr_id}"
        self.service_name_api = "honserver-registration"
        if exists(config_global):
            config = configparser.ConfigParser()
            config.read(config_global)
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
    def get_startupcfg(self):
        config_startup = dmgr.mData().parse_config(os.path.dirname(os.path.realpath(__file__))+"\\config\\honfig.ini")
        return config_startup
    def get_service(service_name):
        service = None
        try:
            service = psutil.win_service_get(service_name)
            service = service.as_dict()
        except Exception as ex:
            # raise psutil.NoSuchProcess if no service with such name exists
            print(f"{service_name} does not exist")
            #print(str(ex))
        return service
    def playerCount(self):
        check = subprocess.Popen([self.dataDict['player_count_exe'],self.dataDict['hon_file_name']],stdout=subprocess.PIPE, text=True)
        i = int(check.stdout.read())
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
    def parse_config(self,filename):
        svr_options = ["svr_port","svr_name","svr_location","man_port","man_startServerPort","man_endServerPort","svr_proxyLocalVoicePort","svr_proxyPort","svr_proxyRemoteVoicePort","svr_voicePortEnd","svr_voicePortStart","man_cowServerPort","man_cowVoiceProxyPort"]
        COMMENT_CHAR = '#'
        OPTION_CHAR =  ' '
        options = {}
        f = open(filename)
        for line in f:
            for i in svr_options:
                if i in line:
                    #First, remove comments:
                    # remove garbage
                    line=line.replace("SetSave ","")
                    line=line.strip(" \"0\"\n")
                    line=line.replace('"','')
                    if COMMENT_CHAR in line:
                        # split on comment char, keep only the part before
                        line, comment = line.split(COMMENT_CHAR, 1)
                    # Second, find lines with an option=value:
                    if OPTION_CHAR in line:
                        # split on option char:
                        option, value = line.split(OPTION_CHAR, 1)
                        # strip spaces:
                        option = option.strip()
                        value = value.strip()
                        # store in dictionary:
                        options[option] = value
                        print (option +": "+ value)
        f.close()
        return options

    def create_config(self,filename,serverID,serverHoster,location,svr_total,svr_ip):
        iter = self.dataDict['incr_port']
        svr_identifier = self.dataDict['svrid_total']
        print("customising startup.cfg with the following values")
        print("svr_id: " + str(serverID))
        print("svr_host: " + str(serverHoster))
        print("svr_location: " + str(location))
        print("svr_total: " + str(svr_total))
        print("svr_ip: " + str(svr_ip))
        #self.startup = dmgr.mData.parse_config(self,os.path.dirname(os.path.realpath(__file__))+"\\config\\honfig.ini")
        networking = ["svr_port","svr_proxyLocalVoicePort","svr_proxyPort","svr_proxyRemoteVoicePort","svr_voicePortEnd","svr_voicePortStart"]
        for i in networking:
            temp_port = self.startup[i]
            temp_port = temp_port.strip('"')
            temp_port = int(temp_port)
            temp_port = temp_port + iter
            self.startup.update({i:f'"{temp_port}"'})
        self.startup.update({"man_enableProxy":"false"})
        self.startup.update({"svr_name":serverHoster + " " + str(svr_identifier)})
        self.startup.update({"svr_location":location})
        self.startup.update({"svr_ip":svr_ip})
        self.startup.update({"svr_login":self.master_user})
        self.startup.update({"svr_password":self.master_pass})
        print (temp_port)
        dmgr.mData.setData(NULL,filename,self.startup)
        return True

    def configureEnvironment(self,configLoc,force_update):
        global hon_api_updated
        global players_connected
        global guilog

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
        guilog.insert(END,f"================= {self.service_name_bot} ===================\n")

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
            initialise.parse_config(self,f"{self.hon_game_dir}\\startup.cfg")
        if not exists(f"{self.hon_game_dir}\\startup.cfg") or bot_first_launch == True or bot_needs_update == True or force_update == True:
        #   below commented as we are no longer using game_settings_local.cfg
        #if not exists(f"{{hon_game_dir}\\startup.cfg") or not exists(f"{self.hon_logs_dir}\\..\\game_settings_local.cfg") or bot_first_launch == True or bot_needs_update == True or force_update == True:
            if bot_needs_update or force_update == True:
                #guilog.insert(END,"==========================================\n")
                guilog.insert(END,f"FORCE or UPDATE DETECTED, APPLYING v{self.bot_version}\n")
                #guilog.insert(END,"==========================================\n")
            if not exists(f"{self.hon_game_dir}\\startup.cfg"):
            #   below commented as we are no longer using game_settings_local.cfg
            # if not exists(f"{self.hon_logs_dir}\\..\\startup.cfg") or not exists(f"{self.hon_logs_dir}\\..\\game_settings_local.cfg"):
                print(f"Server {self.service_name_bot} requires full configuration. No existing startup.cfg or game_settings_local.cfg. Configuring...")
            #   below commented as we are no longer using game_settings_local.cfg
            #initialise.create_config(self,f"{self.hon_logs_dir}\\..\\startup.cfg",f"{self.hon_logs_dir}\\..\\game_settings_local.cfg",self.svr_id,self.svr_hoster,self.svr_region,self.svr_total,self.svr_ip)
            initialise.create_config(self,f"{self.hon_game_dir}\\startup.cfg",self.svr_id,self.svr_hoster,self.svr_region,self.svr_total,self.svr_ip)
            print(f"copying {self.service_name_bot} script and related configuration files to HoN environment: "+ self.hon_home_dir + "..")
            #config = ["sdc.py","multiguild.py"]
            # for i in config:
            #     if exists(os.path.dirname(os.path.realpath(__file__))+"\\"+i):
            #         shutil.copy(os.path.dirname(os.path.realpath(__file__))+"\\"+i,self.sdc_home_dir+"\\"+i)
            shutil.copy(os.path.dirname(os.path.realpath(__file__))+"\\sdc.py", f'{self.sdc_home_dir}\\sdc.py')
            #shutil.copy(os.path.dirname(os.path.realpath(__file__))+"\\sdc.py", f'{self.sdc_home_dir}\\sdc.py')
            distutils.dir_util.copy_tree(os.path.dirname(os.path.realpath(__file__))+"\\cogs\\", f'{self.sdc_home_dir}\\cogs\\')
            distutils.dir_util.copy_tree(os.path.dirname(os.path.realpath(__file__))+"\\config\\", f'{self.sdc_home_dir}\\config\\')
            #
            #   FIX BELOW
            distutils.dir_util.copy_tree(os.path.dirname(os.path.realpath(__file__))+"\\icons\\", f'{self.sdc_home_dir}\\icons\\')
            #shutil.copy(os.path.dirname(os.path.realpath(__file__))+"\\multiguild.py", f'{self.sdc_home_dir}\\multiguild.py')
            #shutil.copy(configLoc,f"{self.sdc_home_dir}\\config\\sdc.ini")
            #shutil.copy(os.path.dirname(os.path.realpath(__file__))+"\\config\\honfig.py",f"{self.sdc_home_dir}\\config\\honfig.py")
            print("Done!")
            print("Checking and creating required dependencies...")
            if not exists(f"{self.hon_directory}\\HON_SERVER_{self.svr_id}.exe"):
                shutil.copy(os.path.dirname(os.path.realpath(__file__))+f"\\dependencies\\server_exe\\HON_SERVER_1.exe",f"{self.hon_directory}\\HON_SERVER_{self.svr_id}.exe")
                print("copying server exe...")
            #if not exists(f"{self.hon_directory}\\API_HON_SERVER.exe"):
            # shutil.copy(os.path.dirname(os.path.realpath(__file__))+f"\\dependencies\\server_exe\\API_HON_SERVER.exe",f"{self.hon_directory}API_HON_SERVER.exe")
            print("copying master server registration API...")
            if not exists(f"{self.hon_directory}\\eko-pid.exe"):
                shutil.copy(os.path.dirname(os.path.realpath(__file__))+f"\\dependencies\\server_exe\\eko-pid.exe",f"{self.hon_directory}\\eko-pid.exe")
                print("copying other dependencies...")
            if not exists(f"{self.hon_directory}\\eko-name.exe"):
                shutil.copy(os.path.dirname(os.path.realpath(__file__))+f"\\dependencies\\server_exe\\eko-name.exe",f"{self.hon_directory}\\eko-name.exe")
            if not exists(f"{self.hon_directory}\\nssm.exe"):
                shutil.copy(os.path.dirname(os.path.realpath(__file__))+f"\\dependencies\\server_exe\\nssm.exe",f"{self.hon_directory}\\nssm.exe")
            print("Done!")
        service_api = initialise.get_service(self.service_name_api)
        if service_api:
            #print("HON Registration API STATUS: " + self.service_name_api)
            if service_api['status'] == 'running' or service_api['status'] == 'paused':
                if force_update != True and bot_needs_update != True:
                    guilog.insert(END,"HON Registration API STATUS: RUNNING\n")
                elif (force_update == True or bot_needs_update == True) and hon_api_updated !=True:
                    initialise.stop_service(self,self.service_name_api)
                    time.sleep(1)
                    service_api = initialise.get_service(self.service_name_api)
                    if service_api['status'] == 'stopped':
                        try:
                            shutil.copy(os.path.dirname(os.path.realpath(__file__))+f"\\dependencies\\server_exe\\API_HON_SERVER.exe",f"{self.hon_directory}API_HON_SERVER.exe")
                        except PermissionError:
                            guilog.insert(END,"COULD NOT UPGRADE SERVICE: " + self.service_name_api +" The service is currently runing so we cannot replace this file. We'll try again later\n")
                            print("COULD NOT UPGRADE SERVICE: " + self.service_name_api +" The service is currently runing so we cannot replace this file. We'll try again later\n")
                        except: print(traceback.format_exc())
                    if initialise.configure_service_api(self,self.service_name_api):
                        hon_api_updated = True
                    time.sleep(1)
                    initialise.start_service(self,self.service_name_api)
            else:
                if (force_update ==True or bot_needs_update == True) and hon_api_updated !=True:
                    try:
                        shutil.copy(os.path.dirname(os.path.realpath(__file__))+f"\\dependencies\\server_exe\\API_HON_SERVER.exe",f"{self.hon_directory}API_HON_SERVER.exe")
                    except PermissionError:
                        guilog.insert(END,"COULD NOT UPGRADE SERVICE: " + self.service_name_api +" The service is currently in use so we cannot replace this file. We'll try again later\n")
                        print("COULD NOT UPGRADE SERVICE: " + self.service_name_api +" The service is currently runing so we cannot replace this file. We'll try again later\n")
                    except: print(traceback.format_exc())
                    #shutil.copy(os.path.dirname(os.path.realpath(__file__))+f"\\dependencies\\server_exe\\API_HON_SERVER.exe",f"{self.hon_directory}API_HON_SERVER.exe")
                    if initialise.configure_service_api(self,self.service_name_api):
                        hon_api_updated = True
                    time.sleep(1)
                    initialise.start_service(self,self.service_name_api)
                else:
                    print("Windows Service STARTING...")
                    initialise.start_service(self,self.service_name_api)
                    service_api = initialise.get_service(self.service_name_api)
                if service_api['status'] == 'running':
                    guilog.insert(END,"HON Registration API STATUS: " + self.service_name_api +": RUNNING\n")
                else:
                    guilog.insert(END,"HON Registration API STATUS: " + self.service_name_api +":  FAILED TO START!\n")
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
                guilog.insert(END,"HON Registration API STATUS: " + self.service_name_api +": RUNNING\n")
            else:
                guilog.insert(END,"HON Registration API STATUS: " + self.service_name_api +":  FAILED TO START!\n")
            print("==========================================")
        
        service_bot = initialise.get_service(self.service_name_bot)
        if service_bot:
            print(f"HONSERVER STATUS: {self.service_name_bot}")
            #service_bot = initialise.get_service(self.service_name_bot)
            if service_bot['status'] == 'running' or service_bot['status'] == 'paused':
                guilog.insert(END,f"HONSERVER STATUS: {self.service_name_bot}: RUNNING\n")
                if force_update == True or bot_needs_update == True:
                    #reconfigure service + restart
                    initialise.configure_service_bot(self,self.service_name_bot)
                    time.sleep(1)
                    svr_state = svrcmd.honCMD()
                    svr_state.getDataDict()
                    playercount = initialise.playerCount(self)
                    if playercount <= 0:
                        print("No players connected, safe to restart...")
                        initialise.restart_service(self,self.service_name_bot)
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
                    guilog.insert(END,f"HONSERVER STATUS: {self.service_name_bot} RUNNING\n")
                else:
                    guilog.insert(END,f"HONSERVER STATUS: {self.service_name_bot} FAILED TO START!\n")
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
            #guilog.insert(END,"==============================================\n")
            #guilog.insert(END,f"Updated {self.service_name_bot} to version v{self.bot_version}.\n")
            if players_connected == True:
                #playercount = svr_state.playerCount()
                guilog.insert(END,f"{self.service_name_bot}: {playercount} Players are connected, scheduling restart for after the current match finishes..\n")
                print(f"{self.service_name_bot}: {playercount} Players are connected, scheduling restart for after the current match finishes..\n")
            print("==========================================")
        else:
            print("==========================================")
            guilog.insert(END,f"ADMINBOT{self.svr_id} v{self.bot_version}\n")
            guilog.insert(END,"NO UPDATES OR CONFIGURATION CHANGES MADE\n")
            #guilog.insert(END,"==============================================\n")
        guilog.insert(END,f"Server ports: Game ({self.startup['svr_port']}), Voice ({self.startup['svr_proxyLocalVoicePort']})\n")
        bot_needs_update = False
        players_connected = False

class gui():
    global guilog
    def __init__(self):
        self.initdict = dmgr.mData()
        self.dataDict = self.initdict.returnDict()
        print (self.dataDict)
        return
    # def getConfDict(self):
    #     self.dataDict = dmgr.mData()
    #     print (self.dataDict)
    def corecount(self):
        cores = []
        for i in range(multiprocessing.cpu_count()):
            cores.append(i+1)
        return cores
    def regions(self):
        return [["US - West","US - East","Thailand","Australia","Malaysia"],["USW","USE","TH","AUS","MY"]]
    
    def sendData(self,identifier,hoster, region, regionshort, serverid, servertotal,hondirectory, bottoken,discordadmin,master_server,master_user,master_pass,force_update,botmatches):
        global config_local
        global config_global
        conf_local = configparser.ConfigParser()
        conf_global = configparser.ConfigParser()
        #   adds a trailing slash to the end of the path if there isn't one. Required because the code breaks if a slash isn't provided
        hondirectory = os.path.join(hondirectory, '')

        if identifier == "single":
            print()
            #guilog.insert(END,"==========================================\n")
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
            conf_local.set("OPTIONS","master_user",master_user)
            conf_local.set("OPTIONS","master_pass",master_pass)
            conf_local.set("OPTIONS","allow_botmatches",f'{botmatches}')
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
        if identifier == "all":
            #guilog.insert(END,"==========================================\n")
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
                conf_local.set("OPTIONS","master_user",master_user)
                conf_local.set("OPTIONS","master_pass",master_pass)
                conf_local.set("OPTIONS","allow_botmatches",f'{botmatches}')
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
        #guilog.insert(END,f"Updated {self.service_name_bot} to version v{self.bot_version}.\n")
        return
    def svr_num_link(self,var,index,mode):
        if self.svr_id_var.get() == "(for single server)":
            return
        elif int(self.svr_id_var.get()) > int(self.svr_total_var.get()):
            self.svr_id_var.set(self.svr_total_var.get())
    #def botCount(self,num_of_bots):
        # for i in range(0,num_of_bots):
        #     for i in range(0,num_of_bots):
        #         row = i%8
        #         column1 = (i/8)
        #         column2 = int(column1)*2
        #         if int(column2)==0:
        #             column2 = 1
        #         self.bot_cmd_buttons[i][0].grid(column=int(column1),row=row,sticky='e',padx=[60,0],pady=[10,0])
        #         self.bot_cmd_buttons[i][1].grid(column=column2,row=row,sticky='w',padx=[0,20],pady=[10,0])
        #         self.bot_cmd_buttons[i][1].configure(textvariable=self.bot_cmd_buttons[i][2])
            
                
    def regions(self):
        return [["US - West","US - East","Thailand","Australia","Malaysia"],["USW","USE","TH","AUS","MY"]]
    def reg_def_link(self,var,index,mode):
        reglist = self.regions()
        svrloc = str(self.svr_loc.get()).lower()
        #svrid = str(self.svr_reg_code.get()).lower()
        for reg in reglist[0]:
            if svrloc == reg.lower():
                self.svr_loc.set(reglist[0][reglist[0].index(reg)])
                self.svr_reg_code.set(reglist[1][reglist[0].index(reg)])
    def startServer(self):
        
        return
    def testfunc(self):
        print(self.forceupdate.get())
    def creategui(self):
        global guilog
        app = tk.Tk()
        applet = ttk
        app.title("HoNfigurator")
        #   importing icon
        honico = PhotoImage(file = os.path.dirname(os.path.realpath(__file__))+f"\\icons\\honico.png")
        app.iconphoto(False, honico) 
        honlogo = PhotoImage(file = os.path.dirname(os.path.realpath(__file__))+f"\\icons\\logo.png")
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
        tabgui.add(tab2,text="Advanced Server Setup")
        #tabgui.add(tab3,text="Discord Integration")
        
        """
        creating tooltips
        """

        
        """
        simple server setup tab
        """
        #   title
        logolabel_tab1 = applet.Label(tab1,text="HoNfigurator",background=maincolor,foreground='white',image=honlogo)
        logolabel_tab1.grid(columnspan=5,column=0, row=0,sticky="n",pady=[10,0],padx=[40,0])
        #   
        #   Simple Server data
        applet.Label(tab1, text="Hon Server Data",background=maincolor,foreground='white').grid(columnspan=1,column=1, row=1,sticky="w")
        #   hoster
        applet.Label(tab1, text="Server Hoster:",background=maincolor,foreground='white').grid(column=0,row=2,sticky="e")
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
        applet.Label(tab1, text="Region Code:",background=maincolor,foreground='white').grid(column=0, row=4,sticky="e")
        tab1_regionsd = applet.Combobox(tab1,foreground=textcolor,value=self.regions()[1],textvariable=self.svr_reg_code)
        tab1_regionsd.grid(column= 1 , row = 4,sticky="w",pady=4)
        self.svr_reg_code.trace_add('write', self.reg_def_link)
        #   server id
        self.svr_id_var = tk.StringVar(app,self.dataDict['svr_id'])
        applet.Label(tab1, text="Server ID:",background=maincolor,foreground='white').grid(column=0, row=5,sticky="e")
        tab1_serveridd = applet.Combobox(tab1,foreground=textcolor,value=self.corecount(),textvariable=self.svr_id_var)
        tab1_serveridd.grid(column= 1 , row = 5,sticky="w",pady=4)
        self.svr_id_var.trace_add('write', self.svr_num_link)
        #   server total    
        self.svr_total_var = tk.StringVar(app,self.dataDict['svr_total'])
        applet.Label(tab1, text="Total Servers:",background=maincolor,foreground='white').grid(column=0, row=6,sticky="e")
        tab1_servertd = applet.Combobox(tab1,foreground=textcolor,value=self.corecount(),textvariable=self.svr_total_var)
        tab1_servertd.grid(column= 1 , row = 6,sticky="w",pady=4)
        self.svr_total_var.trace_add('write', self.svr_num_link)
        #   HoN Directory
        applet.Label(tab1, text="HoN Directory:",background=maincolor,foreground='white').grid(column=0, row=7,sticky="e",padx=[20,0])
        tab1_hondird = applet.Entry(tab1,foreground=textcolor,width=40)
        tab1_hondird.insert(0,self.dataDict['hon_directory'])
        tab1_hondird.grid(column= 1, row = 7,sticky="w",pady=4)
        #  HoN master server
        applet.Label(tab1, text="HoN Master Server:",background=maincolor,foreground='white').grid(column=0, row=8,sticky="e",padx=[20,0])
        tab1_masterserver = applet.Entry(tab1,foreground=textcolor,width=40)
        tab1_masterserver.insert(0,self.dataDict['master_server'])
        tab1_masterserver.grid(column= 1, row = 8,sticky="w",pady=4)
        #   HoN master server user
        applet.Label(tab1, text="masterserver user:",background=maincolor,foreground='white').grid(column=0, row=9,sticky="e",padx=[20,0])
        tab1_masteruser = applet.Entry(tab1,foreground=textcolor,width=40)
        tab1_masteruser.insert(0,self.dataDict['master_user'])
        tab1_masteruser.grid(column= 1, row = 9,sticky="w",pady=4)
        #   HoN master user password
        applet.Label(tab1, text="masterserver pass:",background=maincolor,foreground='white').grid(column=0, row=10,sticky="e",padx=[20,0])
        tab1_masterpass = applet.Entry(tab1,foreground=textcolor,width=40)
        tab1_masterpass.insert(0,self.dataDict['master_pass'])
        tab1_masterpass.grid(column= 1, row = 10,sticky="w",pady=4)
        #   force update
        applet.Label(tab1, text="Force Update:",background=maincolor,foreground='white').grid(column=0, row=11,sticky="e",padx=[20,0])
        self.forceupdate = tk.BooleanVar(app)
        tab1_forceupdate_btn = applet.Checkbutton(tab1,variable=self.forceupdate)
        tab1_forceupdate_btn.grid(column= 1, row = 11,sticky="w",pady=4)
        #
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
        #   bot version
        applet.Label(tab1, text="Bot Version:",background=maincolor,foreground='white').grid(column=3, row=5,sticky="e",padx=[20,0])
        applet.Label(tab1,text=self.dataDict['bot_version'],background=maincolor,foreground='white').grid(column= 4, row = 5,sticky="w",pady=4)
        print(self.forceupdate.get())
        

        guilog = tk.Text(tab1,foreground=textcolor,width=70,height=10,background=textbox)
        guilog.grid(columnspan=6,column=0,row=12,sticky="n")
        #   button
        tab1_singlebutton = applet.Button(tab1, text="Configure Single Server",command=lambda: self.sendData("single",tab1_hosterd.get(),tab1_regiond.get(),tab1_regionsd.get(),tab1_serveridd.get(),tab1_servertd.get(),tab1_hondird.get(),tab1_bottokd.get(),tab1_discordadmin.get(),tab1_masterserver.get(),tab1_masteruser.get(),tab1_masterpass.get(),self.forceupdate.get(),self.botmatches.get()))
        tab1_singlebutton.grid(columnspan=3, column=1, row=13,stick='n',padx=[0,10],pady=[20,10])
        tab1_allbutton = applet.Button(tab1, text="Configure All Servers",command=lambda: self.sendData("all",tab1_hosterd.get(),tab1_regiond.get(),tab1_regionsd.get(),tab1_serveridd.get(),tab1_servertd.get(),tab1_hondird.get(),tab1_bottokd.get(),tab1_discordadmin.get(),tab1_masterserver.get(),tab1_masteruser.get(),tab1_masterpass.get(),self.forceupdate.get(),self.botmatches.get()))
        tab1_allbutton.grid(columnspan=4, column=1, row=13,stick='n',padx=[10,0],pady=[20,10])
        
        """
        
        This is the advanced server setup tab
        
        """
        #   
        #   message
        applet.Label(tab2, text="STILL TESTING, DOESN'T DO ANYTHING YET",background=maincolor,foreground='white').grid(columnspan=10,column=0, row=1,sticky="n")
        i=1
        c1=0
        c2=1
        for config_item in config_startup:
            valuename = f"tab2{config_item}"
            startup_values = []
            i+=1
            applet.Label(tab2, text=config_item,background=maincolor,foreground='white').grid(column=c1, row=i,sticky="e",padx=[5,0])
            valuename = applet.Entry(tab2,foreground=textcolor,width=10)
            valuename.insert(0,config_startup[config_item])
            valuename.grid(column= c2, row = i,sticky="w",pady=4,padx=[5,5])
            startup_values.append(valuename)
            if i == 22:
                i=1
                c1+=2
                c2+=2
        #   title
        logolabel_tab2 = applet.Label(tab2,text="HoNfigurator",background=maincolor,foreground='white',image=honlogo)
        logolabel_tab2.grid(columnspan=c2+1,column=0, row=0,sticky="n",pady=[10,0])
        
        """
        
        This is the bot command center tab
        
        """
        # #list of buttons
        # self.bot_cmd_buttons = []
        # #
        # #   creates the buttons
        # for i in range(0,20):
        #     tk.StringVar(app,'offline')
        #     self.tab1_status1_label = applet.Label(tab1, text=f"Bot {i+1}: ",background=maincolor, foreground='white')
        #     self.tab1_status1_current = applet.Label(tab1)
        #     #sends buttons to list
        #     self.bot_cmd_buttons.append([self.tab1_status1_label,self.tab1_status1_current,tk.StringVar(app,'offline')])
        # tab1_startBot = applet.Button(tab1, text="Configure Single Server")
        # tab1_startBot.grid(columnspan=3, column=1, row=9,stick='n',padx=[0,10],pady=[20,10])
        # tab1_startall = applet.Button(tab1, text="Configure All Servers",command=lambda: self.sendData("all",tab1_hosterd.get(),tab1_regiond.get(),tab1_regionsd.get(),tab1_serveridd.get(),tab1_servertd.get(),tab1_hondird.get(),tab1_bottokd.get(),tab1_discordadmin.get(),tab1_masteruser.get(),tab1_masterpass.get(),self.forceupdate.get()))
        # tab1_startall.grid(columnspan=4, column=1, row=9,stick='n',padx=[10,0],pady=[20,10])
        # self.botCount(20)
        tabgui.select(0)
        app.mainloop()
    def hellotest(self):
        print("hello")
test = gui()
test.creategui()