import discord
from discord.ext import commands
import os
from asyncio.windows_events import NULL
from cogs.dataManager import mData
import cogs.server_status as svrcmd
import asyncio
import traceback


bot = commands.Bot(command_prefix='!', case_insensitive=True)

dmgr = mData()
svr_state = svrcmd.honCMD()
#
#   Processed data from honfigurator and server deployment
#   hon_directory, hon_logs_directory, total servers, hoster
processed_data_dict = dmgr.returnDict()
nssm = processed_data_dict['nssm_exe']
hon_directory = processed_data_dict['hon_directory']
hon_game_dir = processed_data_dict['hon_game_dir']
sdc_home_dir = processed_data_dict['sdc_home_dir']
hon_logs_dir = processed_data_dict['hon_logs_dir']
bot_version = f"{processed_data_dict['bot_version']}-{processed_data_dict['environment']}"
hon_home_dir = processed_data_dict['hon_home_dir']
svr_hoster = processed_data_dict['svr_hoster']
svr_region = processed_data_dict['svr_region']
svr_region_short = processed_data_dict['svr_region_short']
svr_id = processed_data_dict['svr_id']
svr_id_total = processed_data_dict['svrid_total']
svr_ip = processed_data_dict['svr_ip']
svr_dns = processed_data_dict['svr_dns']
svr_identifier = processed_data_dict['svr_identifier']    # eg. AUS-1

#
#   dictionary of data from the hon startup.cfg file. Real info for svr_name, ip, port etc
#   game server data like svr_ip, svr_port, svr_name etc that is sent to the master server
#server_data_dict = dmgr.parse_config(f"{processed_data_dict['hon_game_dir']}\\startup.cfg")
server_data_dict = dmgr.parse_config(f"{hon_game_dir}\\startup.cfg")
svr_name = server_data_dict['svr_name']
svr_name = svr_name.strip('"')
svr_location = server_data_dict['svr_location']
svr_port = server_data_dict['svr_port']
svr_port = svr_port.strip('"')
svr_proxy_enabled = server_data_dict['man_enableProxy']

if processed_data_dict['master_server'] == "honmasterserver.com":
    default_description = '[Hon Server Portal](https://discord.gg/k86ZcA3R8y)  |  [honmasterserver.com](https://honmasterserver.com)  |  [honclientfix.exe](https://store5.gofile.io/download/direct/d8740070-c73e-43ec-9c00-2ea83c639e8d/HonClientFix-honmasterserver.exe)'
elif processed_data_dict['master_server'] == "kongor.online:666":
    default_description = '[Hon Server Portal](https://discord.gg/k86ZcA3R8y)  |  [Kongor Online](https://kongor.online)  |  [Kongor Client Fix](https://store5.gofile.io/download/direct/d0f38bed-0d69-4d0e-a621-87e99d084b2a/HonClientFix-kongor.exe)'
default_footer = "v{bot_version}  |  Games Played: {self.server_status['total_games_played']}  |  Last Restart: {self.last_restart}"

os.environ["USERPROFILE"] = processed_data_dict['hon_home_dir']
os.chdir(processed_data_dict['hon_logs_dir'])



#   colors for embed strips
#   list of colors:
#   blue, blurple, dark_blue, dark_gold, dark_gray, dark_green, dark_grey, dark_magenta, dark_orange, 
#   dark_purple, dark_red, dark_teal, dark_theme, darker_gray, darker_grey, default, gold, green, greyple, 
#   light_gray, light_grey, lighter_gray, lighter_grey, magenta, orange, purple, random, red, teal
stripColor_init = discord.Color.magenta()
stripColor_log = discord.Color.dark_red()
stripColor_offline = discord.Color.dark_red()
stripColor_starting = discord.Color.gold()
stripColor_online = discord.Color.teal()
stripColor_restart = discord.Color.orange()
stripColor_selected = discord.Color.purple()
stripColor_lobby = discord.Color.green()
stripColor_ingame = discord.Color.blue()
stripColor_help = discord.Color.gold()

