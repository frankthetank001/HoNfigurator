#from cogs.dataManager import mData
import cogs.dataManager as dmgr
import os
import subprocess
import psutil
from os.path import exists
import glob
import time
import shutil
import sys
import asyncio
import re

processed_data_dict = dmgr.mData().returnDict()
server_status_dict = {}
os.environ["USERPROFILE"] = processed_data_dict['hon_home_dir']
#os.chdir(processed_data_dict['hon_logs_dir'])
#
#   hooks onto hon.exe and manages hon
class honCMD():
    def __init__(self):
        self.server_status = server_status_dict
        #server_status_dict.update({"last_restart":honCMD.getData(self,"lastRestart")})
        return

    def playerCount(self):
        check = subprocess.Popen([processed_data_dict['player_count_exe_loc'],processed_data_dict['hon_file_name']],stdout=subprocess.PIPE, text=True)
        i = int(check.stdout.read())
        check.terminate()
        return i

    def changePriority(self,priority_realtime):
        if priority_realtime:
            if processed_data_dict['process_priority'] == "normal":
                self.server_status['hon_pid_hook'].nice(psutil.NORMAL_PRIORITY_CLASS)
            elif processed_data_dict['process_priority'] == "high":
                self.server_status['hon_pid_hook'].nice(psutil.HIGH_PRIORITY_CLASS)
            elif processed_data_dict['process_priority'] == "realtime":
                self.server_status['hon_pid_hook'].nice(psutil.REALTIME_PRIORITY_CLASS)
            print("priority set to realtime")
            self.server_status.update({'priority_realtime':True})
        else:
            self.server_status['hon_pid_hook'].nice(psutil.NORMAL_PRIORITY_CLASS)
            print("priority set to normal")
            self.server_status.update({'priority_realtime':False})
        return priority_realtime

    def updateStatus(self,data):
        #
        #   Combine temp data into the sever_status dictionary
        server_status_dict.update(data)
        print("updated dictionary: " + str(server_status_dict))
        return

    def getStatus(self):
        return server_status_dict
    def getDataDict(self):
        return processed_data_dict
   #   Starts server
    def startSERVER(self):
        #playercount = playercount()
        if self.playerCount() < 0 :
            returnlist = []
            free_mem = psutil.virtual_memory().free
            if free_mem > 1000000000:
                ram = True
                #   reload dictionary
                #self.total_games_played_prev = honCMD.getData(self,"TotalGamesPlayed")
                #server_status_dict.update[{'total_games_played_prev':honCMD.getData(self,"TotalGamesPlayed")}]
                #
                #   Start the HoN Server!
                print("starting service")
                self.honEXE = subprocess.Popen([processed_data_dict['hon_exe'],"-dedicated","-masterserver",processed_data_dict['master_server']])
                #   get the ACTUAL PID, otherwise it's just a string. Furthermore we use honp now when talking to PID
                server_status_dict.update({'hon_exe':self.honEXE})
                self.honP = self.honEXE.pid
                server_status_dict.update({'hon_pid':self.honP})
                #server_status_dict.update({"hon_pid":self.honP})
                honPID = psutil.Process(pid=self.honEXE.pid)
                server_status_dict.update({'hon_pid_hook':honPID})
                honPID.cpu_affinity([processed_data_dict['svr_affinity'][0],processed_data_dict['svr_affinity'][1]])

                self.server_status['hon_pid_hook'].nice(psutil.IDLE_PRIORITY_CLASS)
                
                self.first_run = True
                self.just_collected = False
                self.game_started = False
                self.tempcount = -5
                self.embed_updated = False
                self.lobby_created = False
                self.last_restart = honCMD.getData(self,"lastRestart")
                honCMD().getData("update_last_restarted")
                #
                #   Initialise some variables upon hon server starting
                #self.available_maps = honCMD().getData("availMaps")
                server_status_dict.update({"last_restart":self.last_restart})
                server_status_dict.update({"first_run":self.first_run})
                server_status_dict.update({"just_collected":self.just_collected})
                server_status_dict.update({"game_started":self.game_started})
                server_status_dict.update({"tempcount":self.tempcount})
                server_status_dict.update({"embed_updated":self.embed_updated})
                server_status_dict.update({"lobby_created":self.lobby_created})
                server_status_dict.update({"game_map":"empty"})
                server_status_dict.update({"game_type":"empty"})
                server_status_dict.update({"game_mode":"empty"})
                server_status_dict.update({"game_host":"empty"})
                server_status_dict.update({"game_name":"empty"})
                server_status_dict.update({"game_version":"empty"})
                server_status_dict.update({"spectators":0})
                server_status_dict.update({"slots":10})
                server_status_dict.update({"referees":0})
                server_status_dict.update({"client_ip":"empty"})
                server_status_dict.update({"match_info_obtained":False})
                server_status_dict.update({"priority_realtime":False})
                server_status_dict.update({"restart_required":False})
                server_status_dict.update({"game_log_location":"empty"})
                server_status_dict.update({"match_log_location":"empty"})
                server_status_dict.update({"slave_log_location":"empty"})
                server_status_dict.update({"total_games_played_prev":honCMD.getData(self,"TotalGamesPlayed")})
                #server_status_dict.update({'tempcount':-5})
                server_status_dict.update({"server_ready":False})
                server_status_dict.update({'elapsed_duration':0})
                server_status_dict.update({'pending_restart':False})
                server_status_dict.update({'server_ready':False})
                server_status_dict.update({'server_starting':True})
                #self.server_status.update({'restarting_server':False})
                return True
            else:
                return False
    #
    #   Stop server
    def stopSERVER(self):
        if self.playerCount() == 0 or self.server_status['restart_required']==True:
            if self.server_status['hon_exe'] == "empty":
                for proc in psutil.process_iter():
                    if proc.name() == processed_data_dict['hon_file_name']:
                        proc.terminate()
            else: self.server_status['hon_exe'].terminate()
            return True
        return
    def forceSERVER(self):
        if self.server_status['hon_exe'] == "empty":
            for proc in psutil.process_iter():
                if proc.name() == processed_data_dict['hon_file_name']:
                    proc.terminate()
        else: self.server_status['hon_exe'].terminate()
        return True

    def restartSERVER(self):
        if self.playerCount() == 0 or self.server_status['restart_required']==True:
            hard_reset = honCMD().getData("CheckForUpdates")
            if hard_reset:
                self.server_status.update({'hard_reset':True})
                honCMD().restartSELF()
            else: 
                honCMD().stopSERVER()
                #
                #   Code is stuck waiting for server to turn off
                self.server_status.update({'server_restarting':True})
                playercount = self.playerCount()
                while playercount >= 0:
                    time.sleep(1)
                    playercount = self.playerCount()
                #
                #   Once detects server is offline with above code start the server
                honCMD().startSERVER()
        return True

    def restartSELF(self):
        #service_name = "adminbot"+processed_data_dict['svr_id']
        #os.system(f'net stop {service_name} & net start {service_name}')
        sys.exit(1)
    def reportPlayer(self,reason):
        #
        #   sinister behaviour detected, save log to file.
        #   Players can attempt to start a game on an uknown map file. This causes the server to crash and hang.
        #   We will firstly handle the error, restart the server, and then log the event for investigation.
        if self.server_status['slave_log_location'] == "empty":
            honCMD().getData("getLogList_Slave")
        t = time.localtime()
        timestamp = time.strftime('%b-%d-%Y_%H%M', t)
        save_path = f"{processed_data_dict['sdc_home_dir']}\\suspicious\\[{reason}]-{processed_data_dict['svr_identifier']}-{self.server_status['game_map']}-{self.server_status['game_host']}-{self.server_status['client_ip']}-{timestamp}.log"
        shutil.copyfile(self.server_status['slave_log_location'], save_path)
