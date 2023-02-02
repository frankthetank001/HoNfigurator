from asyncio.windows_events import NULL
from email import message
import discord
from discord.ext import commands
from os.path import exists
import os
from cogs.dataManager import mData
import cogs.server_status as srvcmd
import cogs.behemothHeart as heart
import cogs.embedManagerCog as embedMgr
import asyncio
from datetime import datetime
from random import randint
from time import sleep
import traceback
from discord.ext import tasks
import ctypes, sys
from typing import Optional
import psutil
import signal
import subprocess as sp
import time
import cogs.setupEnv as setup
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
    except Exception:
        return False
if is_admin():
    def show_exception_and_exit(exc_type, exc_value, tb):
        traceback.print_exception(exc_type, exc_value, tb)
        raw_input = input(f"Due to the above error, HoNfigurator has failed to launch. Ensure you have all dependencies installed by running {application_path}\\honfigurator-install-dependencies.bat.")
        sys.exit()
    sys.excepthook = show_exception_and_exit

    svr_cmd = srvcmd.honCMD()
    dmgr = mData()
    processed_data_dict = dmgr.returnDict()
    #   load environment, check pip packages
    packages_updated = setup.update_dependencies()
    if packages_updated:
        if packages_updated.returncode == 0:
            print("Relaunching code...")
            python = sys.executable
            os.execl(python, '"' + python + '"', *sys.argv)
        
    discver = (discord.__version__).split(".")
    intents = discord.Intents.default()
    if int(discver[0]) >= 2: intents.message_content=True
    bot = commands.Bot(command_prefix='!',case_insensitive=True,intents=intents)

    #bot.remove_command("help")
    embed_ids=[]
    embed_obj=[]
    embed_log=[]
    prev_dm = []
    dm_active_embed = []
    waited = False
    owner_reachable = True
    
    os.chdir(processed_data_dict['hon_logs_dir'])
    svr_id = processed_data_dict['svr_id']
    svr_id = int(svr_id)
    svr_id_delay = svr_id * 20
    svr_identifier = processed_data_dict['svr_identifier']
    svr_hoster = processed_data_dict['svr_hoster']
    ctypes.windll.kernel32.SetConsoleTitleW(f"adminbot{svr_id} v{processed_data_dict['bot_version']}")

    try:
        for p in psutil.process_iter():
            if processed_data_dict['app_name'] in p.name():
                current_pid = os.getpid()
                other_pid = p.pid
                if other_pid != current_pid:
                    p.kill()
    except Exception:
            print(traceback.format_exc())
            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
    if not exists(processed_data_dict['dm_discord_hist']):
        with open(processed_data_dict['dm_discord_hist'],'w'):
            pass
    if not exists(processed_data_dict['dm_discord_alert_hist']):
        with open(processed_data_dict['dm_discord_alert_hist'],'w'):
            pass
    def handler(signum, frame):
        svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"Received SIGNUM: {signum} , frame: {frame}","INFO")
        exit(1)
    signal.signal(signal.SIGINT, handler)

    # clean up previous instance, import pending configurations
    old_adminbot_exes = [f"{processed_data_dict['sdc_home_dir']}\\adminbot{svr_id}_old.exe",f"{processed_data_dict['sdc_home_dir']}\\adminbot{svr_id}_old2.exe"]
    for old_adminbot_exe in old_adminbot_exes:
        if exists(old_adminbot_exe):
            try:
                os.remove(old_adminbot_exe)
            except Exception:
                print(traceback.format_exc())
                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
    # class logging:
    class hsl():
        def __init__(self):
            self.server_status = svr_cmd.getStatus()
            return
        @bot.event
        async def on_ready():
            print(f'Online')
        async def get_msg_ctx(self):
            global embed_log
            global prev_dm
            global dm_active_embed
            # read previous message data from local file
            if not exists(processed_data_dict['dm_discord_temp']):
                return False
            embedData = open(processed_data_dict['dm_discord_temp'], 'r')
            embed_file = embedData.readlines()
            for dataLine in embed_file:
                if "-" in dataLine:
                    embedData.close()
                    os.remove(processed_data_dict['dm_discord_temp'])
                    break
                prev_msg = dataLine.split(",")
                #   channel ID
                prev_dm.append(int(prev_msg[0]))
                #   msg ID
                prev_dm.append(int(prev_msg[1]))
            embedData.close()
            #   check if there was any data in the file
            #   TODO: test if dm_roots len will ever be more than 1
            if len(prev_dm) == 0:
                return False
            #   Loads channel
            try:
                tempChannel = bot.get_channel(prev_dm[0])
                if tempChannel is None:
                    tempChannel = await bot.fetch_channel(prev_dm[0])
                #
                #   fetches message
                prev_msg = await tempChannel.fetch_message(prev_dm[1])
                prev_admin = prev_msg.channel.recipient.id
                if prev_admin != int(processed_data_dict['discord_admin']):
                    return False
                ctx = await bot.get_context(prev_msg)
                dm_active_embed.append(prev_msg)
            except discord.errors.NotFound:
                print(traceback.format_exc())
                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                print(f"Previous message not found.. clearing it from message cache")
                ctx=False
            except discord.errors.Forbidden:
                print(traceback.format_exc())
                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                print("No permissions to the previous message.. clearing message cache")
                ctx=False
            except discord.errors.HTTPException:
                print(traceback.format_exc())
                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                print(f"Most likely we are being rate limited\nResponse from last discord API request: {dm_active_embed[0]}")
                ctx=False
            except Exception:
                print(traceback.format_exc())
                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                return None
            return ctx
            
        async def send_user_msg(self,log_msg,alert):
            global embed_log
            global prev_dm
            global dm_active_embed
            send_fresh_message = False
            try:
                if len(dm_active_embed) == 0:
                    if await hsl.get_msg_ctx(self):
                        print("found previous message.")
                    else:
                        send_fresh_message = True
                if len(dm_active_embed) > 0:
                    user_embed = await embedMgr.offlineEmbedManager().embedLog(log_msg=f"[{hsl.time()}] {log_msg}",alert=alert)
                    await dm_active_embed[0].edit(embed=user_embed)
            except discord.errors.NotFound:
                print(traceback.format_exc())
                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                print(f"Previous message not found.. clearing it from message cache")
                send_fresh_message=True
            except discord.errors.Forbidden:
                print(traceback.format_exc())
                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                print("No permissions to the previous message.. clearing message cache")
                send_fresh_message=True
            except discord.errors.HTTPException:
                print(traceback.format_exc())
                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                print(f"Most likely we are being rate limited\nResponse from last discord API request: {dm_active_embed[0]}")
                return False
            except UnboundLocalError:
                print(traceback.format_exc())
                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                print("No message context found. Require new message.")
                send_fresh_message = True
            except Exception:
                print(traceback.format_exc())
                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            
            if send_fresh_message:
                try:
                    dm_active_embed.clear()
                    with open(processed_data_dict['dm_discord_temp'], 'w'):
                        pass

                    user_embed = await embedMgr.offlineEmbedManager().embedLog(log_msg=f"[{hsl.time()}] {log_msg}",alert=alert,data=processed_data_dict)
                    sent_message = await discord_admin_ctx.send(embed=user_embed)
                    dm_active_embed.append(sent_message)
                
                    #   now update the file
                    embedFile = open(processed_data_dict['dm_discord_temp'], 'w')
                    embedFile.write(str(sent_message.channel.id)+","+str(sent_message.id)+"\n")
                    embedFile.close()
                except discord.errors.Forbidden:
                        print(f"The discord bot may not be a member in your discord server. Please make sure it's invited to your discrd.")
                        return None
                except discord.errors.HTTPException:
                        print(f"Most likely we are being rate limited\nResponse from last discord API request: {sent_message}")
                        return False
                except Exception:
                    print(traceback.format_exc())
                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    return None
            if len(dm_active_embed) > 0:
                ctx = await bot.get_context(dm_active_embed[0])
                asyncio.create_task(ctx.invoke(bot.get_command('removeprevious')))
                await ctx.invoke(bot.get_command('sendEmbedLog'),embed_log=dm_active_embed)
                return ctx
            else:
                return None

        def time():
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        @tasks.loop(count=1)
        async def wait_until_ready(self):
            await bot.wait_until_ready()
            global embed_obj
            global discord_admin_ctx
            global owner_reachable

            self.server_status = svr_cmd.getStatus()
            #   loads the embed manager class
            if int(discver[0]) >= 2:
                await bot.load_extension("cogs.embedManagerCog")
                await bot.load_extension("cogs.behemothHeart")
            else:
                bot.load_extension("cogs.embedManagerCog")
                bot.load_extension("cogs.behemothHeart")
            self.embed_log=[]
            #   loads the embed_ids list for read
            global embed_ids

            rate_limited = bot.is_ws_ratelimited()

            try:
                discord_admin_ctx = await bot.fetch_user(processed_data_dict['discord_admin'])
                owner_reachable = True
                tempData = ({'discord_admin_ctx':discord_admin_ctx,'discord_admin_name':f"@{discord_admin_ctx.name}",'bot_first_run':True})
            except:
                print(f"{processed_data_dict['discord_admin']} is not reachable. Please ensure you have provided the correct owner ID and reconfigure the server instance.")
                print("The other possibility is that you have not invited the discord bot to a discord server which you are apart of.")
                owner_reachable = False
                tempData = ({'bot_first_run':True})
            svr_cmd.updateStatus(tempData)
            if len(embed_ids) > 0:
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
                                embedObj = await discord_admin_ctx.send(embed=temp_log)
                            except Exception:
                                print(traceback.format_exc())
                                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                            embed_log.append(embedObj)
                            #hsl.LastEmbedLog(embed_log)
                        logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [OK] Connected to link in: ``{str(tempGuild.name)} ({str(tempChannel.name)})``"))
                        try:
                            await embed_log[0].edit(embed=logEmbed)
                            await ctx.invoke(bot.get_command('sendEmbedLog'),embed_log)
                        except Exception:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        # await user.send("hello")
                    except discord.errors.Forbidden:
                        print("No permissions to the previous message.. clearing it from message cache")
                        try:
                            embed_ids.remove(embed)
                            embedFile = open(processed_data_dict['ch_discord_temp'], 'w')
                            for i in range(len(embed_ids)):
                                embedFile.write(str(embed_ids[i][0])+","+str(embed_ids[i][1])+","+str(embed_ids[i][2])+"\n")
                            embedFile.close()
                        except Exception:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    except discord.errors.NotFound:
                        print("Previous message not found.. clearing it from message cache")
                        try:
                            embed_ids.remove(embed)
                            embedFile = open(processed_data_dict['ch_discord_temp'], 'w')
                            for i in range(len(embed_ids)):
                                embedFile.write(str(embed_ids[i][0])+","+str(embed_ids[i][1])+","+str(embed_ids[i][2])+"\n")
                            embedFile.close()
                        except Exception:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        print("No permissions to the previous message.. clearing message cache")
                    except Exception:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            # await ctx.invoke(bot.get_command('getStatus'))
            try:
                result = srvcmd.honCMD().startSERVER("Attempting to start server as the first launch of adminbot")
                log_msg = False
                if result == True:
                    print("server started successfully")
                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"The server has started successfully.","INFO")
                    log_msg = f"[OK] Server Started successfully."
                    alert = False
                elif result == "server already started":
                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"Adminbot has hooked onto the already running server.","INFO")
                    log_msg = f"[OK] Hooked onto existing HoN Server."
                    alert=False
                elif result == "ram":
                    print("not enough free RAM to start the server.")
                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"Starting the server failed because there is not enough free RAM (1GB minimum required).","FATAL")
                    log_msg = f"``{hsl.time()}`` [ERR] Not enough free RAM or server already running."
                    alert = True
                elif result == "proxy":
                    print("Proxy port is not online.")
                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"Starting the server failed because the proxy port is not online.","FATAL")
                    log_msg = f"``{hsl.time()}`` [ERR] Game trying to start on PROXY port which isn't online."
                    alert = True
                else:
                    print("starting the server completely failed.")
                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"Starting the server failed without any way to proceed. Return code: {result}.","FATAL")
                    log_msg=f"``{hsl.time()}`` [ERR] Starting the server failed for unknown reason."
                    alert = True
                print(log_msg)
                ctx = await hsl.get_msg_ctx(self)
                if ctx:
                    await ctx.invoke(bot.get_command('sendEmbedLog'),embed_log=dm_active_embed)
                if log_msg:
                    if not ctx:
                        ctx = await hsl.send_user_msg(self,log_msg,alert)
            except Exception:
                print(traceback.format_exc())
                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")

            try:
                if len(embed_ids) > 0:
                    await ctx.invoke(bot.get_command('embedsync'), object_list=embed_obj)
                print("starting behemoth heart.")
                if ctx != None and ctx != False:
                    await ctx.invoke(bot.get_command('startheart'))
                else:
                    await heart.heartbeat.startheart(self,ctx)

            except Exception:
                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                print(traceback.format_exc())
                print("starting server in local mode.")
                await heart.heartbeat.startheart(self,None)
                
        @bot.command()
        async def sendEmbedLog(ctx,embed_log):
            await ctx.invoke(bot.get_command('getembedlog'),embed_log)
        @bot.command()
        async def showlinks(ctx,hoster):
            msg = ctx.message
            print(f"received command: {msg.content}")
            global embed_ids
            if hoster == svr_hoster or hoster == svr_identifier:
                try:
                    await ctx.message.delete()
                except Exception: pass
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
        # @bot.command()
        # async def createlinks(ctx,hoster):
        #     msg = ctx.message
        #     print(f"received command: {msg.content}")
        #     global waited
        #     global sent_embed
        #     global embed_ids
        #     if hoster == svr_identifier or hoster == svr_hoster:
        #         try:
        #             await ctx.message.delete()
        #         except Exception: pass
        #         if hoster == svr_hoster:
        #             await asyncio.sleep(svr_id_delay)
        #             waited = True
        #         try:
        #             await ctx.invoke(bot.get_command('desync'),hoster)
        #         except Exception:
        #             print(traceback.format_exc())
        #             svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
        #         try:
        #             await ctx.invoke(bot.get_command('destroylinkshere'),hoster)
        #         except Exception:
        #             print(traceback.format_exc())
        #             svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
        #         sent_embed = await ctx.invoke(bot.get_command('initiateEmbed'))
        #         #await asyncio.sleep(1)
        #         sent_embed_holder = [int(sent_embed.guild.id), int(sent_embed.channel.id),int(sent_embed.id)]
        #         for embed in embed_ids:
        #             temp_sent_embed_holder = sent_embed_holder[1]
        #             temp_embed_check = embed[1]
        #             if temp_sent_embed_holder == temp_embed_check:
        #                 embed_ids.remove(embed)
        #                 embed_ids.append(sent_embed_holder)
        #                 try:
        #                     embedFile = open(processed_data_dict['ch_discord_temp'], 'w')
        #                     for i in range(len(embed_ids)):
        #                         embedFile.write(str(embed_ids[i][0])+","+str(embed_ids[i][1])+","+str(embed_ids[i][2])+"\n")
        #                     embedFile.close()
        #                 except Exception:
        #                     print(traceback.format_exc())
        #                     svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
        #                 if len(embed_log) == 0:
        #                     temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg=f"``{hsl.time()}`` Welcome owner... :)")
        #                     try:
        #                         if owner_reachable:
        #                             embedObj = await discord_admin_ctx.send(embed=temp_log)
        #                         else:
        #                             embedObj = await ctx.author.send(embed=temp_log)
        #                     except Exception:
        #                         print(traceback.format_exc())
        #                         svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
        #                     embed_log.append(embedObj)
        #                 logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [OK] link exists and has been replaced"))
        #                 try:
        #                     await embed_log[0].edit(embed=logEmbed)
        #                 except Exception:
        #                     print(traceback.format_exc())
        #                     svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
        #                 break
                    
        #         if sent_embed_holder not in embed_ids:
        #             try:
        #                 #
        #                 #   Loads guild
        #                 tempGuild = bot.get_guild(sent_embed_holder[0])
        #                 if tempGuild is None:
        #                     tempGuild = await bot.fetch_guild(sent_embed_holder[0])
        #                 #
        #                 #   Loads channel
        #                 tempChannel = tempGuild.get_channel(sent_embed_holder[1])
        #                 if tempChannel is None:
        #                     tempChannel = await bot.fetch_channel(sent_embed_holder[1])
        #                 if len(embed_log) == 0:
        #                     temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg=f"``{hsl.time()}`` Welcome owner... :)")
        #                     try:
        #                         if owner_reachable:
        #                             embedObj = await discord_admin_ctx.send(embed=temp_log)
        #                         else:
        #                             embedObj = await ctx.author.send(embed=temp_log)
        #                     except Exception:
        #                         print(traceback.format_exc())
        #                         svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
        #                     embed_log.append(embedObj)
        #                     #hsl.LastEmbedLog(embed_log)
        #                 print(f"``{hsl.time()}`` [OK] Link successfully created in ``{tempGuild.name} ({tempChannel.name})`` by ``{ctx.author.name}``")
        #                 logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [OK] Link successfully created by ``{ctx.author.name}``"))
        #                 try:
        #                     await embed_log[0].edit(embed=logEmbed)
        #                 except Exception:
        #                     print(traceback.format_exc())
        #                     svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
        #             except Exception:
        #                 print(traceback.format_exc())
        #                 svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
        #             embed_ids.append(sent_embed_holder)
        #             embedData = open(processed_data_dict['ch_discord_temp'], 'w')
        #             for i in range(len(embed_ids)):
        #                 embedData.write(str(embed_ids[i][0])+","+str(embed_ids[i][1])+","+str(embed_ids[i][2])+"\n")   
        #             embedData.close()
        #         #await ctx.invoke(bot.get_command('createEmbed'),5)
        #         await ctx.invoke(bot.get_command('sync'),hoster)

        #         if hoster == svr_hoster:
        #             waited = False
        """

            Turns the list of embed ids from embed_ids into a list of embed objects in embed_obj
            
        """
        @bot.command()
        async def desync(ctx,hoster):
            msg = ctx.message
            print(f"received command: {msg.content}")
            global waited
            #if hoster == svr_hoster:
            try:
                await ctx.message.delete()
            except Exception: pass
            global embed_obj
            embed_obj = []

        @bot.command()
        async def sync(ctx,hoster):
            msg = ctx.message
            print(f"received command: {msg.content}")
            global waited
            global embed_obj
            global sent_embed
            if hoster == svr_hoster or hoster == svr_identifier:
                try:
                    await ctx.message.delete()
                except Exception: pass
                embed_id_list = [ctx.guild.id, ctx.channel.id]
                for embed in embed_ids:
                    try:
                        temp_sent_embed_holder = embed_id_list[1]
                        temp_embed_check = embed[1]
                        if temp_sent_embed_holder == temp_embed_check:
                            tempGuild = bot.get_guild(embed[0])
                            if tempGuild is None:
                                tempGuild = await bot.fetch_guild(embed[0])
                            #   Loads channel
                            tempChannel = tempGuild.get_channel(embed[1])
                            if tempChannel is None:
                                tempChannel = await bot.fetch_channel(embed[1])
                            #   fetches message
                            tempEmbed = await tempChannel.fetch_message(int(embed[2]))
                            embed_obj.append(tempEmbed)
                    except Exception:
                        print(traceback.format_exc())
                        svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                if len(embed_log) == 0:
                    temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg="Initialising...")
                    try:
                        if owner_reachable:
                            embedObj = await discord_admin_ctx.send(embed=temp_log)
                        else:
                            embedObj = await ctx.author.send(embed=temp_log)
                    except Exception:
                        print(traceback.format_exc())
                        svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    embed_log.append(embedObj)
                    #hsl.LastEmbedLog(embed_log)
                logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [OK] Connected to **"+str(len(embed_ids))+"** server links"))
                try:
                    await embed_log[0].edit(embed=logEmbed)
                except Exception:
                    print(traceback.format_exc())
                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                await ctx.invoke(bot.get_command('embedsync'), object_list=embed_obj)
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
            msg = ctx.message
            print(f"received command: {msg.content}")
            global waited
            if hoster == svr_hoster or hoster == svr_identifier:
                try:
                    await ctx.message.delete()
                except Exception: pass
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
                                        embedObj = await discord_admin_ctx.send(embed=temp_log)
                                    else:
                                        embedObj = await ctx.author.send(embed=temp_log)
                                except Exception:
                                    print(traceback.format_exc())
                                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                                embed_log.append(embedObj)
                                #hsl.LastEmbedLog(embed_log)
                            logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [OK] Destroyed link in: ``{str(ctx.guild.name)} ({str(tempChannel.name)})``"))
                            try:
                                await embed_log[0].edit(embed=logEmbed)
                            except Exception:
                                print(traceback.format_exc())
                                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    except discord.errors.Forbidden:
                        print("No permissions to the previous message.. clearing message cache")
                        try:
                            embed_ids.remove(embed)
                            embedFile = open(processed_data_dict['ch_discord_temp'], 'w')
                            for i in range(len(embed_ids)):
                                embedFile.write(str(embed_ids[i][0])+","+str(embed_ids[i][1])+","+str(embed_ids[i][2])+"\n")
                            embedFile.close()
                        except Exception:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        if len(embed_log) == 0:
                            temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg=f"``{hsl.time()}`` Welcome owner... :)")
                            try:
                                if owner_reachable:
                                    embedObj = await discord_admin_ctx.send(embed=temp_log)
                                else:
                                    embedObj = await ctx.author.send(embed=temp_log)
                            except Exception:
                                print(traceback.format_exc())
                                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                            embed_log.append(embedObj)
                            #hsl.LastEmbedLog(embed_log)
                        logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [WARN] No access/unknown message. Removed from cache"))
                        try:
                            await embed_log[0].edit(embed=logEmbed)
                        except Exception:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    except discord.errors.NotFound:
                        print("No permissions to the previous message.. clearing message cache")
                        try:
                            embed_ids.remove(embed)
                            embedFile = open(processed_data_dict['ch_discord_temp'], 'w')
                            for i in range(len(embed_ids)):
                                embedFile.write(str(embed_ids[i][0])+","+str(embed_ids[i][1])+","+str(embed_ids[i][2])+"\n")
                            embedFile.close()
                        except Exception:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        if len(embed_log) == 0:
                            temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg=f"``{hsl.time()}`` Welcome owner... :)")
                            try:
                                if owner_reachable:
                                    embedObj = await discord_admin_ctx.send(embed=temp_log)
                                else:
                                    embedObj = await ctx.author.send(embed=temp_log)
                            except Exception:
                                print(traceback.format_exc())
                                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                            embed_log.append(embedObj)
                            #hsl.LastEmbedLog(embed_log)
                        logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [WARN] No access/unknown message. Removed from cache"))
                        try:
                            await embed_log[0].edit(embed=logEmbed)
                        except Exception:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    except Exception:
                        print(traceback.format_exc())
                        svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                try:
                    embedFile = open(processed_data_dict['ch_discord_temp'], 'w')
                    for i in range(len(embed_ids)):
                        embedFile.write(str(embed_ids[i][0])+","+str(embed_ids[i][1])+","+str(embed_ids[i][2])+"\n")
                    embedFile.close()
                except Exception:
                    print(traceback.format_exc())
                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                # if hoster == svr_hoster:
                #     waited = False


        @bot.command()
        async def testsync(self,ctx):
            global embed_obj
            print(embed_obj)

        @bot.command()
        async def destroylinks(ctx,hoster):
            msg = ctx.message
            print(f"received command: {msg.content}")
            global waited
            global embed_obj
            global embed_ids
            if hoster == svr_hoster or hoster == svr_identifier:
                try:
                    await ctx.message.delete()
                except Exception: pass
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
                                    embedObj = await discord_admin_ctx.send(embed=temp_log)
                                else:
                                    embedObj = await ctx.author.send(embed=temp_log)
                            except Exception:
                                print(traceback.format_exc())
                                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                            embed_log.append(embedObj)
                            #hsl.LastEmbedLog(embed_log)
                        logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [OK] Destroyed link in: ``{str(tempGuild.name)} ({str(tempChannel.name)})``"))
                        try:
                            await embed_log[0].edit(embed=logEmbed)
                        except Exception:
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
                    embedData = open(processed_data_dict['ch_discord_temp'], 'w')
                    embedData.write("")   
                    embedData.close()
                    if len(embed_log) == 0:
                        temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg=f"``{hsl.time()}`` Welcome owner... :)")
                        try:
                            if owner_reachable:
                                embedObj = await discord_admin_ctx.send(embed=temp_log)
                            else:
                                embedObj = await ctx.author.send(embed=temp_log)
                        except Exception:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        embed_log.append(embedObj)
                        #hsl.LastEmbedLog(embed_log)
                    logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [OK] Deleted **"+links_deleted+"** server links"))
                    try:
                        await embed_log[0].edit(embed=logEmbed)
                    except Exception:
                        print(traceback.format_exc())
                        svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                    #await ctx.author.send(svr_identifier + f" Destroyed all links.")
                except Exception:
                    embed_obj = []
                    embed_ids = []
                    #
                    #   empties the file of messages (will need to create new links)
                    embedData = open(processed_data_dict['ch_discord_temp'], 'w')
                    embedData.write("")
                    embedData.close()
                    if len(embed_log) == 0:
                        temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg=f"``{hsl.time()}`` Welcome owner... :)")
                        try:
                            if owner_reachable:
                                embedObj = await discord_admin_ctx.send(embed=temp_log)
                            else:
                                embedObj = await ctx.author.send(embed=temp_log)
                        except Exception:
                            print(traceback.format_exc())
                            svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                        embed_log.append(embedObj)
                        #hsl.LastEmbedLog(embed_log)
                    logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [OK] Deleted **"+links_deleted+"** server links"))
                    try:
                        await embed_log[0].edit(embed=logEmbed)
                    except Exception:
                        print(traceback.format_exc())
                        svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                if hoster == svr_hoster:
                    waited = False
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
                            svr_cmd.restartSERVER(False)
                            heart = await ctx.invoke(bot.get_command('statusheart'))
                            if not heart:
                                await ctx.invoke(bot.get_command('startheart'))
                        #
                        #   Sends the start server command
                        elif (react.emoji.name == "🔼"):
                            heart = await ctx.invoke(bot.get_command('statusheart'))
                            if svr_cmd.startSERVER("Someone pressed start server in discord."):
                                await ctx.invoke(bot.get_command('sendEmbedLog'),embed_log)
                            if not heart:
                                await ctx.invoke(bot.get_command('startheart'))
                            
                        #
                        #   Sends the stop server command
                        elif (react.emoji.name == "🔽"):
                            svr_cmd.stopSERVER(False,"Graceful shutdown from discord embed")
                            
                        #
                        #   only admins can force stop.
                        elif (react.emoji.name == "🛑") and str(react.member.id) in processed_data_dict['discord_admin']:
                            svr_cmd.stopSERVER(True,"Force stopped from discord embed")
                            if len(embed_log) == 0:
                                temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg="Initialising...")
                                try:
                                    if owner_reachable:
                                        embedObj = await discord_admin_ctx.send(embed=temp_log)
                                    else:
                                        embedObj = await ctx.author.send(embed=temp_log)
                                except Exception:
                                    print(traceback.format_exc())
                                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                                embed_log.append(embedObj)
                            logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"``{hsl.time()}`` [WARN] {react.member} Force Stopped {svr_identifier}"))
                            try:
                                await embed_log[0].edit(embed=logEmbed)
                            except Exception:
                                print(traceback.format_exc())
                                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
        async def run_bot_local(self):
            try:
                print("bot started in local mode.")
                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"Starting in local mode as discord bot is disabled.","INFO")
                tempData = {'bot_first_run':True}
                svr_cmd.updateStatus(tempData)
                result = srvcmd.honCMD().startSERVER("Attempting to start server as the first launch of adminbot")
                if result == True:
                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"The server has started successfully.","INFO")
                elif result == "server already started":
                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"Adminbot has hooked onto the already running server.","INFO")
                elif result == "ram":
                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"Starting the server failed because there is not enough free RAM (1GB minimum required).","FATAL")
                elif result == "proxy":
                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"Starting the server failed because the proxy port is not online.","FATAL")
                else:
                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"Starting the server failed without any way to proceed. Return code: {result}.","FATAL")
            except Exception:
                print(traceback.format_exc())
                svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
            await heart.heartbeat.startheart(self,None)
        # def run_bot_disc(self):
        #     if processed_data_dict['disable_bot'] == 'False':
        #         hsl(bot)
        #         hsl.wait_until_ready().start
        #         bot.run(processed_data_dict['token'])
    @bot.command()
    async def removeprevious(ctx):
        global dm_active_embed
            # if svr_id == 1:
        messages_to_remove = 50
        ch_id = dm_active_embed[0].channel.id
        ch = bot.get_channel(ctx.channel.id)
        if ch == None:
            ch = bot.fetch_channel(ch_id)
        async for message in ctx.channel.history(limit=messages_to_remove):
            if message.author.id == bot.user.id and message.id != ctx.message.id:
                embed = message.embeds
                if len(embed) > 0:
                    if embed[0].title == f"{svr_identifier} Adminbot Event Log":
                        await message.delete()
                        await asyncio.sleep(0.5)
                else:
                    if "[ERROR] No message context found" in message.content:
                        await message.delete()
                        await asyncio.sleep(0.5)
    @bot.command()
    async def cleardm(ctx):
        global dm_active_embed
        msg = ctx.message
        print(f"received command: {msg.content}")
        if msg.author.id == discord_admin_ctx.id:
            if svr_id == 1:
                messages_to_remove = 9999
                async for message in ctx.history(limit=messages_to_remove):
                    if message.author.id == bot.user.id:
                        await message.delete()
                        await asyncio.sleep(0.5)
    @bot.command()
    async def pruneall(ctx, hoster):
        msg = ctx.message
        print(f"received command: {msg.content}")
        if msg.author.id == discord_admin_ctx.id:
            if svr_id == 1:
                if hoster == svr_hoster:
                    #await ctx.message.delete()
                    def _check(message):
                        if message.author != bot.user:
                            return False
                        _check.count += 1
                        return _check.count
                    _check.count = 0
                    await ctx.channel.purge(limit=1000, check=_check)
    @bot.command()
    async def portalhelp(ctx):
        msg = ctx.message
        print(f"received command: {msg.content}")
        global waited
        if svr_id == 1:
            msg = ctx.message
            if msg.author.id == discord_admin_ctx.id:
                embed = await ctx.invoke(bot.get_command('helpembed'))
                try:
                    await ctx.message.delete()
                except Exception:
                    print(traceback.format_exc())
                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
                try:
                    await discord_admin_ctx.send(embed=embed)
                except Exception:
                    print(traceback.format_exc())
                    svr_cmd.append_line_to_file(f"{processed_data_dict['app_log']}",f"{traceback.format_exc()}","WARNING")
    # @bot.event
    # async def on_command_error(ctx, error):
    #     print(f"Command: {ctx.message}\Error:{error}")
    #     if svr_id == 1:
    #         msg = ctx.message
    #         if msg.author.id == discord_admin_ctx.id:
    #             await ctx.send("Wrong command, Master. Help is coming in your DMs",delete_after=20)
    #         #     if isinstance(error, commands.CommandNotFound):
    #         #         await ctx.send("words i guess")
    #         await ctx.invoke(bot.get_command('portalhelp'))
    async def main():
        if processed_data_dict['disable_bot'] == 'True':
            await hsl().run_bot_local()
        else:
            if int(discver[0]) >= 2:
                hsl().wait_until_ready.start()
                await bot.start(processed_data_dict['token'])
            else:
                hsl().wait_until_ready.start()
                await bot.run(processed_data_dict['token'])
    if __name__ == '__main__':
        if int(discver[0]) >= 2:
            asyncio.run(main())
        else:
            if processed_data_dict['disable_bot'] == 'True':
                asyncio.run(hsl(None).run_bot_local())
            else:
                hsl().wait_until_ready.start()
                bot.run(processed_data_dict['token'])
    
else:
    # Re-run the program with admin rights
    # os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
    ctypes.windll.shell32.ShellExecuteW(None, "runas", f"{application_path}\\adminbot.bat", " ".join(sys.argv), None, 5)