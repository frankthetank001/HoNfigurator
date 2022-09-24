from email import message
import discord
from discord.ext import commands
from os.path import exists
import os
from cogs.dataManager import mData
import cogs.server_status as srvcmd
import cogs.behemothHeart as heart
import asyncio
from datetime import datetime
from random import randint
from time import sleep
import traceback
from discord.ext import tasks
import ctypes, sys
from typing import Optional 

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

# check if running as admin
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
if is_admin():
    bot = commands.Bot(command_prefix='!',case_insensitive=True)
    client = discord.Client(intents=discord.Intents.default())
    bot.remove_command("help")
    embed_ids=[]
    embed_obj=[]
    embed_log=[]
    waited = False
    owner_reachable = True
    # svr_status = srvcmd.serverStatus()
    svr_cmd = srvcmd.honCMD()
    # svr_playerCount = svr_status.playerCount()

    dmgr = mData()
    #processed_data_dict = dmgr.returnDict(f"{os.path.dirname(os.path.realpath(__file__))}\\config\\sdc.ini")
    processed_data_dict = dmgr.returnDict()
    os.chdir(processed_data_dict['hon_logs_dir'])
    svr_id = processed_data_dict['svr_id']
    svr_id = int(svr_id)
    svr_id_delay = svr_id * 20
    print(svr_id)
    #svr_id_delay = 0
    svr_identifier = processed_data_dict['svr_identifier']
    svr_hoster = processed_data_dict['svr_hoster']
    ctypes.windll.kernel32.SetConsoleTitleW(f"adminbot{svr_id}")
    #os.environ["USERPROFILE"] = processed_data_dict['hon_root_dir']

    old_adminbot_exe = f"{processed_data_dict['sdc_home_dir']}\\adminbot{svr_id}_old.exe"
    if exists(old_adminbot_exe):
        try:
            os.remove(old_adminbot_exe)
        except:
            print(traceback.format_exc())
            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
    # class logging:
    class hsl(commands.Cog):
        def __init__(self,bot):
            self.bot = bot
            self.server_status = svr_cmd.getStatus()

            #   loads the embed manager class
            bot.load_extension("cogs.embedManagerCog")
            bot.load_extension("cogs.behemothHeart")
            self.embed_log=[]
            #   loads the embed_ids list for read
            global embed_ids
            #
            #   grabs the ids from test.txt and inserts them into the embed_ids list
            if exists(processed_data_dict['discord_temp']):
                embedData = open(processed_data_dict['discord_temp'], 'r')
                embed_file = embedData.readlines()
                for dataLine in embed_file:
                    if "-" in dataLine:
                        embedData.close()
                        os.remove(processed_data_dict['discord_temp'])
                        break
                    temp_embed = dataLine.split(",")
                    embed_ids.append([int(temp_embed[0]),int(temp_embed[1]),int(temp_embed[2])])
                embedData.close()
            #
            #   if file does not exists creates it
            else:
                embedData = open(processed_data_dict['discord_temp'],'w')
                embedData.close()
            return
        def time():
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        @tasks.loop(count=1)
        async def wait_until_ready():
            await bot.wait_until_ready()
            global embed_obj
            global discord_admin
            discord_admin = await bot.fetch_user(processed_data_dict['discord_admin'])
            tempData = ({'discord_admin_name':f"@{discord_admin.name}"})
            svr_cmd.updateStatus(tempData)
            if processed_data_dict['disable_bot'] == 'False':
                for embed in embed_ids:
                    try:
                        #sleep(randint(1,5))
                        #
                        #   Loads guild
                        tempGuild = bot.get_guild(embed[0])
                        if tempGuild is None:
                            tempGuild = await bot.fetch_guild(embed[0])
                        #
                        #   Loads channel
                        tempChannel = tempGuild.get_channel(embed[1])
                        if tempChannel is None:
                            tempChannel = await bot.fetch_channel(embed[1])
                        #
                        #   fetches message
                        tempEmbed = await tempChannel.fetch_message(embed[2])
                        embed_obj.append(tempEmbed)
                        ctx = await bot.get_context(embed_obj[0])
                        if len(embed_log) == 0:
                            temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg="Welcome owner... :) " + "``"+hsl.time()+"``")
                            try:
                                embedObj = await discord_admin.send(embed=temp_log)
                            except:
                                print(traceback.format_exc())
                                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                            embed_log.append(embedObj)
                            #hsl.LastEmbedLog(embed_log)
                        logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [OK] Connected to link in: ``{str(tempGuild.name)} ({str(tempChannel.name)})``"))
                        try:
                            await embed_log[0].edit(embed=logEmbed)
                            await ctx.invoke(bot.get_command('sendEmbedLog'),embed_log)
                        except:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        # await user.send("hello")
                    except discord.errors.Forbidden:
                        print("No permissions to the previous message.. clearing it from message cache")
                        try:
                            embed_ids.remove(embed)
                            embedFile = open(processed_data_dict['discord_temp'], 'w')
                            for i in range(len(embed_ids)):
                                embedFile.write(str(embed_ids[i][0])+","+str(embed_ids[i][1])+","+str(embed_ids[i][2])+"\n")
                            embedFile.close()
                        except:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    except discord.errors.NotFound:
                        print("Previous message not found.. clearing it from message cache")
                        try:
                            embed_ids.remove(embed)
                            embedFile = open(processed_data_dict['discord_temp'], 'w')
                            for i in range(len(embed_ids)):
                                embedFile.write(str(embed_ids[i][0])+","+str(embed_ids[i][1])+","+str(embed_ids[i][2])+"\n")
                            embedFile.close()
                        except:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        print("No permissions to the previous message.. clearing message cache")
                    except:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            # await ctx.invoke(bot.get_command('getStatus'))
            try:
                result = srvcmd.honCMD().startSERVER(False)
                if result == True:
                    print("server started successfully")
                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"The server has started successfully.","INFO")
                    if len(embed_log) == 0:
                        temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg=f"``{hsl.time()}`` Welcome owner... :)")
                        try:
                            if owner_reachable:
                                embedObj = await discord_admin.send(embed=temp_log)
                            else:
                                embedObj = await ctx.author.send(embed=temp_log)
                        except:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        embed_log.append(embedObj)
                        #hsl.LastEmbedLog(embed_log)
                    logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [OK] Server Started."))
                    try:
                        await embed_log[0].edit(embed=logEmbed)
                    except:
                        print(traceback.format_exc())
                        svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                elif result == "ram":
                    print("not enough free RAM to start the server.")
                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"Starting the server failed because there is not enough free RAM (1GB minimum required).","FATAL")
                    if processed_data_dict['disable_bot'] == 'False':
                        if len(embed_log) == 0:
                            temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg=f"``{hsl.time()}`` Welcome owner... :)")
                            try:
                                if owner_reachable:
                                    embedObj = await discord_admin.send(embed=temp_log)
                                else:
                                    embedObj = await ctx.author.send(embed=temp_log)
                            except:
                                print(traceback.format_exc())
                                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                            embed_log.append(embedObj)
                            #hsl.LastEmbedLog(embed_log)
                        logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [ERR] Not enough free RAM or server already running."))
                        try:
                            await embed_log[0].edit(embed=logEmbed)
                        except:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                elif result == "proxy":
                    print("Proxy port is not online.")
                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"Starting the server failed because the proxy port is not online.","FATAL")
                    if processed_data_dict['disable_bot'] == 'False':
                        if len(embed_log) == 0:
                            temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg=f"``{hsl.time()}`` Welcome owner... :)")
                            try:
                                if owner_reachable:
                                    embedObj = await discord_admin.send(embed=temp_log)
                                else:
                                    embedObj = await ctx.author.send(embed=temp_log)
                            except:
                                print(traceback.format_exc())
                                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                            embed_log.append(embedObj)
                            #hsl.LastEmbedLog(embed_log)
                        logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [ERR] Game trying to start on PROXY port which isn't online."))
                        try:
                            await embed_log[0].edit(embed=logEmbed)
                        except:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        return
                else:
                    print("starting the server completely failed.")
                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"Starting the server failed for an unknown reason.","FATAL")
                    if processed_data_dict['disable_bot'] == 'False':
                        if len(embed_log) == 0:
                            temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg=f"``{hsl.time()}`` Welcome owner... :)")
                            try:
                                if owner_reachable:
                                    embedObj = await discord_admin.send(embed=temp_log)
                                else:
                                    embedObj = await ctx.author.send(embed=temp_log)
                            except:
                                print(traceback.format_exc())
                                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                            embed_log.append(embedObj)
                            #hsl.LastEmbedLog(embed_log)
                        logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [ERR] Starting the server failed."))
                        try:
                            await embed_log[0].edit(embed=logEmbed)
                        except:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    return
            except:
                print(traceback.format_exc())
                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            if processed_data_dict['disable_bot'] == 'False':
                try:
                    await ctx.invoke(bot.get_command('embedsync'), object_list=embed_obj)
                except UnboundLocalError:
                    temp_log = f"``{hsl.time()}``[ERROR] No message context found, please run ``!createlinks {svr_identifier}`` in your discord channel.\nUse the !portalhelp command for a full list of commands."
                    try:
                        await discord_admin.send(temp_log)
                    except discord.errors.Forbidden:
                        print("Owner is not reachable. We will message the person to send me a command then.")
                        owner_reachable = False
                    except:
                        print(traceback.format_exc())
                        svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    print(traceback.format_exc())
                print("starting behemoth heart.")
                await ctx.invoke(bot.get_command('startheart'))
                # except:
                #     print(traceback.format_exc())
                #     svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"The bot is enabled, yet no one has summoned it to discord yet. Please invite bot to discord and summon it using !createlinks {processed_data_dict['svr_hoster']}","WARNING")
                #     print("starting backup heart until discord !createinks command is run.")
                #     svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"Starting in local mode.","WARNING")
                #     await heart.heartbeat.startheart_bkp()
            else:
                print("bot started in local mode.")
                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"Starting in local mode as discord bot is disabled.","INFO")
                await heart.heartbeat.startheart_bkp()
        #@bot.event
        # async def on_ready():
            
                
        @bot.command()
        async def sendEmbedLog(ctx,embed_log):
            await ctx.invoke(bot.get_command('getembedlog'),embed_log)
        @bot.command()
        async def showlinks(ctx,hoster):
            global embed_ids
            if hoster == svr_hoster or hoster == svr_identifier:
                try:
                    await ctx.message.delete()
                except: pass
                if hoster == svr_hoster:
                    await asyncio.sleep(svr_id)
                for embedList in embed_ids:
                    #
                    #   Loads guild
                    tempGuild = bot.get_guild(embedList[0])
                    if tempGuild is None:
                        tempGuild = await bot.fetch_guild(embedList[0])
                    #
                    #   Loads channel
                    tempChannel = tempGuild.get_channel(embedList[1])
                    if tempChannel is None:
                        tempChannel = await bot.fetch_channel(embedList[1])
                    #
                    #   fetches message
                    tempEmbed = await tempChannel.fetch_message(embedList[2])
                    embed_obj.append(tempEmbed)
                    await ctx.send(svr_identifier + f" Connected to link in: ``{str(tempGuild.name)} ({str(tempChannel.name)})``",delete_after=20)
        """
        
        Creates an intial embed and stores the id as a list of ids [guild,channel,message]

        
        """
        @bot.command()
        async def createlinks(ctx,hoster):
            global waited
            global sent_embed
            global embed_ids
            if hoster == svr_identifier or hoster == svr_hoster:
                try:
                    await ctx.message.delete()
                except: pass
                if hoster == svr_hoster:
                    await asyncio.sleep(svr_id_delay)
                    waited = True
                try:
                    await ctx.invoke(bot.get_command('desync'),hoster)
                except:
                    print(traceback.format_exc())
                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                try:
                    await ctx.invoke(bot.get_command('destroylinkshere'),hoster)
                except:
                    print(traceback.format_exc())
                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                sent_embed = await ctx.invoke(bot.get_command('initiateEmbed'))
                #await asyncio.sleep(1)
                sent_embed_holder = [int(sent_embed.guild.id), int(sent_embed.channel.id),int(sent_embed.id)]
                for embed in embed_ids:
                    temp_sent_embed_holder = sent_embed_holder[1]
                    temp_embed_check = embed[1]
                    if temp_sent_embed_holder == temp_embed_check:
                        embed_ids.remove(embed)
                        embed_ids.append(sent_embed_holder)
                        try:
                            embedFile = open(processed_data_dict['discord_temp'], 'w')
                            for i in range(len(embed_ids)):
                                embedFile.write(str(embed_ids[i][0])+","+str(embed_ids[i][1])+","+str(embed_ids[i][2])+"\n")
                            embedFile.close()
                        except:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        if len(embed_log) == 0:
                            temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg=f"``{hsl.time()}`` Welcome owner... :)")
                            try:
                                if owner_reachable:
                                    embedObj = await discord_admin.send(embed=temp_log)
                                else:
                                    embedObj = await ctx.author.send(embed=temp_log)
                            except:
                                print(traceback.format_exc())
                                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                            embed_log.append(embedObj)
                        logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [OK] link exists and has been replaced"))
                        try:
                            await embed_log[0].edit(embed=logEmbed)
                        except:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        break
                    
                if sent_embed_holder not in embed_ids:
                    try:
                        #
                        #   Loads guild
                        tempGuild = bot.get_guild(sent_embed_holder[0])
                        if tempGuild is None:
                            tempGuild = await bot.fetch_guild(sent_embed_holder[0])
                        #
                        #   Loads channel
                        tempChannel = tempGuild.get_channel(sent_embed_holder[1])
                        if tempChannel is None:
                            tempChannel = await bot.fetch_channel(sent_embed_holder[1])
                        if len(embed_log) == 0:
                            temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg=f"``{hsl.time()}`` Welcome owner... :)")
                            try:
                                if owner_reachable:
                                    embedObj = await discord_admin.send(embed=temp_log)
                                else:
                                    embedObj = await ctx.author.send(embed=temp_log)
                            except:
                                print(traceback.format_exc())
                                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                            embed_log.append(embedObj)
                            #hsl.LastEmbedLog(embed_log)
                        logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [OK] Link successfully created in ``{tempGuild} ({tempChannel})`` by ``{ctx.author}``"))
                        try:
                            await embed_log[0].edit(embed=logEmbed)
                        except:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    except:
                        print(traceback.format_exc())
                        svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    embed_ids.append(sent_embed_holder)
                    embedData = open(processed_data_dict['discord_temp'], 'w')
                    for i in range(len(embed_ids)):
                        embedData.write(str(embed_ids[i][0])+","+str(embed_ids[i][1])+","+str(embed_ids[i][2])+"\n")   
                    embedData.close()
                #await ctx.invoke(bot.get_command('createEmbed'),5)
                await ctx.invoke(bot.get_command('sync'),hoster)

                if hoster == svr_hoster:
                    waited = False
        """

            Turns the list of embed ids from embed_ids into a list of embed objects in embed_obj
            
        """
        @bot.command()
        async def desync(ctx,hoster):
            global waited
            #if hoster == svr_hoster:
            try:
                await ctx.message.delete()
            except: pass
            global embed_obj
            embed_obj = []

        @bot.command()
        async def sync(ctx,hoster):
            global waited
            global embed_obj
            global sent_embed
            if hoster == svr_hoster or hoster == svr_identifier:
                try:
                    await ctx.message.delete()
                except: pass
                # if hoster == svr_hoster:
                #     if not waited:
                #         await asyncio.sleep(svr_id_delay)
                #         waited = True
                #if len(embed_obj)==0:
                #await ctx.invoke(bot.get_command('embedsync'), object_list=embed_obj)
                embed_id_list = [ctx.guild.id, ctx.channel.id]
                for embed in embed_ids:
                    try:
                        temp_sent_embed_holder = embed_id_list[1]
                        temp_embed_check = embed[1]
                        if temp_sent_embed_holder == temp_embed_check:
                            tempGuild = bot.get_guild(embed[0])
                            if tempGuild is None:
                                tempGuild = await bot.fetch_guild(embed[0])
                            # print("guild")
                            # print(str(tempGuild))
                            #
                            #   Loads channel
                            tempChannel = tempGuild.get_channel(embed[1])
                            if tempChannel is None:
                                tempChannel = await bot.fetch_channel(embed[1])
                            # print("channel")
                            # print(str(tempChannel))
                            #
                            #   fetches message
                            tempEmbed = await tempChannel.fetch_message(int(embed[2]))
                            embed_obj.append(tempEmbed)
                    except:
                        print(traceback.format_exc())
                        svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                """
                the below is legacy
                """
                """
                embed_obj = []
                for embed in embed_ids:
                    try:
                        #
                        #   Loads guild
                        tempGuild = bot.get_guild(embed[0])
                        if tempGuild is None:
                            tempGuild = await bot.fetch_guild(embed[0])
                        #
                        #   Loads channel
                        tempChannel = tempGuild.get_channel(embed[1])
                        if tempChannel is None:
                            tempChannel = await bot.fetch_channel(embed[1])
                        #
                        #   fetches message
                        tempEmbed = await tempChannel.fetch_message(embed[2])
                        embed_obj.append(tempEmbed)
                    except:
                        print("clearning unknown message from cache")
                        embed_ids.remove(embed)
                        try:
                            embedFile = open(processed_data_dict['discord_temp'], 'w')
                            for i in range(len(embed_ids)):
                                embedFile.write(str(embed_ids[i][0])+","+str(embed_ids[i][1])+","+str(embed_ids[i][2])+"\n")
                            embedFile.close()
                        except:
            print(traceback.format_exc())
            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        if len(embed_log) == 0:
                            temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg=f"``{hsl.time()}`` Welcome owner... :)")
                            try:
                                if owner_reachable:
                                    embedObj = await discord_admin.send(embed=temp_log)
                                else:
                                    embedObj = await ctx.author.send(embed=temp_log)
                            except:
            print(traceback.format_exc())
            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                            embed_log.append(embedObj)
                            #hsl.LastEmbedLog(embed_log)
                        logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [WARN] No access/unknown message. Removed from cache"))
                        try:
                            await embed_log[0].edit(embed=logEmbed)
                        except:
            print(traceback.format_exc())
            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    #await ctx.author.send(svr_identifier + f" Connected to link in: ``{str(tempGuild.name)} ({str(tempChannel.name)})``")
                    if len(embed_log) == 0:
                        temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg="Initialising...")
                        try:
                            if owner_reachable:
                                embedObj = await discord_admin.send(embed=temp_log)
                            else:
                                embedObj = await ctx.author.send(embed=temp_log)
                        except:
            print(traceback.format_exc())
            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        embed_log.append(embedObj)
                        #hsl.LastEmbedLog(embed_log)
                    logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [OK] Connected to link in: ``{str(tempGuild.name)} ({str(tempChannel.name)})``"))
                    try:
                        await embed_log[0].edit(embed=logEmbed)
                    except:
            print(traceback.format_exc())
            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                #for embedObjects in embed_obj:
                #    created_embed = await ctx.invoke(bot.get_command('offlineEmbed'),)
                #if len(embed_log) == 0:
                """
                if len(embed_log) == 0:
                    temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg="Initialising...")
                    try:
                        if owner_reachable:
                            embedObj = await discord_admin.send(embed=temp_log)
                        else:
                            embedObj = await ctx.author.send(embed=temp_log)
                    except:
                        print(traceback.format_exc())
                        svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    embed_log.append(embedObj)
                    #hsl.LastEmbedLog(embed_log)
                logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [OK] Connected to **"+str(len(embed_ids))+"** server links"))
                try:
                    await embed_log[0].edit(embed=logEmbed)
                except:
                    print(traceback.format_exc())
                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                await ctx.invoke(bot.get_command('embedsync'), object_list=embed_obj)
                # else:
                #     # for embed in embed_ids:
                #     #     await ctx.invoke(bot.get_command('embedsync'), object_list=embed_obj)
                #     if len(embed_log) == 0:
                #         temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg="Initialising...")
                #         try:
                #             if owner_reachable:
                #                 embedObj = await discord_admin.send(embed=temp_log)
                #             else:
                #                 embedObj = await ctx.author.send(embed=temp_log)
                #         except:
                            # print(traceback.format_exc())
                            # svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                #         embed_log.append(embedObj)
                #         #hsl.LastEmbedLog(embed_log)
                #     logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [OK] Links are already synced"))
                #     try:
                #         await embed_log[0].edit(embed=logEmbed)
                #     except:
                        # print(traceback.format_exc())
                        # svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                heart = await ctx.invoke(bot.get_command('statusheart'))
                if not heart:
                    await ctx.invoke(bot.get_command('startheart'))
                if hoster == svr_hoster:
                    waited = False
                
            """
            start the heartbeat, bum bum, bum bum
            heartbeat()
            """
            
        """

            Destroys a link by removing the message from discord and then removing the id from embed_id and the object from embed_obj

        """
        @bot.command()
        async def destroylinkshere(ctx,hoster):
            
            global waited
            if hoster == svr_hoster or hoster == svr_identifier:
                try:
                    await ctx.message.delete()
                except: pass
                if hoster == svr_hoster:
                    if not waited:
                        await asyncio.sleep(svr_id_delay)
                        waited = True
                embed_id_list = [ctx.guild.id, ctx.channel.id]
                for embed in embed_ids:
                    try:
                        temp_sent_embed_holder = embed_id_list[1]
                        temp_embed_check = embed[1]
                        if temp_sent_embed_holder == temp_embed_check:
                            tempGuild = bot.get_guild(embed[0])
                            if tempGuild is None:
                                tempGuild = await bot.fetch_guild(embed[0])
                            # print("guild")
                            # print(str(tempGuild))
                            #
                            #   Loads channel
                            tempChannel = tempGuild.get_channel(embed[1])
                            if tempChannel is None:
                                tempChannel = await bot.fetch_channel(embed[1])
                            # print("channel")
                            # print(str(tempChannel))
                            #
                            #   fetches message
                            tempEmbed = await tempChannel.fetch_message(int(embed[2]))
                            embed_ids.remove(embed)
                            if tempEmbed in embed_obj:
                                embed_obj.remove(tempEmbed)
                            await tempEmbed.delete()
                            if len(embed_log) == 0:
                                temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg=f"``{hsl.time()}`` Welcome owner... :)")
                                try:
                                    if owner_reachable:
                                        embedObj = await discord_admin.send(embed=temp_log)
                                    else:
                                        embedObj = await ctx.author.send(embed=temp_log)
                                except:
                                    print(traceback.format_exc())
                                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                                embed_log.append(embedObj)
                                #hsl.LastEmbedLog(embed_log)
                            logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [OK] Destroyed link in: ``{str(ctx.guild.name)} ({str(tempChannel.name)})``"))
                            try:
                                await embed_log[0].edit(embed=logEmbed)
                            except:
                                print(traceback.format_exc())
                                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    except discord.errors.Forbidden:
                        print("No permissions to the previous message.. clearing message cache")
                        try:
                            embed_ids.remove(embed)
                            embedFile = open(processed_data_dict['discord_temp'], 'w')
                            for i in range(len(embed_ids)):
                                embedFile.write(str(embed_ids[i][0])+","+str(embed_ids[i][1])+","+str(embed_ids[i][2])+"\n")
                            embedFile.close()
                        except:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        if len(embed_log) == 0:
                            temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg=f"``{hsl.time()}`` Welcome owner... :)")
                            try:
                                if owner_reachable:
                                    embedObj = await discord_admin.send(embed=temp_log)
                                else:
                                    embedObj = await ctx.author.send(embed=temp_log)
                            except:
                                print(traceback.format_exc())
                                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                            embed_log.append(embedObj)
                            #hsl.LastEmbedLog(embed_log)
                        logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [WARN] No access/unknown message. Removed from cache"))
                        try:
                            await embed_log[0].edit(embed=logEmbed)
                        except:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    except discord.errors.NotFound:
                        print("No permissions to the previous message.. clearing message cache")
                        try:
                            embed_ids.remove(embed)
                            embedFile = open(processed_data_dict['discord_temp'], 'w')
                            for i in range(len(embed_ids)):
                                embedFile.write(str(embed_ids[i][0])+","+str(embed_ids[i][1])+","+str(embed_ids[i][2])+"\n")
                            embedFile.close()
                        except:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        if len(embed_log) == 0:
                            temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg=f"``{hsl.time()}`` Welcome owner... :)")
                            try:
                                if owner_reachable:
                                    embedObj = await discord_admin.send(embed=temp_log)
                                else:
                                    embedObj = await ctx.author.send(embed=temp_log)
                            except:
                                print(traceback.format_exc())
                                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                            embed_log.append(embedObj)
                            #hsl.LastEmbedLog(embed_log)
                        logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [WARN] No access/unknown message. Removed from cache"))
                        try:
                            await embed_log[0].edit(embed=logEmbed)
                        except:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    except:
                        print(traceback.format_exc())
                        svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                try:
                    embedFile = open(processed_data_dict['discord_temp'], 'w')
                    for i in range(len(embed_ids)):
                        embedFile.write(str(embed_ids[i][0])+","+str(embed_ids[i][1])+","+str(embed_ids[i][2])+"\n")
                    embedFile.close()
                except:
                    print(traceback.format_exc())
                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                # if hoster == svr_hoster:
                #     waited = False


        @bot.command()
        async def testsync(ctx):
            global embed_obj
            print(embed_obj)

        @bot.command()
        async def destroylinks(ctx,hoster):
            global waited
            global embed_obj
            global embed_ids
            if hoster == svr_hoster or hoster == svr_identifier:
                try:
                    await ctx.message.delete()
                except: pass
                if hoster == svr_hoster:
                    if not waited:
                        await asyncio.sleep(svr_id_delay)
                        waited = True
                #await ctx.message.delete()
                #await asyncio.sleep(svr_id_delay)
                #
                #   goes through every embed
                try:
                    for embedList in embed_ids:
                        #
                        #   attempts to load guild from cache
                        tempGuild = bot.get_guild(embedList[0])
                        if tempGuild is None:
                            tempGuild = await bot.fetch_guild(embedList[0])
                        #
                        #   attempts to load channel from cache
                        tempChannel = tempGuild.get_channel(embedList[1])
                        if tempChannel is None:
                            tempChannel = await bot.fetch_channel(embedList[1])
                        #
                        #   attempts to load message from cache
                        tempEmbed = tempChannel.get_partial_message(embedList[2])
                        if tempEmbed is None:
                            tempEmbed = await tempChannel.fetch_message(embedList[2])
                        #
                        #   Deletes embed
                        await tempEmbed.delete()
                        #await ctx.author.send(svr_identifier + f" Deleted link in: ``{str(tempGuild.name)} ({str(tempChannel.name)})``")
                        if len(embed_log) == 0:
                            temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg=f"``{hsl.time()}`` Welcome owner... :)")
                            try:
                                if owner_reachable:
                                    embedObj = await discord_admin.send(embed=temp_log)
                                else:
                                    embedObj = await ctx.author.send(embed=temp_log)
                            except:
                                print(traceback.format_exc())
                                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                            embed_log.append(embedObj)
                            #hsl.LastEmbedLog(embed_log)
                        logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [OK] Destroyed link in: ``{str(tempGuild.name)} ({str(tempChannel.name)})``"))
                        try:
                            await embed_log[0].edit(embed=logEmbed)
                        except:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    #
                    #   Gets how many items existed
                    links_deleted = str(len(embed_ids))
                    #
                    #   empties the lists
                    embed_obj = []
                    embed_ids = []
                    #
                    #   empties the file of messages (will need to create new links)
                    embedData = open(processed_data_dict['discord_temp'], 'w')
                    embedData.write("")   
                    embedData.close()
                    if len(embed_log) == 0:
                        temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg=f"``{hsl.time()}`` Welcome owner... :)")
                        try:
                            if owner_reachable:
                                embedObj = await discord_admin.send(embed=temp_log)
                            else:
                                embedObj = await ctx.author.send(embed=temp_log)
                        except:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        embed_log.append(embedObj)
                        #hsl.LastEmbedLog(embed_log)
                    logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [OK] Deleted **"+links_deleted+"** server links"))
                    try:
                        await embed_log[0].edit(embed=logEmbed)
                    except:
                        print(traceback.format_exc())
                        svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    #await ctx.author.send(svr_identifier + f" Destroyed all links.")
                except:
                    embed_obj = []
                    embed_ids = []
                    #
                    #   empties the file of messages (will need to create new links)
                    embedData = open(processed_data_dict['discord_temp'], 'w')
                    embedData.write("")
                    embedData.close()
                    if len(embed_log) == 0:
                        temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg=f"``{hsl.time()}`` Welcome owner... :)")
                        try:
                            if owner_reachable:
                                embedObj = await discord_admin.send(embed=temp_log)
                            else:
                                embedObj = await ctx.author.send(embed=temp_log)
                        except:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        embed_log.append(embedObj)
                        #hsl.LastEmbedLog(embed_log)
                    logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [OK] Deleted **"+links_deleted+"** server links"))
                    try:
                        await embed_log[0].edit(embed=logEmbed)
                    except:
                        print(traceback.format_exc())
                        svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                if hoster == svr_hoster:
                    waited = False
        """
        
        testing the edit functionality
        test worked
        
        """
            
        @bot.command()
        async def testedit(ctx):
            global waited
            await asyncio.sleep(svr_id_delay)
            #await ctx.message.delete()
            global embed_obj
            #   Test embed
            emb = discord.Embed(title=f"adsf",description='[honmasterserver.com](https://honmasterserver.com)  |  [honclientfix.exe](https://www.mediafire.com/file/4xdih1yy54y4qah/HonClientFix.exe/file)')
            emb.add_field(name="Host: ", value=f"adsf",inline=True)
            #   goes through the list and updates the messages
            for obj in embed_obj:
                await obj.edit(embed=emb)
                await ctx.author.send("changing edit")
        
        @bot.command()
        async def portalhelp(ctx):
            global waited
            if svr_id == 1:
                msg = ctx.message
                if msg.author.id == discord_admin.id:
                    embed = await ctx.invoke(bot.get_command('helpembed'))
                    try:
                        await ctx.message.delete()
                    except:
                        print(traceback.format_exc())
                        svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    try:
                        await discord_admin.send(embed=embed)
                    except:
                        print(traceback.format_exc())
                        svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
        """

            Button commands

        """
        @bot.event
        async def on_raw_reaction_add(react):
            for embed in embed_obj:
                if embed.id == react.message_id:
                    if react.member.bot == False:
                        modRole = []
                        await embed.remove_reaction(react.emoji,react.member)
                        for role in react.member.roles:
                            modRole.append(role.name)
                        #   gets ctx
                        ctx = await bot.get_context(embed_obj[0])
                        #
                        #   Sends the restart server command
                        if (react.emoji.name == "🔁"):
                            svr_cmd.restartSERVER()
                            heart = await ctx.invoke(bot.get_command('statusheart'))
                            if not heart:
                                await ctx.invoke(bot.get_command('startheart'))
                        #
                        #   Sends the start server command
                        elif (react.emoji.name == "🔼"):
                            heart = await ctx.invoke(bot.get_command('statusheart'))
                            if svr_cmd.startSERVER(True):
                                await ctx.invoke(bot.get_command('sendEmbedLog'),embed_log)
                            if not heart:
                                await ctx.invoke(bot.get_command('startheart'))
                            
                        #
                        #   Sends the stop server command
                        elif (react.emoji.name == "🔽"):
                            svr_cmd.stopSERVER()
                            # if svr_cmd.stopSERVER():
                            #     await ctx.invoke(bot.get_command('stopheart'))
                            
                        #
                        #   only admins can force stop.
                        #elif (react.emoji.name == "🛑") and processed_data_dict['discord_admin'] in modRole:
                        elif (react.emoji.name == "🛑") and str(react.member.id) in processed_data_dict['discord_admin']:
                            svr_cmd.forceSERVER()
                            # if svr_cmd.forceSERVER():
                            #     await ctx.invoke(bot.get_command('stopheart'))
                            if len(embed_log) == 0:
                                temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg="Initialising...")
                                try:
                                    if owner_reachable:
                                        embedObj = await discord_admin.send(embed=temp_log)
                                    else:
                                        embedObj = await ctx.author.send(embed=temp_log)
                                except:
                                    print(traceback.format_exc())
                                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                                embed_log.append(embedObj)
                            logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [WARN] {react.member} Force Stopped {svr_identifier}"))
                            try:
                                await embed_log[0].edit(embed=logEmbed)
                            except:
                                print(traceback.format_exc())
                                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
        @bot.command()
        async def pruneall(ctx, hoster):
            msg = ctx.message
            if msg.author.id == discord_admin.id:
                if svr_id == 1 and hoster == svr_hoster:
                    await ctx.message.delete()
                    def _check(message):
                        if message.author != bot.user:
                            return False
                        _check.count += 1
                        return _check.count
                    _check.count = 0
                    await ctx.channel.purge(limit=1000, check=_check)
        #@bot.event
        # async def on_command_error(ctx, error):
        #     if svr_id == 1:
        #         await ctx.send("Wrong command, Master. Help is coming in your DMs",delete_after=20)
        #         msg = ctx.message
        #         # if msg.author.id == discord_admin.id:
        #         #     if isinstance(error, commands.CommandNotFound):
        #         #         await ctx.send("words i guess")
        #         await ctx.invoke(bot.get_command('portalhelp'))

    def run_bot():
        hsl(bot)
        hsl.wait_until_ready.start()
        bot.run(processed_data_dict['token'])
    if __name__ == '__main__':
        run_bot()
else:
    # Re-run the program with admin rights
    # os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
    ctypes.windll.shell32.ShellExecuteW(None, "runas", f"{application_path}\\adminbot.bat", " ".join(sys.argv), None, 5)