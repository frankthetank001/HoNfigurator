# When using the bot, use !startNew<serverNum> to create the bot message in channel of your choice
# After this use !startbot<serverNum> to continue using the same message location but start the bot again
# if you have a domain name registered against your IP address, the bot will attempt to look this up and display it
# After a lobby has been created, if the lobby is closed the server will automatically restart
# The bot reports on whether a match is in-game or not by checking if the newest gamelog file has been written to.
# if all players disconnect from the game without conceding, winning, remaking etc, then there will be a 3 minute delay until the bot restarts itself.

import asyncio
from asyncio.windows_events import NULL
import discord
from discord.ext import commands
from os.path import exists
import psutil
import cogs.dataManager as dmgr
import subprocess
import os
import glob
import hashlib
import shutil
import time
import subprocess as sp

#
#   Global variables
#
global honEXE
global mainEmbed
global playerCount
global stripColor
global discordData
global honPID
global honP
global tempcount
global map
global mode
global slots
global teamsize
global spectators
global referees
global host
global version
global just_collected
global firstrunthrough
global total_games_played
global total_games_played_prev
global game_started
global gameLoc
global gameDllHash
global oldDLL
global newDLL
global lobby_created
global client_ip

#
#   Initialize global variables
#

gameDllHash = "3d97c3fb6121219344cfabe8dfcc608fac122db4"
map = "empty"
mode = "empty"
host = "empty"
version = "empty"
spectators = 0
slots = "empty"
referees = 0
dns = "empty"
tempcount = -5
honP = 0
honPID = 0
honEXE = "empty"
check_lobby = True
tempMap = "empty"
client_ip = "empty"
useClog = False
total_games_played = 0
total_games_played_prev = 0
firstrunthrough = True
firstrunthrough = True
just_collected = False
game_started = False
oldDLL = False
newDLL = False
lobby_created = False
first_initialisation = False
config_data = dmgr.mData(f"{os.path.dirname(os.path.realpath(__file__))}\\config\\sdc.ini")
config_dataDict = config_data.returnDict()
nssm = config_dataDict['nssm_exe']
hon_directory = config_dataDict['hon_directory']
hon_game_dir = config_dataDict['hon_game_dir']
sdc_home_dir = config_dataDict['sdc_home_dir']
hon_logs_dir = config_dataDict['hon_logs_dir']
bot_version = config_dataDict['bot_version']
hon_home_dir = config_dataDict['hon_home_dir']
svr_hoster = config_dataDict['svr_hoster']
svr_region = config_dataDict['svr_region']
svr_region_short = config_dataDict['svr_region_short']
svr_id = config_dataDict['svr_id']
svr_id_total = config_dataDict['svrid_total']
svr_ip = config_dataDict['svr_ip']
svr_dns = config_dataDict['svr_dns']
svr_identifier = config_dataDict['svr_identifier']
print("Server Identifier: " + svr_identifier)
svr_total = config_dataDict['svr_total']
bot_token = config_dataDict['token']
pythonLoc = config_dataDict['python_location']
affinity = config_dataDict['svr_affinity']
last_restart_loc = config_dataDict['last_restart_loc']
discord_temp = config_dataDict['discord_temp']
discord_admin = config_dataDict['discord_admin']

server_dataDict = dmgr.mData.parse_config(NULL,f"{hon_game_dir}\\startup.cfg")
print(server_dataDict)
svr_name = server_dataDict['svr_name']
svr_location = server_dataDict['svr_location']
svr_port = server_dataDict['svr_port']
svr_proxy_enabled = server_dataDict['man_enableProxy']

os.environ["USERPROFILE"] = hon_home_dir
os.chdir(hon_logs_dir)

