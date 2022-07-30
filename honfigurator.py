import tkinter as tk
from tkinter import *
from tkinter import getboolean, ttk
import multiprocessing
import cogs.dataManager as dmgr
import configparser
import psutil
import os
import subprocess as sp
from asyncio.windows_events import NULL
import time
from os.path import exists
import shutil
from tkinter import PhotoImage
import ctypes
from tkinter import END

#
#   This changes the taskbar icon by telling windows that python is not an app but an app hoster
#   Otherwise taskbar icon will be python shell icon
myappid = 'honfiguratoricon.1.0' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
configLoc = os.path.dirname(os.path.realpath(__file__))+"\\config\\sdc.ini"


#
#
#
class initialise():
    global configLoc
    def init(self,configLoc):
        
        
        self.data = dmgr.mData(configLoc)
        self.dataDict = self.data.returnDict()

        self.nssm = self.dataDict['nssm_exe']
        self.hon_directory = self.dataDict['hon_directory']
        self.hon_game_dir = self.dataDict['hon_game_dir']
        self.sdc_home_dir = self.dataDict['sdc_home_dir']
        self.hon_logs_dir = self.dataDict['hon_logs_dir']
        self.bot_version = self.dataDict['bot_version']
        self.hon_home_dir = self.dataDict['hon_home_dir']
        self.svr_hoster = self.dataDict['svr_hoster']
        self.svr_region = self.dataDict['svr_region']
        self.svr_region_short = self.dataDict['svr_region_short']
        self.svr_id = self.dataDict['svr_id']
        self.svr_ip = self.dataDict['svr_ip']
        self.svr_total = self.dataDict['svr_total']
        self.bot_token = self.dataDict['token']
        self.pythonLoc = self.dataDict['python_location']
        self.master_user = self.dataDict['master_user']
        self.master_pass = self.dataDict['master_pass']
        self.service_name_bot = f"adminbot{self.svr_id}"
        self.service_name_api = "honserver-registration"
        if exists(f"{self.sdc_home_dir}\\config\\sdc.ini"):
            config = configparser.ConfigParser()
            config.read(f"{self.sdc_home_dir}\\config\\sdc.ini")
            self.ver_existing = config['OPTIONS']['bot_version']
            try:
                self.ver_existing = float(self.ver_existing)
            except: pass
        else:
            self.ver_existing = 0
        return

    def get_service(service_name):
        service = None
        try:
            service = psutil.win_service_get(service_name)
            service = service.as_dict()
        except Exception as ex:
            # raise psutil.NoSuchProcess if no service with such name exists
            print(f"{service_name} does not exist")
            #print(str(ex))
        return service

    def start_service(self,service_name):
        try:
            os.system(f'net start {service_name}')
        except:
            print ('could not start service {}'.format(service_name))

    def create_service_bot(self,service_name):
        sp.Popen([self.nssm, "install",service_name,"python.exe",f"sdc.py"])

    def create_service_api(self,service_name):
        sp.Popen([self.nssm, "install",service_name,f"{self.hon_directory}\\API_HON_SERVER.exe"])
        
    def configure_service(self,service_name):
        sp.Popen([self.nssm, "set",service_name,f"AppDirectory",f"{self.sdc_home_dir}"])
        time.sleep(1)
        sp.Popen([self.nssm, "set",service_name,f"AppStderr",f"{self.sdc_home_dir}\\sdc.log"])

    def parse_config(self,filename):
        svr_options = ["svr_port","svr_name","svr_location","man_port","man_startServerPort","man_endServerPort","svr_proxyLocalVoicePort","svr_proxyPort" "14235","svr_proxyRemoteVoicePort","svr_voicePortEnd" "14535","svr_voicePortStart","man_cowServerPort","man_cowVoiceProxyPort"]
        COMMENT_CHAR = '#'
        OPTION_CHAR =  ' '
        options = {}
        f = open(filename)
        for line in f:
            for i in svr_options:
                if i in line:
                    #First, remove comments:
                    # remove garbage
                    line=line.replace("SetSave ","")
                    line=line.strip(" \"0\"\n")
                    line=line.replace('"','')
                    if COMMENT_CHAR in line:
                        # split on comment char, keep only the part before
                        line, comment = line.split(COMMENT_CHAR, 1)
                    # Second, find lines with an option=value:
                    if OPTION_CHAR in line:
                        # split on option char:
                        option, value = line.split(OPTION_CHAR, 1)
                        # strip spaces:
                        option = option.strip()
                        value = value.strip()
                        # store in dictionary:
                        options[option] = value
                        print (option +": "+ value)
        f.close()
        return options

    def create_config(self,filename,serverID,serverHoster,location,svr_total,svr_ip):
        iter = self.dataDict['incr_port']
        svr_identifier = self.dataDict['svrid_total']
        print("customising startup.cfg with the following values")
        print("svr_id: " + str(serverID))
        print("svr_host: " + str(serverHoster))
        print("svr_location: " + str(location))
        print("svr_total: " + str(svr_total))
        print("svr_ip: " + str(svr_ip))
        startup = dmgr.mData.parse_config(self,os.path.dirname(os.path.realpath(__file__))+"\\config\\honfig.ini")
        networking = ["svr_port","svr_proxyLocalVoicePort","svr_proxyPort","svr_proxyRemoteVoicePort","svr_voicePortEnd","svr_voicePortStart"]
        for i in networking:
            temp_port = startup[i]
            temp_port = temp_port.strip('"')
            temp_port = int(temp_port)
            temp_port = temp_port + iter
            startup.update({i:temp_port})
        startup.update({"man_enableProxy":"true"})
        startup.update({"svr_name":serverHoster + " " + str(svr_identifier)})
        startup.update({"svr_location":location})
        startup.update({"svr_ip":svr_ip})
        startup.update({"svr_login":self.master_user})
        startup.update({"svr_password":self.master_pass})
        print (temp_port)
        dmgr.mData.setData(NULL,filename,startup)




    def configureEnvironment(self,configLoc,force_update):
        initialise.init(self,configLoc)
        self.bot_version = float(self.bot_version)
        bot_needs_update = False
        bot_first_launch = False
        #self.ver_existing = float(self.ver_existing)
        if self.bot_version > self.ver_existing: # or checkbox force is on:
            bot_needs_update = True
        
        print()
        print("==========================================")
        print("CHECKING EXISTING HON ENVIRONMENT")
        print("==========================================")

        if exists(f"{self.hon_home_dir}\\Documents"):
            os.environ["USERPROFILE"] = self.hon_home_dir
            print(f"Environment EXISTS for {self.service_name_bot}: " + (os.environ["USERPROFILE"] + "!"))

        else:
            os.makedirs(f"{self.hon_home_dir}\\Documents")
            #os.environ["USERPROFILE"] = self.hon_home_dir
            print(f"Environment requires creating for new server {self.service_name_bot}...")
            print("Created & Configured HoN environment: " + (os.environ["USERPROFILE"] + "!"))
            bot_first_launch = True

        if exists(self.hon_logs_dir):
            print("exists: " + self.hon_logs_dir)
            #   os.chdir(self.hon_logs_dir)     # not required as we're honfigurator not a bot.
        else:
            os.makedirs(self.hon_logs_dir)
            print(f"creating: {self.hon_logs_dir} ...")
            #   os.chdir(self.hon_logs_dir)     # not required as we're honfigurator not a bot.

        if not exists(self.sdc_home_dir):
            print(f"creating: {self.sdc_home_dir} ...")
            os.makedirs(self.sdc_home_dir)

        if not exists(f"{self.sdc_home_dir}\\messages"):
            print(f"creating: {self.sdc_home_dir}\\messages ...")
            os.makedirs(f"{self.sdc_home_dir}\\messages")

        if not exists(f"{self.sdc_home_dir}\\suspicious"):
            print(f"creating: {self.sdc_home_dir}\\suspicious ...")
            os.makedirs(f"{self.sdc_home_dir}\\suspicious")
        
        if not exists(f"{self.sdc_home_dir}\\config"):
            print(f"creating: {self.sdc_home_dir}\\config ...")
            os.makedirs(f"{self.sdc_home_dir}\\config")
        
        if not exists(f"{self.sdc_home_dir}\\cogs"):
            print(f"creating: {self.sdc_home_dir}\\cogs ...")
            os.makedirs(f"{self.sdc_home_dir}\\cogs")
        #
        #   Check if startup.cfg exists.
        if exists(f"{self.hon_game_dir}\\startup.cfg") and bot_first_launch != True and bot_needs_update != True and force_update != True:
            print(f"Server is already configured, checking values for {self.service_name_bot}...")
            initialise.parse_config(self,f"{self.hon_game_dir}\\startup.cfg")
        if not exists(f"{self.hon_game_dir}\\startup.cfg") or bot_first_launch == True or bot_needs_update == True or force_update == True:
        #   below commented as we are no longer using game_settings_local.cfg
        #if not exists(f"{{hon_game_dir}\\startup.cfg") or not exists(f"{self.hon_logs_dir}\\..\\game_settings_local.cfg") or bot_first_launch == True or bot_needs_update == True or force_update == True:
            if bot_needs_update:
                print("==========================================")
                print("BOT VERSION UPDATE DETECTED, APPLYING...")
                print("==========================================")
            if force_update == True:
                print("==========================================")
                print("FORCE UPDATE DETECTED, APPLYING...")
                print("==========================================")
            if not exists(f"{self.hon_game_dir}\\startup.cfg"):
            #   below commented as we are no longer using game_settings_local.cfg
            # if not exists(f"{self.hon_logs_dir}\\..\\startup.cfg") or not exists(f"{self.hon_logs_dir}\\..\\game_settings_local.cfg"):
                print(f"Server {self.service_name_bot} requires full configuration. No existing startup.cfg or game_settings_local.cfg. Configuring...")
            #   below commented as we are no longer using game_settings_local.cfg
            #initialise.create_config(self,f"{self.hon_logs_dir}\\..\\startup.cfg",f"{self.hon_logs_dir}\\..\\game_settings_local.cfg",self.svr_id,self.svr_hoster,self.svr_region,self.svr_total,self.svr_ip)
            initialise.create_config(self,f"{self.hon_game_dir}\\startup.cfg",self.svr_id,self.svr_hoster,self.svr_region,self.svr_total,self.svr_ip)
            print(f"copying {self.service_name_bot} script and related configuration files to HoN environment: "+ self.hon_home_dir + "..")
            shutil.copy(os.path.dirname(os.path.realpath(__file__))+"\\sdc.py", f'{self.sdc_home_dir}\\sdc.py')
            shutil.copy(os.path.dirname(os.path.realpath(__file__))+"\\cogs\\dataManager.py", f'{self.sdc_home_dir}\\cogs\\dataManager.py')
            shutil.copy(configLoc,f"{self.sdc_home_dir}\\config\\sdc.ini")
            #shutil.copy(os.path.dirname(os.path.realpath(__file__))+"\\config\\honfig.py",f"{self.sdc_home_dir}\\config\\honfig.py")
            print("Done!")
            print("Checking and creating required dependencies...")
            if not exists(f"{self.hon_directory}\\HON_SERVER_{self.svr_id}.exe"):
                shutil.copy(os.path.dirname(os.path.realpath(__file__))+f"\\dependencies\\server_exe\\HON_SERVER_1.exe",f"{self.hon_directory}\\HON_SERVER_{self.svr_id}.exe")
                print("copying server exe...")
            if not exists(f"{self.hon_directory}\\API_HON_SERVER.exe"):
                shutil.copy(os.path.dirname(os.path.realpath(__file__))+f"\\dependencies\\server_exe\\API_HON_SERVER.exe",f"{self.hon_directory}\\API_HON_SERVER.exe")
                print("copying master server registration API...")
            if not exists(f"{self.hon_directory}\\eko-pid.exe"):
                shutil.copy(os.path.dirname(os.path.realpath(__file__))+f"\\dependencies\\server_exe\\eko-pid.exe",f"{self.hon_directory}\\eko-pid.exe")
                print("copying other dependencies...")
            if not exists(f"{self.hon_directory}\\eko-name.exe"):
                shutil.copy(os.path.dirname(os.path.realpath(__file__))+f"\\dependencies\\server_exe\\eko-name.exe",f"{self.hon_directory}\\eko-name.exe")
            if not exists(f"{self.hon_directory}\\nssm.exe"):
                shutil.copy(os.path.dirname(os.path.realpath(__file__))+f"\\dependencies\\server_exe\\nssm.exe",f"{self.hon_directory}\\nssm.exe")
            print("Done!")
            if bot_needs_update:
                print("==========================================")
                print("BOT VERSION APPLIED.")
                print("EXISTING CONFIGURATION UPDATED!")
                print("==========================================")
            
        service_api = initialise.get_service(self.service_name_api)
        if service_api:
            print("==========================================")
            print("HON Registration API STATUS: " + self.service_name_api)
            if service_api['status'] == 'running':
                print("Windows Service RUNNING")
            else:
                print("Windows Service STARTING...")
                initialise.start_service(self,self.service_name_api)
                service_api = initialise.get_service(self.service_name_api)
                if service_api['status'] == 'running':
                    print("Windows Service now RUNNING")
                else:
                    print("SERVICE FAILED TO START!")
                print("==========================================")
        else:
            bot_needs_update = True
            print("==========================================")
            print(f"Creating hon server registration API: {self.service_name_api}..")
            print("==========================================")
            initialise.create_service_api(self,self.service_name_api)
            print("starting service.. " + self.service_name_api)
            initialise.start_service(self,self.service_name_api)
            print("==========================================")
            print("HON Registration API STATUS: " + self.service_name_api)
            service_api = initialise.get_service(self.service_name_api)
            if service_api['status'] == 'running':
                print("Windows Service RUNNING")
            else:
                print("Windows Service NOT RUNNING")
            print("==========================================")
        
        service_bot = initialise.get_service(self.service_name_bot)
        if service_bot:
            print(f"HONSERVER STATUS: {self.service_name_bot}")
            if service_bot['status'] == 'running':
                print("Windows Service RUNNING")
            else:
                print("Windows Service STARTING...")
                initialise.start_service(self,self.service_name_bot)
                service_bot = initialise.get_service(self.service_name_bot)
                if service_bot['status'] == 'running':
                    print("Windows Service now RUNNING")
                else:
                    print("SERVICE FAILED TO START!")
                print("==========================================")
        else:
            bot_needs_update = True
            print("==========================================")
            print(f"Creating adminbot: {self.service_name_bot}..")
            print("==========================================")
            initialise.create_service_bot(self,self.service_name_bot)
            time.sleep(1)
            initialise.configure_service(self,self.service_name_bot)
            initialise.start_service(self,self.service_name_bot)
            print("==========================================")
            print(f"HONSERVER STATUS: {self.service_name_bot}")
        if force_update == True or bot_first_launch == True or bot_needs_update == True:
            print("==========================================")
            print("UPDATED CONFIGURATION FILES TO VERSION: "+str(self.bot_version))
            print("==========================================")
        else:
            print("==========================================")
            print("NO UPDATES OR CONFIGURATION CHANGES MADE")
            print("==========================================")
        bot_needs_update = False

