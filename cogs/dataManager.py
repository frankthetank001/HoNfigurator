"""
    This class manages the data for the bot


"""
import configparser
from fileinput import filename
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

config = configparser.ConfigParser()

class mData():
    def __init__(self,configFile):
        #   Read in config file from the honfigurator repo location
        #config.read(os.path.dirname(os.path.realpath(__file__))+"\\..\\config\\sdc.ini")
        
        config.read(configFile)
        self.confDict = {}
        for option in config.options("OPTIONS"):
            self.confDict.update({option:config['OPTIONS'][option]})
        #
        #   some variables which we will use
        self.svr_id = self.confDict['svr_id']
        #
        #   Update the dictionary with some processed data
        self.confDict.update({"hon_home_dir":f"{self.confDict['hon_directory']}instances\Hon_Server_{self.confDict['svr_id']}"})
        self.confDict.update({"hon_game_dir":f"{self.confDict['hon_directory']}instances\Hon_Server_{self.confDict['svr_id']}\Documents\Heroes of Newerth x64\game"})
        self.confDict.update({"hon_logs_dir":f"{self.confDict['hon_home_dir']}\Documents\Heroes of Newerth x64\game\logs"})
        self.confDict.update({"sdc_home_dir":f"{self.confDict['hon_logs_dir']}\sdc"})
        self.confDict.update({"nssm_exe":f"{self.confDict['hon_directory']}"+"nssm.exe"})
        self.confDict.update({"svr_identifier":f"{self.confDict['svr_region_short']}-{self.confDict['svr_id']}"})
        self.confDict.update({"svrid_total":f"{self.confDict['svr_id']}/{self.confDict['svr_total']}"})
        self.confDict.update({"hon_file_name":f"hon_server_{self.confDict['svr_id']}.exe"})
        self.confDict.update({"hon_exe":f"{self.confDict['hon_directory']}{self.confDict['hon_file_name']}"})
        self.confDict.update({"svr_k2dll":f"{self.confDict['hon_directory']}k2_x64.dll"})
        self.confDict.update({"discord_location":f"{self.confDict['sdc_home_dir']}\messages"})
        self.confDict.update({"discord_temp":f"{self.confDict['sdc_home_dir']}\messages\message{self.confDict['svr_identifier']}.txt"})
        self.confDict.update({"svr_ip":mData.getData(self,"svr_ip")})
        #self.confDict.update({"svr_port":f"1{self.svr_id}000"})
        #self.confDict.update({"svr_port":f"1{self.svr_id}000"})
        self.confDict.update({"svr_dns":mData.getData(self,"DNSName")})
        self.confDict.update({"python_location":mData.getData(self,"pythonLoc")})
        self.confDict.update({"svr_affinity":mData.getData(self,"cores")})
        self.confDict.update({"last_restart_loc":mData.getData(self,"lastRestartLoc")})
        self.confDict.update({"incr_port":mData.getData(self,"incr_port")})

        return
    
    def returnDict(self):
        return self.confDict
    def getData(self, dtype):
        if dtype == "hon":
            return "data"
        if dtype == "svr_ip":
            external_ip = urllib.request.urlopen('https://4.ident.me').read().decode('utf8')
            return external_ip
        if dtype == "cores":
            #print(self.confDict)
            cores = []
            #print(self.svr_id)
            self.svr_id = int(self.svr_id)
            #
            #   Get total cores, logical included
            total_cores = psutil.cpu_count(logical = True)
            #
            #   Set affinity of the hon process to total cores - server ID
            affinity = total_cores - self.svr_id
            #print("AFFINITY" + str(affinity))
            return affinity
        if dtype == "pythonLoc":
            return sp.getoutput('where python')
        if dtype == "port":
            #   re implementing once port is more dynamic.
            # for proc in psutil.process_iter():
            #         #if proc.name() == serverDATA.grabData(self,"honFilename"):
            #         if proc.pid == honP:
            #             for c in proc.connections(kind='udp'):
            #                 port = "%s:%s" % (c.laddr)
            #                 port = port.split(":")
            #                 return port[1]
            return f"1{self.svr_id}000"
        if dtype == "incr_port":
            incr_port = 0
            for i in range(0,self.svr_id):
                i +=1
                incr_port = 1000 * i
                incr_port = int(incr_port)
            print("port iteration: " +str(incr_port))
            return incr_port
        if dtype == "DNSName":
            try:
                dns = socket.gethostbyaddr(self.svr_ip)
                dns = dns[0]
                #print("DNS: "+dns)
                return dns
            except:
                print("no DNS lookup for host.")
        if dtype == "lastRestartLoc":
            tmp = f"{self.confDict['sdc_home_dir']}\\last_restart_time"
            return tmp
    def parse_config(self,filename):
        # svr_options = ["svr_port","svr_name","svr_location","man_port","man_startServerPort","man_endServerPort","svr_proxyLocalVoicePort","svr_proxyPort","svr_proxyRemoteVoicePort","svr_voicePortEnd","svr_voicePortStart","man_cowServerPort","man_cowVoiceProxyPort","man_enableProxy"]
        COMMENT_CHAR = '#'
        OPTION_CHAR =  ' '
        options = {}
        f = open(filename)
        for line in f:
            #for i in svr_options:
                #if i in line:
            #First, remove comments:
            # remove garbage
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
    def setData(self,filename,dict):
        #configGame = mData.parse_config(self,"c:\\temp\\admintools\\admintools\\config\\honfig.ini")
        if exists(filename):
            os.chmod(filename,stat.S_IWRITE )
        with open(filename, 'w') as startup:
            for k, v in dict.items():
                startup.write(f'SetSave "{k}" {v} "0"\n')
        if exists(filename):
            os.chmod(filename, S_IREAD|S_IRGRP|S_IROTH)
        return