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
        
        alive = True
        test = self.bot.get_cog("embedManager")
        # alive = True
        self.server_status = svrcmd.honCMD().getStatus()
        self.match_status = svrcmd.honCMD().getMatchInfo()
        self.available_maps = svr_state.getData("availMaps")
        self.server_status.update({'server_restarting':False})
        #self.server_status.update({'server_starting':False})
        self.server_status.update({'hard_reset':False})

        restart_timer = 10
        counter_heartbeat = 0
        counter_heartbeat_attempts = 0
        counter_hosted = 0
        counter_gamecheck = 0
        counter_lobbycheck = 0
        #  Debug setting
        #  playercount = 0
        threshold_heartbeat = 30    # how long to wait before break from heartbeat to update embeds
        threshold_hosted = 60   # how long we wait for someone to host a game without starting
        threshold_gamecheck = 5 # how long we wait before checking if the game has started again
        threshold_lobbycheck = 5 # how long we wait before checking if the lobby has been created yet
        x = 0
        #   this is the start of the heartbeat
        #   anything below is looping
        while alive == True:
            counter_heartbeat+=1
            await asyncio.sleep(1)
            playercount = svrcmd.honCMD().playerCount()
            # print(str(playercount))
            #
            #   Check if the server is ready yet
            if self.server_status['server_ready'] == False:
                if svr_state.getData("ServerReadyCheck"):
                    self.server_status.update({'server_starting':False})
                    self.server_status.update({'server_restarting':False})
                    if self.processed_data_dict['debug_mode'] == 'True':
                        logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [DEBUG] Server Ready.")
                        try:
                            await embed_log.edit(embed=logEmbed)
                        except: print(traceback.format_exc())
                else:
                    if self.server_status['server_restarting'] == False:
                        self.server_status.update({'server_starting':True})
                    elif self.server_status['server_restarting'] == True:
                        self.server_status.update({'server_starting':False})
                # else:
                #     self.server_status.update({'server_restarting':True})

            #
            #   playercount has returned to 0 after a game has been completed, or a lobby closed. Server restart required
            if playercount == 0:
                if self.server_status['priority_realtime'] == True:
                    svr_state.changePriority(False)
                if self.server_status['hard_reset'] == False:
                    self.server_status.update({'hard_reset':svr_state.getData("CheckForUpdates")})
                if self.server_status['scheduled_shutdown']==False:
                    self.server_status.update({'scheduled_shutdown':svr_state.getData("CheckSchdShutdown")})
                    if self.server_status['scheduled_shutdown']:
                        logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [DEBUG] SCHEDULED SHUTDOWN")
                        try:
                            await embed_log.edit(embed=logEmbed)
                        except: print(traceback.format_exc())
                        await test.createEmbed(ctx,-3)
                        svr_state.stopSELF()
                if self.server_status['hard_reset'] == True:
                    self.server_status.update({'restart_required':True})
                    # await test.createEmbed(ctx,playercount)
                    await asyncio.sleep(restart_timer)
                    self.server_status.update({'tempcount':playercount})    # prevents the heartbeat
                    self.server_status.update({'update_embeds':False})
                    # restart notification
                    if self.processed_data_dict['debug_mode'] == 'True':
                        logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [DEBUG] RESTARTING SERVER FOR UPDATE")
                        try:
                            await embed_log.edit(embed=logEmbed)
                        except: print(traceback.format_exc())
                    svr_state.restartSELF()
                if self.server_status['first_run'] == False:
                    self.server_status.update({"server_restarting":True})
                    await test.createEmbed(ctx,playercount)
                    await asyncio.sleep(restart_timer)
                    # restart notification
                    if self.processed_data_dict['debug_mode'] == 'True':
                        match_id = self.server_status['match_log_location']
                        match_id = match_id.replace(".log","")
                        logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [DEBUG] RESTARTING SERVER INBETWEEN GAME {match_id}")
                        try:
                            await embed_log.edit(embed=logEmbed)
                        except: print(traceback.format_exc())
                    svr_state.restartSERVER()
                    self.server_status.update({'tempcount':playercount})    # prevents the heartbeat
                if counter_heartbeat_attempts == 4:
                    check_ip = dmgr.mData.getData(self,"svr_ip")
                    if check_ip != self.server_status['svr_ip']:
                        self.server_status.update({"server_restarting":True})
                        await test.createEmbed(ctx,playercount)
                        if self.processed_data_dict['debug_mode'] == 'True':
                            logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [DEBUG] RESTARTING AS PUBLIC IP HAS CHANGED.\nFrom{self.server_status['svr_ip']} to {check_ip}")
                            try:
                                await embed_log.edit(embed=logEmbed)
                            except: print(traceback.format_exc())
                        svr_state.restartSERVER()
                        self.server_status.update({'tempcount':playercount})    # prevents the heartbeat

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
                            except: print(traceback.format_exc())
                        if self.server_status['match_info_obtained'] == False:
                            try:
                                svr_state.getData("MatchInformation")
                            except: print(traceback.format_exc())
                            if self.server_status['game_started'] == True and self.server_status['match_info_obtained'] == True and self.processed_data_dict['debug_mode'] == 'True':
                                match_id = self.server_status['match_log_location']
                                match_id = match_id.replace(".log","")
                                logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [DEBUG] Game Started / Lobby made - {match_id}")
                                try:
                                    await embed_log.edit(embed=logEmbed)
                                except: print(traceback.format_exc())
                # Verify the lobby settings. Look out for sinister events and handle it.
                #
                #   sinister behaviour detected, save log to file.
                #   Players can attempt to start a game on an uknown map file. This causes the server to crash and hang.
                #   We will firstly handle the error, restart the server, and then log the event for investigation.
                if playercount == 1:
                    if (self.server_status['game_map'] != "empty" and self.server_status['game_map'] not in self.available_maps):
                        #hard_reset = svr_state.getData("CheckForUpdates")
                        self.server_status.update({'restart_required':True})
                        svr_state.reportPlayer("No_Map")
                        logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [WARN] Kicked {self.server_status['game_host']} (IP: ``{self.server_status['client_ip']}``) (Reason: Crashing server with false map value: ``{self.server_status['game_map']}``), RESTARTING...")
                        try:
                            await embed_log.edit(embed=logEmbed)
                        except: print(traceback.format_exc())
                        self.server_status.update({"server_restarting":True})
                        self.server_status.update({"restart_required":True})
                        svr_state.restartSERVER()
                        await test.createEmbed(ctx,playercount)
                        self.server_status.update({'tempcount':playercount})    # prevents the heartbeat
                        self.server_status.update({'update_embeds':False})
                    elif (self.server_status['game_mode'] == "botmatch" or self.server_status['game_mode'] == "BotMatch") and self.processed_data_dict['allow_botmatches'] == 'False':
                        svr_state.reportPlayer("botmatch")
                        logEmbed = await test.embedLog(ctx,f"``{heartbeat.time()}`` [WARN] Kicked {self.server_status['game_host']} (IP: ``{self.server_status['client_ip']}``) (Reason: creating botmatches), RESTARTING...")
                        try:
                            await embed_log.edit(embed=logEmbed)
                        except: print(traceback.format_exc())
                        self.server_status.update({"server_restarting":True})
                        self.server_status.update({"restart_required":True})
                        svr_state.restartSERVER()
                        await test.createEmbed(ctx,playercount)
                        self.server_status.update({'tempcount':playercount})    # prevents the heartbeat
                        self.server_status.update({'update_embeds':False})
                #
                #   Game in progress
                #   Start a timer so we can show the elapsed time of the match
                if counter_heartbeat == threshold_heartbeat:
                    counter_heartbeat=0
                    counter_heartbeat_attempts +=1
                    if self.server_status['game_started'] == True:
                        elapsed_duration = self.server_status['elapsed_duration']
                        elapsed_duration = int(elapsed_duration)
                        elapsed_duration +=1
                        self.server_status.update({'elapsed_duration':elapsed_duration})
                        # self.server_status.update({'update_embeds':True})
                        svr_state.getData("CheckInGame")
                    if playercount != self.server_status['tempcount']:
                        self.server_status.update({'update_embeds':True})


            if playercount >=2:
                if self.server_status['priority_realtime'] == False:
                    svr_state.changePriority(True)
            #
            #   break out from the heartbeat every threshold_heartbeat if we're in a game
            # if counter_heartbeat == threshold_heartbeat:
            #     counter_heartbeat=0
            #     counter_heartbeat_attempts +=1
            #     if playercount >= 1:
            #         if  self.server_status['game_started'] == True:
            #             self.server_status.update({'tempcount':-5})   # force an update
            #             svr_state.getData("CheckInGame")
            #             print(self.match_status)
            #         # if self.server_status['lobby_created'] == True and self.server_status['game_started'] == False:
            #         #     break
            #         self.server_status.update({'update_embeds':True})
            #     if counter_heartbeat_attempts == 4 and playercount > 0:
            #         counter_heartbeat_attempts = 0
            #         #self.server_status.update({'tempcount':-5})   # force an update
            #         self.server_status.update({'update_embeds':True})
            #   
            #   if nothing new has happened, sit here and take a break for a bit. Every 15 seconds we leave the idle mode in case something has changed and we missed it.
            #if playercount == self.server_status['tempcount'] and self.server_status['just_collected'] != True and (not self.server_status['server_restarting'] == True or not self.server_status['server_starting'] == True): #and just_collected is False:
            if self.server_status['update_embeds'] == False or playercount == self.server_status['tempcount'] and (self.server_status['just_collected'] != True and not self.server_status['server_restarting'] == True or not self.server_status['server_starting'] == True): #and just_collected is False:
                alive = True
                #print("idle")
            #   update embeds.
            else:
                counter_heartbeat=0
                print("moving to update")
                self.server_status.update({'tempcount':playercount})
                self.server_status.update({'update_embeds':False})
                self.server_status.update({'time_waited':counter_hosted})
                svr_state.updateStatus(self.server_status)
                await test.createEmbed(ctx,playercount)
                # if playercount < 0:
                #     self.alive = False

    
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
            except: print(traceback.format_exc())
            if not alive:
                await ctx.invoke(bot.get_command('startheart'),ctx)
    @bot.command()
    async def kick(self,ctx,hoster):
        if hoster == self.processed_data_dict['svr_hoster'] or hoster == self.processed_data_dict['svr_identifier']:
            try:
                await ctx.message.delete()
            except: print(traceback.format_exc())
            if hoster == self.processed_data_dict['svr_hoster']:
                await asyncio.sleep(int(self.processed_data_dict['svr_id']))
            self.server_status.update({'update_embeds':True})
            self.server_status.update({'tempcount':-5})
    @bot.command()
    async def pullPlug(self,ctx,hoster):
        if hoster == self.processed_data_dict['svr_identifier']:
            try:
                await ctx.message.delete()
            except: print(traceback.format_exc())
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
            except: print(traceback.format_exc())
    
def setup(bot):
    bot.add_cog(heartbeat(bot))