class gui():
    global configLoc
    def __init__(self):
        self.data = dmgr.mData(configLoc)
        self.dataDict = self.data.returnDict()
        print (self.dataDict)
        return
    # def getConfDict(self):
    #     self.dataDict = dmgr.mData()
    #     print (self.dataDict)
    def corecount(self):
        cores = []
        for i in range(multiprocessing.cpu_count()):
            cores.append(i+1)
        return cores
    def regions(self):
        return [["US - West","US - East","Thailand","Australia","Malaysia"],["USW","USE","TH","AUS","MY"]]

    def sendData(self,identifier,hoster, region, regionshort, serverid, servertotal,hondirectory, bottoken,discordadmin,master_user,master_pass,force_update):
        global configLoc
        #   adds a trailing slash to the end of the path if there isn't one. Required because the code breaks if a slash isn't provided
        hondirectory = os.path.join(hondirectory, '')
        if identifier == "single":
            print()
            print("==========================================")
            print(f"Selected option to configure adminbot-server{serverid}")
            print("==========================================")
            config = configparser.ConfigParser()
            if not config.has_section("OPTIONS"):
                config.add_section("OPTIONS")
                config.set("OPTIONS","bot_version",self.dataDict['bot_version'])
                config.set("OPTIONS","svr_hoster",hoster)
                config.set("OPTIONS","svr_region",region)
                config.set("OPTIONS","svr_region_short",regionshort)
                config.set("OPTIONS","svr_id",serverid)
                config.set("OPTIONS","svr_ip",self.dataDict['svr_ip'])
                config.set("OPTIONS","svr_total",servertotal)
                config.set("OPTIONS","token",bottoken)
                config.set("OPTIONS","hon_directory",hondirectory)
                config.set("OPTIONS","discord_admin",discordadmin)
                config.set("OPTIONS","master_user",master_user)
                config.set("OPTIONS","master_pass",master_pass)
            #with open(f"{self.dataDict['sdc_home_dir']}\\Config\\sdc.ini", "w") as configLoc:
            with open(configLoc, "w") as configFile:
                config.write(configFile)
            configFile.close()
            #initialise().init()
            initialise().configureEnvironment(configLoc,force_update)
        if identifier == "all":
            for i in range(0,int(servertotal)):
                serverid = i + 1
                #   need something like the below
                config = configparser.ConfigParser()
                if not config.has_section("OPTIONS"):
                    config.add_section("OPTIONS")
                    config.set("OPTIONS","bot_version",self.dataDict['bot_version'])
                    config.set("OPTIONS","svr_hoster",hoster)
                    config.set("OPTIONS","svr_region",region)
                    config.set("OPTIONS","svr_region_short",regionshort)
                    config.set("OPTIONS","svr_id",str(serverid))
                    config.set("OPTIONS","svr_ip",self.dataDict['svr_ip'])
                    config.set("OPTIONS","svr_total",servertotal)
                    config.set("OPTIONS","token",bottoken)
                    config.set("OPTIONS","hon_directory",hondirectory)
                    config.set("OPTIONS","discord_admin",discordadmin)
                    config.set("OPTIONS","master_user",master_user)
                    config.set("OPTIONS","master_pass",master_pass)
                print("updating servers: " + str(serverid))
                with open(configLoc, "w") as configFile:
                    config.write(configFile)
                configFile.close()
                #sdc.initialise()
                initialise().configureEnvironment(configLoc,force_update)
        return
    def svr_num_link(self,var,index,mode):
        if self.svr_id_var.get() == "(for single server)":
            return
        elif int(self.svr_id_var.get()) > int(self.svr_total_var.get()):
            self.svr_id_var.set(self.svr_total_var.get())
    def regions(self):
        return [["US - West","US - East","Thailand","Australia","Malaysia"],["USW","USE","TH","AUS","MY"]]
    def reg_def_link(self,var,index,mode):
        reglist = self.regions()
        svrloc = str(self.svr_loc.get()).lower()
        #svrid = str(self.svr_reg_code.get()).lower()
        for reg in reglist[0]:
            if svrloc == reg.lower():
                self.svr_loc.set(reglist[0][reglist[0].index(reg)])
                self.svr_reg_code.set(reglist[1][reglist[0].index(reg)])
    def testfunc(self):
        print(self.forceupdate.get())
    def creategui(self):
        app = tk.Tk()
        applet = ttk
        app.title("HoNfigurator")
        #   importing icon
        honico = PhotoImage(file = os.path.dirname(os.path.realpath(__file__))+f"\\honico.png")
        app.iconphoto(False, honico) 
        honlogo = PhotoImage(file = os.path.dirname(os.path.realpath(__file__))+f"\\logo.png")
        #colors
        maincolor = '#14283A'
        titlecolor = 'black'
        textbox = "#152035"
        textcolor = 'white'
        bordercolor = '#48505D'
        buttoncolorselect = "#782424"
        buttoncolor = '#4F1818'
        style= ttk.Style()
        style.theme_use('clam')
        #selectbackground, selectforeground
        style.configure("TCombobox", fieldbackground= textbox, background= maincolor,lightcolor=bordercolor,bordercolor=bordercolor,darkcolor=bordercolor)
        style.configure('TEntry', fieldbackground= textbox, background= maincolor,lightcolor=bordercolor,bordercolor=bordercolor,darkcolor=bordercolor)
        #
        #Checkbutton style options
        #   background, compound, foreground, indicatorbackground, indicatorcolor, indicatormargin, indicatorrelief, padding
        #   states
        #   active, alternate, disabled, pressed, selected, readonly.
        style.configure("TCheckbutton", background= maincolor,indicatorcolor=maincolor)
        style.map('TCheckbutton', background=[('active',maincolor)])
        #   styling colors
        #   background, bordercolor, darkcolor, foreground, highlightcolor, lightcolor
        #   anchor, compound, font, highlightthickness, padding, relief, sihftrelief, width
        #   state
        #   active, disabled, pressed, readonly.
        style.configure('TButton', background=buttoncolor,foreground='white',lightcolor=bordercolor,bordercolor=bordercolor,darkcolor=bordercolor)
        style.map('TButton', background=[('active',buttoncolorselect)])
        gui = tk.Frame(app,bg=maincolor,padx=10,pady=10)
        app.configure(bg=maincolor)
        gui.grid()
        #   title
        logolabel = applet.Label(gui, text="HoNfigurator",background=maincolor,foreground='white',image=honlogo)
        logolabel.grid(columnspan=5,column=0, row=0,sticky="n",pady=[0,20])
        #logolabel.image(honlogo)
        #   Server data
        applet.Label(gui, text="Server Data:",background=maincolor,foreground='white').grid(columnspan=1,column=0, row=1)
        #   hoster
        applet.Label(gui, text="Hoster:",background=maincolor,foreground='white').grid(column=0, row=2,sticky="e")
        hosterd = applet.Entry(gui,foreground=textcolor)
        hosterd.insert(0,self.dataDict['svr_hoster'])
        hosterd.grid(column= 1 , row = 2,sticky="w",pady=4)
        
        #
        #   region
        self.svr_loc = tk.StringVar(app,self.dataDict["svr_region"])
        applet.Label(gui, text="Location:",background=maincolor,foreground='white').grid(column=0, row=3,sticky="e")
        regiond = applet.Combobox(gui,foreground=textcolor,value=self.regions()[0],textvariable=self.svr_loc)
        regiond.grid(column= 1 , row = 3,sticky="w",pady=4)
        self.svr_loc.trace_add('write', self.reg_def_link)
        #   regionId
        self.svr_reg_code = tk.StringVar(app,self.dataDict["svr_region_short"])
        applet.Label(gui, text="Region Code:",background=maincolor,foreground='white').grid(column=0, row=4,sticky="e")
        regionsd = applet.Combobox(gui,foreground=textcolor,value=self.regions()[1],textvariable=self.svr_reg_code)
        regionsd.grid(column= 1 , row = 4,sticky="w",pady=4)
        self.svr_reg_code.trace_add('write', self.reg_def_link)
        #   server id
        self.svr_id_var = tk.StringVar(app,self.dataDict['svr_id'])
        applet.Label(gui, text="Server ID:",background=maincolor,foreground='white').grid(column=0, row=5,sticky="e")
        serveridd = applet.Combobox(gui,foreground=textcolor,value=self.corecount(),textvariable=self.svr_id_var)
        serveridd.grid(column= 1 , row = 5,sticky="w",pady=4)
        self.svr_id_var.trace_add('write', self.svr_num_link)
        #   server total    
        self.svr_total_var = tk.StringVar(app,self.dataDict['svr_total'])
        applet.Label(gui, text="Total Servers:",background=maincolor,foreground='white').grid(column=0, row=6,sticky="e")
        servertd = applet.Combobox(gui,foreground=textcolor,value=self.corecount(),textvariable=self.svr_total_var)
        servertd.grid(column= 1 , row = 6,sticky="w",pady=4)
        self.svr_total_var.trace_add('write', self.svr_num_link)
        #   token
        applet.Label(gui, text="Force Update:",background=maincolor,foreground='white').grid(column=0, row=7,sticky="e",padx=[20,0])
        self.forceupdate = tk.BooleanVar(app)
        botbutton = applet.Checkbutton(gui,variable=self.forceupdate)
        botbutton.grid(column= 1, row = 7,sticky="w",pady=4)
        #
        #
        
        #    Setup Info
        applet.Label(gui, text="Setup Data:",background=maincolor,foreground='white').grid(columnspan=1,column=3, row=1,padx=[20,0])
        #   HoN Directory
        applet.Label(gui, text="HoN Directory:",background=maincolor,foreground='white').grid(column=3, row=2,sticky="e",padx=[20,0])
        hondird = applet.Entry(gui,foreground=textcolor,width=45)
        hondird.insert(0,self.dataDict['hon_directory'])
        hondird.grid(column= 4, row = 2,sticky="w",pady=4)
        #   discord admin
        applet.Label(gui, text="Discord Admin Role/s:",background=maincolor,foreground='white').grid(column=3, row=3,sticky="e",padx=[20,0])
        discordadmin = applet.Entry(gui,foreground=textcolor,width=45)
        discordadmin.insert(0,self.dataDict['discord_admin'])
        discordadmin.grid(column= 4, row = 3,sticky="w",pady=4)
        #   token
        applet.Label(gui, text="Bot Token (SECRET):",background=maincolor,foreground='white').grid(column=3, row=4,sticky="e",padx=[20,0])
        bottokd = applet.Entry(gui,foreground=textcolor,width=45)
        bottokd.insert(0,self.dataDict['token'])
        bottokd.grid(column= 4, row = 4,sticky="w",pady=4)
            #   masterserver user
        applet.Label(gui, text="masterserver user:",background=maincolor,foreground='white').grid(column=3, row=5,sticky="e",padx=[20,0])
        masteruser = applet.Entry(gui,foreground=textcolor,width=45)
        masteruser.insert(0,self.dataDict['master_user'])
        masteruser.grid(column= 4, row = 5,sticky="w",pady=4)
        #   masterserver password
        applet.Label(gui, text="masterserver pass:",background=maincolor,foreground='white').grid(column=3, row=6,sticky="e",padx=[20,0])
        masterpass = applet.Entry(gui,foreground=textcolor,width=45)
        masterpass.insert(0,self.dataDict['master_pass'])
        masterpass.grid(column= 4, row = 6,sticky="w",pady=4)
        #   bot version
        applet.Label(gui, text="Bot Version:",background=maincolor,foreground='white').grid(column=3, row=7,sticky="e",padx=[20,0])
        botverd = applet.Label(gui,text=self.dataDict['bot_version'],background=maincolor,foreground='white').grid(column= 4, row = 7,sticky="w",pady=4)
        print(self.forceupdate.get())
        #   guilog
        #
        # guilog = tk.Text(gui,foreground=textcolor,width=55,height=4,background=textbox)
        # guilog.grid(columnspan=6,column=0,row=7,sticky="n")


        #   button
        singlebutton = applet.Button(gui, text="Configure Single Server",command=lambda: self.sendData("single",hosterd.get(),regiond.get(),regionsd.get(),serveridd.get(),servertd.get(),hondird.get(),bottokd.get(),discordadmin.get(),masteruser.get(),masterpass.get(),self.forceupdate.get()))
        singlebutton.grid(columnspan=3, column=1, row=9,stick='n',padx=[0,10],pady=[20,10])
        allbutton = applet.Button(gui, text="Configure All Servers",command=lambda: self.sendData("all",hosterd.get(),regiond.get(),regionsd.get(),serveridd.get(),servertd.get(),hondird.get(),bottokd.get(),discordadmin.get(),masteruser.get(),masterpass.get(),self.forceupdate.get()))
        allbutton.grid(columnspan=4, column=1, row=9,stick='n',padx=[10,0],pady=[20,10])
        app.mainloop()
    def hellotest(self):
        print("hello")
test = gui()
test.creategui()