init = "https://i.ibb.co/s3HSrjd/corepool.png"
online = "https://i.ibb.co/fd7yFKw/thumbs-up.png"
offline = "https://i.ibb.co/GMZdkT9/thumbs-down.png"
hosted = "https://i.ibb.co/FwcvZQg/icon-loading.png"
map_capturetheflag ="https://i.ibb.co/7gQvL8t/Capture-the-Flag.png"
map_darkwoodvale ="https://i.ibb.co/TtpsHLK/Darkwoodvale.png"
map_devowars ="https://i.ibb.co/KsyFp46/Devo-Wars.png"
map_caldavar ="https://i.ibb.co/CMgknjD/Forest-of-Caldavar.png"
map_grimmhunt ="https://i.ibb.co/B2JZbPP/Grimm-Hunt.png"
map_grimmscrossing ="https://i.ibb.co/bJ85jbm/Grimms-Crossing.png"
map_midwars ="https://i.ibb.co/rmgq5Z9/Midwars.png"
map_midwars_bet ="https://i.ibb.co/cQvZ7RH/midwars-beta.png"
map_prophets ="https://i.ibb.co/Y732h6B/Prophets.png"
map_riftwars ="https://i.ibb.co/q0V1g1h/Rift-Wars.png"
map_soccer ="https://i.ibb.co/mFTMyVb/Soccer-Pick.png"
map_spotlight ="https://i.ibb.co/VSq1tzR/Spotlight.png"
map_deathmatch ="https://i.ibb.co/VQwJWxr/Team-Deathmatch.png"
map_tutorial ="https://i.ibb.co/F6vvLBm/tutorial.png"
map_watchtower ="https://i.ibb.co/C8Wp3gM/watchtower.png"

import signal

class timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)

class embedManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_status = svr_state.getStatus()
        #self.total_games_played_prev = self.server_status['total_games_played_prev_prev']
        self.total_games_played = svr_state.getData("TotalGamesPlayed")
        self.server_status.update({'total_games_played':self.total_games_played})
        self.event_log = ""
        self.event_list = []
        print("server status dictionary: " + str(self.server_status))

    """

        This function creates the initial Embed when a server link is created

    """
    @bot.command()
    async def initiateEmbed(self,ctx):
        sent_embed = discord.Embed(title=f"{processed_data_dict['svr_region_short']} {processed_data_dict['svr_id_w_total']}  |  Syncing..",description=default_description, color=stripColor_init)
        sent_embed.set_author(name=self.server_status['discord_admin_name'])
        #name='\u200b' to hide title
        sent_embed.set_footer(text=f"v{bot_version}  |  Games Played: {self.server_status['total_games_played']}  |  Last Restart: {self.server_status['last_restart']}")
        sent_embed.set_thumbnail(url=init)
        #sent_embed_obj = await ctx.send(file=attachment_init, embed=sent_embed)
        sent_embed_obj = await ctx.send(embed=sent_embed)
        for i in range(0,4):
            if i == 0:
                await sent_embed_obj.add_reaction("🔁")
            elif i == 1:
                await sent_embed_obj.add_reaction("🔼")
            elif i == 2:
                await sent_embed_obj.add_reaction("🔽")
            elif i == 3:
                await sent_embed_obj.add_reaction("🛑")
        return sent_embed_obj
    @bot.command()
    async def embedsync(self,ctx,object_list):
        self.server_status = svr_state.getStatus()
        self.mEmbed_objects = object_list
        playercount = svr_state.playerCount()
        # self.server_status.update({'server_restarting':False})
        # self.server_status.update({'server_starting':False})
        # self.server_status.update({'hard_reset':False})
        # self.server_status.update({'restart_required':False})
        #await ctx.invoke(bot.get_command('createEmbed'),ctx,playercount)
        for embedObjects in self.mEmbed_objects:
            try:
                if self.server_status['server_starting']:
                    await ctx.invoke(bot.get_command('startingEmbed'),rec_embed = embedObjects)
                elif self.server_status['server_restarting']:
                    await ctx.invoke(bot.get_command('restartEmbed'),rec_embed = embedObjects)
                elif self.server_status['hard_reset']:
                    await ctx.invoke(bot.get_command('offlineEmbed'),rec_embed = embedObjects)
                else:
                    #
                    #   Server is offline
                    if playercount < 0:
                        await ctx.invoke(bot.get_command('offlineEmbed'),rec_embed = embedObjects)
                    #
                    #   Server is online
                    elif playercount == 0:
                        await ctx.invoke(bot.get_command('onlineEmbed'),rec_embed = embedObjects)
                    # lobby active
                    elif playercount >= 1:
                        await ctx.invoke(bot.get_command('active'),rec_embed = embedObjects,playercount = playercount)
            except Exception as e: 
                print(e)
                print("we mustn't have data for this yet")
    """

        This command invokes a function based on playercount

    """
    @bot.command()
    async def testinglink(self,ctx):
        await ctx.message.delete()
        print(self.mEmbed_objects)
    @bot.command()
    async def createEmbed(self,ctx,playercount):
        #await ctx.message.delete()
        playercount = int(playercount)
        for embedObjects in self.mEmbed_objects:
            if self.server_status['server_starting']:
                await ctx.invoke(bot.get_command('startingEmbed'),rec_embed = embedObjects)
            elif self.server_status['server_restarting']:
                await ctx.invoke(bot.get_command('restartEmbed'),rec_embed = embedObjects)
            elif self.server_status['hard_reset']:
                await ctx.invoke(bot.get_command('offlineEmbed'),rec_embed = embedObjects)
            else:
                #
                #   Server is offline
                if playercount < 0:
                    await ctx.invoke(bot.get_command('offlineEmbed'),rec_embed = embedObjects)
                #
                #   Server is online
                elif playercount == 0:
                    await ctx.invoke(bot.get_command('onlineEmbed'),rec_embed = embedObjects)
                # lobby active
                elif playercount >= 1:
                    await ctx.invoke(bot.get_command('active'),rec_embed = embedObjects,playercount = playercount)
            
    @bot.command()
    async def offlineEmbed(self,rec_embed):
        self.server_status = svr_state.getStatus()
        created_embed = discord.Embed(title=f"{processed_data_dict['svr_region_short']} {processed_data_dict['svr_id_w_total']}  |  Offline",description=default_description, color=stripColor_offline)
        created_embed.set_author(name=self.server_status['discord_admin_name'])
            #name='\u200b' to hide title
        created_embed.set_footer(text=f"v{bot_version}  |  Games Played: {self.server_status['total_games_played']}  |  Last Restart: {self.server_status['last_restart']}")
        created_embed.set_thumbnail(url=offline)
        try:
            await rec_embed.edit(embed=created_embed)
        except: print(traceback.format_exc())

    @bot.command()
    async def startingEmbed(self,rec_embed):
        self.server_status = svr_state.getStatus()
        #embedManager.__init__(self,bot)
        created_embed = discord.Embed(title=f"{processed_data_dict['svr_region_short']} {processed_data_dict['svr_id_w_total']}  |  Starting Server..",description=default_description, color=stripColor_starting)
        created_embed.set_author(name=self.server_status['discord_admin_name'])
        created_embed.set_footer(text=f"v{bot_version}  |  Games Played: {self.server_status['total_games_played']}  |  Last Restart: {self.server_status['last_restart']}")
        try:
            await rec_embed.edit(embed=created_embed)
        except: print(traceback.format_exc())
        return

    @bot.command()
    async def onlineEmbed(self,rec_embed):
        self.server_status = svr_state.getStatus()
        #embedManager.__init__(self,bot)

        created_embed = discord.Embed(title=f"{processed_data_dict['svr_region_short']} {processed_data_dict['svr_id_w_total']}  |  OPEN",description=default_description, color=stripColor_online)
        created_embed.set_author(name=self.server_status['discord_admin_name'])
        if svr_dns is None:
            #created_embed.add_field(name=f"Connect (ready):",value=f"```\nconnect {svr_ip}:{svr_port}\n```",inline=True)
            created_embed.add_field(name=f"Server is ready!",value=f"```\nconnnect via public games.```",inline=True)
        else:
            #created_embed.add_field(name=f"Connect (ready):",value=f"```\nconnect {svr_dns}:{svr_port}\n```",inline=True)
            created_embed.add_field(name=f"Server is ready!",value=f"```\nconnnect via public games.```",inline=True)
        created_embed.set_footer(text=f"v{bot_version}  |  Games Played: {self.server_status['total_games_played']}  |  Last Restart: {self.server_status['last_restart']}")
        created_embed.set_thumbnail(url=online)
        try:
            await rec_embed.edit(embed=created_embed)
        except: print(traceback.format_exc())
        return
    
    @bot.command()
    async def restartEmbed(self,rec_embed):
        #self.server_status.update({'restarting_server':True})
        #embedManager.__init__(self,bot)
        created_embed = discord.Embed(title=f"{processed_data_dict['svr_region_short']} {processed_data_dict['svr_id_w_total']}                           RESTARTING SERVER...", color=stripColor_restart)
        try:
            await rec_embed.edit(embed=created_embed)
        except: print(traceback.format_exc())


    
    @bot.command()
    async def active(self,rec_embed,playercount):
        self.server_status = svr_state.getStatus()
        #embedManager.__init__(self,bot)
        #
        #   logic info
        self.just_collected = self.server_status['just_collected']
        self.first_run = self.server_status['first_run']
        self.game_started = self.server_status['game_started']
        self.embed_updated = self.server_status['embed_updated']
        self.lobby_created = self.server_status['lobby_created']
        #
        #   First run
        if self.just_collected is False and self.first_run == True:
            #
            #   BASE EMBED: embed when server has been selected by a player
            #   server selected not hosted
            created_embed = discord.Embed(title=f"{processed_data_dict['svr_region_short']} {processed_data_dict['svr_id_w_total']}  |  SELECTING GAME SETTINGS",description=default_description, color=stripColor_selected)
            created_embed.set_author(name=self.server_status['discord_admin_name'])
            if self.server_status['game_host'] != "empty":
                created_embed.add_field(name=f"No Lobby",value=f"```\nPlease wait for the host ({self.server_status['game_host']}) to begin the game..\n60 seconds until kick```")
            else:
                created_embed.add_field(name=f"No Lobby",value=f"```\nPlease wait for the host to begin the game..\n60 seconds until kick```")
            created_embed.set_footer(text=f"v{bot_version}  |  Games Played: {self.server_status['total_games_played']}  |  Last Restart: {self.server_status['last_restart']}")
            created_embed.set_thumbnail(url=hosted)
            try:
                await rec_embed.edit(embed=created_embed)
            except: print(traceback.format_exc())
        #
        #   BASE EMBED: embed when a lobby has been created
        #   server selected lobby created
        elif self.just_collected == True or self.lobby_created == True:
            self.server_status.update({'just_collected':False})
            print("----updating with map data----")
            #   
            #   Lobby online
            if self.game_started == False: 
                created_embed = discord.Embed(title=f"{processed_data_dict['svr_region_short']} {processed_data_dict['svr_id_w_total']}  |  LOOKING FOR PLAYERS",description=default_description, color=stripColor_lobby)
            #   
            #   Match in progress
            elif self.game_started == True:
                created_embed = discord.Embed(title=f"{processed_data_dict['svr_region_short']} {processed_data_dict['svr_id_w_total']}  |  MATCH IN PROGRESS",description=default_description, color=stripColor_ingame)
            created_embed.set_author(name=self.server_status['discord_admin_name'])
            #   
            #   Lobby online or match in progress
            # game_information = ['game_name','game_type','game_host','game_map','game_mode','slots']
            # for info in game_information:
            #     if self.server_status[info] != 'empty':
            if self.server_status['game_name'] != 'empty':
                created_embed.add_field(name="Name: ", value=f"{self.server_status['game_name']}",inline=True)
            if self.server_status['game_type'] != 'empty':
                created_embed.add_field(name="Type: ", value=f"{self.server_status['game_type']}",inline=True)
            if self.server_status['game_host'] != 'empty':
                created_embed.add_field(name="Host: ", value=f"{self.server_status['game_host']}",inline=True)
            if self.server_status['game_map'] != 'empty':
                created_embed.add_field(name="Map: ", value=f"{self.server_status['game_map']}",inline=True)
            created_embed.add_field(name="Slots: ", value=f"{playercount}/{self.server_status['slots']}",inline=True)
            if self.server_status['game_mode'] != 'empty':
                created_embed.add_field(name="Mode: ", value=f"{self.server_status['game_mode']}",inline=True)
            # created_embed.add_field(name="Spectators: ", value=f"{self.server_status['spectators']}",inline=True)
            # created_embed.add_field(name="Referees: ", value=f"{self.server_status['referees']}",inline=True)
            #   
            #   Lobby online
            if self.game_started == False:
                created_embed.add_field(name=f"Server is ready!",value=f"```\nconnnect via public games.```",inline=False)
            #   
            #   Match in progress
            elif self.game_started == True:
                minutes, seconds = divmod(self.server_status['elapsed_duration'], 60)
                created_embed.add_field(name=f"Match in progress",value=f"```Elapsed duration: {str(minutes)}:{str(seconds)}```",inline=False)
            created_embed.set_footer(text=f"v{bot_version}  |  Games Played: {self.server_status['total_games_played']}  |  Last Restart: {self.server_status['last_restart']}")

            if self.server_status['game_map'] == "caldavar" or self.server_status['game_map'] == "caldavar_old" or self.server_status['game_map'] == "caldavar_reborn":
                created_embed.set_thumbnail(url=map_caldavar)
            elif self.server_status['game_map'] == "midwars" or self.server_status['game_map'] == "midwars_pbt" or self.server_status['game_map'] == "midwars_reborn":
                created_embed.set_thumbnail(url=map_midwars)
            elif self.server_status['game_map'] == "capturetheflag":
                created_embed.set_thumbnail(url=map_capturetheflag)
            elif self.server_status['game_map'] == "darkwoodvale":
                created_embed.set_thumbnail(url=map_darkwoodvale)
            elif self.server_status['game_map'] == "grimmscrossing":
                created_embed.set_thumbnail(url=map_grimmscrossing)
            elif self.server_status['game_map'] == "prophets":
                created_embed.set_thumbnail(url=map_prophets)
            elif self.server_status['game_map'] == "riftwars":
                created_embed.set_thumbnail(url=map_riftwars)
            elif self.server_status['game_map'] == "soccer":
                created_embed.set_thumbnail(url=map_soccer)
            elif self.server_status['game_map'] == "spotlight":
                created_embed.set_thumbnail(url=map_spotlight)
            elif self.server_status['game_map'] == "team_deathmatch":
                created_embed.set_thumbnail(url=map_deathmatch)
            elif self.server_status['game_map'] == "thegrimmhunt":
                created_embed.set_thumbnail(url=map_grimmhunt)
            elif self.server_status['game_map'] == "tutorial":
                created_embed.set_thumbnail(url=map_tutorial)
            elif self.server_status['game_map'] == "watchtower":
                created_embed.set_thumbnail(url=map_watchtower)
            else:
                created_embed.set_thumbnail(url=online)
            try:
                await rec_embed.edit(embed=created_embed)
            except: print(traceback.format_exc())
        
    @bot.command()
    async def helpembed(self, ctx):
        created_embed = discord.Embed(title="Commands for bot",description='', color=stripColor_help)
        created_embed.add_field(name=f"``!createlinks {processed_data_dict['svr_hoster']}``: ", value=f"        Creates links for **ALL** {processed_data_dict['svr_hoster']} servers in this discord",inline=False)
        created_embed.add_field(name=f"``!createlinks {processed_data_dict['svr_identifier']}``: ", value=f"        Creates links for just the **SINGLE** {processed_data_dict['svr_identifier']} server in this discord",inline=False)
        created_embed.add_field(name=f"``!destroylinks {processed_data_dict['svr_hoster']}``: ", value=f"        Removes links/messages for **ALL** {processed_data_dict['svr_hoster']} servers in every discord",inline=False)
        created_embed.add_field(name=f"``!destroylinks {processed_data_dict['svr_identifier']}``: ", value=f"        Removes links/messages for **SINGLE** {processed_data_dict['svr_identifier']} server in every discord",inline=False)
        created_embed.add_field(name=f"``!destroylinkshere {processed_data_dict['svr_hoster']}``: ", value=f"        Removes links/messages for **ALL** {processed_data_dict['svr_hoster']} servers in this discord server only",inline=False)
        created_embed.add_field(name=f"``!destroylinkshere {processed_data_dict['svr_identifier']}``: ", value=f"        Removes link/message for **SINGLE** {processed_data_dict['svr_identifier']} server in this discord server only",inline=False)
        created_embed.add_field(name=f"``!heartbeat {processed_data_dict['svr_hoster']}``: ", value=f"        checks the heartbeat of **ALL** {processed_data_dict['svr_hoster']} servers",inline=False)
        created_embed.add_field(name=f"``!heartbeat {processed_data_dict['svr_identifier']}``: ", value=f"        checks the heartbeat of **SINGLE** {processed_data_dict['svr_identifier']} server",inline=False)
        created_embed.add_field(name=f"``!giveCPR {processed_data_dict['svr_identifier']}``: ", value=f"        EMERGENCY! Starts the heartbeat of **ALL** {processed_data_dict['svr_hoster']} servers",inline=False)
        created_embed.add_field(name=f"``!giveCPR {processed_data_dict['svr_identifier']}``: ", value=f"        EMERGENCY! Starts the heartbeat of **SINGLE** {processed_data_dict['svr_identifier']} server",inline=False)
        created_embed.add_field(name=f"``!pullplug {processed_data_dict['svr_identifier']}``: ", value=f"        EMERGENCY! Stops the heartbeat of **SINGLE** {processed_data_dict['svr_identifier']} server",inline=False)
        return created_embed

    @bot.command()
    async def embedLog(self,ctx,log_msg):
        list_limit = 6
        self.event_list.append(log_msg + "\n")
        self.event_log =  (self.event_log + log_msg + "\n")
        self.event_string = ""
        if len(self.event_list)>list_limit:
            self.event_list.remove(self.event_list[0])
            for event_msg in self.event_list:
                self.event_string = (self.event_string+event_msg)
        if len(self.event_list)<=list_limit:
            for event_msg in self.event_list:
                self.event_string = (self.event_string+event_msg)
        created_embed = discord.Embed(title=processed_data_dict['svr_identifier'] + " Adminbot Event Log",description=self.event_string, color=stripColor_log)
        return created_embed

def setup(bot):
    bot.add_cog(embedManager(bot))