#
#   reads and parses hon server log data
    def getData(self, dtype):
        #
        #   We look if a file called "restart_required" exists. If it does we determine whether an update is pending for the bot, therefore needing to restart
        if dtype == "CheckForUpdates":
            temFile = processed_data_dict['sdc_home_dir']+"\\pending_restart"
            if exists(temFile):
                with open(temFile, "r") as f:
                    data = f.readline()
                f.close()
                os.remove(temFile)
                if data == "True":
                    return True
            else:
                return False
        if dtype == "TotalGamesPlayed":
                tempList = []
                for item in os.listdir(processed_data_dict['hon_logs_dir']):
                    if "game" in item or (item.startswith("M") and item.endswith(".log")):
                        tempList.append(item)
                if not tempList:
                    print("NO GAME FILE EITHER, we should make one")
                    with open(processed_data_dict['hon_logs_dir']+'\\game_0000.log', 'w'): pass
                    tempList.append("game_0000.log")
                total_games_played = len(tempList) 
                return total_games_played
            #
            # Compare the total games played when server started to now. If it's changed, there's a new lobby, come here to check if we're in a match yet.
        elif dtype == "CheckInGame":
            if self.server_status["game_log_location"] == "empty":
                honCMD.getData(self,"getLogList_Game")
            total_games_played_prev_int = int(server_status_dict['total_games_played_prev'])
            total_games_played_now_int = int(honCMD.getData(self,"TotalGamesPlayed"))
            print ("about to check game started")
            if (total_games_played_now_int > total_games_played_prev_int and os.stat(self.server_status['game_log_location']).st_size > 0):
                print("checking for game started now")
                with open (self.server_status['game_log_location'], "r", encoding='utf-16-le') as f:
                    for line in f:
                        if "PLAYER_SELECT" in line or "PLAYER_RANDOM" in line or "GAME_START" in line or "] StartMatch" in line:
                            server_status_dict.update({'game_started':True})
                            server_status_dict.update({'tempcount':-5})
                            return True
            return
        elif dtype == "MatchInformation":
            tempData = {}
            
            if self.server_status['match_log_location'] == "empty":
                honCMD.getData(self,"getLogList_Match")
            #softSlave = mData.getData(self,"loadSoftSlave")
            #hardSlave = mData.getData(self,"loadHardSlave")

            #if softSlave is not hardSlave: #and check_lobby is True:
            dataL = open(self.server_status['match_log_location'],encoding='utf-16-le')
            data = dataL.readlines()
            dataL.close()
            total_games_played_prev_int = int(server_status_dict['total_games_played_prev'])
            total_games_played_now_int = int(honCMD.getData(self,"TotalGamesPlayed"))
            print ("about to check match information")
            if (total_games_played_now_int > total_games_played_prev_int and os.stat(self.server_status['game_log_location']).st_size > 0):
                print("checking match information")
                with open (self.server_status['match_log_location'], "r", encoding='utf-16-le') as f:
                    for line in f:
                        if "INFO_MATCH name:" in line:
                            game_name = re.findall(r'"([^"]*)"', line)
                            game_name = game_name[0]
                            tempData.update({'game_name':game_name})
                            honCMD().updateStatus(tempData)
                            print("game_name: "+ game_name)
                            if 'TMM' in game_name:
                                tempData.update({'game_type':'Ranked TMM'})
                                honCMD().updateStatus(tempData)
                            else:
                                tempData.update({'game_type':'Public Games'})
                                honCMD().updateStatus(tempData)
                        if "INFO_MAP name:" in line:
                            game_map = re.findall(r'"([^"]*)"', line)
                            game_map = game_map[0]
                            tempData.update({'game_map':game_map})
                            honCMD().updateStatus(tempData)
                            print("map: "+ game_map)
                        if "INFO_SETTINGS mode:" in line:
                            game_mode = re.findall(r'"([^"]*)"', line)
                            game_mode = game_mode[0]
                            tempData.update({'game_mode':game_mode})
                            honCMD().updateStatus(tempData)
                            print("game_mode: "+ game_mode)
                            tempData.update({"match_info_obtained":True})
                            tempData.update({"game_started":True})
                            honCMD().updateStatus(tempData)
        #
        #   Get the last restart time
        elif dtype == "lastRestart":
            if exists(processed_data_dict['last_restart_loc']):
                with open(processed_data_dict['last_restart_loc'], 'r') as f:
                    last_restart = f.readline()
                f.close()
            else:
                last_restart = "not yet restarted"
                with open(processed_data_dict['last_restart_loc'], 'w') as f:
                    f.write(last_restart)
            return last_restart
        #
        #   Update the last restart time
        elif dtype == "update_last_restarted":
            t = time.localtime()
            last_restart_time = time.strftime('%b-%d-%Y %H:%M', t)
            with open (processed_data_dict['last_restart_loc'], 'w') as f:
                f.write(last_restart_time)
            return
        #
        #   Get a list of all local maps
        elif dtype == "availMaps":
            available_maps = []
            for item in os.listdir(f"{processed_data_dict['hon_directory']}game\\maps"):
                if item.endswith(".s2z"):
                    item = item.replace('.s2z','')
                    print("adding to list: "+str(item))
                    available_maps.append(item)
            return available_maps
        #
        #   Get latest match log
        elif dtype == "getLogList_Match":
            print("checking game logs")
            tempList = []
            try:
                # get list of files that matches pattern
                pattern="M*.log"
                #pattern="M*log"

                files = list(filter(os.path.isfile,glob.glob(pattern)))

                # sort by modified time
                files.sort(key=lambda x: os.path.getmtime(x))

                # get last item in list
                matchLoc = files[-1]
                self.server_status.update({"match_log_location":matchLoc})
                print("Most recent match, matching {}: {}".format(pattern,matchLoc))
                
                # for item in os.listdir():
                #     if "game" in item or (item.startswith("M") and item.endswith(".log")):
                #         tempList.append(item)
                # gameLoc = tempList[len(tempList)-1]
            except Exception as e:
                print(e)
                pass
            
            return True
        #
        #   Get latest game lobby logs
        elif dtype == "getLogList_Game":
            print("checking game logs")
            tempList = []
            try:
                # get list of files that matches pattern
                pattern="Slave-1_M*console.clog"
                #pattern="M*log"

                files = list(filter(os.path.isfile,glob.glob(pattern)))

                # sort by modified time
                files.sort(key=lambda x: os.path.getmtime(x))

                # get last item in list
                gameLoc = files[-1]
                self.server_status.update({"game_log_location":gameLoc})
                print("Most recent file matching {}: {}".format(pattern,gameLoc))
                
                # for item in os.listdir():
                #     if "game" in item or (item.startswith("M") and item.endswith(".log")):
                #         tempList.append(item)
                # gameLoc = tempList[len(tempList)-1]
            except Exception as e:
                print(e)
                pass
            
            return True
        #
        #   Get latest server slave log
        elif dtype == "getLogList_Slave":
            print("checking slave logs")
            tempList = []
            for item in os.listdir():
                if (item.startswith("Slave") and item.endswith(".log")) and "Slave-1_M_console.clog" not in item and 'Slave-Temp.log' not in item: #or (item.startswith("Slave-1_M") and item.endswith("console.clog")) 
                    tempList.append(item)
            if not tempList:
                # catch error where there is no slave log, create a temp one.
                print("NO SLAVE LOG. FIRST TIME BOT IS BEING LAUNCHED")
                with open("Slave-Temp.log", 'w'): pass
                tempList.append("Slave-Temp.log")
            slaveLog = tempList[len(tempList)-1]
            self.server_status.update({"slave_log_location":slaveLog})
            return True
            
        #
        #   Get the file size of the slave log and write it to a temporary file
        elif dtype == "loadHardSlave":
            last_modified_time_file = f"{processed_data_dict['sdc_home_dir']}\\last_modified_time"
            #
            #   This reads the data if it exists
            if (exists(last_modified_time_file)):
                with open(last_modified_time_file, 'r') as last_modified:
                    lastmodData = last_modified.readline()
                last_modified.close()
                lastmodData = int(lastmodData)
                #
                #   Gets the current byte size of the slave log
                if self.server_status['slave_log_location'] == "empty":
                    honCMD.getData(self,"getLogList_Slave")
                fileSize = os.stat(self.server_status['slave_log_location']).st_size
                #
                #   After reading data set temporary file to current byte size
                with open(last_modified_time_file, 'w') as last_modifiedw:
                    last_modifiedw.write(f"{fileSize}")
                last_modifiedw.close()
                return lastmodData
            #
            #   If there was no temporary file to load data from, create it.
            else:
                if self.server_status['slave_log_location'] == "empty":
                    honCMD.getData(self,"getLogList_Slave")
                try:
                    fileSize = os.stat(self.server_status['slave_log_location']).st_size
                    with open(last_modified_time_file, 'w') as last_modified:
                        last_modified.write(f"{fileSize}")
                    last_modified.close()
                except Exception as e:
                    print(e)
                    pass
                return fileSize
        #
        #    Get the real byte size of the slave log.
        elif dtype == "loadSoftSlave":
            if self.server_status['slave_log_location'] == "empty":
                    honCMD.getData(self,"getLogList_Slave")
            fileSize = os.stat(self.server_status['slave_log_location']).st_size
            return fileSize
        #
        # Come here when a lobby has been created, and the real slave log byte is different to the current byte size, and start collecting lobby information.
        elif dtype == "GameCheck":
            tempData = {}
            
            if self.server_status['slave_log_location'] == "empty":
                honCMD.getData(self,"getLogList_Slave")
            #softSlave = mData.getData(self,"loadSoftSlave")
            #hardSlave = mData.getData(self,"loadHardSlave")

            #if softSlave is not hardSlave: #and check_lobby is True:
            dataL = open(self.server_status['slave_log_location'],encoding='utf-16-le')
            data = dataL.readlines()
            dataL.close()
            #
            #   Someone has connected to the server and is about to host a game
            for line in data:
                if "Name: " in line:
                    host = line.split(": ")
                    host = host[2].replace('\n','')
                    tempData.update({'game_host':host})
                    honCMD().updateStatus(tempData)
                    print ("host: "+host)
                if "Version: " in line:
                    version = line.split(": ")
                    version = version[2].replace('\n','')
                    tempData.update({'game_version':version})
                    honCMD().updateStatus(tempData)
                    print("version: "+version)
                if "Connection request from: " in line:
                    client_ip = line.split(": ")
                    client_ip = client_ip[2].replace('\n','')
                    tempData.update({'client_ip':client_ip})
                    honCMD().updateStatus(tempData)
                    print(client_ip)
                #
                #   Arguments passed to server, and lobby starting
                if "GAME_CMD_CREATE_GAME" in line:
                    print("lobby starting....")
                    test = line.split(' ')
                    for parameter in test:
                        if "map:" in parameter:
                            map = parameter.split(":")
                            map = map[1]
                            tempData.update({'game_map':map})
                            print("map: "+ map)
                        if "mode:" in parameter:
                            mode = parameter.split(":")
                            mode = mode[1]
                            tempData.update({'game_mode':mode})
                            print("mode: "+ mode)
                        if "teamsize:" in parameter:
                            teamsize = parameter.split(":")
                            teamsize = teamsize[1]
                            slots = int(teamsize)
                            slots *= 2
                            tempData.update({'slots':slots})
                            print("teamsize: "+ teamsize)
                            print("slots: "+ str(slots))
                        if "spectators:" in parameter:
                            spectators = parameter.split(":")
                            spectators = spectators[1]
                            spectators = int(spectators)
                            tempData.update({'spectators':spectators})
                            print("spectators: "+ str(spectators))
                        if "referees:" in parameter:
                            referees = parameter.split(":")
                            referees = referees[1]
                            referees = int(referees)
                            tempData.update({'referees':referees})
                            print("referees: "+ str(referees))
                    total_slots = slots + spectators + referees
                    # 
                    #   Set firstrunthrough to false so we don't accidentally come back here and waste IO.
                    #   Also set some other booleans for code logic later on
                    self.first_run = False
                    self.just_collected = True
                    self.lobby_created = True

                    tempData.update({'first_run':self.first_run})
                    tempData.update({'just_collected':self.just_collected})
                    tempData.update({'lobby_created':self.lobby_created})
                    tempData.update({'total_slots':total_slots})

                    honCMD().updateStatus(tempData)
                    #server_status_dict.update[{"first_run":"true"}]
                    #server_status_dict.update[{'just_collected':self.just_collected}]
                    #server_status_dict.update[{'lobby_created':self.lobby_created}]
                elif "Successfully got a match ID" in line:
                    self.first_run = False
                    self.just_collected = True
                    self.lobby_created = True

                    tempData.update({'first_run':self.first_run})
                    tempData.update({'just_collected':self.just_collected})
                    tempData.update({'lobby_created':self.lobby_created})
                    tempData.update({'game_type':"Ranked TMM"})
                    honCMD().updateStatus(tempData)
                    #tempData.update({'total_slots':total_slots})
            return tempData
        elif dtype == "ServerReadyCheck":
            tempData = {}
            # while True:
            if self.server_status['slave_log_location'] == "empty":
                honCMD().getData("getLogList_Slave")
            file1 = os.stat(self.server_status['slave_log_location']) # initial file size
            file1_size = file1.st_size
        
            # your script here that collects and writes data (increase file size)
            time.sleep(1)
            file2 = os.stat(self.server_status['slave_log_location']) # updated file size
            file2_size = file2.st_size
            comp = file2_size - file1_size # compares sizes
            if comp == 0:
                tempData.update({'server_ready':True})
                tempData.update({'tempcount':-5})
                honCMD().updateStatus(tempData)
                return True
            else:
                return
                #time.sleep(5)
