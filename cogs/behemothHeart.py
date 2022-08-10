from discord.ext import commands
import asyncio
import cogs.server_status as svrcmd
from datetime import datetime
import traceback

svr_state = svrcmd.honCMD()
hard_reset = False
bot = commands.Bot(command_prefix='!', case_insensitive=True)
alive = True
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
        self.available_maps = svr_state.getData("availMaps")
        self.server_status.update({'server_restarting':False})
        self.server_status.update({'server_starting':False})
        self.server_status.update({'hard_reset':False})

        restart_timer = 1
        counter_heartbeat = 0
        counter_hosted = 0
        counter_gamecheck = 0
        counter_lobbycheck = 0
        threshold_heartbeat = 15    # how long to wait before break from heartbeat to update embeds
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
            print(str(playercount))
            #
            #   playercount has returned to 0 after a game has been completed, or a lobby closed. Server restart required
            if playercount == 0 and self.server_status['first_run'] == False or (playercount == 1 and self.server_status['map'] != "empty" and self.server_status['map'] not in self.available_maps) or (playercount == 1 and self.server_status['mode'] == "botmatch" and self.processed_data_dict['allow_botmatches'] == 'False'):
                hard_reset = svr_state.getData("CheckForUpdates")
                self.server_status.update({'restart_required':True})
                if playercount == 1:
                    #
                    #   sinister behaviour detected, save log to file.
                    #   Players can attempt to start a game on an uknown map file. This causes the server to crash and hang.
                    #   We will firstly handle the error, restart the server, and then log the event for investigation.
                    if self.server_status['mode'] == "botmatch":
                        svr_state.reportPlayer("botmatch")
                        logEmbed = await test.embedLog(ctx,f"[WARN] Kicked {self.server_status['host']} (IP: ``{self.server_status['client_ip']}``) (Reason: creating botmatches)")
                        try:
                            await embed_log.edit(embed=logEmbed)
                        except: print(traceback.format_exc())
                    else:
                        svr_state.reportPlayer("No_Map")
                        logEmbed = await test.embedLog(ctx,f"[WARN] Kicked {self.server_status['host']} (IP: ``{self.server_status['client_ip']}``) (Reason: Crashing server with false map value: ``{self.server_status['map']}``)")
                        try:
                            await embed_log.edit(embed=logEmbed)
                        except: print(traceback.format_exc())
                if not hard_reset:
                    self.server_status.update({"server_restarting":True})
                    await test.createEmbed(ctx,playercount)
                    await asyncio.sleep(restart_timer)
                    svr_state.restartSERVER()
                    self.server_status.update({'tempcount':playercount})    # prevents the heartbeat
                elif hard_reset:
                    self.server_status.update({'hard_reset':True})
                    await test.createEmbed(ctx,playercount)
                    await asyncio.sleep(restart_timer)
                    self.server_status.update({'tempcount':playercount})    # prevents the heartbeat
                    svr_state.restartSELF()

            if playercount == 1:
                if self.server_status['lobby_created'] == False:
                    counter_hosted+=1
                    counter_lobbycheck+=1
                    if counter_hosted == threshold_hosted:
                        counter_hosted = 0
                        self.server_status.update({'server_restarting':True})
                        self.server_status.update({'restart_required':True})
                        logEmbed = await test.embedLog(ctx,f"[WARN] Kicked {self.server_status['host']} for taking too long to create a lobby")
                        try:
                            await embed_log.edit(embed=logEmbed)
                        except:
                            print(traceback.format_exc())
                            print("most likely due to using auto-sync")
                        svr_state.restartSERVER()
                        self.server_status.update({'tempcount':playercount})    # prevents the heartbeat

                if counter_lobbycheck == threshold_lobbycheck:
                    counter_lobbycheck=0
                    #   
                    #   this is the part where the server has been selected, so we need to parse the game logs carefully now to catch lobby information
                    # hardSlave = svr_state.getData("loadHardSlave")
                    # softSlave = svr_state.getData("loadSoftSlave")
                    #if (str(softSlave) != str(hardSlave)) or self.server_status['first_run'] == True:
                    if self.server_status['first_run'] == True:
                        svr_state.getData("GameCheck")
                        #print("Just collected: "+str(self.just_collected))
                        # print(state)
                        #self.server_status.update({'tempcount':-5})
                        if self.server_status['lobby_created'] == True and self.server_status['priority_realtime'] == False:
                            svr_state.changePriority(True)
            #
            #   Server has been turned on but is not yet ready
            if self.server_status['server_ready'] == False:
                if svr_state.getData("ServerReadyCheck"):
                    self.update = False
                    self.server_status.update({'server_starting':False})
                    self.server_status.update({'server_restarting':False})
                else:
                    self.update = True
                    if self.server_status['server_restarting'] == False:
                        self.server_status.update({'server_starting':True})
                    elif self.server_status['server_restarting'] == True:
                        self.server_status.update({'server_starting':False})
                # else:
                #     self.server_status.update({'server_restarting':True})
            #
            #   Check if the match has begun
            if playercount >= 1 and self.server_status['game_started'] == False and self.server_status['lobby_created'] == True:
                counter_gamecheck+=1
                if counter_gamecheck==threshold_gamecheck:
                    counter_gamecheck=0
                    try:
                        svr_state.getData("CheckInGame")
                    except: print(traceback.format_exc())
                         # force an update
            #
            #   Start a timer so we can show the elapsed time of the match
            if playercount >=1 and self.server_status['game_started'] == True:
                elapsed_duration = self.server_status['elapsed_duration']
                elapsed_duration = int(elapsed_duration)
                elapsed_duration +=1
                self.server_status.update({'elapsed_duration':elapsed_duration})
            #
            #   break out from the heartbeat every threshold_heartbeat if we're in a game
            if counter_heartbeat == threshold_heartbeat:
                counter_heartbeat=0
                if playercount >= 1 and self.server_status['game_started'] == True:
                    self.server_status.update({'tempcount':-5})   # force an update
                    # if self.server_status['lobby_created'] == True and self.server_status['game_started'] == False:
                    #     break
            #   
            #   if nothing new has happened, sit here and take a break for a bit. Every 15 seconds we leave the idle mode in case something has changed and we missed it.
            if playercount == self.server_status['tempcount'] and self.server_status['just_collected'] != True and (not self.server_status['server_restarting'] == True or not self.server_status['server_starting'] == True): #and just_collected is False:
                print("idle")
            #   update embeds.
            else:
                counter_heartbeat=0
                self.server_status.update({'tempcount':playercount})
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
            if hoster == self.processed_data_dict['svr_hoster']:
                await asyncio.sleep(int(self.processed_data_dict['svr_id']))
            try:
                if alive:
                    await ctx.send(f"{self.processed_data_dict['svr_identifier']} Behemoth heart beating 💓",delete_after=5)
                else:
                    await ctx.send(f"{self.processed_data_dict['svr_identifier']} Behemoth heart stopped! :broken_heart:",delete_after=5)
            except: print(traceback.format_exc())
    
def setup(bot):
    bot.add_cog(heartbeat(bot))