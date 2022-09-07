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
import multiprocessing

#import cogs.server_status as svrcmd

conf_parse_global = configparser.ConfigParser()
conf_parse_local = configparser.ConfigParser()

class mData():
    def __init__(self):
        return
    
    #def returnDict(self,configFile):      
    def returnDict(self):
        conf_parse_local.read(f"{os.path.dirname(os.path.realpath(__file__))}\\..\\config\\local_config.ini")
        conf_parse_global.read(f"{os.path.dirname(os.path.realpath(__file__))}\\..\\config\\global_config.ini")
        self.confDict = {}
        for option in conf_parse_local.options("OPTIONS"):
            self.confDict.update({option:conf_parse_local['OPTIONS'][option]})
        for option in conf_parse_global.options("OPTIONS"):
            self.confDict.update({option:conf_parse_global['OPTIONS'][option]})
        #   some variables which we will use
        self.svr_id = self.confDict['svr_id']
        #
        #   Update the dictionary with some processed data
        self.confDict.update({"hon_home_dir":f"{self.confDict['hon_directory']}..\\hon_server_instances\\Hon_Server_{self.confDict['svr_id']}"})
        self.confDict.update({"hon_game_dir":f"{self.confDict['hon_directory']}..\\hon_server_instances\\Hon_Server_{self.confDict['svr_id']}\\Documents\\Heroes of Newerth x64\\game"})
        self.confDict.update({"hon_logs_dir":f"{self.confDict['hon_home_dir']}\\Documents\Heroes of Newerth x64\\game\\logs"})
        self.confDict.update({"sdc_home_dir":f"{self.confDict['hon_logs_dir']}\\sdc"})
        self.confDict.update({"nssm_exe":f"{self.confDict['hon_directory']}"+"nssm.exe"})
        self.confDict.update({"svr_identifier":f"{self.confDict['svr_hoster']}-{self.confDict['svr_id']}"})
        self.confDict.update({"svrid_total":f"{self.confDict['svr_id']}/{self.confDict['svr_total']}"})
        self.confDict.update({"svr_id_w_total":f"{self.confDict['svr_hoster']}-{self.confDict['svr_id']}/{self.confDict['svr_total']}"})
        if 'core_assignment' not in self.confDict:
            self.confDict.update({'core_assignment':'one'})
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
            self.confDict.update({'debug_mode':False})
        if 'use_proxy' not in self.confDict:
            self.confDict.update({'use_proxy':'True'})
        #self.confDict.update({"hon_file_name":f"HON_SERVER_{self.confDict['svr_id']}.exe"})
        #   Kongor testing
        if self.confDict['master_server'] == "honmasterserver.com":
            self.confDict.update({"hon_file_name":f"HON_SERVER_{self.svr_id}.exe"})
        elif self.confDict['master_server'] == "kongor.online:666":
            self.confDict.update({"hon_file_name":f"KONGOR_ARENA_{self.svr_id}.exe"})
        #
        self.confDict.update({"hon_exe":f"{self.confDict['hon_directory']}{self.confDict['hon_file_name']}"})
        self.confDict.update({"proxy_exe":f"{self.confDict['hon_directory']}proxy.exe"})
        self.confDict.update({"proxy_manager_exe":f"{self.confDict['hon_directory']}proxymanager.exe"})
        self.confDict.update({"svr_k2dll":f"{self.confDict['hon_directory']}k2_x64.dll"})
        self.confDict.update({"svr_cgame_dll":f"{self.confDict['hon_directory']}game\\cgame_x64.dll"})
        self.confDict.update({"svr_game_shared_dll":f"{self.confDict['hon_directory']}game\\game_shared_x64.dll"})
        self.confDict.update({"svr_game_dll":f"{self.confDict['hon_directory']}game\\game_x64.dll"})
        self.confDict.update({"discord_location":f"{self.confDict['sdc_home_dir']}\\messages"})
        self.confDict.update({"discord_temp":f"{self.confDict['sdc_home_dir']}\\messages\\message{self.confDict['svr_identifier']}.txt"})
        self.confDict.update({"svr_ip":mData.getData(self,"svr_ip")})
        self.confDict.update({"svr_dns":mData.getData(self,"DNSName")})
        self.confDict.update({"python_location":mData.getData(self,"pythonLoc")})
        self.confDict.update({"svr_affinity":mData.getData(self,"cores")})
        self.confDict.update({"last_restart_loc":mData.getData(self,"lastRestartLoc")})
        self.confDict.update({"incr_port":mData.getData(self,"incr_port")})
        self.confDict.update({"total_games_played":mData.getData(self,"TotalGamesPlayed")})
        #self.confDict.update({"last_restart":mData.getData(self,"last_restart")})
        if exists(f"{self.confDict['hon_game_dir']}\\startup.cfg"):
            self.game_config = mData.parse_config(self,f"{self.confDict['hon_game_dir']}\\startup.cfg")
        gameDllHash = mData.getData(self,"gameDllHash")
        if gameDllHash == "70E841D98E59DFE9347E24260719E1B7B590EBB8":
            self.confDict.update({"player_count_exe_loc":f"{self.confDict['hon_directory']}pingplayerconnected-70.exe"})
            self.confDict.update({"player_count_exe":"pingplayerconnected-70.exe"})
        elif gameDllHash == "3D97C3FB6121219344CFABE8DFCC608FAC122DB4":
            self.confDict.update({"player_count_exe_loc":f"{self.confDict['hon_directory']}pingplayerconnected-3D.exe"})
            self.confDict.update({"player_count_exe":"pingplayerconnected-3D.exe"})
        elif gameDllHash == "DC9E9869936407231F4D1B942BF7B81FCC9834FF":
            self.confDict.update({"player_count_exe_loc":f"{self.confDict['hon_directory']}pingplayerconnected-DC.exe"})
            self.confDict.update({"player_count_exe":"pingplayerconnected-DC.exe"})
        return self.confDict
    def returnDict_basic(self,svr_id):
        conf_parse_local.read(f"{os.path.dirname(os.path.realpath(__file__))}\\..\\config\\local_config.ini")
        conf_parse_global.read(f"{os.path.dirname(os.path.realpath(__file__))}\\..\\config\\global_config.ini")
        self.confDict_basic = {}
        for option in conf_parse_local.options("OPTIONS"):
            self.confDict_basic.update({option:conf_parse_local['OPTIONS'][option]})
        for option in conf_parse_global.options("OPTIONS"):
            self.confDict_basic.update({option:conf_parse_global['OPTIONS'][option]})
        self.confDict_basic.update({"hon_home_dir":f"{self.confDict_basic['hon_directory']}..\\hon_server_instances\\Hon_Server_{svr_id}"})
        self.confDict_basic.update({"hon_game_dir":f"{self.confDict_basic['hon_directory']}..\\hon_server_instances\\Hon_Server_{svr_id}\\Documents\\Heroes of Newerth x64\\game"})
        self.confDict_basic.update({"hon_logs_dir":f"{self.confDict_basic['hon_home_dir']}\\Documents\Heroes of Newerth x64\\game\\logs"})
        self.confDict_basic.update({"sdc_home_dir":f"{self.confDict_basic['hon_logs_dir']}\\sdc"})
        self.confDict_basic.update({"nssm_exe":f"{self.confDict_basic['hon_directory']}"+"nssm.exe"})
        self.confDict_basic.update({"svr_identifier":f"{self.confDict_basic['svr_hoster']}-{svr_id}"})
        self.confDict_basic.update({"svrid_total":f"{svr_id}/{self.confDict_basic['svr_total']}"})
        self.confDict_basic.update({"svr_id_w_total":f"{self.confDict_basic['svr_hoster']}-{svr_id}/{self.confDict_basic['svr_total']}"})
        return self.confDict_basic
    def getData(self, dtype):
        if dtype == "hon":
            return "data"
        if dtype == "svr_ip":
            external_ip = urllib.request.urlopen('https://4.ident.me').read().decode('utf8')
            return external_ip
        if dtype == "cores":
            self.svr_id = int(self.svr_id)
            #
            #   Get total cores, logical included
            total_cores = psutil.cpu_count(logical = True)
            if self.confDict['core_assignment'] == 'two':
                total_cores +=1
                affinity = [total_cores - self.svr_id,total_cores - self.svr_id - 1]
                #
                #   Set affinity of the hon process to total cores - server ID
                affinity[0] = affinity[0]-self.svr_id
                affinity[1] = affinity[1]-self.svr_id
            elif self.confDict['core_assignment'] == 'one':
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
            print("CPU Affinity: "+str(affinity))
            return affinity
        if dtype == "pythonLoc":
            return sp.getoutput('where python')
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
        if dtype == "gameDllHash":
            #
            # 3d97c3fb6121219344cfabe8dfcc608fac122db4 = new DLL
            # 70e841d98e59dfe9347e24260719e1b7b590ebb8 = old DLL
            #
            sha1 = hashlib.sha1()
            if exists(self.confDict['svr_k2dll']):
                with open(self.confDict['svr_k2dll'],'rb') as file:
                #   loop till the end of the file
                    chunk = 0
                    while chunk != b'':
                        #   read only 1024 bytes at a time
                        chunk = file.read(1024)
                        sha1.update(chunk)
                hash = sha1.hexdigest()
                hash = hash.upper()
                gameDllHash = hash
                return gameDllHash
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
                    v = v.replace('"','')
                    proxy.write(f'{k}={v}\n')
            if exists(filename):
                os.chmod(filename, S_IREAD|S_IRGRP|S_IROTH)
            return