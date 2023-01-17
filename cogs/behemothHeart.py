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

        heartbeat_freq = 1
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
        counter_ipcheck_threshold = 1800
        replay_threshold = 330 / heartbeat_freq
        process_priority = self.processed_data_dict['process_priority']
        process_priority = process_priority.upper()
        x = 0
        #   this is the start of the heartbeat
        #   anything below is looping

        svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"Starting heartbeat, data dump: {self.processed_data_dict}","INFO")
        print(self.processed_data_dict)
        while alive == True:
            alive=True
            try:
                proc_priority = svrcmd.honCMD.get_process_priority(self.processed_data_dict['hon_file_name'])
            except: pass
            if alive_bkp==True:
                print("switching to discord heartbeat - with bots.")
                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"switching to discord heartbeat - with bots.","INFO")
                alive_bkp=False
            counter_heartbeat+=1
            await asyncio.sleep(heartbeat_freq)
            try:
                playercount = svrcmd.honCMD.playerCount(self)
                #print(playercount)
            except:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            if playercount >=2:
                try:
                    if proc_priority != process_priority:
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
                                    print("Health check: port healthy")
                                else:
                                    proxy_online=False
                                    print(f"Health check: proxy port: {self.server_status['svr_proxyport']} not online")
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
                        if self.server_status['slave_log_location'] != 'empty':
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
                    if svrcmd.honCMD.check_port(int(self.processed_data_dict['svr_proxyLocalVoicePort'])):
                        print(f"Port {self.processed_data_dict['svr_proxyLocalVoicePort']} is open")
                        self.server_status.update({'server_ready':True})
                    #if svr_state.getData("ServerReadyCheck"):
                        self.server_status.update({'server_starting':False})
                        self.server_status.update({'server_restarting':False})
                        self.server_status.update({'update_embeds':True})
                        self.server_status.update({'tempcount':-5})
                        # if self.processed_data_dict['core_assignment'] not in ("one","two"):
                        #     svr_state.assign_cpu()
                        #     print("Server ready.")
                        if self.processed_data_dict['debug_mode'] == 'True':
                            logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [DEBUG] Server Ready.")
                            try:
                                await embed_log.edit(embed=logEmbed)
                            except:
                                print(traceback.format_exc())
                                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    else:
                        if not waiting:
                            waiting = True
                            print(f"Port {self.processed_data_dict['svr_proxyLocalVoicePort']} is not open. Waiting for server to start")
                        if self.server_status['bot_first_run'] == True:
                            self.server_status.update({'bot_first_run':False})
                            self.server_status.update({'tempcount':playercount})    # prevents the heartbeat
                            self.server_status.update({'update_embeds':False})
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
                    if proc_priority != "IDLE":
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
                                match_id = self.server_status['match_log_location']
                                match_id = match_id.replace(".log","")
                                # restart notification
                                if self.processed_data_dict['debug_mode'] == 'True':
                                    logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [DEBUG] RESTARTING SERVER INBETWEEN GAME {match_id}")
                                    try:
                                        await embed_log.edit(embed=logEmbed)
                                    except:
                                        print(traceback.format_exc())
                                        svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"[{match_id}] Server restarting inbetween games","INFO")
                                svr_state.restartSERVER(False)
                            else: pass
                        else: 
                            self.server_status.update({"server_restarting":True})
                            await test.createEmbed(ctx,playercount)
                            # restart notification
                            match_id = self.server_status['match_log_location']
                            match_id = match_id.replace(".log","")
                            if self.processed_data_dict['debug_mode'] == 'True':
                                logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [DEBUG] RESTARTING SERVER INBETWEEN GAME {match_id}")
                                try:
                                    await embed_log.edit(embed=logEmbed)
                                except:
                                    print(traceback.format_exc())
                                    svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                            svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"[{match_id}] Server restarting inbetween games","INFO")
                            svr_state.restartSERVER(False)
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
                                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"The server's public IP has changed from {self.processed_data_dict['svr_ip']} to {check_ip}. Restarting server to update.","INFO")
                                svr_state.restartSERVER(False)
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
                    #     logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [WARN] Kicked {self.server_status['game_host']} for taking too long to create a lobby")
                    #     try:
                    #         await embed_log.edit(embed=logEmbed)
                    #     except:
                    #         print(traceback.format_exc())
                    #         print("most likely due to using auto-sync")
                    #     svr_state.restartSERVER(True)
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
                            await test.createEmbed(ctx,playercount)
                            svr_state.reportPlayer("No_Map")
                            logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [WARN] Kicked {self.server_status['game_host']} (IP: ``{self.server_status['client_ip']}``) (Reason: Crashing server with false map value: ``{self.server_status['game_map']}``), RESTARTING...")
                            try:
                                await embed_log.edit(embed=logEmbed)
                            except:
                                print(traceback.format_exc())
                                svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                            svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"Server restarting due to attempt to crash server with false map.","INFO")
                            svr_state.restartSERVER(True)
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
                        await test.createEmbed(ctx,playercount)
                        try:
                            svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"Server restarting due to bot match (disallowed).","INFO")
                            svr_state.restartSERVER(True)
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
                                if match_too_long_hrs >= 1:
                                    self.server_status.update({"server_restarting":True})
                                    await test.createEmbed(ctx,playercount)
                                    print("Restarting the server. Last remaining player has not left yet.")
                                    svr_state.append_line_to_file(f"{self.processed_data_dict['app_log']}",f"Server restarting due to match ongoing for 1+ with only 1 players connected.","INFO")
                                    svr_state.restartSERVER(True)
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
        waited=0
        wait=1800 / heartbeat_freq
        #  Debug setting
        #  playercount = 0
        threshold_gamecheck = 5  / heartbeat_freq # how long we wait before checking if the game has started again
        threshold_lobbycheck = 5  / heartbeat_freq # how long we wait before checking if the lobby has been created yet
        threshold_health_checks = 30 / heartbeat_freq
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
            except: pass
            if exists(bkup_heart_file):
                with open(bkup_heart_file,'r') as f:
                    alive_bkp = f.readline()

            await asyncio.sleep(heartbeat_freq)
            try:
                playercount = svr_state.playerCount_pid()
                # if match_status_bkp['now'] == "in lobby":
                #     playercount = 0
                # else: playercount = 1
                waited+=1
                if (waited >= wait or server_status_bkp['bot_first_run'] == True) and processed_data_dict_bkp['svr_id'] == "1":
                    waited+=0
                    server_status_bkp.update({'bot_first_run':False})
                    svrcmd.honCMD.launch_keeper()
            except:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
            
            if playercount >=2:
                if proc_priority != process_priority:
                    try:
                        svr_state.changePriority(True)
                    except:
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
                if not proxy_online:
                    if svrcmd.honCMD.check_port(int(processed_data_dict_bkp['svr_proxyPort'])):
                        announce_proxy_health = True
                        proxy_online = True
                        svr_state.startSERVER(True)
                    else:
                        if announce_proxy_health:
                            announce_proxy_health = False
                            print("proxy is not online. Waiting.")
            try:
                if playercount == 0:
                    counter_ipcheck +=1
                    if proc_priority != "IDLE":
                        try:
                            svr_state.changePriority(False)
                        except:
                            svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
                    # check for or action a scheduled restart
                    if server_status_bkp['hard_reset'] == False:
                        try:
                            server_status_bkp.update({'hard_reset':svr_state.check_for_updates("pending_restart")})
                        except:
                            print(traceback.format_exc())
                            svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
                    if server_status_bkp['hard_reset'] == True:
                        if match_status_bkp['now'] in ["in lobby","in game"]:
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
                        if match_status_bkp['now'] in ["in lobby","in game"]:
                            if svr_state.wait_for_replay(replay_threshold):
                                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}","Scheduled shutdown initiated.","INFO")
                                svr_state.stopSELF()
                            else: pass
                        else:
                            print("scheduled shutdown, moving to stop server")
                            svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}","Scheduled shutdown initiated.","INFO")
                            svr_state.stopSELF()
                    # check for or action a natural restart inbetween games
                    if match_status_bkp['now'] in ["in lobby","in game"]:
                        if match_status_bkp['now'] == "in game":
                            svr_state.wait_for_replay(replay_threshold)
                                #svr_state.initialise_variables("reload")
                        else:
                            svr_state.initialise_variables("soft")
                    if match_status_bkp['now'] == "idle":
                        running_cmdline = server_status_bkp['hon_pid_hook'].cmdline()
                        incoming_cmd = dmgr.mData().return_commandline(processed_data_dict_bkp)
                        if running_cmdline != incoming_cmd:
                            svr_state.restartSERVER(False,"A configuration change has been detected. The server is being restarted to load the new configuration.")
                        elif processed_data_dict_bkp['use_console'] == 'True':
                            current_login = os.getlogin()
                            if current_login not in server_status_bkp['hon_pid_owner']:
                                svr_state.restartSERVER(False,f"The user account which started the server is not the same one which just configured the server. Restarting to load server on {current_login} login")
                        else:
                            if server_status_bkp['hon_pid_owner'] != "NT AUTHORITY\\SYSTEM":
                                svr_state.restartSERVER(False,"Restarting the server as it has been configured to run in windows service mode. Console will be offloaded to back end system.")
                    # else:
                    #     svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"[{match_status_bkp['match_id']}] Server restarting inbetween games","INFO")
                    #     svr_state.restartSERVER(False)
                    # every x seconds, check if the public IP has changed for the server. Schedule a restart if it has
                    if counter_ipcheck == counter_ipcheck_threshold and 'static_ip' not in processed_data_dict_bkp:
                        counter_ipcheck = 0
                        if server_status_bkp['game_started'] == False:
                            check_ip = dmgr.mData.getData(NULL,"svr_ip")
                            # check if svr id is here
                            if check_ip != processed_data_dict_bkp['svr_ip']:
                                #TODO: Check if this causes any restart loop due to svr_ip not updating?
                                msg = f"The server's public IP has changed from {processed_data_dict_bkp['svr_ip']} to {check_ip}. Restarting server to update."
                                svr_state.restartSERVER(False,msg)
                    # every x seconds, check if the proxy port is still listening. If it isn't shutdown the server.
                    #if playercount >=0:
                    counter_health_checks +=1
                    if counter_health_checks>=threshold_health_checks or healthcheck_first_run:
                        healthcheck_first_run = False
                        counter_health_checks=0
                        if processed_data_dict_bkp['use_proxy'] == 'True':
                            if 'svr_proxyPort' in processed_data_dict_bkp:
                                proxy_online=svrcmd.honCMD.check_port(int(processed_data_dict_bkp['svr_proxyPort']))
                                if proxy_online:
                                    print(f"Health check: proxy port {processed_data_dict_bkp['svr_proxyPort']} healthy")
                                else:
                                    print(f"Health check: proxy port {processed_data_dict_bkp['svr_proxyPort']} not online")
                                    svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}","The proxy port has stopped listening.","INFO")
                                    # svr_state.stopSELF()
                        # config_hash = dmgr.mData.get_hash(f"{processed_data_dict_bkp['sdc_home_dir']}\\config\\local_config.ini")
                        # if 'config_hash' in processed_data_dict_bkp:
                        #     if config_hash != processed_data_dict_bkp['config_hash']:
                        #         svr_state.restartSERVER(True)
                        #         processed_data_dict_bkp.update({'config_hash':config_hash})
                        # else:
                        #     processed_data_dict_bkp.update({'config_hash':config_hash})
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
                if server_status_bkp['server_ready'] == False:
                    if svrcmd.honCMD.check_port(int(processed_data_dict_bkp['svr_proxyLocalVoicePort'])):
                        waiting = False
                        print(f"Port {processed_data_dict_bkp['svr_proxyLocalVoicePort']} is open")
                        server_status_bkp.update({'server_ready':True})
                        # required if dynamically assigning CPU cores for launching servers
                        # if processed_data_dict_bkp['core_assignment'] not in ("one","two"):
                        #     svr_state.assign_cpu()
                        #     print("Server ready.")
                    else:
                        if not waiting:
                            waiting = True
                            print(f"Port {processed_data_dict_bkp['svr_proxyLocalVoicePort']} is not open. Waiting for server to start")
            except:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
            try:
                if playercount >= 1:
                    if match_status_bkp['now'] == "in lobby":
                        counter_gamecheck+=1
                        if counter_gamecheck==threshold_gamecheck:
                            counter_gamecheck=0
                            try:
                                #TODO: game time?
                                svr_state.check_game_started()
                            except:
                                print(traceback.format_exc())
                                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
                            try:
                                if not match_status_bkp['lobby_info_obtained']:
                                    #svr_state.get_lobby_information()
                                    pass
                            except:
                                print(traceback.format_exc())
                                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
                    elif match_status_bkp['now'] == "in game":
                        svr_state.check_current_game_time()
                    else:
                        if playercount > 1:
                            svr_state.check_current_match_id(True)
                        else:
                            svr_state.check_current_match_id(False)
                    if match_status_bkp['now'] != "idle":
                        if not match_status_bkp['match_info_obtained']:
                            #print("checking for match information....")
                            try:
                                svr_state.get_match_information()
                            except:
                                print(traceback.format_exc())
                                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
                    if (server_status_bkp['game_map'] != "empty" and server_status_bkp['game_map'] not in available_maps_bkp):
                        msg = f"Server restarting due to attempt to crash server with false map."
                        #svr_state.reportPlayer("invalid_map")
                        svr_state.restartSERVER(True,msg)
                    elif (server_status_bkp['game_mode'] == "botmatch" or server_status_bkp['game_mode'] == "BotMatch") and processed_data_dict_bkp['allow_botmatches'] == 'False':
                        msg = f"Server restarting due to bot match (disallowed)."
                        #svr_state.reportPlayer("botmatch")
                        svr_state.restartSERVER(True,msg)
            except:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
            try:
                if match_status_bkp['now'] == "in game":
                    if playercount == 1:
                        counter_game_end +=1
                        if counter_game_end == threshold_game_end_check:
                            counter_game_end = 0
                            if svr_state.check_game_ended():
                                svr_state.restartSERVER(True,f"Server restarting due to game end but 1 player has remained connected for {threshold_game_end_check} seconds.")
                    # if match_status_bkp['now'] == "in game":
                    #     match_time = match_status_bkp['match_time']
                    #     if ":" in match_time:
                    #         match_too_long = match_time.split(":")
                    #         match_too_long_hrs = int(match_too_long[0])
                    #         match_too_long_mins = int(match_too_long[1])
                    #         if match_too_long_hrs >= 1:
                    #             msg = f"Server restarting due to match ongoing for 1+ with only 1 players connected."
                    #             print(msg)
                    #             svr_state.restartSERVER(True,msg)
            except:
                print(traceback.format_exc())
                svr_state.append_line_to_file(f"{processed_data_dict_bkp['app_log']}",f"{traceback.format_exc()}","WARNING")
            
            if 'tempcount_bkp' not in server_status_bkp or playercount != server_status_bkp["tempcount_bkp"]:
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
