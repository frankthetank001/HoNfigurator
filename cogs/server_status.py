#from cogs.dataManager import mData
import cogs.dataManager as dmgr
import cogs.homecoming as udp_lsnr
import os
import subprocess
import psutil
from os.path import exists
from threading import Thread
import glob
import time
import shutil
from datetime import datetime
import traceback
import re

processed_data_dict = dmgr.mData().returnDict()
server_status_dict = {}
match_status = {}
size_changed = True
replay_wait=0
#os.chdir(processed_data_dict['hon_logs_dir'])
#
#   hooks onto hon.exe and manages hon
class honCMD():
    def __init__(self):
        self.server_status = server_status_dict
        #server_status_dict.update({"last_restart":honCMD.getData(self,"lastRestart")})
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
    def check_proc(proc_name):
        for proc in psutil.process_iter():
            if proc.name() == proc_name:
                return True
        return False
    def stop_proc(proc_name):
        for proc in psutil.process_iter():
            if proc.name() == proc_name:
                try:
                    proc.kill()
                except Exception as e:
                    print(e)
    def check_port(port):
            result = os.system(f'netstat -oan |findstr 0.0.0.0:{port}')
            if result == 0:
                print(f"Port {int(port)} is open")
                return True
            else:
                print(f"Port {int(port)} is not open")
                return False
    def playerCount(self):
        check = subprocess.Popen([processed_data_dict['player_count_exe_loc'],processed_data_dict['hon_file_name']],stdout=subprocess.PIPE, text=True)
        i = int(check.stdout.read())
        check.terminate()
        return i
    def simple_match_data(log,type):
        simple_match_data = {}
        simple_match_data.update({'match_time':'In-Lobby phase...'})
        skipped_frames = 0
        skipped_count=True
        match_status.update({'skipped_frames_from_line':0})
        frame_size = 0
        frame_sizes = []
        with open (log, "r", encoding='utf-16-le') as f:
            if type == "match":
                #for num,line in reversed(list(f)):
                for num, line in reversed(list(enumerate(f, 1))):
                    if "PLAYER_SELECT" in line or "PLAYER_RANDOM" in line or "GAME_START" in line or "] StartMatch" in line:
                        if simple_match_data['match_time'] in ('In-Lobby phase...'):
                            simple_match_data.update({'match_time':'Hero select phase...'})
                        skipped_count=False
                    if "Phase(5)" in line:
                        if match_status['skipped_frames_from_line'] == 0:
                            match_status.update({'skipped_frames_from_line':num})
                    if "Server Status" in line and simple_match_data['match_time'] in ('In-Lobby phase...','Hero select phase...'):
                        #Match Time(00:07:00)
                        if "Match Time" in line:
                            pattern="(Match Time\()(.*)(\))"
                            try:
                                match_time=re.search(pattern,line)
                                match_time = match_time.group(2)
                                simple_match_data.update({'match_time':match_time})
                                #tempData.update({'match_log_last_line':num})
                                #print("match_time: "+ match_time)
                                continue
                            except AttributeError as e:
                                pass
                    if skipped_count:
                        if num > match_status['skipped_frames_from_line']:
                            if "Skipped" in line or "skipped" in line:
                                pattern = "\(([^\)]+)\)"
                                skipped_frames+=1
                                try:
                                    frame_size = re.findall(r'\(([^\)]+)\)', line)
                                    frame_size = frame_size[0]
                                    frame_size = frame_size.split(" ")
                                    frame_sizes.append(int(frame_size[0]))
                                except: pass
        try:
            largest_frame = max(frame_sizes)
            simple_match_data.update({'largest_skipped_frame':f"{largest_frame}msec"})
        except:
            simple_match_data.update({'largest_skipped_frame':"No skipped frames."})
        simple_match_data.update({'skipped_frames':skipped_frames})
        return simple_match_data

    def wait_for_replay(self,wait):
        global replay_wait
        # match_id = self.server_status['match_log_location']
        # match_id = match_id.replace(".log","")
        # pattern = f"{match_id}*"
        # list_of_files = glob.glob(processed_data_dict['hon_replays_dir']+"\\"+pattern) # * means all if need specific format then *.csv
        # latest_file = max(list_of_files, key=os.path.getctime)
        replay_wait +=1
        if exists(f"{processed_data_dict['hon_replays_dir']}\\{match_status['match_id']}.honreplay"):
            print("replay generated. closing server NOW")
            honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"[{match_status['match_id']}] {processed_data_dict['hon_replays_dir']}\\{match_status['match_id']}.honreplay generated. Closing server now.","INFO")
            time.sleep(1)
            return True
        else: 
            print(f"[{match_status['match_id']}] Generating replay for match. Delaying restart for up to 5 minutes ({replay_wait}/{wait}sec until server is restarted).")
            if 'replay_notif_in_log' not in match_status:
                honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"[{match_status['match_id']}] Match finished. Waiting for generation of replay (can take up to {wait} seconds","INFO")
                match_status.update({'replay_notif_in_log':True})
            if replay_wait == wait:
                honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"[{match_status['match_id']}] timed out ({replay_wait}/{wait} seconds) waiting for replay. Closing server..","INFO")
                honCMD().restartSERVER(False)
            return False
    def check_cookie(server_status,log,name):
        def write_mtime(log,name):
            last_modified_time_file = f"{server_status['sdc_home_dir']}\\cogs\\{name}_mtime"
            #
            #   This reads the data if it exists
            if (exists(last_modified_time_file)):
                with open(last_modified_time_file, 'r') as last_modified:
                    lastmodData = last_modified.readline()
                last_modified.close()
                try:
                    lastmodData = int(lastmodData)
                except: pass
                #
                #   Gets the current byte size of the log
                fileSize = os.stat(log).st_size
                #
                #   After reading data set temporary file to current byte size
                with open(last_modified_time_file, 'w') as last_modifiedw:
                    last_modifiedw.write(f"{fileSize}")
                last_modifiedw.close()
                return lastmodData
            #
            #   If there was no temporary file to load data from, create it.
            else:
                try:
                    fileSize = os.stat(log).st_size
                    with open(last_modified_time_file, 'w') as last_modified:
                        last_modified.write(f"{fileSize}")
                    last_modified.close()
                except:
                    print(traceback.format_exc())
                    honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    pass
                return fileSize
        hard_data = write_mtime(log,name)
        soft_data = os.stat(log).st_size # initial file size
        status={}
        # if (soft_data > hard_data) or 'first_check' not in status:
        session_cookie_errors = ["session cookie request failed!","invalid session cookie"]
        with open (log, "r", encoding='utf-16-le') as f:
            for line in reversed(list(f)):
                for item in session_cookie_errors:
                    if item in line.lower():
                        return False
                    elif "new session cookie " in line.lower():
                        return True
        return True
        # status.update({'first_check':'Done'})
        #return True
        # else:
        #     return True
    def changePriority(self,priority_realtime):
        if priority_realtime:
            if processed_data_dict['process_priority'] == "normal":
                self.server_status['hon_pid_hook'].nice(psutil.NORMAL_PRIORITY_CLASS)
            elif processed_data_dict['process_priority'] == "high":
                self.server_status['hon_pid_hook'].nice(psutil.HIGH_PRIORITY_CLASS)
            elif processed_data_dict['process_priority'] == "realtime":
                self.server_status['hon_pid_hook'].nice(psutil.REALTIME_PRIORITY_CLASS)
            print("priority set to realtime")
            self.server_status.update({'priority_realtime':priority_realtime})
        else:
            self.server_status['hon_pid_hook'].nice(psutil.IDLE_PRIORITY_CLASS)
            print("priority set to normal")
            self.server_status.update({'priority_realtime':priority_realtime})
        return priority_realtime

    def updateStatus(self,data):
        #
        #   Combine temp data into the sever_status dictionary
        server_status_dict.update(data)
        #print("updated dictionary: " + str(server_status_dict))
        return
    def updateStatus_GI(self,data):
        #
        #   Combine temp data into the sever_status dictionary
        match_status.update(data)
        #print("updated dictionary: " + str(server_status_dict))
        return

    def check_upstream_patch(self): # function to check latest version on masterserver
        import requests
        import re

        version=None
        url = 'http://api.kongor.online/patcher/patcher.php'
        payload = {
            'latest' : '',
            'os': 'was-crIac6LASwoafrl8FrOa',
            'arch' : 'x86_64'
            }
        x = requests.post(url,data=payload)
        data=x.text
        data=re.split(';s:\d+:',data)

        for i in range(len(data)):
            if '"latest_version"' in data[i]:
                version=data[i+1]

        if version != None:
            if '"' in version:
                version=version.replace('"','')
            return version
        else:
            return False

    def getStatus(self):
        return server_status_dict
    def getDataDict(self):
        return processed_data_dict
    def getMatchInfo(self):
        return match_status
   #   Starts server
    def initialise_variables(self):
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
        self.server_status.update({"last_restart":self.last_restart})
        self.server_status.update({"first_run":self.first_run})
        self.server_status.update({"just_collected":self.just_collected})
        self.server_status.update({"game_started":self.game_started})
        self.server_status.update({"tempcount":self.tempcount})
        self.server_status.update({'update_embeds':False})
        self.server_status.update({"embed_updated":self.embed_updated})
        self.server_status.update({"lobby_created":self.lobby_created})
        self.server_status.update({"game_map":"empty"})
        self.server_status.update({"game_type":"empty"})
        self.server_status.update({"game_mode":"empty"})
        self.server_status.update({"game_host":"empty"})
        self.server_status.update({"game_name":"empty"})
        self.server_status.update({"game_version":"empty"})
        self.server_status.update({"spectators":0})
        self.server_status.update({"slots":10})
        self.server_status.update({"referees":0})
        self.server_status.update({"client_ip":"empty"})
        self.server_status.update({"match_info_obtained":False})
        self.server_status.update({"priority_realtime":False})
        self.server_status.update({"restart_required":False})
        self.server_status.update({"game_log_location":"empty"})
        self.server_status.update({"match_log_location":"empty"})
        self.server_status.update({"slave_log_location":"empty"})
        self.server_status.update({"total_games_played_prev":honCMD.getData(self,"TotalGamesPlayed")})
        self.server_status.update({"total_games_played":honCMD.getData(self,"TotalGamesPlayed")})
        #self.server_status.update({'tempcount':-5})
        self.server_status.update({"server_ready":False})
        self.server_status.update({'elapsed_duration':0})
        self.server_status.update({'pending_restart':False})
        self.server_status.update({'server_ready':False})
        self.server_status.update({'server_starting':True})
        self.server_status.update({'cookie':True})
        if processed_data_dict['use_proxy']=='True':
            self.server_status.update({'proxy_online':True})
        self.server_status.update({'scheduled_shutdown':False})
        self.server_status.update({'update_embeds':True})
        self.server_status.update({"hard_reset":False})
        self.server_status.update({'crash':True})
        self.server_status.update({'server_start_attempts':0})
        #self.server_status.update({'restarting_server':False})

        #
        # Match info dictionary
        match_status.update({'match_log_last_line':0})
        match_status.update({'match_id':'empty'})
        match_status.update({'match_time':'Preparation phase..'})
    def assign_cpu(self):
        self.server_status['hon_pid_hook'].cpu_affinity([processed_data_dict['svr_affinity'][0],processed_data_dict['svr_affinity'][1]])
        print()
    def startSERVER(self,from_react):
        #playercount = playercount()
        if self.playerCount() < 0:
            returnlist = []
            if processed_data_dict['use_proxy'] == 'False':
                udp_listener_port = int(processed_data_dict['game_starting_port']) - 1
            else:
                udp_listener_port = int(processed_data_dict['game_starting_port']) + 10000 - 1
            if honCMD.check_port(udp_listener_port) == False:
                try:
                    # create a thread
                    thread = Thread(target=udp_lsnr.Listener.start_listener)
                    thread.start()
                except:
                    print(traceback.format_exc())
                    honCMD().append_line_to_file(f"{processed_data_dict['app_log']}\nCouldn't start the UDP listener required for auto server selection",f"{traceback.format_exc()}","WARNING")


            free_mem = psutil.virtual_memory().free
            if free_mem > 1000000000:
                ram = True
                #
                # set the environment
                os.environ["USERPROFILE"] = processed_data_dict['hon_home_dir']
                os.environ["APPDATA"] = processed_data_dict['hon_root_dir']
                #
                # clean up temporary old files
                old_hon_exe1 = f"{processed_data_dict['hon_directory']}HON_SERVER_{processed_data_dict['svr_id']}_old.exe"
                old_hon_exe2 = f"{processed_data_dict['hon_directory']}KONGOR_ARENA_{processed_data_dict['svr_id']}_old.exe"
                if exists(old_hon_exe1):
                    try:
                        os.remove(old_hon_exe1)
                    except:
                        print(traceback.format_exc())
                        honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                if exists(old_hon_exe2):
                    try:
                        os.remove(old_hon_exe2)
                    except:
                        print(traceback.format_exc())
                        honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                #
                # move replays off into the manager directory. clean up other temporary files
                replays_dest_dir = f"{processed_data_dict['hon_manager_dir']}Documents\\Heroes of Newerth x64\\game\\replays\\"
                try:
                    if not exists(processed_data_dict['hon_replays_dir']):
                        os.makedirs(processed_data_dict['hon_replays_dir'])
                except:
                    print(traceback.format_exc())
                    honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                try:
                    files = os.listdir(processed_data_dict['hon_replays_dir'])
                    replays=[]
                    for file in files:
                        if os.path.isfile(processed_data_dict['hon_replays_dir']+"\\"+file):
                            if file.endswith(".honreplay"):
                                replays.append
                                try:
                                    shutil.move(processed_data_dict['hon_replays_dir']+"\\"+file,replays_dest_dir)
                                except:
                                    print(traceback.format_exc())
                                    honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                            elif file.endswith(".tmp"):
                                print("deleting temporary file "+file)
                                try:
                                    os.remove(processed_data_dict['hon_replays_dir']+"\\"+file)
                                except:
                                    print(traceback.format_exc())
                                    honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        else:
                            print("removing unrequired replay folder " + file)
                            try:
                                shutil.rmtree(processed_data_dict['hon_replays_dir']+"\\"+file,onerror=honCMD.onerror)
                            except:
                                print(traceback.format_exc())
                                honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                except:
                    print(traceback.format_exc())
                    honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                #
                # move stats files off into the manager directory. so manager can resubmit stats
                stats_dest_dir = f"{processed_data_dict['hon_manager_dir']}Documents\\Heroes of Newerth x64\\game\\logs\\"
                try:
                    files = os.listdir(processed_data_dict['hon_logs_dir'])
                    for file in files:
                        if os.path.isfile(processed_data_dict['hon_logs_dir']+"\\"+file):
                            if file.endswith(".stats"):
                                try:
                                    shutil.move(processed_data_dict['hon_logs_dir']+"\\"+file,stats_dest_dir)
                                except:
                                    print(traceback.format_exc())
                                    honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                except:
                    print(traceback.format_exc())
                    honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                #
                # gather networking details
                print("starting service")
                print("collecting port info...")
                tempData = {}
                svr_port = int(processed_data_dict['game_starting_port']) + processed_data_dict['incr_port']
                svr_proxyport = svr_port + 10000
                svr_proxyLocalVoicePort = int(processed_data_dict['voice_starting_port']) + processed_data_dict['incr_port']
                svr_proxyRemoteVoicePort = svr_proxyLocalVoicePort + 10000
                if 'static_ip' not in processed_data_dict:
                    try:
                        svr_ip = dmgr.mData.getData(self,"svr_ip")
                    except:
                        print(traceback.format_exc())
                        honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        svr_ip = processed_data_dict['svr_ip']
                else:
                    svr_ip = processed_data_dict['svr_ip']
                tempData.update({'svr_port':svr_port})
                tempData.update({'svr_proxyLocalVoicePort':svr_proxyLocalVoicePort})
                tempData.update({'svr_proxyport':svr_proxyport})
                tempData.update({'svr_proxyRemoteVoicePort':svr_proxyRemoteVoicePort})
                honCMD.updateStatus(self,tempData)

                #
                #   Start the HoN Server!
                if processed_data_dict['use_proxy']=='True':
                    if honCMD.check_port(svr_proxyport):
                        print()
                    else:
                        print (f"proxy port {svr_proxyport} not online")
                        return "proxy"
                # remove any pending shutdown or pending restart files on startup
                honCMD.check_for_updates(self,"pending_restart")
                honCMD.check_for_updates(self,"pending_shutdown")

                self.honEXE = subprocess.Popen([processed_data_dict['hon_exe'],"-dedicated","-noconfig","-execute",f"Set svr_login {processed_data_dict['svr_login']}:{processed_data_dict['svr_id']}; Set svr_password {processed_data_dict['svr_password']}; Set sv_masterName {processed_data_dict['svr_login']}:; Set svr_slave {processed_data_dict['svr_id']}; Set svr_adminPassword; Set svr_name {processed_data_dict['svr_hoster']} {processed_data_dict['svr_id']}/{processed_data_dict['svr_total']} 0; Set svr_ip {svr_ip}; Set svr_port {svr_port}; Set svr_proxyPort {svr_proxyport}; Set svr_proxyLocalVoicePort {svr_proxyLocalVoicePort}; Set svr_proxyRemoteVoicePort {svr_proxyRemoteVoicePort}; Set man_enableProxy {processed_data_dict['use_proxy']}; Set svr_location {processed_data_dict['svr_region_short']}; Set svr_broadcast true; Set upd_checkForUpdates false; Set sv_autosaveReplay true; Set sys_autoSaveDump true; Set sys_dumpOnFatal true; Set svr_chatPort 11031; Set svr_maxIncomingPacketsPerSecond 300; Set svr_maxIncomingBytesPerSecond 1048576; Set con_showNet false; Set http_printDebugInfo false; Set php_printDebugInfo false; Set svr_debugChatServer false; Set svr_submitStats true; Set svr_chatAddress 96.127.149.202;Set http_useCompression false; Set man_resubmitStats true; Set man_uploadReplays true; Set sv_remoteAdmins ; Set sv_logcollection_highping_value 100; Set sv_logcollection_highping_reportclientnum 1; Set sv_logcollection_highping_interval 120000","-masterserver",processed_data_dict['master_server']])
                
                honCMD().append_line_to_file(processed_data_dict['app_log'],"Server starting.","INFO")
                #
                #   get the ACTUAL PID, otherwise it's just a string. Furthermore we use honp now when talking to PID
                self.server_status.update({'hon_exe':self.honEXE})
                self.honP = self.honEXE.pid
                self.server_status.update({'hon_pid':self.honP})
                honPID = psutil.Process(pid=self.honEXE.pid)
                self.server_status.update({'hon_pid_hook':honPID})

                if processed_data_dict['core_assignment'] not in ("one","two"):
                    honPID.cpu_affinity([0,1])
                else:
                    honPID.cpu_affinity([processed_data_dict['svr_affinity'][0],processed_data_dict['svr_affinity'][1]])

                self.server_status['hon_pid_hook'].nice(psutil.IDLE_PRIORITY_CLASS)
                
                #
                # Reload the dictionary. This is important as we want to start with a blank slate with every server restart.
                honCMD().initialise_variables()
                return True
            else:
                self.server_status.update({'crash':True})
                honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"Insufficient RAM to start server.","WARNING")
                return "ram"
        elif honCMD.check_proc(f"{processed_data_dict['hon_file_name']}") and from_react == False:
            print("detected already running hon instance, attempting to hook on..")
            for proc in psutil.process_iter():
                if proc.name() == processed_data_dict['hon_file_name']:
                    self.honEXE=proc
                    self.honP=proc.pid
            try:
                self.server_status.update({'hon_exe':self.honEXE})
                self.honP = self.honEXE.pid
                self.server_status.update({'hon_pid':self.honP})
                honPID = psutil.Process(pid=self.honEXE.pid)
                self.server_status.update({'hon_pid_hook':honPID})
                honCMD().initialise_variables()
                self.server_status.update({'realtime_priority':True})
                return True
            except:
                print(traceback.format_exc())
                honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")


                
    #
    #   Stop server
    def stopSERVER(self,force):
        if self.playerCount() == 0 or force:
            if self.server_status['hon_exe'] == "empty":
                for proc in psutil.process_iter():
                    if proc.name() == processed_data_dict['hon_file_name']:
                        proc.terminate()
            else: self.server_status['hon_exe'].terminate()
            honCMD().append_line_to_file(processed_data_dict['app_log'],"Server stopped.","INFO")
            # if processed_data_dict['use_proxy'] == 'True':
            #     try:
            #         p = psutil.Process(self.server_status['proxy_pid'])
            #         p.terminate()
            #     except:
            #        print(traceback.format_exc())
            #        honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            self.server_status.update({'update_embeds':True})
            self.server_status.update({'crash':False})
            return True
        return
    def forceSERVER(self):
        if self.server_status['hon_exe'] == "empty":
            for proc in psutil.process_iter():
                if proc.name() == processed_data_dict['hon_file_name']:
                    proc.terminate()
        else: self.server_status['hon_exe'].terminate()
        honCMD().append_line_to_file(processed_data_dict['app_log'],"Server force stopped.","INFO")
        # if processed_data_dict['use_proxy'] == 'True':        
        #     try:
        #         p = psutil.Process(self.server_status['proxy_pid'])
        #         p.terminate()
        #     except:
        #        print(traceback.format_exc())
        #        honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
        self.server_status.update({'update_embeds':True})
        return True

    def restartSERVER(self,force):
        if self.playerCount() == 0 or force:
            hard_reset = honCMD().check_for_updates("pending_restart")
            if hard_reset:
                self.server_status.update({'hard_reset':True})
                honCMD().restartSELF()
            else: 
                honCMD().append_line_to_file(processed_data_dict['app_log'],"Server about to restart.","INFO")
                try:
                    honCMD().stopSERVER(force)
                except:
                    honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                #
                #   Code is stuck waiting for server to turn off
                self.server_status.update({'server_restarting':True})
                #self.server_status.update({'update_embeds':True})
                playercount = self.playerCount()
                while playercount >= 0:
                    time.sleep(1)
                    playercount = self.playerCount()
                #
                #   Once detects server is offline with above code start the server
                try:
                    honCMD().startSERVER(False)
                except:
                    honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
        else:
            self.server_status.update({'update_embeds':True})
            self.server_status.update({'tempcount':-5})
        return True

    def restartSELF(self):
        honCMD().append_line_to_file(processed_data_dict['app_log'],"Server restarting HARD - means we are restarting the actual service or adminbot console for updating.","INFO")
        honCMD().stopSERVER(True)
        incoming_config = dmgr.mData().returnDict_temp()
        if len(incoming_config) > 0:
            if processed_data_dict['use_console'] == 'True':
                if incoming_config['use_console'] == 'True':
                    os.chdir(processed_data_dict['sdc_home_dir'])
                    os.startfile(f"adminbot{processed_data_dict['svr_id']}-launch.exe")
                    os._exit(0)
                elif incoming_config['use_console'] == 'False':
                    os.chdir(processed_data_dict['sdc_home_dir'])
                    os.startfile(f"adminbot{processed_data_dict['svr_id']}-launch.exe")
                    os._exit(0)
            if processed_data_dict['use_console'] == 'False':
                if incoming_config['use_console'] == 'False':
                    os._exit(1)
                elif incoming_config['use_console'] == 'True':
                    honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"I have turned off because I am unable to transition from a windows service to console mode automatically. Sorry about that. Please start me manually in whatever mode you require.","WARNING")
        # No changed configuration inbound
        else:
            if processed_data_dict['use_console'] == 'True':
                os.chdir(processed_data_dict['sdc_home_dir'])
                os.startfile(f"adminbot{processed_data_dict['svr_id']}-launch.exe")
                os._exit(0)
            else:
                os._exit(1)
    def stopSELF(self):
        honCMD().append_line_to_file(processed_data_dict['app_log'],"Server stopping HARD - means we are intentionally stopping the service via server administrator.","INFO")
        try:
            honCMD().stopSERVER(True)
        except:
            honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            return
        if processed_data_dict['use_console'] == 'True':
            os._exit(0)
        else:
            os.system(f"net stop {processed_data_dict['app_name']}")
        #sys.exit(0)
    def reportPlayer(self,reason):
        #
        #   sinister behaviour detected, save log to file.
        #   Players can attempt to start a game on an uknown map file. This causes the server to crash and hang.
        #   We will firstly handle the error, restart the server, and then log the event for investigation.
        if self.server_status['slave_log_location'] == "empty":
            honCMD().getData("getLogList_Slave")
        t = time.localtime()
        timestamp = time.strftime('%b-%d-%Y_%H%M', t)
        with open(f"{processed_data_dict['sdc_home_dir']}\\suspicious\\evt-{timestamp}-{reason}.txt", 'w') as f:
            f.write(f"{reason}\n{processed_data_dict['svr_identifier']}\n{self.server_status['game_map']}\n{self.server_status['game_host']}\n{self.server_status['client_ip']}")
        honCMD().append_line_to_file(processed_data_dict['app_log'],f"Player reported ({self.server_status['game_host']}). Reason: {reason}. Deatils in {processed_data_dict['sdc_home_dir']}\\suspicious\\evt-{timestamp}-{reason}.txt","INFO")
        #save_path = f"{processed_data_dict['sdc_home_dir']}\\suspicious\\[{reason}]-{processed_data_dict['svr_identifier']}-{self.server_status['game_map']}-{self.server_status['game_host']}-{self.server_status['client_ip']}-{timestamp}.log"
        #shutil.copyfile(self.server_status['slave_log_location'], save_path)
    def time():
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    def append_line_to_file(self,file,text,level):
        timenow = honCMD.time()
        with open(file, 'a+') as f:
            f.seek(0)
            data = f.read(100)
            if len(data) > 0:
                f.write("\n")
            f.write(f"[{timenow}] [{level}] {text}")
    def compare_filesizes(self,file,name):
        last_modified_time_file = f"{processed_data_dict['sdc_home_dir']}\\cogs\\{name}_mtime"
        #
        #   This reads the data if it exists
        if (exists(last_modified_time_file)):
            with open(last_modified_time_file, 'r') as last_modified:
                lastmodData = last_modified.readline()
            last_modified.close()
            lastmodData = int(lastmodData)
            #
            #   Gets the current byte size of the log
            fileSize = os.stat(file).st_size
            #
            #   After reading data set temporary file to current byte size
            with open(last_modified_time_file, 'w') as last_modifiedw:
                last_modifiedw.write(f"{fileSize}")
            last_modifiedw.close()
            return lastmodData
        #
        #   If there was no temporary file to load data from, create it.
        else:
            try:
                fileSize = os.stat(file).st_size
                with open(last_modified_time_file, 'w') as last_modified:
                    last_modified.write(f"{fileSize}")
                last_modified.close()
            except:
                print(traceback.format_exc())
                honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                pass
            return fileSize
    def check_for_updates(self,type):
        temFile = processed_data_dict['sdc_home_dir']+"\\"+type
        if exists(temFile):
            if type == "pending_restart":
                remove_me=processed_data_dict['sdc_home_dir']+"\\"+"pending_shutdown"
                if exists(remove_me):
                    try:
                        os.remove(remove_me)
                    except:
                        print(traceback.format_exc())
                        honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            elif type == "pending_shutdown":
                remove_me=processed_data_dict['sdc_home_dir']+"\\"+"pending_restart"
                if exists(remove_me):
                    try:
                        os.remove(remove_me)
                    except:
                        print(traceback.format_exc())
                        honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            try:
                os.remove(temFile)
                honCMD().append_line_to_file(processed_data_dict['app_log'],f"scheduled {type} detected.","INFO")
                #ctypes.windll.kernel32.SetConsoleTitleW(f"{processed_data_dict['app_name']} - {type}")
                return True
            except:
                print(traceback.format_exc())
                honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
        else:
            #ctypes.windll.kernel32.SetConsoleTitleW(f"{processed_data_dict['app_name']}")
            return False
