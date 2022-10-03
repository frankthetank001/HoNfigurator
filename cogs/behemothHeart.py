from asyncio.windows_events import NULL
from os.path import exists
from discord.ext import commands
import asyncio
import cogs.server_status as svrcmd
import cogs.dataManager as dmgr
from datetime import datetime
import traceback

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
        except: 
            print(traceback.format_exc())
            print("most likely because the auto-sync function is being used, therefore we can't send a log message to anyone yet.")

    @bot.command()
    async def startheart(self,ctx):
        global embed_log
        global alive
        global alive_bkp

        alive = True
        test = self.bot.get_cog("embedManager")
        # alive = True
        self.server_status = svrcmd.honCMD().getStatus()
        self.match_status = svrcmd.honCMD().getMatchInfo()
        self.available_maps = svr_state.getData("availMaps")
        self.server_status.update({'server_restarting':False})
        #self.server_status.update({'server_starting':False})
        self.server_status.update({'hard_reset':False})
        self.server_status.update({'backup_heart':False})
        bkup_heart_file=f"{self.processed_data_dict['sdc_home_dir']}\\cogs\\bkup_heart"
        with open(bkup_heart_file, 'w') as f:
            f.write("False")

        restart_timer = 10
        counter_heartbeat = 0
        counter_heartbeat_attempts = 0
        counter_hosted = 0
        counter_gamecheck = 0
        counter_lobbycheck = 0
        counter_health_checks = 0
        counter_ipcheck = 0
        #  Debug setting
        #  playercount = 0
        threshold_heartbeat = 30    # how long to wait before break from heartbeat to update embeds
        threshold_hosted = 60   # how long we wait for someone to host a game without starting
        threshold_gamecheck = 5 # how long we wait before checking if the game has started again
        threshold_lobbycheck = 5 # how long we wait before checking if the lobby has been created yet
        threshold_health_checks = 30
        counter_ipcheck_threshold = 30
        replay_threshold = 300
        x = 0
        #   this is the start of the heartbeat
        #   anything below is looping

        svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"Starting heartbeat, data dump: {self.processed_data_dict}","INFO")
        while alive == True:
            alive=True
            if alive_bkp==True:
                alive_bkp=False
            counter_heartbeat+=1
            await asyncio.sleep(1)
            try:
                playercount = svrcmd.honCMD.playerCount(self)
                #print(playercount)
            except:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            if playercount >=2:
                try:
                    if self.server_status['priority_realtime'] == False:
                        svr_state.changePriority(True)
                except:
                    print(traceback.format_exc())
                    svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            if playercount == -3:
                if 'crash' in self.server_status:
                    if self.server_status['crash'] == True:
                        if self.server_status['server_start_attempts'] <= 3:
                            start_attempts=self.server_status['server_start_attempts']
                            # server may have crashed, check if we can restart.
                            try:
                                if svr_state.startSERVER(False):
                                    svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"SERVER Auto-Recovered due to most likely crash. Check {self.processed_data_dict['hon_game_dir']} for any crash dump files.","WARNING")
                                    continue
                                else:
                                    start_attempts+=1
                                    self.server_status.update({'server_start_attempts':start_attempts})
                            except:
                                start_attempts+=1
                                self.server_status.update({'server_start_attempts':start_attempts})
                                print(traceback.format_exc())
                                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            if playercount >=0:
                try:
                    counter_health_checks +=1
                    if counter_health_checks>=threshold_health_checks:
                        counter_health_checks=0
                        if self.processed_data_dict['use_proxy'] == 'True':
                            if 'svr_proxyport' in self.server_status:
                                proxy_online=svrcmd.honCMD.check_port(int(self.server_status['svr_proxyport']))
                                if proxy_online:
                                    print("port healthy")
                                else:
                                    proxy_online=False
                                    print(f"proxy port: {self.server_status['svr_proxyport']} not online")
                                    logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [ERROR] Proxy port {self.server_status['svr_proxyport']} offline.")
                                    try:
                                        await embed_log.edit(embed=logEmbed)
                                    except:
                                        print(traceback.format_exc())
                                        svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                                    # svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}","The proxy port has stopped listening. Stopping server to reduce TMM failures.","INFO")
                                    # await test.createEmbed(ctx,playercount)
                                    # svr_state.stopSERVER()
                                if proxy_online !=self.server_status['proxy_online']:
                                    self.server_status.update({'proxy_online':proxy_online})
                                    self.server_status.update({'update_embeds':True})
                                    self.server_status.update({'tempcount':-5})
                        cookie=svrcmd.honCMD.check_cookie(self.processed_data_dict,self.server_status['slave_log_location'],'slave_cookie_check')
                        if cookie != self.server_status['cookie']:
                            self.server_status.update({'cookie':cookie})
                            self.server_status.update({'update_embeds':True})
                            self.server_status.update({'tempcount':-5})
                            if cookie == False:
                                logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [ERROR] No session cookie.")
                                try:
                                    await embed_log.edit(embed=logEmbed)
                                except:
                                    print(traceback.format_exc())
                                    svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                            else:
                                logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [OK] Connection recovered.")
                                try:
                                    await embed_log.edit(embed=logEmbed)
                                except:
                                    print(traceback.format_exc())
                                    svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                except:
                    print(traceback.format_exc())
                    svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            # print(str(playercount))
            #
            #   Check if the server is ready yet
            try:
                if self.server_status['server_ready'] == False:
                    if svr_state.getData("ServerReadyCheck"):
                        self.server_status.update({'server_starting':False})
                        self.server_status.update({'server_restarting':False})
                        if self.processed_data_dict['debug_mode'] == 'True':
                            logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [DEBUG] Server Ready.")
                            try:
                                await embed_log.edit(embed=logEmbed)
                            except:
                                print(traceback.format_exc())
                                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    else:
                        if self.server_status['server_restarting'] == False:
                            self.server_status.update({'server_starting':True})
                        elif self.server_status['server_restarting'] == True:
                            self.server_status.update({'server_starting':False})
            except:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                # else:
                #     self.server_status.update({'server_restarting':True})

            #
            #   playercount has returned to 0 after a game has been completed, or a lobby closed. Server restart required
            if playercount == 0:
                counter_ipcheck +=1
                try:
                    if self.server_status['priority_realtime'] == True:
                        svr_state.changePriority(False)
                except:
                    print(traceback.format_exc())
                    svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","SEVERE")
                # check for or action a scheduled restart
                if self.server_status['hard_reset'] == False:
                    try:
                        self.server_status.update({'hard_reset':svr_state.check_for_updates("pending_restart")})
                    except:
                        print(traceback.format_exc())
                        svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                if self.server_status['hard_reset'] == True:
                    if self.server_status['game_started'] == True:
                        if svr_state.wait_for_replay(replay_threshold):
                            self.server_status.update({'restart_required':True})
                            # dont need to delay the restart if we have the replay.
                            #await asyncio.sleep(restart_timer)
                            self.server_status.update({'tempcount':playercount})    # prevents the heartbeat
                            self.server_status.update({'update_embeds':False})
                            # restart notification
                            if self.processed_data_dict['debug_mode'] == 'True':
                                logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [DEBUG] RESTARTING SERVER FOR UPDATE")
                                try:
                                    await embed_log.edit(embed=logEmbed)
                                except:
                                    print(traceback.format_exc())
                                    svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                            svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}","Scheduled restart initiated.","INFO")
                            svr_state.restartSELF()
                        else: pass
                    else: 
                        self.server_status.update({'restart_required':True})
                        # await test.createEmbed(ctx,playercount)
                        # await asyncio.sleep(restart_timer)
                        self.server_status.update({'tempcount':playercount})    # prevents the heartbeat
                        self.server_status.update({'update_embeds':False})
                        # restart notification
                        if self.processed_data_dict['debug_mode'] == 'True':
                            logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [DEBUG] RESTARTING SERVER FOR UPDATE")
                            try:
                                await embed_log.edit(embed=logEmbed)
                            except:
                                print(traceback.format_exc())
                                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}","Scheduled restart initiated.","INFO")
                        svr_state.restartSELF()
                # check for or action a scheduled shutdown
                if self.server_status['scheduled_shutdown']==False:
                    try:
                        self.server_status.update({'scheduled_shutdown':svr_state.check_for_updates("pending_shutdown")})
                    except:
                        print(traceback.format_exc())
                        svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                if self.server_status['scheduled_shutdown']:
                    if self.server_status['game_started'] == True:
                        if svr_state.wait_for_replay(replay_threshold):
                            logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [DEBUG] SCHEDULED SHUTDOWN")
                            try:
                                await embed_log.edit(embed=logEmbed)
                            except:
                                print(traceback.format_exc())
                                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                            await test.createEmbed(ctx,-3)
                            svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}","Scheduled shutdown initiated.","INFO")
                            svr_state.stopSELF()
                        else: pass
                    else:
                        logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [DEBUG] SCHEDULED SHUTDOWN")
                        try:
                            await embed_log.edit(embed=logEmbed)
                        except:
                            print(traceback.format_exc())
                            svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        await test.createEmbed(ctx,-3)
                        svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}","Scheduled shutdown initiated.","INFO")
                        svr_state.stopSELF()
                # check for or action a natural restart inbetween games
                try:
                    if self.server_status['first_run'] == False:
                        if self.server_status['game_started'] == True:
                            if svr_state.wait_for_replay(replay_threshold):
                                self.server_status.update({"server_restarting":True})
                                await test.createEmbed(ctx,playercount)
                                # restart notification
                                if self.processed_data_dict['debug_mode'] == 'True':
                                    match_id = self.server_status['match_log_location']
                                    match_id = match_id.replace(".log","")
                                    logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [DEBUG] RESTARTING SERVER INBETWEEN GAME {match_id}")
                                    try:
                                        await embed_log.edit(embed=logEmbed)
                                    except:
                                        print(traceback.format_exc())
                                        svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                                svr_state.restartSERVER()
                            else: pass
                        else: 
                            self.server_status.update({"server_restarting":True})
                            await test.createEmbed(ctx,playercount)
                            # restart notification
                            if self.processed_data_dict['debug_mode'] == 'True':
                                match_id = self.server_status['match_log_location']
                                match_id = match_id.replace(".log","")
                                logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [DEBUG] RESTARTING SERVER INBETWEEN GAME {match_id}")
                                try:
                                    await embed_log.edit(embed=logEmbed)
                                except:
                                    print(traceback.format_exc())
                                    svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                            svr_state.restartSERVER()
                        self.server_status.update({'tempcount':playercount})    # prevents the heartbeat
                        self.server_status.update({'update_embeds':False})
                except:
                    print(traceback.format_exc())
                    svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                # every x seconds, check whether the public IP of the server has changed. If so, schedule a restart
                if counter_ipcheck == counter_ipcheck_threshold and 'static_ip' not in self.processed_data_dict:
                    counter_ipcheck = 0
                    try:
                        if self.server_status['game_started'] == False:
                            check_ip = dmgr.mData.getData(self,"svr_ip")
                            if check_ip != self.processed_data_dict['svr_ip']:
                                self.server_status.update({"server_restarting":True})
                                await test.createEmbed(ctx,playercount)
                                if self.processed_data_dict['debug_mode'] == 'True':
                                    logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [DEBUG] RESTARTING AS PUBLIC IP HAS CHANGED.\nFrom ``{self.processed_data_dict['svr_ip']}`` to ``{check_ip}``")
                                    try:
                                        await embed_log.edit(embed=logEmbed)
                                    except:
                                        print(traceback.format_exc())
                                        svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                                svr_state.restartSERVER()
                                self.server_status.update({'tempcount':playercount})    # prevents the heartbeat
                                self.server_status.update({'update_embeds':False})
                    except:
                        print(traceback.format_exc())
                        svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                """
                60 second hosted kick
                COMMENTED TEMPORARILY DUE TO ISSUES WITH MATCH MAKING BOOTING FROM LOBBY
                """
            #if playercount >= 1 and self.server_status['lobby_created'] == False:
                #if self.server_status['lobby_created'] == False:
                    #counter_hosted+=1
                    #counter_lobbycheck+=1
                    # if counter_hosted == threshold_hosted:
                    #     counter_hosted = 0
                    #     self.server_status.update({'server_restarting':True})
                    #     self.server_status.update({'restart_required':True})
                    #     logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [WARN] Kicked {self.server_status['game_host']} for taking too long to create a lobby")
                    #     try:
                    #         await embed_log.edit(embed=logEmbed)
                    #     except:
                    #         print(traceback.format_exc())
                    #         print("most likely due to using auto-sync")
                    #     svr_state.restartSERVER()
                    #     self.server_status.update({'tempcount':-5})    # force the heartbeat

                #if counter_lobbycheck == threshold_lobbycheck:
                #    counter_lobbycheck=0
                #    if self.server_status['first_run'] == True:
                #        svr_state.getData("GameCheck")
                #        if self.server_status['lobby_created'] == True and self.server_status['priority_realtime'] == False:
                #            svr_state.changePriority(True)
            #
            #   Server has been turned on but is not yet ready
                """
                END COMMENT
                """
            #
            #   Check if the match has begun
            if playercount >= 1:
                try:
                    #
                    # Check if a lobby is made
                    if self.server_status['lobby_created'] == False:
                        counter_lobbycheck+=1
                        if counter_lobbycheck == threshold_lobbycheck:
                            counter_lobbycheck=0
                            if self.server_status['first_run'] == True:
                                svr_state.getData("GameCheck")
                    if (self.server_status['game_started'] == False and self.server_status['lobby_created'] == True) or self.server_status['match_info_obtained'] == False:
                        counter_gamecheck+=1
                        if counter_gamecheck==threshold_gamecheck:
                            counter_gamecheck=0
                            if self.server_status['game_started'] == False:
                                try:
                                    svr_state.getData("CheckInGame")
                                except:
                                    print(traceback.format_exc())
                                    svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                            if self.server_status['match_info_obtained'] == False:
                                try:
                                    svr_state.getData("MatchInformation")
                                except:
                                    print(traceback.format_exc())
                                    svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                                if self.server_status['game_started'] == True and self.server_status['match_info_obtained'] == True and self.processed_data_dict['debug_mode'] == 'True':
                                    match_id = self.server_status['match_log_location']
                                    match_id = match_id.replace(".log","")
                                    logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [DEBUG] Game Started / Lobby made - {match_id}")
                                    try:
                                        await embed_log.edit(embed=logEmbed)
                                    except:
                                        print(traceback.format_exc())
                                        svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                except:
                    print(traceback.format_exc())
                    svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                # Verify the lobby settings. Look out for sinister events and handle it.
                #
                #   sinister behaviour detected, save log to file.
                #   Players can attempt to start a game on an uknown map file. This causes the server to crash and hang.
                #   We will firstly handle the error, restart the server, and then log the event for investigation.
                if playercount == 1:
                    if (self.server_status['game_map'] != "empty" and self.server_status['game_map'] not in self.available_maps):
                        try:
                            #hard_reset = svr_state.getData("CheckForUpdates")
                            self.server_status.update({"server_restarting":True})
                            self.server_status.update({"restart_required":True})
                            await test.createEmbed(ctx,playercount)
                            svr_state.reportPlayer("No_Map")
                            logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [WARN] Kicked {self.server_status['game_host']} (IP: ``{self.server_status['client_ip']}``) (Reason: Crashing server with false map value: ``{self.server_status['game_map']}``), RESTARTING...")
                            try:
                                await embed_log.edit(embed=logEmbed)
                            except:
                                print(traceback.format_exc())
                                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                            svr_state.restartSERVER()
                            self.server_status.update({'tempcount':playercount})    # prevents the heartbeat
                            self.server_status.update({'update_embeds':False})
                        except:
                            print(traceback.format_exc())
                            svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    elif (self.server_status['game_mode'] == "botmatch" or self.server_status['game_mode'] == "BotMatch") and self.processed_data_dict['allow_botmatches'] == 'False':
                        try:
                            svr_state.reportPlayer("botmatch")
                        except:
                            print(traceback.format_exc())
                            svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [WARN] Kicked {self.server_status['game_host']} (IP: ``{self.server_status['client_ip']}``) (Reason: creating botmatches), RESTARTING...")
                        try:
                            await embed_log.edit(embed=logEmbed)
                        except:
                            print(traceback.format_exc())
                            svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        self.server_status.update({"server_restarting":True})
                        self.server_status.update({"restart_required":True})
                        await test.createEmbed(ctx,playercount)
                        try:
                            svr_state.restartSERVER()
                        except:
                            print(traceback.format_exc())
                            svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        # try:
                        #     await test.createEmbed(ctx,playercount)
                        # except:
                        #     print(traceback.format_exc())
                        #     svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        self.server_status.update({'tempcount':playercount})    # prevents the heartbeat
                        self.server_status.update({'update_embeds':False})
                        
                    # check for a long-running game of over 1 hr, where there is but a single player connected. Most likely a bug, server should close
                    try:
                        if self.server_status['game_started'] == True:
                            match_time = self.match_status['match_time']
                            if ":" in match_time:
                                match_too_long = match_time.split(":")
                                match_too_long_hrs = int(match_too_long[0])
                                match_too_long_mins = int(match_too_long[1])
                                if match_too_long_hrs > 1:
                                    self.server_status.update({"server_restarting":True})
                                    self.server_status.update({"restart_required":True})
                                    await test.createEmbed(ctx,playercount)
                                    print("Restarting the server. Last remaining player has not left yet.")
                                    svr_state.restartSERVER()
                                    logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [WARN] {self.match_status['match_id']} - Game ongoing for over 1 hour, with only 1 player connected, RESTARTING...")
                                    try:
                                        await embed_log.edit(embed=logEmbed)
                                    except:
                                        print(traceback.format_exc())
                                        svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    except:
                        print(traceback.format_exc())
                        svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        
                #
                #   Game in progress
                #   Start a timer so we can show the elapsed time of the match
                if counter_heartbeat == threshold_heartbeat:
                    counter_heartbeat=0
                    try:
                        if 'game_started' in self.server_status:
                            if self.server_status['game_started'] == True:
                                elapsed_duration = self.server_status['elapsed_duration']
                                elapsed_duration = int(elapsed_duration)
                                elapsed_duration +=1
                                self.server_status.update({'elapsed_duration':elapsed_duration})
                                # self.server_status.update({'update_embeds':True})
                                svr_state.getData("CheckInGame")
                        if playercount != self.server_status['tempcount']:
                            self.server_status.update({'update_embeds':True})
                    except:
                        print(traceback.format_exc())
                        svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        
        
            if self.server_status['update_embeds'] == False or playercount == self.server_status['tempcount'] and (self.server_status['just_collected'] != True and not self.server_status['server_restarting'] == True or not self.server_status['server_starting'] == True): #and just_collected is False:
                alive = True
                #print("idle")
            #   update embeds.
            else:
                counter_heartbeat=0
                print(f"moving to update discord message.. playercount ({str(playercount)})")
                self.server_status.update({'tempcount':playercount})
                self.server_status.update({'update_embeds':False})
                self.server_status.update({'time_waited':counter_hosted})
                svr_state.updateStatus(self.server_status)
                await test.createEmbed(ctx,playercount)
                # if playercount < 0:
                #     self.alive = False

    async def startheart_bkp():
        global alive_bkp
        global alive
        alive_bkp='True'
        processed_data_dict_bkp = svr_state.getDataDict()
        server_status_bkp = svr_state.getStatus()
        match_status_bkp = svr_state.getMatchInfo()
        available_maps_bkp = svr_state.getData("availMaps")
        server_status_bkp.update({'hard_reset':False})
        server_status_bkp.update({'backup_heart':True})
        bkup_heart_file=f"{processed_data_dict_bkp['sdc_home_dir']}\\cogs\\bkup_heart"
        with open(bkup_heart_file, 'w') as f:
            f.write("True")

        heartbeat_freq = 5

        restart_timer = 10
        counter_gamecheck = 0
        counter_lobbycheck = 0
        counter_health_checks = 0
        counter_ipcheck = 0
        #  Debug setting
        #  playercount = 0
        threshold_gamecheck = 5  / heartbeat_freq # how long we wait before checking if the game has started again
        threshold_lobbycheck = 5  / heartbeat_freq # how long we wait before checking if the lobby has been created yet
        threshold_health_checks = 30 / heartbeat_freq
        counter_ipcheck_threshold = 30 / heartbeat_freq
        replay_threshold = 300 / heartbeat_freq

        svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"Starting heartbeat, data dump: {processed_data_dict_bkp}","INFO")
        while alive_bkp == 'True':
            if exists(bkup_heart_file):
                with open(bkup_heart_file,'r') as f:
                    alive_bkp = f.readline()

            await asyncio.sleep(heartbeat_freq)
            try:
                playercount = svrcmd.honCMD().playerCount()
                print("players: " + str(playercount))
            except:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
            
            if playercount >=2:
                try:
                    if server_status_bkp['priority_realtime'] == False:
                        svr_state.changePriority(True)
                except:
                    print(traceback.format_exc())
                    svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
            if playercount == -3:
                if 'crash' in server_status_bkp:
                    if server_status_bkp['crash'] == True:
                        if server_status_bkp['server_start_attempts'] <= 3:
                            start_attempts=server_status_bkp['server_start_attempts']
                            # server may have crashed, check if we can restart.
                            try:
                                if svr_state.startSERVER(False):
                                    svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"SERVER Auto-Recovered due to most likely crash. Check {processed_data_dict_bkp['hon_game_dir']} for any crash dump files.","WARNING")
                                    continue
                                else:
                                    start_attempts+=1
                                    server_status_bkp.update({'server_start_attempts':start_attempts})
                            except:
                                start_attempts+=1
                                server_status_bkp.update({'server_start_attempts':start_attempts})
                                print(traceback.format_exc())
                                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
            try:
                if playercount == 0:
                    counter_ipcheck +=1
                    if server_status_bkp['priority_realtime'] == True:
                        svr_state.changePriority(False)
                    # check for or action a scheduled restart
                    if server_status_bkp['hard_reset'] == False:
                        try:
                            server_status_bkp.update({'hard_reset':svr_state.check_for_updates("pending_restart")})
                        except:
                            print(traceback.format_exc())
                            svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
                    if server_status_bkp['hard_reset'] == True:
                        if server_status_bkp['game_started'] == True:
                            if svr_state.wait_for_replay(replay_threshold):
                                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}","Scheduled restart initiated.","INFO")
                                svr_state.restartSELF()
                            else: pass
                        else:
                            svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}","Scheduled restart initiated.","INFO")
                            svr_state.restartSELF()    
                    # check for or action a scheduled shutdown
                    if server_status_bkp['scheduled_shutdown']==False:
                        try:
                            server_status_bkp.update({'scheduled_shutdown':svr_state.check_for_updates("pending_shutdown")})
                        except:
                            print(traceback.format_exc())
                            svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
                    if server_status_bkp['scheduled_shutdown'] == True:
                        if server_status_bkp['game_started'] == True:
                            if svr_state.wait_for_replay(replay_threshold):
                                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}","Scheduled shutdown initiated.","INFO")
                                svr_state.stopSELF()
                            else: pass
                        else:
                            print("scheduled shutdown, moving to stop server")
                            svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}","Scheduled shutdown initiated.","INFO")
                            svr_state.stopSELF()
                    # check for or action a natural restart inbetween games
                    if server_status_bkp['first_run'] == False:
                        if server_status_bkp['game_started'] == True:
                            if svr_state.wait_for_replay(replay_threshold):
                                svr_state.restartSERVER()
                            else: pass
                        else:
                            svr_state.restartSERVER()
                    # every x seconds, check if the public IP has changed for the server. Schedule a restart if it has
                    if counter_ipcheck == counter_ipcheck_threshold and 'static_ip' not in processed_data_dict_bkp:
                        counter_ipcheck = 0
                        if server_status_bkp['game_started'] == False:
                            check_ip = dmgr.mData.getData(NULL,"svr_ip")
                            # check if svr id is here
                            if check_ip != processed_data_dict_bkp['svr_ip']:
                                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"The server's public IP has changed from {processed_data_dict_bkp['svr_ip']} to {check_ip}. Restarting server to update.","WARN")
                                svr_state.restartSERVER()
                    # every x seconds, check if the proxy port is still listening. If it isn't shutdown the server.
                    if playercount >=0:
                        counter_health_checks +=1
                        if counter_health_checks>=threshold_health_checks:
                            counter_health_checks=0
                            if processed_data_dict_bkp['use_proxy'] == 'True':
                                if 'svr_proxyport' in server_status_bkp:
                                    proxy_online=svrcmd.honCMD.check_port(int(server_status_bkp['svr_proxyport']))
                                    if proxy_online:
                                        print("port healthy")
                                    else:
                                        proxy_online=False
                                        print(f"proxy port: {server_status_bkp['svr_proxyport']} not online")
                                        svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}","The proxy port has stopped listening.","INFO")
                                        # svr_state.stopSELF()
            except:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
            try:
                if playercount >=2:
                    if server_status_bkp['priority_realtime'] == False:
                        svr_state.changePriority(True)
            except:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")

            try:
                if playercount >= 1:
                    #
                    # Check if a lobby is made
                    if server_status_bkp['lobby_created'] == False:
                        counter_lobbycheck+=1
                        if counter_lobbycheck == threshold_lobbycheck:
                            counter_lobbycheck=0
                            if server_status_bkp['first_run'] == True:
                                svr_state.getData("GameCheck")
                    if (server_status_bkp['game_started'] == False and server_status_bkp['lobby_created'] == True) or server_status_bkp['match_info_obtained'] == False:
                        counter_gamecheck+=1
                        if counter_gamecheck==threshold_gamecheck:
                            counter_gamecheck=0
                            if server_status_bkp['game_started'] == False:
                                try:
                                    svr_state.getData("CheckInGame")
                                except:
                                    print(traceback.format_exc())
                                    svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
                            if server_status_bkp['match_info_obtained'] == False:
                                try:
                                    svr_state.getData("MatchInformation")
                                except:
                                    print(traceback.format_exc())
                                    svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
            except:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
            try:
                if playercount == 1:
                    if (server_status_bkp['game_map'] != "empty" and server_status_bkp['game_map'] not in available_maps_bkp):
                        svr_state.restartSERVER()
                    elif (server_status_bkp['game_mode'] == "botmatch" or server_status_bkp['game_mode'] == "BotMatch") and processed_data_dict_bkp['allow_botmatches'] == 'False':
                        try:
                            svr_state.reportPlayer("botmatch")
                        except:
                            print(traceback.format_exc())
                            svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
                        svr_state.restartSERVER()
            except:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
            try:
                if 'game_started' in server_status_bkp:
                    if server_status_bkp['game_started'] == True:
                        match_time = match_status_bkp['match_time']
                        if ":" in match_time:
                            match_too_long = match_time.split(":")
                            match_too_long_hrs = int(match_too_long[0])
                            match_too_long_mins = int(match_too_long[1])
                            if match_too_long_hrs > 1:
                                print("Restarting the server. Last remaining player has not left yet.")
                                svr_state.restartSERVER()
            except:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")

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
            except:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            if not alive:
                await ctx.invoke(bot.get_command('startheart'),ctx)
    @bot.command()
    async def kick(self,ctx,hoster):
        if hoster == self.processed_data_dict['svr_hoster'] or hoster == self.processed_data_dict['svr_identifier']:
            try:
                await ctx.message.delete()
            except:
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
            except:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            await ctx.invoke(bot.get_command('stopheart'),ctx)
    @bot.command()
    async def heartbeat(self,ctx,hoster):
        if hoster == self.processed_data_dict['svr_hoster'] or hoster == self.processed_data_dict['svr_identifier']:
            try:
                await ctx.message.delete()
            except: pass
            playercount = svrcmd.honCMD().playerCount()
            if hoster == self.processed_data_dict['svr_hoster']:
                await asyncio.sleep(int(self.processed_data_dict['svr_id']))
            alive = await ctx.invoke(bot.get_command('statusheart'),ctx)
            try:
                if alive:
                    await ctx.send(f"{self.processed_data_dict['svr_identifier']} Behemoth heart beating 💓 {playercount} players connected",delete_after=5)
                else:
                    await ctx.send(f"{self.processed_data_dict['svr_identifier']} Behemoth heart stopped! :broken_heart:",delete_after=5)
            except:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
    
def setup(bot):
    bot.add_cog(heartbeat(bot))
