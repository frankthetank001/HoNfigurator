from email import message
import discord
from discord.ext import commands
from os.path import exists
import os
from cogs.dataManager import mData
import cogs.server_status as srvcmd
import asyncio
from datetime import datetime
from random import randint
from time import sleep
import traceback

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

svr_id = processed_data_dict['svr_id']
svr_id = int(svr_id)
svr_id_delay = svr_id * 20
#svr_id_delay = 0
svr_identifier = processed_data_dict['svr_identifier']
svr_hoster = processed_data_dict['svr_hoster']

os.environ["USERPROFILE"] = processed_data_dict['hon_home_dir']
os.chdir(processed_data_dict['hon_logs_dir'])

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
    @bot.event
    async def on_ready():
        global embed_obj
        global discord_admin
        discord_admin = await bot.fetch_user(processed_data_dict['discord_admin'])
        tempData = ({'discord_admin_name':f"@{discord_admin.name}"})
        svr_cmd.updateStatus(tempData)
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
                    except: print(traceback.format_exc())
                    embed_log.append(embedObj)
                    #hsl.LastEmbedLog(embed_log)
                logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"[OK] Connected to link in: ``{str(tempGuild.name)} ({str(tempChannel.name)})``"))
                try:
                    await embed_log[0].edit(embed=logEmbed)
                    await ctx.invoke(bot.get_command('sendEmbedLog'),embed_log)
                except: print(traceback.format_exc())
                # await user.send("hello")
            except discord.errors.Forbidden:
                print("No permissions to the previous message.. clearing it from message cache")
                try:
                    embed_ids.remove(embed)
                    embedFile = open(processed_data_dict['discord_temp'], 'w')
                    for i in range(len(embed_ids)):
                        embedFile.write(str(embed_ids[i][0])+","+str(embed_ids[i][1])+","+str(embed_ids[i][2])+"\n")
                    embedFile.close()
                except: print(traceback.format_exc())
            except discord.errors.NotFound:
                print("Previous message not found.. clearing it from message cache")
                try:
                    embed_ids.remove(embed)
                    embedFile = open(processed_data_dict['discord_temp'], 'w')
                    for i in range(len(embed_ids)):
                        embedFile.write(str(embed_ids[i][0])+","+str(embed_ids[i][1])+","+str(embed_ids[i][2])+"\n")
                    embedFile.close()
                except: print(traceback.format_exc())
                print("No permissions to the previous message.. clearing message cache")
            except: print(traceback.format_exc())
        # await ctx.invoke(bot.get_command('getStatus'))
        try:
            result = srvcmd.honCMD().startSERVER()
            if result == True:
                if len(embed_log) == 0:
                    temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg="Welcome owner... :)" + "``"+hsl.time()+"``")
                    try:
                        if owner_reachable:
                            embedObj = await discord_admin.send(embed=temp_log)
                        else:
                            embedObj = await ctx.author.send(embed=temp_log)
                    except: print(traceback.format_exc())
                    embed_log.append(embedObj)
                    #hsl.LastEmbedLog(embed_log)
                logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"[OK] Server Started."))
                try:
                    await embed_log[0].edit(embed=logEmbed)
                except: print(traceback.format_exc())
            elif result == False:
                if len(embed_log) == 0:
                    temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg="Welcome owner... :)" + "``"+hsl.time()+"``")
                    try:
                        if owner_reachable:
                            embedObj = await discord_admin.send(embed=temp_log)
                        else:
                            embedObj = await ctx.author.send(embed=temp_log)
                    except: print(traceback.format_exc())
                    embed_log.append(embedObj)
                    #hsl.LastEmbedLog(embed_log)
                logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"[ERR] Not enough free RAM or server already running."))
                try:
                    await embed_log[0].edit(embed=logEmbed)
                except: print(traceback.format_exc())
        except: print(traceback.format_exc())
        try:
            await ctx.invoke(bot.get_command('embedsync'), object_list=embed_obj)
            await ctx.invoke(bot.get_command('startheart'))
        except UnboundLocalError:
            temp_log = f"[ERROR] No message context found, please run ``!createlinks {svr_identifier}`` in your discord channel.\nUse the !portalhelp command for a full list of commands."
            try:
                await discord_admin.send(temp_log)
            except discord.errors.Forbidden:
                print("Owner is not reachable. We will message the person to send me a command then.")
                owner_reachable = False
            except: print(traceback.format_exc())
            print(traceback.format_exc())
            
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
            except: print(traceback.format_exc())
            try:
                await ctx.invoke(bot.get_command('destroylinkshere'),hoster)
            except: print(traceback.format_exc())
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
                    except: print(traceback.format_exc())
                    if len(embed_log) == 0:
                        temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg="Welcome owner... :)" + "``"+hsl.time()+"``")
                        try:
                            if owner_reachable:
                                embedObj = await discord_admin.send(embed=temp_log)
                            else:
                                embedObj = await ctx.author.send(embed=temp_log)
                        except: print(traceback.format_exc())
                        embed_log.append(embedObj)
                    logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=("[OK] link exists and has been replaced"))
                    try:
                        await embed_log[0].edit(embed=logEmbed)
                    except: print(traceback.format_exc())
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
                        temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg="Welcome owner... :)" + "``"+hsl.time()+"``")
                        try:
                            if owner_reachable:
                                embedObj = await discord_admin.send(embed=temp_log)
                            else:
                                embedObj = await ctx.author.send(embed=temp_log)
                        except: print(traceback.format_exc())
                        embed_log.append(embedObj)
                        #hsl.LastEmbedLog(embed_log)
                    logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"[OK] Link successfully created in ``{tempGuild} ({tempChannel})`` by ``{ctx.author}``"))
                    try:
                        await embed_log[0].edit(embed=logEmbed)
                    except: print(traceback.format_exc())
                except: print(traceback.format_exc())
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
                        print("guild")
                        print(str(tempGuild))
                        #
                        #   Loads channel
                        tempChannel = tempGuild.get_channel(embed[1])
                        if tempChannel is None:
                            tempChannel = await bot.fetch_channel(embed[1])
                        print("channel")
                        #print(str(tempChannel))
                        #
                        #   fetches message
                        tempEmbed = await tempChannel.fetch_message(int(embed[2]))
                        embed_obj.append(tempEmbed)
                except: print(traceback.format_exc())
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
                    except: print(traceback.format_exc())
                    if len(embed_log) == 0:
                        temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg="Welcome owner... :)" + "``"+hsl.time()+"``")
                        try:
                            if owner_reachable:
                                embedObj = await discord_admin.send(embed=temp_log)
                            else:
                                embedObj = await ctx.author.send(embed=temp_log)
                        except: print(traceback.format_exc())
                        embed_log.append(embedObj)
                        #hsl.LastEmbedLog(embed_log)
                    logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"[WARN] No access/unknown message. Removed from cache"))
                    try:
                        await embed_log[0].edit(embed=logEmbed)
                    except: print(traceback.format_exc())
                #await ctx.author.send(svr_identifier + f" Connected to link in: ``{str(tempGuild.name)} ({str(tempChannel.name)})``")
                if len(embed_log) == 0:
                    temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg="Initialising...")
                    try:
                        if owner_reachable:
                            embedObj = await discord_admin.send(embed=temp_log)
                        else:
                            embedObj = await ctx.author.send(embed=temp_log)
                    except: print(traceback.format_exc())
                    embed_log.append(embedObj)
                    #hsl.LastEmbedLog(embed_log)
                logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"[OK] Connected to link in: ``{str(tempGuild.name)} ({str(tempChannel.name)})``"))
                try:
                    await embed_log[0].edit(embed=logEmbed)
                except: print(traceback.format_exc())
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
                except: print(traceback.format_exc())
                embed_log.append(embedObj)
                #hsl.LastEmbedLog(embed_log)
            logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=("[OK] Connected to **"+str(len(embed_ids))+"** server links"))
            try:
                await embed_log[0].edit(embed=logEmbed)
            except: print(traceback.format_exc())
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
            #         except: print(traceback.format_exc())
            #         embed_log.append(embedObj)
            #         #hsl.LastEmbedLog(embed_log)
            #     logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=("[OK] Links are already synced"))
            #     try:
            #         await embed_log[0].edit(embed=logEmbed)
            #     except: print(traceback.format_exc())
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
                        print("guild")
                        print(str(tempGuild))
                        #
                        #   Loads channel
                        tempChannel = tempGuild.get_channel(embed[1])
                        if tempChannel is None:
                            tempChannel = await bot.fetch_channel(embed[1])
                        print("channel")
                        #print(str(tempChannel))
                        #
                        #   fetches message
                        tempEmbed = await tempChannel.fetch_message(int(embed[2]))
                        embed_ids.remove(embed)
                        if tempEmbed in embed_obj:
                            embed_obj.remove(tempEmbed)
                        await tempEmbed.delete()
                        if len(embed_log) == 0:
                            temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg="Welcome owner... :)" + "``"+hsl.time()+"``")
                            try:
                                if owner_reachable:
                                    embedObj = await discord_admin.send(embed=temp_log)
                                else:
                                    embedObj = await ctx.author.send(embed=temp_log)
                            except: print(traceback.format_exc())
                            embed_log.append(embedObj)
                            #hsl.LastEmbedLog(embed_log)
                        logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"[OK] Destroyed link in: ``{str(ctx.guild.name)} ({str(tempChannel.name)})``"))
                        try:
                            await embed_log[0].edit(embed=logEmbed)
                        except: print(traceback.format_exc())
                except discord.errors.Forbidden:
                    print("No permissions to the previous message.. clearing message cache")
                    try:
                        embed_ids.remove(embed)
                        embedFile = open(processed_data_dict['discord_temp'], 'w')
                        for i in range(len(embed_ids)):
                            embedFile.write(str(embed_ids[i][0])+","+str(embed_ids[i][1])+","+str(embed_ids[i][2])+"\n")
                        embedFile.close()
                    except: print(traceback.format_exc())
                    if len(embed_log) == 0:
                        temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg="Welcome owner... :)" + "``"+hsl.time()+"``")
                        try:
                            if owner_reachable:
                                embedObj = await discord_admin.send(embed=temp_log)
                            else:
                                embedObj = await ctx.author.send(embed=temp_log)
                        except: print(traceback.format_exc())
                        embed_log.append(embedObj)
                        #hsl.LastEmbedLog(embed_log)
                    logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"[WARN] No access/unknown message. Removed from cache"))
                    try:
                        await embed_log[0].edit(embed=logEmbed)
                    except: print(traceback.format_exc())
                except discord.errors.NotFound:
                    print("No permissions to the previous message.. clearing message cache")
                    try:
                        embed_ids.remove(embed)
                        embedFile = open(processed_data_dict['discord_temp'], 'w')
                        for i in range(len(embed_ids)):
                            embedFile.write(str(embed_ids[i][0])+","+str(embed_ids[i][1])+","+str(embed_ids[i][2])+"\n")
                        embedFile.close()
                    except: print(traceback.format_exc())
                    if len(embed_log) == 0:
                        temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg="Welcome owner... :)" + "``"+hsl.time()+"``")
                        try:
                            if owner_reachable:
                                embedObj = await discord_admin.send(embed=temp_log)
                            else:
                                embedObj = await ctx.author.send(embed=temp_log)
                        except: print(traceback.format_exc())
                        embed_log.append(embedObj)
                        #hsl.LastEmbedLog(embed_log)
                    logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"[WARN] No access/unknown message. Removed from cache"))
                    try:
                        await embed_log[0].edit(embed=logEmbed)
                    except: print(traceback.format_exc())
                except: print(traceback.format_exc())
            try:
                embedFile = open(processed_data_dict['discord_temp'], 'w')
                for i in range(len(embed_ids)):
                    embedFile.write(str(embed_ids[i][0])+","+str(embed_ids[i][1])+","+str(embed_ids[i][2])+"\n")
                embedFile.close()
            except: print(traceback.format_exc())
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
                        temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg="Welcome owner... :)" + "``"+hsl.time()+"``")
                        try:
                            if owner_reachable:
                                embedObj = await discord_admin.send(embed=temp_log)
                            else:
                                embedObj = await ctx.author.send(embed=temp_log)
                        except: print(traceback.format_exc())
                        embed_log.append(embedObj)
                        #hsl.LastEmbedLog(embed_log)
                    logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"[OK] Destroyed link in: ``{str(tempGuild.name)} ({str(tempChannel.name)})``"))
                    try:
                        await embed_log[0].edit(embed=logEmbed)
                    except: print(traceback.format_exc())
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
                    temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg="Welcome owner... :)" + "``"+hsl.time()+"``")
                    try:
                        if owner_reachable:
                            embedObj = await discord_admin.send(embed=temp_log)
                        else:
                            embedObj = await ctx.author.send(embed=temp_log)
                    except: print(traceback.format_exc())
                    embed_log.append(embedObj)
                    #hsl.LastEmbedLog(embed_log)
                logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"[OK] Deleted **"+links_deleted+"** server links"))
                try:
                    await embed_log[0].edit(embed=logEmbed)
                except: print(traceback.format_exc())
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
                    temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg="Welcome owner... :)" + "``"+hsl.time()+"``")
                    try:
                        if owner_reachable:
                            embedObj = await discord_admin.send(embed=temp_log)
                        else:
                            embedObj = await ctx.author.send(embed=temp_log)
                    except: print(traceback.format_exc())
                    embed_log.append(embedObj)
                    #hsl.LastEmbedLog(embed_log)
                logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"[OK] Deleted **"+links_deleted+"** server links"))
                try:
                    await embed_log[0].edit(embed=logEmbed)
                except: print(traceback.format_exc())
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
            embed = await ctx.invoke(bot.get_command('helpembed'))
            try:
                await ctx.message.delete()
            except: print(traceback.format_exc())
            try:
                await discord_admin.send(embed=embed)
            except: print(traceback.format_exc())
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
                        if svr_cmd.startSERVER():
                            await ctx.invoke(bot.get_command('sendEmbedLog'),embed_log)
                        if not heart:
                            await ctx.invoke(bot.get_command('startheart'))
                        
                    #
                    #   Sends the stop server command
                    elif (react.emoji.name == "🔽"):
                        if svr_cmd.stopSERVER():
                            await ctx.invoke(bot.get_command('stopheart'))
                        
                    #
                    #   only admins can force stop.
                    #elif (react.emoji.name == "🛑") and processed_data_dict['discord_admin'] in modRole:
                    elif (react.emoji.name == "🛑") and str(react.member.id) in processed_data_dict['discord_admin']:
                        if svr_cmd.forceSERVER():
                            await ctx.invoke(bot.get_command('stopheart'))
                        if len(embed_log) == 0:
                            temp_log = await ctx.invoke(bot.get_command('embedLog'), log_msg="Initialising...")
                            try:
                                if owner_reachable:
                                    embedObj = await discord_admin.send(embed=temp_log)
                                else:
                                    embedObj = await ctx.author.send(embed=temp_log)
                            except: print(traceback.format_exc())
                            embed_log.append(embedObj)
                        logEmbed = await ctx.invoke(bot.get_command('embedLog'), log_msg=(f"[WARN] {react.member} Force Stopped {svr_identifier}"))
                        try:
                            await embed_log[0].edit(embed=logEmbed)
                        except: print(traceback.format_exc())
def run_bot():
    hsl(bot)
    bot.run(processed_data_dict['token'])
if __name__ == '__main__':
    run_bot()