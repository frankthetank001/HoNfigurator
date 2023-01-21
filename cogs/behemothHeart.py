from asyncio.windows_events import NULL
from os.path import exists
from discord.ext import commands
import asyncio
import cogs.server_status as svrcmd
import cogs.dataManager as dmgr
from datetime import datetime
import traceback
import os
import time

svr_state = svrcmd.honCMD()
#hard_reset = False
bot = commands.Bot(command_prefix='!', case_insensitive=True)
alive = False
alive_bkp = False
global embed_log

class heartbeat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.alive = False
        self.processed_data_dict = svr_state.getDataDict()
        #self.svr_ctrl = svrcmd.honCMD()
    # @bot.command()
    # async def getStatus(self,ctx):
    #     return self.server_status
    def time():
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    @bot.command()
    async def heart(self,ctx):
        await ctx.send("💓")
    @bot.command()
    async def getembedlog(self,ctx,log_embed):
        global embed_log
        try:
            embed_log = log_embed[0]
        except Exception: 
            print(traceback.format_exc())
            print("most likely because the auto-sync function is being used, therefore we can't send a log message to anyone yet.")

    def print_and_log(self,log_msg,log_lvl):
        print(log_msg)
        svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",log_msg,log_lvl)
        
    @bot.command()
    async def startheart(self,ctx):
        global embed_log
        global alive
        global alive_bkp

        alive = True
        waiting = False
        proxy_online = False
        
        bot_message = self.bot.get_cog("embedManager")

        self.processed_data_dict = svr_state.getDataDict()
        self.server_status = svr_state.getStatus()
        self.match_status = svr_state.getMatchInfo()
        available_maps_bkp = svr_state.getData("availMaps")
        self.server_status.update({'hard_reset':False})
        self.server_status.update({'backup_heart':True})
        self.server_status.update({'server_ready':False})
        bkup_heart_file=f"{self.processed_data_dict['sdc_home_dir']}\\cogs\\bkup_heart"
        with open(bkup_heart_file, 'w') as f:
            f.write(self.processed_data_dict['disable_bot'])

        
        svr_state.check_current_match_id(False)
        #
        # move replays off into the manager directory. clean up other temporary files
        svr_state.move_replays_and_stats()
        heartbeat_freq = 1
        process_priority = self.processed_data_dict['process_priority']
        process_priority = process_priority.upper()
        restart_timer = 10
        counter_gamecheck = 0
        counter_lobbycheck = 0
        counter_health_checks = 0
        counter_ipcheck = 0
        counter_game_end = 0
        counter_pending_players_leaving = 0
        waited=0
        wait=1800 / heartbeat_freq
        #  Debug setting
        #  playercount = 0
        threshold_gamecheck = 5  / heartbeat_freq # how long we wait before checking if the game has started again
        threshold_lobbycheck = 5  / heartbeat_freq # how long we wait before checking if the lobby has been created yet
        threshold_health_checks = 120 / heartbeat_freq
        threshold_pending_players_leaving = 120 / heartbeat_freq
        counter_ipcheck_threshold = 1800 / heartbeat_freq
        threshold_game_end_check = 180 / heartbeat_freq
        replay_threshold = 330 / heartbeat_freq

        healthcheck_first_run = True
        announce_proxy_health = True

        svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"Starting heartbeat, data dump: {self.processed_data_dict}","INFO")
        print(self.processed_data_dict)
        while alive:
            try:
                proc_priority = svrcmd.honCMD.get_process_priority(self.processed_data_dict['hon_file_name'])
            except Exception: pass
            if alive_bkp==True:
                heartbeat().print_and_log("switching to local heartbeat - without discord bots.","INFO")
                alive_bkp=False
            if exists(bkup_heart_file):
                with open(bkup_heart_file,'r') as f:
                    alive_bkp = f.readline()

            await asyncio.sleep(heartbeat_freq)
            try:
                if self.server_status['hon_pid'] == 'pending':
                    playercount = svr_state.playerCount()
                else:
                    playercount = svr_state.playerCount_pid()
                waited+=1
                # check the live DDOS blacklist for any changes requiring action in firewall
                if (waited >= wait or self.server_status['bot_first_run'] == True) and self.processed_data_dict['svr_id'] == "1":
                    waited+=0
                    self.server_status.update({'bot_first_run':False})
                    svrcmd.honCMD.launch_keeper()
                # check for a scheduled restart, and queue it
                if self.server_status['hard_reset'] == False:
                    try:
                        self.server_status.update({'hard_reset':svr_state.check_for_updates("pending_restart")})
                    except Exception:
                        print(traceback.format_exc())
                        svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                # check for or a scheduled shutdown, and queue it
                if self.server_status['scheduled_shutdown']==False:
                    try:
                        self.server_status.update({'scheduled_shutdown':svr_state.check_for_updates("pending_shutdown")})
                    except Exception:
                        print(traceback.format_exc())
                        svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            except Exception:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            
            if playercount >=2:
                if proc_priority != process_priority:
                    try:
                        svr_state.changePriority(True)
                    except Exception:
                        svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            if playercount == -3:
                if 'crash' in self.server_status:
                    if self.server_status['crash'] == True:
                        if self.server_status['server_start_attempts'] <= 3:
                            start_attempts=self.server_status['server_start_attempts']
                            # server may have crashed, check if we can restart.
                            try:
                                if svr_state.startSERVER("Attempting to start crashed instance"):
                                    heartbeat().print_and_log(f"{self.processed_data_dict['app_log']}",f"SERVER Auto-Recovered due to most likely crash. Check {self.processed_data_dict['hon_game_dir']} for any crash dump files.","WARNING")
                                    if self.processed_data_dict['discord_bots'] == 'True': logEmbed = await bot_message.embedLog(ctx,f"``{heartbeat.time()}`` [DEBUG] RESTARTING SERVER FOR UPDATE")
                                    continue
                                else:
                                    start_attempts+=1
                                    self.server_status.update({'server_start_attempts':start_attempts})
                            except Exception:
                                start_attempts+=1
                                self.server_status.update({'server_start_attempts':start_attempts})
                                print(traceback.format_exc())
                                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                if not proxy_online:
                    if svrcmd.honCMD.check_port(int(self.processed_data_dict['svr_proxyPort'])):
                        announce_proxy_health = True
                        proxy_online = True
                        svr_state.startSERVER("Proxy was offline. Now it's online, attempting to start dead instance")
                    else:
                        if announce_proxy_health:
                            announce_proxy_health = False
                            print("proxy is not online. Waiting.")
            try:
                if playercount == 0:
                    #   Check the process priority, set it to IDLE if it isn't already
                    if proc_priority != "IDLE":
                        try:
                            svr_state.changePriority(False)
                        except Exception:
                            svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    """   [Players: 0] scheduled (restart / shutdown) checks """
                    #   action a scheduled restart, if it's been queued
                    if self.server_status['hard_reset'] == True:
                        if self.match_status['now'] in ["in lobby","in game"]:
                            if svr_state.wait_for_replay(replay_threshold):
                                svr_state.restartSELF("Scheduled restart initiated.")
                        else:
                            svr_state.restartSELF("Scheduled restart initiated.")
                    #   action a scheduled shutdown, if it's been queued
                    if self.server_status['scheduled_shutdown'] == True:
                        if self.match_status['now'] in ["in lobby","in game"]:
                            if svr_state.wait_for_replay(replay_threshold):
                                svr_state.stopSELF("Scheduled shutdown initiated.")
                            else: pass
                        else:
                            print("scheduled shutdown, moving to stop server")
                            svr_state.stopSELF("Scheduled shutdown initiated.")
                    #   check for or action a natural restart inbetween games
                    if self.match_status['now'] in ["in lobby","in game"]:
                        if self.match_status['now'] == "in game":
                            svr_state.wait_for_replay(replay_threshold)
                        else:
                            svr_state.initialise_variables("soft")
                    
                    """  [Players: 0] idle game health checks """
                    counter_ipcheck +=1
                    if self.match_status['now'] == "idle":
                        #   compare the hon process commandline arguments, to the expected commandline arguments from config file
                        running_cmdline = self.server_status['hon_pid_hook'].cmdline()
                        incoming_cmd = dmgr.mData().return_commandline(self.processed_data_dict)
                        if running_cmdline != incoming_cmd:
                            svr_state.restartSERVER(False,"A configuration change has been detected. The server is being restarted to load the new configuration.")
                        #   check whether the code should "summon" the hon server instance, because it's running under a different user context
                        elif self.processed_data_dict['use_console'] == 'True':
                            current_login = os.getlogin()
                            if current_login not in self.server_status['hon_pid_owner']:
                                svr_state.restartSERVER(False,f"The user account which started the server is not the same one which just configured the server. Restarting to load server on {current_login} login")
                        else:
                            if self.server_status['hon_pid_owner'] != "NT AUTHORITY\\SYSTEM":
                                svr_state.restartSERVER(False,"Restarting the server as it has been configured to run in windows service mode. Console will be offloaded to back end system.")
                        #   every counter_ipcheck_threshold seconds, check if the public IP has changed for the server. Schedule a restart if it has
                        if counter_ipcheck == counter_ipcheck_threshold and 'static_ip' not in self.processed_data_dict:
                            counter_ipcheck = 0
                            check_ip = dmgr.mData.getData(NULL,"svr_ip")
                            if check_ip != self.processed_data_dict['svr_ip']:
                                #TODO: Check if this causes any restart loop due to svr_ip not updating?
                                svr_state.restartSERVER(False,f"The server's public IP has changed from {self.processed_data_dict['svr_ip']} to {check_ip}. Restarting server to update.")
                                logEmbed = await bot_message.embedLog(ctx,f"``{heartbeat.time()}`` The server's public IP has changed from {self.processed_data_dict['svr_ip']} to {check_ip}. Restarting server to update.")
                    # every x seconds, check if the proxy port is still listening.
                    counter_health_checks +=1
                    if counter_health_checks>=threshold_health_checks or healthcheck_first_run:
                        healthcheck_first_run = False
                        counter_health_checks=0
                        if self.processed_data_dict['use_proxy'] == 'True':
                            if 'svr_proxyPort' in self.processed_data_dict:
                                proxy_online=svrcmd.honCMD.check_port(int(self.processed_data_dict['svr_proxyPort']))
                                if proxy_online:
                                    print(f"Health check: server proxy port {self.processed_data_dict['svr_proxyPort']} healthy")
                                else:
                                    heartbeat.print_and_log(f"{self.processed_data_dict['app_log']}","The proxy port has stopped listening.","WARNING")
                                    logEmbed = await bot_message.embedLog(ctx,f"``{heartbeat.time()}`` The proxy port ({self.processed_data_dict['svr_proxyPort']}) has stopped listening.")
            except Exception:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            try:
                if playercount >=2:
                    #   set the priority to the chosen in-game priority, once players are 2 or greater
                    if self.server_status['priority_realtime'] == False:
                        svr_state.changePriority(True)
            except Exception:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            try:
                #   Check whether the server has finished launching, by querying the voice listening port (open or not?)
                if self.server_status['server_ready'] == False:
                    if svrcmd.honCMD.check_port(int(self.processed_data_dict['svr_proxyLocalVoicePort'])):
                        waiting = False
                        print(f"Health check: local voice port {self.processed_data_dict['svr_proxyLocalVoicePort']} healthy")
                        print(f"Server ready")
                        self.server_status.update({'server_ready':True})
                    else:
                        if not waiting:
                            waiting = True
                            print(f"Port {self.processed_data_dict['svr_proxyLocalVoicePort']} is not open. Waiting for server to start")
            except Exception:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            try:
                if playercount >= 1:
                    if self.match_status['now'] == "in lobby":
                        #   every threshold_gamecheck seconds, check whether the match has begun
                        counter_gamecheck+=1
                        if counter_gamecheck==threshold_gamecheck:
                            counter_gamecheck=0
                            try:
                                svr_state.check_game_started()
                            except Exception:
                                print(traceback.format_exc())
                                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    elif self.match_status['now'] == "in game":
                        #   get the current in-game match time elapsed
                        svr_state.check_current_game_time()
                    else:
                        if playercount > 1:
                            #   player has connected, check the match ID.
                            #   This works because there was no match ID, now there is. This won't trigger if the console is restarted while a player is connected.
                            svr_state.check_current_match_id(True)
                            self.match_status.update({'at_least_2_players':True})
                        else:
                            #   check the match ID if 2 or more players are connected and the console has been restarted.
                            #   It has no other way to tell if it's an old match ID or a new one
                            svr_state.check_current_match_id(False)
                    if self.match_status['now'] != "idle":
                        if not self.match_status['match_info_obtained']:
                            #   poll the match logs until the lobby/match information is obtained
                            try:
                                svr_state.get_match_information()
                            except Exception:
                                print(traceback.format_exc())
                                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    if (self.server_status['game_map'] != "empty" and self.server_status['game_map'] not in available_maps_bkp):
                        svr_state.restartSERVER(True,f"Server restarting due to attempt to crash server with false map.")
                    elif (self.server_status['game_mode'] == "botmatch" or self.server_status['game_mode'] == "BotMatch") and self.processed_data_dict['allow_botmatches'] == 'False':
                        svr_state.restartSERVER(True,f"Server restarting due to bot match (disallowed).")
                    #
                    #   cookie health checks
                    if self.server_status['slave_log_location'] != 'empty':
                        cookie=svrcmd.honCMD.check_cookie(self.processed_data_dict,self.server_status['slave_log_location'],'slave_cookie_check')
                    if cookie != self.server_status['cookie']:
                        self.server_status.update({'cookie':cookie})
                        self.server_status.update({'tempcount':-5})
                        if cookie == False:
                            heartbeat.print_and_log(f"``{heartbeat.time()}`` [ERROR] No session cookie.","WARNING")
                            logEmbed = await bot_message.embedLog(ctx,f"``{heartbeat.time()}`` [ERROR] No session cookie.")
                            try:
                                await embed_log.edit(embed=logEmbed)
                            except Exception:
                                print(traceback.format_exc())
                                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        else:
                            heartbeat.print_and_log(f"``{heartbeat.time()}`` [OK] Connection recovered.","INFO")
                            logEmbed = await bot_message.embedLog(ctx,f"``{heartbeat.time()}`` [OK] Connection recovered.")
                            try:
                                await embed_log.edit(embed=logEmbed)
                            except Exception:
                                print(traceback.format_exc())
                                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            except Exception:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            try:
                if playercount == 1:
                    if self.match_status['now'] == "in game":
                        #   OPTION 1: every threshold_game_end_check seconds, check if the match is over, despite there still being 1 player connected.
                        counter_game_end +=1
                        if counter_game_end == threshold_game_end_check:
                            counter_game_end = 0
                            if svr_state.check_game_ended():
                                svr_state.restartSERVER(True,f"Server restarting due to game end but 1 player has remained connected for {threshold_game_end_check} seconds.")
                                svr_state.append_line_to_file(f"Server restarting due to game end but 1 player has remained connected for {threshold_game_end_check} seconds.","WARNING")
                        #   OPTION 2: if the match time is over 1 hour, and 1 player is connected, start a timer for 2 minutes, after that, restart server
                        if self.match_status['at_least_2_players']:
                            match_time = self.match_status['match_time']
                            if ":" in match_time:
                                match_too_long = match_time.split(":")
                                match_too_long_hrs = int(match_too_long[0])
                                match_too_long_mins = int(match_too_long[1])
                                if match_too_long_mins >= 45:
                                    counter_pending_players_leaving +=1
                                    if counter_pending_players_leaving >= threshold_pending_players_leaving:
                                        counter_pending_players_leaving = 0
                                        msg = f"Server restarting due to match ongoing for 45+ mins with only 1 players connected. All other players have left the game."
                                        svr_state.append_line_to_file(f"Server restarting due to match ongoing for 45+ mins with only 1 players connected. All other players have left the game.","WARNING")
                                        print(msg)
                                        svr_state.restartSERVER(True,msg)
            except Exception:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            
            if 'tempcount_bkp' not in self.server_status or playercount != self.server_status["tempcount_bkp"]:
                #   print the playercount when the playercount changes
                self.server_status.update({'tempcount_bkp':playercount})
                print(f"players: {playercount}")

    async def startheart_bkp():
        global alive_bkp
        global alive
        alive_bkp='True'
        waiting = False
        proxy_online = False
        processed_data_dict_bkp = svr_state.getDataDict()
        server_status_bkp = svr_state.getStatus()
        match_status_bkp = svr_state.getMatchInfo()
        available_maps_bkp = svr_state.getData("availMaps")
        server_status_bkp.update({'hard_reset':False})
        server_status_bkp.update({'backup_heart':True})
        server_status_bkp.update({'server_ready':False})
        bkup_heart_file=f"{processed_data_dict_bkp['sdc_home_dir']}\\cogs\\bkup_heart"
        with open(bkup_heart_file, 'w') as f:
            f.write("True")

        
        svr_state.check_current_match_id(False)
        #
        # move replays off into the manager directory. clean up other temporary files
        svr_state.move_replays_and_stats()
        heartbeat_freq = 1
        process_priority = processed_data_dict_bkp['process_priority']
        process_priority = process_priority.upper()
        restart_timer = 10
        counter_gamecheck = 0
        counter_lobbycheck = 0
        counter_health_checks = 0
        counter_ipcheck = 0
        counter_game_end = 0
        counter_pending_players_leaving = 0
        waited=0
        wait=1800 / heartbeat_freq
        #  Debug setting
        #  playercount = 0
        threshold_gamecheck = 5  / heartbeat_freq # how long we wait before checking if the game has started again
        threshold_lobbycheck = 5  / heartbeat_freq # how long we wait before checking if the lobby has been created yet
        threshold_health_checks = 120 / heartbeat_freq
        threshold_pending_players_leaving = 120 / heartbeat_freq
        counter_ipcheck_threshold = 1800 / heartbeat_freq
        threshold_game_end_check = 180 / heartbeat_freq
        replay_threshold = 330 / heartbeat_freq

        healthcheck_first_run = True
        announce_proxy_health = True

        svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"Starting heartbeat, data dump: {processed_data_dict_bkp}","INFO")
        print(processed_data_dict_bkp)
        while alive_bkp == 'True':
            try:
                proc_priority = svrcmd.honCMD.get_process_priority(processed_data_dict_bkp['hon_file_name'])
            except Exception: pass
            if exists(bkup_heart_file):
                with open(bkup_heart_file,'r') as f:
                    alive_bkp = f.readline()

            await asyncio.sleep(heartbeat_freq)
            try:
                if server_status_bkp['hon_pid'] == 'pending':
                    playercount = svr_state.playerCount()
                else:
                    playercount = svr_state.playerCount_pid()
                waited+=1
                # check the live DDOS blacklist for any changes requiring action in firewall
                if (waited >= wait or server_status_bkp['bot_first_run'] == True) and processed_data_dict_bkp['svr_id'] == "1":
                    waited+=0
                    server_status_bkp.update({'bot_first_run':False})
                    svrcmd.honCMD.launch_keeper()
                # check for a scheduled restart, and queue it
                if server_status_bkp['hard_reset'] == False:
                    try:
                        server_status_bkp.update({'hard_reset':svr_state.check_for_updates("pending_restart")})
                    except Exception:
                        print(traceback.format_exc())
                        svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
                # check for or a scheduled shutdown, and queue it
                if server_status_bkp['scheduled_shutdown']==False:
                    try:
                        server_status_bkp.update({'scheduled_shutdown':svr_state.check_for_updates("pending_shutdown")})
                    except Exception:
                        print(traceback.format_exc())
                        svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
            except Exception:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
            
            if playercount >=2:
                if proc_priority != process_priority:
                    try:
                        svr_state.changePriority(True)
                    except Exception:
                        svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
            if playercount == -3:
                if 'crash' in server_status_bkp:
                    if server_status_bkp['crash'] == True:
                        if server_status_bkp['server_start_attempts'] <= 3:
                            start_attempts=server_status_bkp['server_start_attempts']
                            # server may have crashed, check if we can restart.
                            try:
                                if svr_state.startSERVER("Attempting to start crashed instance"):
                                    svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"SERVER Auto-Recovered due to most likely crash. Check {processed_data_dict_bkp['hon_game_dir']} for any crash dump files.","WARNING")
                                    continue
                                else:
                                    start_attempts+=1
                                    server_status_bkp.update({'server_start_attempts':start_attempts})
                            except Exception:
                                start_attempts+=1
                                server_status_bkp.update({'server_start_attempts':start_attempts})
                                print(traceback.format_exc())
                                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
                if not proxy_online:
                    if svrcmd.honCMD.check_port(int(processed_data_dict_bkp['svr_proxyPort'])):
                        announce_proxy_health = True
                        proxy_online = True
                        svr_state.startSERVER("Proxy was offline. Now it's online, attempting to start dead instance")
                    else:
                        if announce_proxy_health:
                            announce_proxy_health = False
                            print("proxy is not online. Waiting.")
            try:
                if playercount == 0:
                    #   Check the process priority, set it to IDLE if it isn't already
                    if proc_priority != "IDLE":
                        try:
                            svr_state.changePriority(False)
                        except Exception:
                            svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
                    """   [Players: 0] scheduled (restart / shutdown) checks """
                    #   action a scheduled restart, if it's been queued
                    if server_status_bkp['hard_reset'] == True:
                        if match_status_bkp['now'] in ["in lobby","in game"]:
                            if svr_state.wait_for_replay(replay_threshold):
                                svr_state.restartSELF("Scheduled restart initiated.")
                        else:
                            svr_state.restartSELF("Scheduled restart initiated.")
                    #   action a scheduled shutdown, if it's been queued
                    if server_status_bkp['scheduled_shutdown'] == True:
                        if match_status_bkp['now'] in ["in lobby","in game"]:
                            if svr_state.wait_for_replay(replay_threshold):
                                svr_state.stopSELF("Scheduled shutdown initiated.")
                            else: pass
                        else:
                            print("scheduled shutdown, moving to stop server")
                            svr_state.stopSELF("Scheduled shutdown initiated.")
                    #   check for or action a natural restart inbetween games
                    if match_status_bkp['now'] in ["in lobby","in game"]:
                        if match_status_bkp['now'] == "in game":
                            svr_state.wait_for_replay(replay_threshold)
                        else:
                            svr_state.initialise_variables("soft")
                    
                    """  [Players: 0] idle game health checks """
                    counter_ipcheck +=1
                    if match_status_bkp['now'] == "idle":
                        #   compare the hon process commandline arguments, to the expected commandline arguments from config file
                        running_cmdline = server_status_bkp['hon_pid_hook'].cmdline()
                        incoming_cmd = dmgr.mData().return_commandline(processed_data_dict_bkp)
                        if running_cmdline != incoming_cmd:
                            svr_state.restartSERVER(False,"A configuration change has been detected. The server is being restarted to load the new configuration.")
                        #   check whether the code should "summon" the hon server instance, because it's running under a different user context
                        elif processed_data_dict_bkp['use_console'] == 'True':
                            current_login = os.getlogin()
                            if current_login not in server_status_bkp['hon_pid_owner']:
                                svr_state.restartSERVER(False,f"The user account which started the server is not the same one which just configured the server. Restarting to load server on {current_login} login")
                        else:
                            if server_status_bkp['hon_pid_owner'] != "NT AUTHORITY\\SYSTEM":
                                heartbeat.print_and_log(f"Currently running under user: {server_status_bkp['hon_pid_owner']}, should be 'NT Authority\\System'",'INFO')
                                svr_state.restartSERVER(False,"Restarting the server as it has been configured to run in windows service mode. Console will be offloaded to back end system.")
                        #   every counter_ipcheck_threshold seconds, check if the public IP has changed for the server. Schedule a restart if it has
                        if counter_ipcheck == counter_ipcheck_threshold and 'static_ip' not in processed_data_dict_bkp:
                            counter_ipcheck = 0
                            check_ip = dmgr.mData.getData(NULL,"svr_ip")
                            if check_ip != processed_data_dict_bkp['svr_ip']:
                                #TODO: Check if this causes any restart loop due to svr_ip not updating?
                                svr_state.restartSERVER(False,f"The server's public IP has changed from {processed_data_dict_bkp['svr_ip']} to {check_ip}. Restarting server to update.")
                    # every x seconds, check if the proxy port is still listening.
                    counter_health_checks +=1
                    if counter_health_checks>=threshold_health_checks or healthcheck_first_run:
                        healthcheck_first_run = False
                        counter_health_checks=0
                        if processed_data_dict_bkp['use_proxy'] == 'True':
                            if 'svr_proxyPort' in processed_data_dict_bkp:
                                proxy_online=svrcmd.honCMD.check_port(int(processed_data_dict_bkp['svr_proxyPort']))
                                if proxy_online:
                                    print(f"Health check: server proxy port {processed_data_dict_bkp['svr_proxyPort']} healthy")
                                else:
                                    print(f"Health check: server proxy port {processed_data_dict_bkp['svr_proxyPort']} not online")
                                    svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}","The proxy port has stopped listening.","WARNING")
            except Exception:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
            try:
                if playercount >=2:
                    #   set the priority to the chosen in-game priority, once players are 2 or greater
                    if server_status_bkp['priority_realtime'] == False:
                        svr_state.changePriority(True)
            except Exception:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
            try:
                #   Check whether the server has finished launching, by querying the voice listening port (open or not?)
                if server_status_bkp['server_ready'] == False:
                    if svrcmd.honCMD.check_port(int(processed_data_dict_bkp['svr_proxyLocalVoicePort'])):
                        waiting = False
                        print(f"Health check: local voice port {processed_data_dict_bkp['svr_proxyLocalVoicePort']} healthy")
                        print(f"Server ready")
                        server_status_bkp.update({'server_ready':True})
                    else:
                        if not waiting:
                            waiting = True
                            print(f"Port {processed_data_dict_bkp['svr_proxyLocalVoicePort']} is not open. Waiting for server to start")
            except Exception:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
            try:
                if playercount >= 1:
                    if match_status_bkp['now'] == "in lobby":
                        #   every threshold_gamecheck seconds, check whether the match has begun
                        counter_gamecheck+=1
                        if counter_gamecheck==threshold_gamecheck:
                            counter_gamecheck=0
                            try:
                                svr_state.check_game_started()
                            except Exception:
                                print(traceback.format_exc())
                                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
                    elif match_status_bkp['now'] == "in game":
                        #   get the current in-game match time elapsed
                        svr_state.check_current_game_time()
                    else:
                        if playercount > 1:
                            #   player has connected, check the match ID.
                            #   This works because there was no match ID, now there is. This won't trigger if the console is restarted while a player is connected.
                            svr_state.check_current_match_id(True)
                            match_status_bkp.update({'at_least_2_players':True})
                        else:
                            #   check the match ID if 2 or more players are connected and the console has been restarted.
                            #   It has no other way to tell if it's an old match ID or a new one
                            svr_state.check_current_match_id(False)
                    if match_status_bkp['now'] != "idle":
                        if not match_status_bkp['match_info_obtained']:
                            #   poll the match logs until the lobby/match information is obtained
                            try:
                                svr_state.get_match_information()
                            except Exception:
                                print(traceback.format_exc())
                                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
                    if (server_status_bkp['game_map'] != "empty" and server_status_bkp['game_map'] not in available_maps_bkp):
                        svr_state.restartSERVER(True,f"Server restarting due to attempt to crash server with false map.")
                    elif (server_status_bkp['game_mode'] == "botmatch" or server_status_bkp['game_mode'] == "BotMatch") and processed_data_dict_bkp['allow_botmatches'] == 'False':
                        svr_state.restartSERVER(True,f"Server restarting due to bot match (disallowed).")
            except Exception:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
            try:
                if playercount == 1:
                    if match_status_bkp['now'] == "in game":
                        #   OPTION 1: every threshold_game_end_check seconds, check if the match is over, despite there still being 1 player connected.
                        counter_game_end +=1
                        if counter_game_end == threshold_game_end_check:
                            counter_game_end = 0
                            if svr_state.check_game_ended():
                                svr_state.restartSERVER(True,f"Server restarting due to game end but 1 player has remained connected for {threshold_game_end_check} seconds.")
                        #   OPTION 2: if the match time is over 1 hour, and 1 player is connected, start a timer for 2 minutes, after that, restart server
                        if match_status_bkp['at_least_2_players']:
                            match_time = match_status_bkp['match_time']
                            if ":" in match_time:
                                match_too_long = match_time.split(":")
                                match_too_long_hrs = int(match_too_long[0])
                                match_too_long_mins = int(match_too_long[1])
                                if match_too_long_mins >= 45:
                                    counter_pending_players_leaving +=1
                                    if counter_pending_players_leaving >= threshold_pending_players_leaving:
                                        counter_pending_players_leaving = 0
                                        msg = f"Server restarting due to match ongoing for 45+ mins with only 1 players connected. All other players have left the game."
                                        print(msg)
                                        svr_state.restartSERVER(True,msg)
            except Exception:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
            
            if 'tempcount_bkp' not in server_status_bkp or playercount != server_status_bkp["tempcount_bkp"]:
                #   print the playercount when the playercount changes
                server_status_bkp.update({'tempcount_bkp':playercount})
                print(f"players: {playercount}")

    @bot.command()
    async def stopheart(self,ctx):
        global alive
        alive = False
    @bot.command()
    async def statusheart(self,ctx):
        return alive
    @bot.command()
    async def giveCPR(self,ctx,hoster):
        if hoster == self.processed_data_dict['svr_hoster'] or hoster == self.processed_data_dict['svr_identifier']:
            try:
                await ctx.message.delete()
            except Exception:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            if not alive:
                await ctx.invoke(bot.get_command('startheart'),ctx)
    @bot.command()
    async def kick(self,ctx,hoster):
        if hoster == self.processed_data_dict['svr_hoster'] or hoster == self.processed_data_dict['svr_identifier']:
            try:
                await ctx.message.delete()
            except Exception:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            if hoster == self.processed_data_dict['svr_hoster']:
                await asyncio.sleep(int(self.processed_data_dict['svr_id']))
            self.server_status.update({'update_embeds':True})
            self.server_status.update({'tempcount':-5})
    @bot.command()
    async def pullPlug(self,ctx,hoster):
        if hoster == self.processed_data_dict['svr_identifier']:
            try:
                await ctx.message.delete()
            except Exception:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            await ctx.invoke(bot.get_command('stopheart'),ctx)
    @bot.command()
    async def heartbeat(self,ctx,hoster):
        if hoster == self.processed_data_dict['svr_hoster'] or hoster == self.processed_data_dict['svr_identifier']:
            try:
                await ctx.message.delete()
            except Exception: pass
            playercount = svrcmd.honCMD().playerCount()
            if hoster == self.processed_data_dict['svr_hoster']:
                await asyncio.sleep(int(self.processed_data_dict['svr_id']))
            alive = await ctx.invoke(bot.get_command('statusheart'),ctx)
            try:
                if alive:
                    await ctx.send(f"{self.processed_data_dict['svr_identifier']} Behemoth heart beating 💓 {playercount} players connected",delete_after=5)
                else:
                    await ctx.send(f"{self.processed_data_dict['svr_identifier']} Behemoth heart stopped! :broken_heart:",delete_after=5)
            except Exception:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
    
def setup(bot):
    bot.add_cog(heartbeat(bot))