class serverDATA():
    global firstrunthrough
    global useClog
    global total_games_played_prev
    global total_games_played
    global game_started
    global gameLoc
    global config_dataDict
    global nssm
    global hon_directory
    global sdc_home_dir
    global hon_logs_dir
    global bot_version
    global hon_home_dir
    global svr_hoster
    global svr_region
    global svr_region_short
    global svr_id
    global svr_ip
    global svr_port
    global svr_dns
    global svr_identifier
    global svr_total
    global bot_token
    global pythonLoc
    global affinity
    global last_restart_loc
    global discord_temp
    def __init__(self):        
        return

    def grabData(self, dataType):
        #
        #   Eckko RAM reader for HoN lobby
        #   -3 = invalid | -2 = no process  | 0 = connection no lobby | 1 = lobby + connection
        if dataType == "honRam":
            global gameDllHash
            global oldDLL
            global newDLL
        #
        #   Determine the game server DLL so we can use the correct player count utility
            if gameDllHash == "70e841d98e59dfe9347e24260719e1b7b590ebb8":
                print("oldDLL")
                oldDLL = True
                return f"{hon_directory}eko-old.exe"
            elif gameDllHash == "3d97c3fb6121219344cfabe8dfcc608fac122db4":
                print("newDLL file")
                newDLL = True
                return f"{hon_directory}eko-pid.exe"
        #
        #   If no match, attempt the newer utility
            else:
                newDLL = True
                return f"{hon_directory}eko-pid.exe"

        #
        #   Hash the game server DLL file
        elif dataType == "gameDllHash":
            #
            # 3d97c3fb6121219344cfabe8dfcc608fac122db4 = ECKKO DLL
            # 70e841d98e59dfe9347e24260719e1b7b590ebb8 = oldDLL DLL
            #
            sha1 = hashlib.sha1()
            #   
            #   make a hash object
            #   open file for reading in binary mode
            with open(config_dataDict['svr_k2dll'],'rb') as file:
                #   loop till the end of the file
                chunk = 0
                while chunk != b'':
                    #   read only 1024 bytes at a time
                    chunk = file.read(1024)
                    sha1.update(chunk)
            gameDllHash = sha1.hexdigest()
            print(gameDllHash)
            #
            #    return the hex representation of digest
            return gameDllHash
        #
        #   Determine the total # of games played by counting files in the logs directory
        elif dataType == "TotalGamesPlayed":
            global total_games_played
            global total_games_played_prev
            global game_started
            tempList = []
            for item in os.listdir():
                if "game" in item or (item.startswith("M") and item.endswith(".log")):
                    tempList.append(item)
            if not tempList:
                print("NO GAME FILE EITHER, we should make one")
                with open('game_0000.log', 'w'): pass
                tempList.append("game_0000.log")
            #total_games_played_file = tempList[len(tempList)-1]
            total_games_played = len(tempList)
            #total_games_played = re.search(r'\d+', total_games_played_file).group(0)    

            return total_games_played
        #
        # Compare the total games played when server started to now. If it's changed, there's a new lobby, come here to check if we're in a match yet.
        elif dataType == "CheckInGame":
            global game_started
            global total_games_played_prev
            global gameLoc
            global tempcount
            
            gameLoc = serverDATA.grabData(self,"getLogList_Game")
            total_games_played_prev_int = int(total_games_played_prev)
            total_games_played_int = int(total_games_played)
            print ("about to check game started")
            if (total_games_played_int > total_games_played_prev_int and os.stat(gameLoc).st_size > 0 and game_started == False):
                print("checking for game started now")
                with open (gameLoc, "r", encoding='utf-16-le') as f:
                        for line in f:
                            if "PLAYER_SELECT" in line or "PLAYER_RANDOM" in line or "GAME_START" in line or "] StartMatch" in line:
                                print("More accurate GAME STARTED")
                                game_started = True
                                tempcount = -5
                                break
            return game_started
        #
        #   Get the last restart time
        elif dataType == "lastRestart":
            if exists(last_restart_loc):
                with open(last_restart_loc, 'r') as f:
                    last_restart = f.readline()
                f.close()
            else:
                last_restart = "not yet restarted"
                with open(last_restart_loc, 'w') as f:
                    f.write(last_restart)
            return last_restart
        #
        #   Get a list of all local maps
        elif dataType == "availMaps":
            available_maps = []
            for item in os.listdir(f"{hon_directory}game\\maps"):
                if item.endswith(".s2z"):
                    item = item.replace('.s2z','')
                    print("adding to list: "+str(item))
                    available_maps.append(item)
            return available_maps
        #
        #   Get latest game lobby logs
        elif dataType == "getLogList_Game":
            print("checking game logs")
            tempList = []
            try:
                # get list of files that matches pattern
                pattern="Slave-1_M*console.clog"
                #pattern="M*log"

                files = list(filter(os.path.isfile, glob.glob(pattern)))

                # sort by modified time
                files.sort(key=lambda x: os.path.getmtime(x))

                # get last item in list
                gameLoc = files[-1]

                print("Most recent file matching {}: {}".format(pattern,gameLoc))
                
                # for item in os.listdir():
                #     if "game" in item or (item.startswith("M") and item.endswith(".log")):
                #         tempList.append(item)
                # gameLoc = tempList[len(tempList)-1]
            except:
                print(e)
                pass
            return gameLoc
        #
        #   Get latest server slave log
        elif dataType == "getLogList_Slave":
            print("checking slave logs")
            global useClog
            global firstrunthrough
            global first_initialisation
            tempList = []
            for item in os.listdir():
                if (item.startswith("Slave") and item.endswith(".log")) and "Slave-1_M_console.clog" not in item and 'Slave-Temp.log' not in item: #or (item.startswith("Slave-1_M") and item.endswith("console.clog")) 
                    tempList.append(item)
            if not tempList:
                # catch error where there is no slave log, create a temp one.
                print("NO SLAVE LOG. FIRST TIME BOT IS BEING LAUNCHED")
                with open('Slave-Temp.log', 'w'): pass
                tempList.append("Slave-Temp.log")
            return tempList[len(tempList)-1]
            
        #
        #   Get the file size of the slave log and write it to a temporary file
        elif dataType == "loadHardSlave":
            last_modified_time_file = f"{sdc_home_dir}\\last_modified_time"
            #
            #   This reads the data if it exists
            if (exists(last_modified_time_file)):
                with open(last_modified_time_file, 'r') as last_modified:
                    lastmodData = last_modified.readline()
                last_modified.close()
                #
                #   Gets the current byte size of the slave log
                checkslave = serverDATA.grabData(self,"getLogList_Slave")
                fileSize = os.stat(checkslave).st_size
                #
                #   After reading data set temporary file to current byte size
                with open(last_modified_time_file, 'w') as last_modifiedw:
                    last_modifiedw.write(f"{fileSize}")
                last_modifiedw.close()
                return lastmodData
            #
            #   If there was no temporary file to load data from, create it.
            else:
                checkslave = serverDATA.grabData(self,"getLogList_Slave")
                try:
                    fileSize = os.stat(checkslave).st_size
                    with open(last_modified_time_file, 'w') as last_modified:
                        last_modified.write(f"{fileSize}")
                    last_modified.close()
                except Exception as e:
                    print(e)
                    pass
                return fileSize
        #
        #    Get the real byte size of the slave log.
        elif dataType == "loadSoftSlave":
            checkslave = serverDATA.grabData(self,"getLogList_Slave")
            fileSize = os.stat(checkslave).st_size
            return fileSize
        #
        # Come here when a lobby has been created, and the real slave log byte is different to the current byte size, and start collecting lobby information.
        elif dataType == "GameCheck":
            global host
            global version
            global check_lobby
            global just_collected
            global lobby_created
            global client_ip
            
            dataFile = serverDATA.grabData(self,"getLogList_Slave")
            #softSlave = serverDATA.grabData(self,"loadSoftSlave")
            #hardSlave = serverDATA.grabData(self,"loadHardSlave")

            #if softSlave is not hardSlave: #and check_lobby is True:
            dataL = open(dataFile,encoding='utf-16-le')
            data = dataL.readlines()
            dataL.close()
            #
            #   Someone has connected to the server and is about to host a game
            for line in data:
                if "Name: " in line:
                    host = line.split(": ")
                    host = host[2].replace('\n','')
                    print ("host: "+host)
                if "Version: " in line:
                    version = line.split(": ")
                    version = version[2].replace('\n','')
                    print("version: "+version)
                if "Connection request from: " in line:
                    client_ip = line.split(": ")
                    client_ip = client_ip[2].replace('\n','')
                    print(client_ip)   
                #
                #   Arguments passed to server, and lobby starting
                if "GAME_CMD_CREATE_GAME" in line:
                    global map
                    global mode
                    global slots
                    global teamsize
                    global spectators
                    global referees

                    print("lobby starting....")
                    test = line.split(' ')
                    for parameter in test:
                        if "map:" in parameter:
                            map = parameter.split(":")
                            map = map[1]
                            print("map: "+ map)
                        if "mode:" in parameter:
                            mode = parameter.split(":")
                            mode = mode[1]
                            print("mode: "+ mode)
                        if "teamsize:" in parameter:
                            teamsize = parameter.split(":")
                            teamsize = teamsize[1]
                            slots = int(teamsize)
                            slots *= 2
                            slots = str(slots)
                            print("teamsize: "+ teamsize)
                            print("slots: "+slots)
                        if "spectators:" in parameter:
                            spectators = parameter.split(":")
                            spectators = spectators[1]
                            print("spectators: "+ spectators)
                        if "referees:" in parameter:
                            referees = parameter.split(":")
                            referees = referees[1]
                            print("referees: "+ str(int(referees)))
                    # 
                    #   Set firstrunthrough to false so we don't accidentally come back here and waste IO.
                    #   Also set some other booleans for code logic later on
                    firstrunthrough = False  
                    just_collected = True
                    lobby_created = True
        #
        #   Check if discord file exists, if it does loads to data, else returns false
        elif dataType == "loadDiscData":
            global discordData
            if (discord_temp):
                dataFile = open(discord_temp)
                discordData = dataFile.readline()
                discordData = discordData.split("-")
                config_dataDict.update({f'discord_data':discordData})
                return True
            else: return False

        elif dataType == "update_last_restarted":
            t = time.localtime()
            last_restart_time = time.strftime('%b-%d-%Y %H:%M', t)
            with open (last_restart_loc, 'w') as f:
                f.write(last_restart_time)

