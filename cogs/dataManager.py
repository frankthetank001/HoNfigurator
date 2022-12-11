"""
    This class manages the data for the bot


"""
import configparser
from fileinput import filename
from queue import Empty
from unittest.mock import DEFAULT
from asyncio.windows_events import NULL
import urllib.request
import os
import psutil
import subprocess as sp
import socket
from os.path import exists
from stat import S_IREAD, S_IRGRP, S_IROTH
import stat
import hashlib
import sys
import traceback
import multiprocessing
import shutil

#import cogs.server_status as svrcmd

conf_parse_global = configparser.ConfigParser()
conf_parse_local = configparser.ConfigParser(interpolation=None)
conf_parse_deployed_global = configparser.ConfigParser(interpolation=None)
conf_parse_deployed_local = configparser.ConfigParser(interpolation=None)
conf_parse_temp_local = configparser.ConfigParser(interpolation=None)
conf_parse_temp_global = configparser.ConfigParser(interpolation=None)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        #print("running from tempdir "+base_path)
    except Exception:
        #base_path = os.path.abspath(".")
        base_path = os.path.dirname(sys.argv[0])
        #print("running from base "+base_path)
    return os.path.join(base_path, relative_path)

class mData():
    def __init__(self):
        return
    
    #def returnDict(self,configFile):      
    def returnDict(self):
        
        print(os.getcwd())
        if exists(resource_path("config\\local_config.ini.incoming")):
            try:
                shutil.move(resource_path("config\\local_config.ini.incoming"),resource_path("config\\local_config.ini"))
            except Exception as e: print(e)
        if exists(resource_path("config\\global_config.ini.incoming")):
            try:
                shutil.move(resource_path("config\\global_config.ini.incoming"),resource_path("config\\global_config.ini"))
            except Exception as e: print(e)

        conf_parse_local.read(resource_path("config\\local_config.ini"))
        conf_parse_global.read(resource_path("config\\global_config.ini"))
        self.confDict = {}
        for option in conf_parse_local.options("OPTIONS"):
            self.confDict.update({option:conf_parse_local['OPTIONS'][option]})
        for option in conf_parse_global.options("OPTIONS"):
            self.confDict.update({option:conf_parse_global['OPTIONS'][option]})
        #   some variables which we will use
        self.svr_id = self.confDict['svr_id']
        #
        #   Update the dictionary with some processed data
        #if 'hon_root_dir' not in self.confDict:
            #self.confDict.update({"hon_root_dir":f"{self.confDict['hon_directory']}..\\hon_server_instances\\hon"})
        self.confDict.update({"hon_root_dir":f"{self.confDict['hon_directory']}..\\hon_server_instances"})
        self.confDict.update({"hon_home_dir":f"{self.confDict['hon_root_dir']}\\Hon_Server_{self.confDict['svr_id']}"})
        self.confDict.update({"hon_game_dir":f"{self.confDict['hon_home_dir']}\\Documents\\Heroes of Newerth x64\\game"})
        self.confDict.update({"hon_replays_dir":f"{self.confDict['hon_home_dir']}\\Documents\\Heroes of Newerth x64\\game\\replays"})
        self.confDict.update({"hon_logs_dir":f"{self.confDict['hon_home_dir']}\\Documents\\Heroes of Newerth x64\\game\\logs"})
        self.confDict.update({"sdc_home_dir":f"{self.confDict['hon_home_dir']}\\Documents\\Heroes of Newerth x64\\game\\logs\\adminbot{self.confDict['svr_id']}"})
        self.confDict.update({"nssm_exe":f"{self.confDict['hon_directory']}"+"nssm.exe"})
        self.confDict.update({"svr_identifier":f"{self.confDict['svr_hoster']}-{self.confDict['svr_id']}"})
        self.confDict.update({"svrid_total":f"{self.confDict['svr_id']}/{self.confDict['svr_total']}"})
        self.confDict.update({"svr_id_w_total":f"{self.confDict['svr_hoster']}-{self.confDict['svr_id']}/{self.confDict['svr_total']}"})
        self.confDict.update({"app_name":f"adminbot{self.confDict['svr_id']}"})
        if 'core_assignment' not in self.confDict:
            self.confDict.update({'core_assignment':'one core/server'})
        if 'process_priority' not in self.confDict:
            self.confDict.update({'process_priority':'realtime'})
        if 'incr_port_by' not in self.confDict:
            self.confDict.update({'incr_port_by':1})
        if 'auto_update' not in self.confDict:
            self.confDict.update({'auto_update':'True'})
        if 'game_starting_port' not in self.confDict:
            self.confDict.update({'game_starting_port':10000})
        if 'voice_starting_port' not in self.confDict:
            self.confDict.update({'voice_starting_port':10060})
        if 'debug_mode' not in self.confDict:
            self.confDict.update({'debug_mode':'False'})
        if 'use_proxy' not in self.confDict:
            self.confDict.update({'use_proxy':'True'})
        if 'use_console' not in self.confDict:
            self.confDict.update({'use_console':'False'})
        if 'svr_login' not in self.confDict:
            self.confDict.update({'svr_login':'<username>'})
        if 'svr_password' not in self.confDict:
            self.confDict.update({'svr_password':'<password>'})
        if 'compiled_hash' not in self.confDict:
            self.confDict.update({'compiled_hash':'requires build'})
        if 'hon_manager_dir' not in self.confDict:
            self.confDict.update({"hon_manager_dir":f"{self.confDict['hon_root_dir']}\\hon"})
        if 'disable_bot' not in self.confDict:
            self.confDict.update({'disable_bot':'False'})
        if 'auto_update' not in self.confDict:
            self.confDict.update({'auto_update':'True'})
        #self.confDict.update({"hon_file_name":f"HON_SERVER_{self.confDict['svr_id']}.exe"})
        #   Kongor testing
        if self.confDict['master_server'] == "honmasterserver.com":
            self.confDict.update({"hon_file_name":f"HON_SERVER_{self.svr_id}.exe"})
        else:
            self.confDict.update({"hon_file_name":f"KONGOR_ARENA_{self.svr_id}.exe"})
        #
        self.confDict.update({"hon_exe":f"{self.confDict['hon_directory']}{self.confDict['hon_file_name']}"})
        self.confDict.update({"hon_version":mData.check_hon_version(self,self.confDict['hon_exe'])})
        self.confDict.update({"proxy_exe":f"{self.confDict['hon_directory']}proxy.exe"})
        self.confDict.update({"proxy_manager_exe":f"{self.confDict['hon_directory']}proxymanager.exe"})
        self.confDict.update({"svr_k2dll":f"{self.confDict['hon_directory']}k2_x64.dll"})
        self.confDict.update({"svr_cgame_dll":f"{self.confDict['hon_directory']}game\\cgame_x64.dll"})
        self.confDict.update({"svr_game_shared_dll":f"{self.confDict['hon_directory']}game\\game_shared_x64.dll"})
        self.confDict.update({"svr_game_dll":f"{self.confDict['hon_directory']}game\\game_x64.dll"})
        self.confDict.update({"discord_location":f"{self.confDict['sdc_home_dir']}\\messages"})
        self.confDict.update({"discord_temp":f"{self.confDict['sdc_home_dir']}\\messages\\message{self.confDict['svr_identifier']}.txt"})
        self.confDict.update({"app_name":f"adminbot{self.svr_id}"})
        self.confDict.update({"app_log":f"{self.confDict['sdc_home_dir']}\\{self.confDict['app_name']}.log"})
        if 'static_ip' not in self.confDict:
            self.confDict.update({"svr_ip":mData.getData(self,"svr_ip")})
        self.confDict.update({"svr_dns":mData.getData(self,"DNSName")})
        self.confDict.update({"python_location":mData.getData(self,"pythonLoc")})
        self.confDict.update({"svr_affinity":mData.getData(self,"cores")})
        self.confDict.update({"last_restart_loc":mData.getData(self,"lastRestartLoc")})
        self.confDict.update({"incr_port":mData.getData(self,"incr_port")})
        self.confDict.update({"total_games_played":mData.getData(self,"TotalGamesPlayed")})
        self.confDict.update({"svr_port":int(self.confDict['game_starting_port'])+int(self.confDict['incr_port'])})
        self.confDict.update({"svr_proxyPort":self.confDict['svr_port']+10000})
        self.confDict.update({"svr_proxyLocalVoicePort":int(self.confDict['voice_starting_port'])+int(self.confDict['incr_port'])})
        self.confDict.update({"svr_proxyRemoteVoicePort":self.confDict['svr_proxyLocalVoicePort']+10000})
        #self.confDict.update({"last_restart":mData.getData(self,"last_restart")})
        if exists(f"{self.confDict['hon_game_dir']}\\startup.cfg"):
            self.game_config = mData.parse_config(self,f"{self.confDict['hon_game_dir']}\\startup.cfg")
        gameDllHash = mData.get_hash(self.confDict['svr_k2dll'])
        if gameDllHash == "70E841D98E59DFE9347E24260719E1B7B590EBB8":
            self.confDict.update({"player_count_exe_loc":f"{self.confDict['hon_directory']}pingplayerconnected-70.exe"})
            self.confDict.update({"player_count_exe":"pingplayerconnected-70.exe"})
        elif gameDllHash == "3D97C3FB6121219344CFABE8DFCC608FAC122DB4":
            self.confDict.update({"player_count_exe_loc":f"{self.confDict['hon_directory']}pingplayerconnected-3D.exe"})
            self.confDict.update({"player_count_exe":"pingplayerconnected-3D.exe"})
        elif gameDllHash == "DC9E9869936407231F4D1B942BF7B81FCC9834FF":
            self.confDict.update({"player_count_exe_loc":f"{self.confDict['hon_directory']}pingplayerconnected-DC.exe"})
            self.confDict.update({"player_count_exe":"pingplayerconnected-DC.exe"})
        else:
            self.confDict.update({"player_count_exe_loc":f"{self.confDict['hon_directory']}pingplayerconnected-DC.exe"})
            self.confDict.update({"player_count_exe":"pingplayerconnected-DC.exe"})
        return self.confDict
    def returnDict_deployed(self,svr_id):
        conf_parse_local.read(resource_path("config\\local_config.ini"))
        conf_parse_global.read(resource_path("config\\global_config.ini"))

        self.confDict_root = {}
        self.confDict_deployed = {}

        for option in conf_parse_local.options("OPTIONS"):
            self.confDict_root.update({option:conf_parse_local['OPTIONS'][option]})
        # for option in conf_parse_local.options("OPTIONS"):
        #     self.confDict_root.update({option:conf_parse_local['OPTIONS'][option]})
        for option in conf_parse_global.options("OPTIONS"):
            self.confDict_root.update({option:conf_parse_global['OPTIONS'][option]})
        #if 'hon_root_dir' not in self.confDict_root:
            #self.confDict_deployed.update({"hon_root_dir":f"{self.confDict_root['hon_directory']}..\\hon_server_instances\\hon"})
        #self.confDict_deployed.update({"hon_root_dir":f"{self.confDict_root['hon_directory']}..\\hon_server_instances\\Hon_Server_{svr_id}"})
            #self.confDict_deployed.update({"hon_home_dir":f"{self.confDict_deployed['hon_root_dir']}\\hon_server_instances\\Hon_Server_{svr_id}"})
        # else:
        #     self.confDict_deployed.update({"hon_root_dir":f"{self.confDict_root['hon_root_dir']}"})
        self.confDict_deployed.update({"hon_root_dir":f"{self.confDict_root['hon_directory']}..\\hon_server_instances"})
        self.confDict_deployed.update({"hon_home_dir":f"{self.confDict_deployed['hon_root_dir']}\\Hon_Server_{svr_id}"})
        self.confDict_deployed.update({"hon_game_dir":f"{self.confDict_deployed['hon_home_dir']}\\Documents\\Heroes of Newerth x64\\game"})
        self.confDict_deployed.update({"hon_logs_dir":f"{self.confDict_deployed['hon_home_dir']}\\Documents\\Heroes of Newerth x64\\game\\logs"})
        self.confDict_deployed.update({"sdc_home_dir":f"{self.confDict_deployed['hon_home_dir']}\\Documents\\Heroes of Newerth x64\\game\\logs\\adminbot{svr_id}"})
        self.confDict_deployed.update({"app_name":f"adminbot{svr_id}"})
        self.confDict_deployed.update({"app_log":f"{self.confDict_deployed['sdc_home_dir']}\\{self.confDict_deployed['app_name']}.log"})
        self.confDict_deployed.update({"nssm_exe":f"{self.confDict_root['hon_directory']}"+"nssm.exe"})
        self.confDict_deployed.update({"svr_identifier":f"{self.confDict_root['svr_hoster']}-{svr_id}"})
        self.confDict_deployed.update({"svrid_total":f"{svr_id}/{self.confDict_root['svr_total']}"})
        self.confDict_deployed.update({"svr_id_w_total":f"{self.confDict_root['svr_hoster']}-{svr_id}/{self.confDict_root['svr_total']}"})
        if exists(f"{self.confDict_deployed['sdc_home_dir']}\\config\\global_config.ini"):
            conf_parse_deployed_global.read(f"{self.confDict_deployed['sdc_home_dir']}\\config\\global_config.ini")
            for option in conf_parse_deployed_global.options("OPTIONS"):
                self.confDict_deployed.update({option:conf_parse_deployed_global['OPTIONS'][option]})
        if exists(f"{self.confDict_deployed['sdc_home_dir']}\\config\\local_config.ini"):
            conf_parse_deployed_local.read(f"{self.confDict_deployed['sdc_home_dir']}\\config\\local_config.ini")
            for option in conf_parse_deployed_local.options("OPTIONS"):
                self.confDict_deployed.update({option:conf_parse_deployed_local['OPTIONS'][option]})
        if 'use_console' not in self.confDict_deployed:
            self.confDict_deployed.update({'use_console':'False'})
        if 'incr_port_by' not in self.confDict_deployed:
            self.confDict_deployed.update({'incr_port_by':self.confDict_root['incr_port_by']})
        self.confDict_deployed.update({"incr_port":mData.incr_port(int(svr_id),self.confDict_deployed['incr_port_by'])})
        if 'game_starting_port' not in self.confDict_deployed:
            self.confDict_deployed.update({'game_starting_port':self.confDict_root['game_starting_port']})
        if 'voice_starting_port' not in self.confDict_deployed:
            self.confDict_deployed.update({'voice_starting_port':self.confDict_root['voice_starting_port']})
        if 'auto_update' not in self.confDict_deployed:
            self.confDict_deployed.update({'auto_update':'True'})
        self.confDict_deployed.update({"svr_port":int(self.confDict_deployed['game_starting_port'])+int(self.confDict_deployed['incr_port'])})
        self.confDict_deployed.update({"svr_proxyPort":self.confDict_deployed['svr_port']+10000})
        self.confDict_deployed.update({"svr_proxyLocalVoicePort":int(self.confDict_deployed['voice_starting_port'])+int(self.confDict_deployed['incr_port'])})
        self.confDict_deployed.update({"svr_proxyRemoteVoicePort":self.confDict_deployed['svr_proxyLocalVoicePort']+10000})
        try:
            self.confDict_deployed.update({"svr_affinity":mData.check_affinity(svr_id,self.confDict_deployed['core_assignment'])})
        except:pass
        if self.confDict_deployed['master_server'] == "honmasterserver.com":
            self.confDict_deployed.update({"hon_file_name":f"HON_SERVER_{svr_id}.exe"})
        else:
            self.confDict_deployed.update({"hon_file_name":f"KONGOR_ARENA_{svr_id}.exe"})
        #
        try:
            hon_dir = self.confDict_deployed['hon_directory']
        except: hon_dir = self.confDict_root['hon_directory']
        self.confDict_deployed.update({"hon_exe":f"{hon_dir}{self.confDict_deployed['hon_file_name']}"})
        self.confDict_deployed.update({"hon_version":mData.check_hon_version(self,self.confDict_deployed['hon_exe'])})

        self.confDict_deployed.update({"proxy_exe":f"{hon_dir}proxy.exe"})
        self.confDict_deployed.update({"proxy_manager_exe":f"{hon_dir}proxymanager.exe"})
        self.confDict_deployed.update({"svr_k2dll":f"{hon_dir}k2_x64.dll"})
        self.confDict_deployed.update({"svr_cgame_dll":f"{hon_dir}game\\cgame_x64.dll"})
        self.confDict_deployed.update({"svr_game_shared_dll":f"{hon_dir}game\\game_shared_x64.dll"})
        self.confDict_deployed.update({"svr_game_dll":f"{hon_dir}game\\game_x64.dll"})
        self.confDict_deployed.update({"svr_id":str(svr_id)})
        self.confDict_deployed.update({"python_location":mData.getData(self,"pythonLoc")})
        
        try:
            gameDllHash = mData.get_hash(self.confDict_deployed['svr_k2dll'])
        except: gameDllHash = "null"
        if gameDllHash == "70E841D98E59DFE9347E24260719E1B7B590EBB8":
            self.confDict_deployed.update({"player_count_exe_loc":f"{hon_dir}pingplayerconnected-70.exe"})
            self.confDict_deployed.update({"player_count_exe":"pingplayerconnected-70.exe"})
        elif gameDllHash == "3D97C3FB6121219344CFABE8DFCC608FAC122DB4":
            self.confDict_deployed.update({"player_count_exe_loc":f"{hon_dir}pingplayerconnected-3D.exe"})
            self.confDict_deployed.update({"player_count_exe":"pingplayerconnected-3D.exe"})
        elif gameDllHash == "DC9E9869936407231F4D1B942BF7B81FCC9834FF":
            self.confDict_deployed.update({"player_count_exe_loc":f"{hon_dir}pingplayerconnected-DC.exe"})
            self.confDict_deployed.update({"player_count_exe":"pingplayerconnected-DC.exe"})
        else:
            self.confDict_deployed.update({"player_count_exe_loc":f"{hon_dir}pingplayerconnected-DC.exe"})
            self.confDict_deployed.update({"player_count_exe":"pingplayerconnected-DC.exe"})

        return self.confDict_deployed
        
    def returnDict_temp(baseDict):
        confDict_temp = {}
        if exists(f"{baseDict['sdc_home_dir']}\\config\\local_config.ini.incoming"):
            conf_parse_temp_local.read(f"{baseDict['sdc_home_dir']}\\config\\local_config.ini.incoming")
            for option in conf_parse_temp_local.options("OPTIONS"):
                confDict_temp.update({option:conf_parse_temp_local['OPTIONS'][option]})
        if exists(f"{baseDict['sdc_home_dir']}\\config\\global_config.ini.incoming"):
            conf_parse_temp_global.read(f"{baseDict['sdc_home_dir']}\\config\\global_config.ini.incoming")
            for option in conf_parse_temp_global.options("OPTIONS"):
                confDict_temp.update({option:conf_parse_temp_global['OPTIONS'][option]})
        return confDict_temp
    def return_value(path,value):
        temp={}
        print(f"config path: {path}")
        if exists(path):
            conf_parse_temp_local.read(path)
            for option in conf_parse_temp_local.options("OPTIONS"):
                temp.update({option:conf_parse_temp_local['OPTIONS'][option]})
        if value in temp:
            return temp[value]
        return False
        
    # def setData(self,key):
    #     temp={}
    #     conf_parse_local.read(f"{os.path.dirname(os.path.realpath(__file__))}\\..\\config\\local_config.ini")
    #     for option in conf_parse_local.options("OPTIONS"):
    #         temp.update({option:conf_parse_local['OPTIONS'][option]})
            
    def returnDict_basic(self,svr_id):
        
        conf_parse_local.read(resource_path("config\\local_config.ini"))
        conf_parse_global.read(resource_path("config\\global_config.ini"))

        self.confDict_root = {}
        self.confDict_basic = {}

        for option in conf_parse_local.options("OPTIONS"):
            self.confDict_root.update({option:conf_parse_local['OPTIONS'][option]})
        # for option in conf_parse_local.options("OPTIONS"):
        #     self.confDict_root.update({option:conf_parse_local['OPTIONS'][option]})
        for option in conf_parse_global.options("OPTIONS"):
            self.confDict_root.update({option:conf_parse_global['OPTIONS'][option]})
        #if 'hon_root_dir' not in self.confDict_root:
            #self.confDict_deployed.update({"hon_root_dir":f"{self.confDict_root['hon_directory']}..\\hon_server_instances\\hon"})
        #self.confDict_deployed.update({"hon_root_dir":f"{self.confDict_root['hon_directory']}..\\hon_server_instances\\Hon_Server_{svr_id}"})
            #self.confDict_deployed.update({"hon_home_dir":f"{self.confDict_deployed['hon_root_dir']}\\hon_server_instances\\Hon_Server_{svr_id}"})
        # else:
        #     self.confDict_deployed.update({"hon_root_dir":f"{self.confDict_root['hon_root_dir']}"})
        self.confDict_basic.update({"hon_root_dir":f"{self.confDict_root['hon_directory']}..\\hon_server_instances"})
        self.confDict_basic.update({"hon_manager_dir":f"{self.confDict_basic['hon_root_dir']}\\hon"})
        self.confDict_basic.update({"hon_home_dir":f"{self.confDict_basic['hon_root_dir']}\\Hon_Server_{svr_id}"})
        self.confDict_basic.update({"hon_game_dir":f"{self.confDict_basic['hon_home_dir']}\\Documents\\Heroes of Newerth x64\\game"})
        self.confDict_basic.update({"hon_logs_dir":f"{self.confDict_basic['hon_home_dir']}\\Documents\\Heroes of Newerth x64\\game\\logs"})
        self.confDict_basic.update({"sdc_home_dir":f"{self.confDict_basic['hon_home_dir']}\\Documents\\Heroes of Newerth x64\\game\\logs\\adminbot{svr_id}"})
        self.confDict_basic.update({"nssm_exe":f"{self.confDict_root['hon_directory']}"+"nssm.exe"})
        self.confDict_basic.update({"svr_identifier":f"{self.confDict_root['svr_hoster']}-{svr_id}"})
        self.confDict_basic.update({"svrid_total":f"{svr_id}/{self.confDict_root['svr_total']}"})
        self.confDict_basic.update({"svr_id_w_total":f"{self.confDict_root['svr_hoster']}-{svr_id}/{self.confDict_root['svr_total']}"})
        if 'use_console' not in self.confDict_basic:
            self.confDict_basic.update({'use_console':'False'})
        return self.confDict_basic

        
    # def setData(self,key):
    #     temp={}
    #     conf_parse_local.read(f"{os.path.dirname(os.path.realpath(__file__))}\\..\\config\\local_config.ini")
    #     for option in conf_parse_local.options("OPTIONS"):
    #         temp.update({option:conf_parse_local['OPTIONS'][option]})    
    def incr_port(svr_id,incr_port_by):
            incr_port = 0
            for i in range(0,svr_id):
                incr_val = int(incr_port_by)
                incr_port = incr_val * i
            #print("port iteration: " +str(incr_port))
            return incr_port
    def check_hon_version(self,file):
        if exists(file):
            version_length=0
            version_offset=88544
            hon_x64=open(file,'rb')
            hon_x64.seek(version_offset,1)
            version=hon_x64.read(16)
            version=version.decode('utf-16-le')
            return(version)
        else:
            return ("pending version check") 
    def check_affinity(svr_id,core_assignment):
        svr_id = int(svr_id)
            #
            #   Get total cores, logical included
        total_cores = psutil.cpu_count(logical = True)
        if core_assignment in ('two','two cores/server'):
            total_cores +=1
            affinity = [total_cores - svr_id,total_cores - svr_id - 1]
            #
            #   Set affinity of the hon process to total cores - server ID
            affinity[0] = affinity[0]-svr_id
            affinity[1] = affinity[1]-svr_id
        elif core_assignment in ('one','one core/server'):
            affinity = [0,0]
            affinity[0] = total_cores - svr_id
            affinity[1] = total_cores - svr_id
        elif core_assignment == 'two servers/core':
            affinity = [0,0]
            t = 0
            for num in range(0, svr_id):
                # checking condition
                if num % 2 == 0:
                    t +=1
            affinity[0] = total_cores - t
            affinity[1] = total_cores - t
        elif core_assignment == 'three servers/core':
                affinity = [0,0]
                t = 0
                for num in range(0, svr_id):
                    # checking condition
                    if num % 3 == 0:
                        t +=1
                affinity[0] = total_cores - t
                affinity[1] = total_cores - t
        elif core_assignment == 'four servers/core':
            affinity = [0,0]
            t = 0
            for num in range(0, svr_id):
                # checking condition
                if num % 4 == 0:
                    t +=1
            affinity[0] = total_cores - t
            affinity[1] = total_cores - t
        return affinity
    def getData(self, dtype):
        if dtype == "hon":
            return "data"
        if dtype == "svr_ip":
            try:
                external_ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
            except:
                external_ip = urllib.request.urlopen('http://api.ipify.org').read().decode('utf8')
            return external_ip
        if dtype == "cores":
            self.svr_id = int(self.svr_id)
            #
            #   Get total cores, logical included
            total_cores = psutil.cpu_count(logical = True)
            if self.confDict['core_assignment'] in ('two cores/server','two'):
                total_cores +=1
                affinity = [total_cores - self.svr_id,total_cores - self.svr_id - 1]
                #
                #   Set affinity of the hon process to total cores - server ID
                affinity[0] = affinity[0]-self.svr_id
                affinity[1] = affinity[1]-self.svr_id
            elif self.confDict['core_assignment'] in ('one','one core/server'):
                affinity = [0,0]
                affinity[0] = total_cores - self.svr_id
                affinity[1] = total_cores - self.svr_id
            elif self.confDict['core_assignment'] == 'two servers/core':
                affinity = [0,0]
                t = 0
                for num in range(0, self.svr_id):
                    # checking condition
                    if num % 2 == 0:
                        t +=1
                affinity[0] = total_cores - t
                affinity[1] = total_cores - t
            elif self.confDict['core_assignment'] == 'three servers/core':
                affinity = [0,0]
                t = 0
                for num in range(0, self.svr_id):
                    # checking condition
                    if num % 3 == 0:
                        t +=1
                affinity[0] = total_cores - t
                affinity[1] = total_cores - t
            elif self.confDict['core_assignment'] == 'four servers/core':
                affinity = [0,0]
                t = 0
                for num in range(0, self.svr_id):
                    # checking condition
                    if num % 4 == 0:
                        t +=1
                affinity[0] = total_cores - t
                affinity[1] = total_cores - t
            print("CPU Affinity: "+str(affinity))
            return affinity
        if dtype == "pythonLoc":
            py_loc = sp.getoutput('where python')
            py_loc = py_loc.split("\n")
            py_loc = py_loc[0]
            return py_loc
        if dtype == "port":
            #   Now that we find the port from the startup.cfg file, this data method should check that it is listening.
            return f"1{self.svr_id}000"
        if dtype == "incr_port":
            incr_port = 0
            for i in range(0,self.svr_id):
                incr_val = int(self.confDict['incr_port_by'])
                incr_port = incr_val * i
            print("port iteration: " +str(incr_port))
            return incr_port
        if dtype == "DNSName":
            try:
                dns = socket.gethostbyaddr(self.confDict['svr_ip'])
                dns = dns[0]
                return dns
            except:
                print("no DNS lookup for host.")
        if dtype == "lastRestartLoc":
            tmp = f"{self.confDict['sdc_home_dir']}\\last_restart_time"
            return tmp
    def get_hash(file):
        sha1 = hashlib.sha1()
        try:
            with open(file,'rb') as f:
            #   loop till the end of the file
                chunk = 0
                while chunk != b'':
                    #   read only 1024 bytes at a time
                    chunk = f.read(1024)
                    sha1.update(chunk)
            hash = sha1.hexdigest()
            hash = hash.upper()
            return hash
        except Exception as e:
            print(e)
    def parse_config(self,filename):
        # svr_options = ["svr_port","svr_name","svr_location","man_port","man_startServerPort","man_endServerPort","svr_proxyLocalVoicePort","svr_proxyPort","svr_proxyRemoteVoicePort","svr_voicePortEnd","svr_voicePortStart","man_cowServerPort","man_cowVoiceProxyPort","man_enableProxy"]
        COMMENT_CHAR = '#'
        OPTION_CHAR =  ' '
        options = {}
        f = open(filename)
        for line in f:
            #   remove garbage
            line=line.replace("SetSave ","")
            #line=line.replace('"','')
            if COMMENT_CHAR in line:
                # split on comment char, keep only the part before
                line, comment = line.split(COMMENT_CHAR, 1)
            # Second, find lines with an option=value:
            if OPTION_CHAR in line:
                # split on option char:
                option, value = line.split(OPTION_CHAR, 1)
                # strip spaces:
                option = option.strip('"')
                value = value.strip()
                value = value.replace(' "0"',"")
                #value = value.strip()
                # store in dictionary:
                options[option] = value
        #print(options)
        f.close()
        return options
    
    def setData(self,filename,type,dict_startup,dict_proxy):
        if exists(filename):
            os.chmod(filename,stat.S_IWRITE )
        if type == "startup":
            with open(filename, 'w') as startup:
                for k, v in dict_startup.items():
                    startup.write(f'SetSave "{k}" {v} "0"\n')
            if exists(filename):
                os.chmod(filename, S_IREAD|S_IRGRP|S_IROTH)
            return
        elif type == "proxy":
            with open(filename, 'w') as proxy:
                for k, v in dict_proxy.items():
                    # v = v.replace('"','')
                    proxy.write(f'{k}={v}\n')
            if exists(filename):
                os.chmod(filename, S_IREAD|S_IRGRP|S_IROTH)
            return