#
#   reads and parses hon server log data
    def getData(self, dtype):
        #
        #   We look if a file called "restart_required" exists. If it does we determine whether an update is pending for the bot, therefore needing to restart
        if dtype == "CheckSchdShutdown":
            temFile = processed_data_dict['sdc_home_dir']+"\\pending_shutdown"
            if exists(temFile):
                try:
                    os.remove(temFile)
                    return True
                except:
                    print(traceback.format_exc())
                    honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            else:
                return False
        if dtype == "TotalGamesPlayed":
            tempList = []
            total_games_file = f"{processed_data_dict['sdc_home_dir']}\\cogs\\total_games_played"
            if (exists(total_games_file)):
                #
                #   Read last value for total games played
                with open(total_games_file, 'r') as f:
                    total_games_from_file = f.read().splitlines()
                f.close()
            #
            #   Add new values to file
            for item in os.listdir(processed_data_dict['hon_logs_dir']):
                if "game" in item or (item.startswith("M") and item.endswith(".log")):
                    tempList.append(item)
            if not tempList:
                print("NO GAME FILE EITHER, we should make one")
                with open(processed_data_dict['hon_logs_dir']+'\\M0000.log', 'w'): pass
                tempList.append("M0000.log")
            try:
                resulting_list = sorted(list(set(total_games_from_file + tempList)))
            except UnboundLocalError:
                resulting_list = sorted(tempList)
            with open(total_games_file, 'wt') as f:
                f.write('\n'.join(resulting_list))
            f.close()
            total_games_played = len(resulting_list)
            return total_games_played

        elif dtype == "CheckInGame":
            tempData = {}
            total_games_played_prev_int = int(self.server_status['total_games_played_prev'])
            total_games_played_now_int = int(honCMD.getData(self,"TotalGamesPlayed"))
            #print ("about to check game started")
            #if (total_games_played_now_int > total_games_played_prev_int and os.stat(self.server_status['game_log_location']).st_size > 0):
            if (total_games_played_now_int > total_games_played_prev_int):
                #
                if self.server_status["game_log_location"] == "empty":
                    honCMD.getData(self,"getLogList_Game")
                #print("checking for game started now")
                
                hard_data = honCMD.compare_filesizes(self,self.server_status["game_log_location"],"slave")
                soft_data = os.stat(self.server_status['game_log_location']).st_size # initial file size

                tempData = {}
                if soft_data > hard_data or 'slave_log_checked' not in self.server_status:
                    self.server_status.update({'slave_log_checked':True})
                    match_id = self.server_status['match_log_location']
                    match_id = match_id.replace(".log","")
                    with open (self.server_status['game_log_location'], "r", encoding='utf-16-le') as f:
                        if self.server_status['game_started'] == False:
                            for line in f:
                                if "PLAYER_SELECT" in line or "PLAYER_RANDOM" in line or "GAME_START" in line or "] StartMatch" in line:
                                    tempData.update({'game_started':True})
                                    tempData.update({'tempcount':-5})
                                    tempData.update({'update_embeds':True})
                                    honCMD.updateStatus(self,tempData)
                                    honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"Match started. {match_id}","INFO")
                                    return True
                        else:
                            # for num, line in enumerate(f, 1):
                            #     if num > match_status['match_log_last_line']:
                            for line in reversed(list(f)):
                                if "Server Status" in line:
                                    #Match Time(00:07:00)
                                    if "Match Time" in line:
                                        pattern="(Match Time\()(.*)(\))"
                                        try:
                                            match_time=re.search(pattern,line)
                                            match_time = match_time.group(2)
                                            if match_time != match_status['match_time']:
                                                tempData.update({'match_time':match_time})
                                                #tempData.update({'match_log_last_line':num})
                                                print("match_time: "+ match_time)
                                                self.server_status.update({'tempcount':-5})
                                                self.server_status.update({'update_embeds':True})
                                                honCMD.updateStatus_GI(self,tempData)
                                                honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"[{match_id}] Match in progress, elapsed duration: {match_time}","INFO")
                                            break
                                        except AttributeError as e:
                                            print(e)
                                    #if "Server Skipped" in line:
                    f.close()                   
            return
        elif dtype == "MatchInformation":
            tempData = {}
            total_games_played_prev_int = int(self.server_status['total_games_played_prev'])
            total_games_played_now_int = int(honCMD.getData(self,"TotalGamesPlayed"))
            #print ("about to check match information")
            if (total_games_played_now_int > total_games_played_prev_int):
                #
                if self.server_status['match_log_location'] == "empty":
                    honCMD.getData(self,"getLogList_Match")

                hard_data = honCMD.compare_filesizes(self,self.server_status["match_log_location"],"match")
                soft_data = os.stat(self.server_status['match_log_location']).st_size # initial file size

                if soft_data > hard_data or 'match_log_checked' not in self.server_status:
                    print("checking match information")
                    self.server_status.update({'match_log_checked':True})
                    with open (self.server_status['match_log_location'], "r", encoding='utf-16-le') as f:
                        if self.server_status['match_info_obtained'] == False:
                            for line in f:
                                if "INFO_MATCH name:" in line:
                                    game_name = re.findall(r'"([^"]*)"', line)
                                    game_name = game_name[0]
                                    tempData.update({'game_name':game_name})
                                    honCMD.updateStatus(self,tempData)
                                    print("game_name: "+ game_name)
                                    if 'TMM' in game_name:
                                        tempData.update({'game_type':'Ranked TMM'})
                                        honCMD.updateStatus(self,tempData)
                                    else:
                                        tempData.update({'game_type':'Public Games'})
                                        honCMD.updateStatus(self,tempData)
                                if "INFO_MAP name:" in line:
                                    game_map = re.findall(r'"([^"]*)"', line)
                                    game_map = game_map[0]
                                    tempData.update({'game_map':game_map})
                                    honCMD.updateStatus(self,tempData)
                                    print("map: "+ game_map)
                                if "INFO_SETTINGS mode:" in line:
                                    game_mode = re.findall(r'"([^"]*)"', line)
                                    game_mode = game_mode[0]
                                    game_mode = game_mode.replace('Mode_','')
                                    tempData.update({'game_mode':game_mode})
                                    honCMD.updateStatus(self,tempData)
                                    print("game_mode: "+ game_mode)
                                    tempData.update({"match_info_obtained":True})
                                    tempData.update({"game_started":True})
                                    tempData.update({"first_run":False})
                                    tempData.update({"lobby_created":True})
                                    tempData.update({"tempcount":-5})
                                    tempData.update({'update_embeds':False})
                                    honCMD.updateStatus(self,tempData)
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
                matchID = matchLoc.replace(".log","")
                match_status.update({'match_id':matchID})
                self.server_status.update({"match_log_location":matchLoc})
                print("Most recent match, matching {}: {}".format(pattern,matchLoc))
                
                # for item in os.listdir():
                #     if "game" in item or (item.startswith("M") and item.endswith(".log")):
                #         tempList.append(item)
                # gameLoc = tempList[len(tempList)-1]
            except:
                print(traceback.format_exc())
                honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                pass
            
            return True
        #
        #   Get latest game lobby logs
        elif dtype == "getLogList_Game":
            print("checking game logs")
            tempList = []
            gameLoc = None
            try:
                # get list of files that matches pattern
                #pattern=f"Slave-1_M*console.clog"
                # new world order - with slaves
                pattern=f"Slave{processed_data_dict['svr_id']}*M*console.clog"
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
                return gameLoc
            except:
                print(traceback.format_exc())
                honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                pass
        #
        #   Get latest server slave log
        elif dtype == "getLogList_Slave":
            print("checking slave logs")
            tempList = []
            for item in os.listdir(processed_data_dict['hon_logs_dir']):
                if (item.startswith("Slave") and item.endswith(".log")) and "Slave-1_M_console.clog" not in item and 'Slave-Temp.log' not in item: #or (item.startswith("Slave-1_M") and item.endswith("console.clog")) 
                    tempList.append(item)
            if not tempList:
                # catch error where there is no slave log, create a temp one.
                print("NO SLAVE LOG. FIRST TIME BOT IS BEING LAUNCHED")
                with open(f"{processed_data_dict['hon_logs_dir']}\\Slave-Temp.log", 'w'): pass
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
                #
                # Commenting temprarily as there are issues if the match is not restarted in between games.
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
                except:
                    print(traceback.format_exc())
                    honCMD().append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
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
            #
            #   Commenting below 3 lines due to an error with encoding. Trying to be consistent
            # dataL = open(self.server_status['slave_log_location'],encoding='utf-16-le')
            # data = dataL.readlines()
            # dataL.close()
            with open (self.server_status['slave_log_location'], "r", encoding='utf-16-le') as f:
                #
                #   Someone has connected to the server and is about to host a game
                for line in f:
                    if "Name: " in line:
                        host = line.split(": ")
                        host = host[2].replace('\n','')
                        tempData.update({'game_host':host})
                        honCMD.updateStatus(self,tempData)
                        print ("host: "+host)
                    if "Version: " in line:
                        version = line.split(": ")
                        version = version[2].replace('\n','')
                        tempData.update({'game_version':version})
                        honCMD.updateStatus(self,tempData)
                        print("version: "+version)
                    if "] IP: " in line:
                        client_ip = line.split(": ")
                        client_ip = client_ip[2].replace('\n','')
                        tempData.update({'client_ip':client_ip})
                        honCMD.updateStatus(self,tempData)
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
                        tempData.update({'update_embeds':True})
                        tempData.update({'tempcount':-5})

                        honCMD.updateStatus(self,tempData)
                        #self.server_status.update[{"first_run":"true"}]
                        #self.server_status.update[{'just_collected':self.just_collected}]
                        #self.server_status.update[{'lobby_created':self.lobby_created}]
                    elif "Successfully got a match ID" in line:
                        self.first_run = False
                        self.just_collected = True
                        self.lobby_created = True

                        tempData.update({'first_run':self.first_run})
                        tempData.update({'just_collected':self.just_collected})
                        tempData.update({'lobby_created':self.lobby_created})
                        honCMD.updateStatus(self,tempData)
            f.close()
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
                tempData.update({'update_embeds':True})
                honCMD.updateStatus(self,tempData)
                return True
            else:
                return
                #time.sleep(5)