bot = commands.Bot(command_prefix='!')

class hsl(commands.Bot):
    def __init__(self,bot):
        return
    #
    #   Checks if bot has been used before, in which case there will be an existing message to update instead of making a new one.
    @bot.command()
    async def startbot(self,serverNum):
        checkData = serverDATA()
        if serverNum == svr_identifier:
            #   If data is found run startPrev
            if checkData.grabData("loadDiscData"):
                await hsl.startPrev(self,serverNum)
            # #   If data is not foud run startNew
            else: await hsl.startNew(self,serverNum)
    #
    #   If new run startbot(self) uses this command
    @bot.command()
    async def startNew(self,serverNum):
        global stripColor
        global mainEmbed
        #   Load sessrsrrrsr tomato
        print(self.author.bot)
        honDATA = serverDATA()
        if serverNum == svr_identifier:
            if self.author.bot == False:
                print("deleted message")
                await self.message.delete()
            else: return
            #   Sets the color of when the first message is sent
            stripColor = discord.Color.light_grey()
            #   Creates embed
            emb = await hsl.manageEmbed(self)
            #   Sends embed and captures as object
            mainEmbed = await self.send(embed = emb)
            #   Sets the guild, channel, and message id to variables
            guildid = mainEmbed.guild.id
            channelid = mainEmbed.channel.id
            msgid = mainEmbed.id
            #   Writes guild, channel, and message id to text file
            with open(discord_temp, 'w') as file_handler:
                file_handler.write(f"{guildid}-")
                file_handler.write(f"{channelid}-")
                file_handler.write(f"{msgid}")
                file_handler.close
            #
            #   Loads reations 1 by 1 else the loop will break because of the check_reaction
            for i in range(0,4):
                if i == 0:
                    await mainEmbed.add_reaction("🔁")
                elif i == 1:
                    await mainEmbed.add_reaction("🔼")
                elif i == 2:
                    await mainEmbed.add_reaction("🔽")
                elif i == 3:
                    await mainEmbed.add_reaction("🛑")
            #   Loads data into the global variable discordDATA
            honDATA.grabData("loadDiscData")
            #   Starts the heartbeat
            await hsl.heartbeat(self)
    #
    #   If bot has been run previous uses this command
    @bot.command()
    async def startPrev(self,serverNum):
        global stripColor
        global mainEmbed
        honDATA = serverDATA()
        print(self.author.bot)
        #
        #   An argument will be passed like "!startbot GUAM-1, so we are checking if the command matches the region of the bot."
        if serverNum == svr_identifier:
            if self.author.bot == False:
                print("deleted")
                await self.message.delete()
            else: return
            #   Resets color to this color
            stripColor = discord.Color.light_grey()
            #   loads guild from cache, else api fetch
            guild = bot.get_guild(discordData[0])
            if guild is None:
                guild = await bot.fetch_guild(discordData[0])
            #   Loads channel from cache, else api fetch
            channel = bot.get_channel(discordData[1])
            if channel is None:
                channel = await bot.fetch_channel(discordData[1])
            #   fetches message, can't use partial message becGUAMe partial message has no edit feature
            mainEmbed = await channel.fetch_message(discordData[2])
            #   Starts the heartbeat
            await hsl.heartbeat(self)

    #
    #   Create and manages embeds
    @bot.command()
    async def manageEmbed(self):
        global discordData
        global playerCount
        global stripColor
        global map
        global mode
        global slots
        global teamsize
        global spectators
        global referees
        global host
        global client_ip
        global version
        global tempMap
        global firstrunthrough
        global total_games_played
        global total_games_played_prev
        global game_started

        #   Loads the data manager
        embData = serverDATA()
        embRam = ramCheck()
        last_restart = embData.grabData("lastRestart")
        #   Grabs ram data
        playerCount = embRam.checkRAM()
        #
        #   Update embed when no player is connected
        if playerCount < 0:
            emb = discord.Embed(title=f"{svr_region_short} {svr_name}  |  Offline",description='[honmasterserver.com](https://honmasterserver.com)  |  [honclientfix.exe](https://www.mediafire.com/file/4xdih1yy54y4qah/HonClientFix.exe/file)', color=stripColor)
            #name='\u200b' to hide title
            emb.set_footer(text=f"v{bot_version}  |  Games Played: {total_games_played_prev}  |  Last Restart: {last_restart}")
            emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/677148268513198127/999338469375615027/thumbs_down.png")
        #   
        #   Update embed when server is alive
        elif playerCount == 0 and firstrunthrough == True:
            emb = discord.Embed(title=f"{svr_region_short} {svr_name}  |  Ready for host...",description='[honmasterserver.com](https://honmasterserver.com)  |  [honclientfix.exe](https://www.mediafire.com/file/4xdih1yy54y4qah/HonClientFix.exe/file)', color=stripColor)
            if svr_dns is None:
                emb.add_field(name=f"Connect (ready):",value=f"```\nconnect {svr_ip}:{svr_port}\n```",inline=True)
            else:
                emb.add_field(name=f"Connect (ready):",value=f"```\nconnect {svr_dns}:{svr_port}\n```",inline=True)
            emb.set_footer(text=f"v{bot_version}  |  Games Played: {total_games_played_prev}  |  Last Restart: {last_restart}")
            emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/677148268513198127/999161222865899602/thumbs_up.png")
        elif playerCount == 0 and firstrunthrough == False:
            emb = discord.Embed(title=f"{svr_region_short} {svr_name}                           RESTARTING SERVER...", color=stripColor)
            serverDATA().grabData("update_last_restarted")
        #
        #    Update embed when host is connected
        elif playerCount == 1:
            total_games_played = embData.grabData("TotalGamesPlayed")
            #total_games_played = re.search(r'\d+', total_games_played).group(0)
        #
        #   Update embed when a lobby has been created
            if just_collected is True or lobby_created == True:
                print("----updating with map data----")
                emb = discord.Embed(title=f"{svr_region_short} {svr_name}  |  Player Count: {playerCount}",description='[honmasterserver.com](https://honmasterserver.com)  |  [honclientfix.exe](https://www.mediafire.com/file/4xdih1yy54y4qah/HonClientFix.exe/file)', color=stripColor)
                emb.add_field(name="Host: ", value=f"{host}",inline=True)
                emb.add_field(name="Map: ", value=f"{map}",inline=True)
                emb.add_field(name="Mode: ", value=f"{mode}",inline=True)
                emb.add_field(name="Slots: ", value=f"{slots}",inline=True)
                emb.add_field(name="Spectators: ", value=f"{spectators}",inline=True)
                emb.add_field(name="Referees: ", value=f"{referees}",inline=True)
                if game_started == False:
                    if svr_dns is None:
                        emb.add_field(name=f"Connect now!",value=f"```\nconnect {svr_ip}:{svr_port}\n```",inline=False)
                    else:
                        emb.add_field(name=f"Connect now!",value=f"```\nconnect {svr_dns}:{svr_port}\n```",inline=False)
                    emb.set_footer(text=f"v{bot_version}  |  Games Played: {total_games_played_prev}  |  Last Restart: {last_restart}")
                    emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/677148268513198127/999161222865899602/thumbs_up.png")
                elif game_started == True:
                    emb.add_field(name=f"Match in progress",value=f"```\nPlease wait until the game is over..\n```",inline=False)
                    emb.set_footer(text=f"v{bot_version}  |  Games Played: {total_games_played_prev}  |  Last Restart: {last_restart}")
                    emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/677148268513198127/999351448217321543/spectator.png")
            #
            #   No lobby still, just a host.
            elif just_collected is False and firstrunthrough == True:
                print("----No map data to add yet----")
                emb = discord.Embed(title=f"{svr_region_short} {svr_name}  |  Hosted",description='[honmasterserver.com](https://honmasterserver.com)  |  [honclientfix.exe](https://www.mediafire.com/file/4xdih1yy54y4qah/HonClientFix.exe/file)', color=stripColor)
                if svr_dns is None:
                    emb.add_field(name=f"No Lobby",value="```\nPlease wait for the host to begin the game..\n```")
                else:
                    emb.add_field(name=f"No Lobby",value="```\nPlease wait for the host to begin the game..\n```")
                emb.set_footer(text=f"v{bot_version}  |  Games Played: {total_games_played_prev}  |  Last Restart: {last_restart}")
                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/677148268513198127/999342199936397342/icon_loading.png")
            #
            #   Update embed for when there's only 1 player and the game is started. This happens when all but 1 player leave the game.
            elif game_started == True:
                emb.add_field(name=f"Match in progress",value=f"```\nPlease wait until the game is over..\n```",inline=False)
                emb.set_footer(text=f"v{bot_version}  |  Games Played: {total_games_played_prev}  |  Last Restart: {last_restart}")
                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/677148268513198127/999351448217321543/spectator.png")
        #
        #   when lobby is created, keep the info there as the rest of the players join the match
        elif playerCount > 1:
            print("----maintain map information----")
            emb = discord.Embed(title=f"{svr_region_short} {svr_name}  |  Player Count: {playerCount}",description='[honmasterserver.com](https://honmasterserver.com)  |  [honclientfix.exe](https://www.mediafire.com/file/4xdih1yy54y4qah/HonClientFix.exe/file)', color=stripColor)
            emb.add_field(name="Host: ", value=f"{host}",inline=True)
            emb.add_field(name="Map: ", value=f"{map}",inline=True)
            emb.add_field(name="Mode: ", value=f"{mode}",inline=True)
            emb.add_field(name="Slots: ", value=f"{slots}",inline=True)
            emb.add_field(name="Spectators: ", value=f"{spectators}",inline=True)
            emb.add_field(name="Referees: ", value=f"{referees}",inline=True)
            if game_started == False:
                if svr_dns is None and game_started == False:
                    emb.add_field(name=f"Connect now!",value=f"```\nconnect {svr_ip}:{svr_port}\n```",inline=False)
                elif svr_dns is not None and game_started == False:
                    emb.add_field(name=f"Connect now!",value=f"```\nconnect {svr_dns}:{svr_port}\n```",inline=False)
                emb.set_footer(text=f"v{bot_version}  |  Games Played: {total_games_played_prev}  |  Last Restart: {last_restart}")
                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/677148268513198127/999161222865899602/thumbs_up.png")
            elif game_started == True:
                emb.add_field(name=f"Match in progress",value=f"```\nPlease wait until the game is over..\n```",inline=False)
                emb.set_footer(text=f"v{bot_version}  |  Games Played: {total_games_played_prev}  |  Last Restart: {last_restart}")
                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/677148268513198127/999351448217321543/spectator.png")
        return emb

    #
    #   This is the bot heart beat, bum bum, bum bum,
    #   This is how we are able to keep the discord embeds always up to date.
    #   The heartbeat will constantly check the # of connected players, when this changes, it knows something may have changed, and to force an update on the embed.
    @bot.command()
    async def heartbeat(self):
        check = ramCheck()
        global stripColor
        global mainEmbed
        global tempcount
        global check_lobby
        global map
        global client_ip
        global tempMap
        global just_collected
        global lobby_created
        global useClog
        global firstrunthrough
        global game_started
        global embed_updated

        priority_normal = False
        priority_realtime = False

        #   This loop is the heart beat
        while True:
            #   Heart beat speed
            await asyncio.sleep(1)
            #   checks hon status
            #   
            playerCount = check.checkRAM()
            print(playerCount)
            #
            #   If hon is closed return red strip
            GameCheck = serverDATA()
            if playerCount == 1 and game_started == False and lobby_created == False:
                #   can be improved so softslave checks the size of the slave file rather than getting the slave list again.
                hardSlave = GameCheck.grabData("loadHardSlave")
                #   can be improved so softslave checks the size of the slave file rather than getting the slave list again.
                softSlave = GameCheck.grabData("loadSoftSlave")

            #
            #   Compare the last saved byte size of slave log, to the current size, so we know if to check whether a match has started.
                if (str(softSlave) != str(hardSlave)) and playerCount == 1 and firstrunthrough == True:
                        print("comparing modified date")
                        print(GameCheck.grabData("loadHardSlave"))
                        print(GameCheck.grabData("loadSoftSlave"))
                        print("getting data")
                        GameCheck.grabData("GameCheck")
                        print("Just collected: "+str(just_collected))

            if game_started != True and playerCount > 1:
                GameCheck.grabData("CheckInGame")
            if playerCount == tempcount and just_collected is False:
                #
                #   The below appears to cause a "loop" recursion error to occur. However it solved the issue of "checkRam" essentially doubling the speed of the heartbeat.
                # await hsl.heartbeat()
                #   The following doubles the speed of heartbeat once.
                print ("idle")
                #return True
                #playerCount = check.checkRAM()
            else:
                tempcount = playerCount
                if playerCount < 0:
                    stripColor = discord.Color.red()
                    pushEmbed = await hsl.manageEmbed(hsl)
                    await mainEmbed.edit(embed = pushEmbed)
                #I don't think we can get -1 with pid anymore
                elif playerCount == 0 and firstrunthrough == True:
                    available_maps = serverDATA().grabData("availMaps")
                    stripColor = discord.Color.teal()
                    pushEmbed = await hsl.manageEmbed(hsl)
                    await mainEmbed.edit(embed = pushEmbed)
                    if priority_realtime == True or priority_normal == False:
                        honPID.nice(psutil.NORMAL_PRIORITY_CLASS)
                        print("priority set to normal")
                        priority_normal = True
                        priority_realtime = False
                elif playerCount == 0 and firstrunthrough == False or (playerCount == 1 and  map != "empty" and map not in available_maps):
                    if playerCount == 1:
                        #
                        #   sinister behaviour detected, save log to file.
                        #   Players can attempt to start a game on an uknown map file. This causes the server to crash and hang.
                        #   We will firstly handle the error, restart the server, and then log the event for investigation.
                        file_name = serverDATA().grabData("getLogList_Slave")
                        serverID = serverDATA().grabData("serverID")
                        t = time.localtime()
                        timestamp = time.strftime('%b-%d-%Y_%H%M', t)
                        #current_dir = os.getcwd()
                        print(client_ip)
                        save_path = f"{hon_logs_dir}\\sdc\\suspicious\\svr{serverID}-{map}-{host}-{client_ip}-{timestamp}.log"
                        shutil.copyfile(file_name, save_path)
                    #
                    #   we are here because the player count has reached 0 and a match has been started, or finished. Either way, the server needs a restart.
                    honShell = honCMD()
                    checkStat = check.checkRAM()
                    #   Set embed to orange while we restart
                    stripColor = discord.Color.orange()
                    pushEmbed = await hsl.manageEmbed(hsl)
                    await mainEmbed.edit(embed = pushEmbed)
                    await asyncio.sleep(30)
                    honShell.stopSERVER()
                    print("RESTARTING AS LOBBY HAS BEEN RESET")
                    #
                    #   Code is stuck waiting for server to turn off
                    while checkStat < 0:
                        checkStat = check.checkRAM()
                    #
                    #   Once detects server is offline with above code start the server
                    honShell.startSERVER()
                #
                #   On playercount reaching one, lets go and advise that the game has been hosted but not yet created.
                elif playerCount == 1 and just_collected is False and lobby_created == False:
                    print("moving to update normally")
                    stripColor = discord.Color.purple()
                    pushEmbed = await hsl.manageEmbed(hsl)
                    await mainEmbed.edit(embed = pushEmbed)
                #
                #
                elif priority_realtime == False and playerCount >= 1 and lobby_created == True:
                    honPID.nice(psutil.REALTIME_PRIORITY_CLASS)
                    print("priority set to realtime")
                    priority_realtime = True
                    priority_normal = False
                #
                #   On playercount reaching one and more, and lobby being created, let's advise the players that they are now able to join.
                elif playerCount >= 1 and just_collected is False and lobby_created == True and game_started == False:
                    print("moving to update normally")
                    stripColor = discord.Color.green()
                    pushEmbed = await hsl.manageEmbed(hsl)
                    await mainEmbed.edit(embed = pushEmbed)
                #
                #   for the instance where a host has connected but not yet started the game, we need to wait until game has been started so that the message can be updated.
                elif playerCount == 1 and just_collected is True:
                    tempcount = playerCount
                    print("collected yet?: "+str(just_collected))
                    print("moving to update with game check")
                    stripColor = discord.Color.green()
                    pushEmbed = await hsl.manageEmbed(hsl)
                    await mainEmbed.edit(embed = pushEmbed)
                    #   set back to false in order to return the heartbeat to "standby mode"
                    just_collected = False
                #
                #   if we're in lobby, keep the embeds updated while players join.
                elif playerCount > 1 and game_started == True and embed_updated == False:
                    tempcount = playerCount
                    print("Game started, updating embed: "+str(just_collected))
                    stripColor = discord.Color.blue()
                    pushEmbed = await hsl.manageEmbed(hsl)
                    await mainEmbed.edit(embed = pushEmbed)
                    embed_updated = True
                elif playerCount >= 1 and game_started ==True and embed_updated == True:
                    tempcount = playerCount
                    print("Game already running, updating embed: "+str(just_collected))
                    stripColor = discord.Color.blue()
                    pushEmbed = await hsl.manageEmbed(hsl)
                    await mainEmbed.edit(embed = pushEmbed)
    #
    #   The buttons
    #
    @bot.event
    async def on_raw_reaction_add(react):
        global mainEmbed
        global stripColor
        global discordData
        """"
         0 guild, 1 channel, 2 message
        """
        #print(react.member.roles)
        if react.member.bot == False:
            modRole = []
            #deletes reactoin
            await mainEmbed.remove_reaction(react.emoji,react.member)
            #add roles to list
            for role in react.member.roles:
                modRole.append(role.name)
            """
               !!! REQUIRES TESTING WITH MULTIBOTS !!!
            
            checks message id with hardcoded txt id
            only way to make buttons function with multiple bots i think
            
            """
            if discordData[2] == str(react.message_id):
                ramData = ramCheck()
                honShell = honCMD()
                #   anyone can restart
                if (react.emoji.name == "🔁"):
                    #checking current server status
                    checkStat = ramData.checkRAM()
                    #   If server is online and empty restart
                    if (checkStat == 0) or (checkStat == -1):
                        honShell.stopSERVER()
                        #
                        #   Code is stuck waiting for server to turn off
                        while checkStat < 0:
                            checkStat = ramData.checkRAM()
                        #
                        #   Once detects server is offline with above code start the server
                        honShell.startSERVER()
                        serverDATA().grabData("update_last_restarted")
                        """
                        This code is depreciated because the heartbeat manages colors

                        #while checkStat <0:
                        #    checkStat = ramData.checkRAM()
                        #pushEmbed = await hsl.manageEmbed(hsl)
                        #await mainEmbed.edit(embed = pushEmbed)
                        """
                #
                #   Starts server
                #   Anyone can use because this button is disabled if server is offline
                elif (react.emoji.name == "🔼"):
                    #   Checks current status of server
                    checkStat = ramData.checkRAM()
                    #   If server has no user start
                    if checkStat < 0:
                        honShell.startSERVER()
                #
                #   Anyone can stop if no players are connected
                elif (react.emoji.name == "🔽"):
                    #   Checks current hon status
                    checkStat = ramData.checkRAM()
                    #   If server is empty restart
                    if checkStat == 0 or checkStat == -1:
                        honShell.stopSERVER()
                #
                #   only admins can force stop.
                elif (react.emoji.name == "🛑") and config_dataDict['discord_admin'] in modRole:
                    honShell.stopSERVER()
            else: return
#
#   check lobby class (player count)
#   This is what the heartbeat calls constantly
class ramCheck():
    def __init__(self):
        return

    def checkRAM(self):
        global honPID
        global honP
        ramDATA = serverDATA()
        check = subprocess.Popen([ramDATA.grabData("honRam"), str(honP)],stdout=subprocess.PIPE, text=True)
        i = int(check.stdout.read())
        check.terminate()
        return i

#
#   hooks onto hon.exe and manages hon
class honCMD():
    def __init__(self):
        return
    global honEXE
    #   Loads the server Data
    honDATA = serverDATA()
    #   Starts server
    def startSERVER(self):
        #serverDATA().setupEnvironment()
        global honEXE
        global honPID
        global honP
        global firstrunthrough
        global just_collected
        global lobby_created
        global tempcount
        global total_games_played_prev
        global game_started
        global embed_updated
        global gameDllHash
        global oldDLL
        global newDLL
        global first_initialisation

        gamesplayed_stat = serverDATA()
        #   Gets the game server DLL hash
        gameDllHash = gamesplayed_stat.grabData("gameDllHash")
        #   Gets the total # of games played so far
        total_games_played_prev = gamesplayed_stat.grabData("TotalGamesPlayed")
        #
        #   Start the HoN Server!
        print("starting service")
        honEXE = subprocess.Popen([config_dataDict['hon_exe'],"-dedicated","-masterserver","honmasterserver.com"])
        #   get the ACTUAL PID, otherwise it's just a string. Furthermore we use honp now when talking to PID
        honP = honEXE.pid
        honPID = psutil.Process(pid=honEXE.pid)
        #   Set server priority to REALTIME for least lag
        #   honPID.nice(psutil.REALTIME_PRIORITY_CLASS)
        #   Set the CPU affinity to use only a single core
        honPID.cpu_affinity([affinity])
        #
        #   Initialise some variables upon hon server starting
        just_collected = False
        firstrunthrough = True
        game_started = False
        tempcount = -5
        embed_updated = False
        lobby_created = False
        first_initialisation = False
        return True
    #
    #   Stop server
    def stopSERVER(self):
        global honEXE
        if honEXE == "empty":
            for proc in psutil.process_iter():
                if proc.name() == config_dataDict['hon_file_name']:
                    proc.terminate()
        else: honEXE.terminate()
#
#   runs bot
def run_bot():
    hsl(bot)
    bot.run(config_dataDict['token'])
if __name__ == '__main__':
    run_bot()