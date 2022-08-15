## HoNfigurator - Server Deployment

The HoNFigurator is an application which allows for easy deployment of HON Servers.

It deploys servers in the most efficient way possible for maximum game server performance.

It is dynamic in the sense that based on the total amount of servers you require, it will create all the necessary directories and configurations without any manual intervention from the user besides providing basic server information you wish to announce to the master server.

The total number of servers supported is limited by the total number of logical processors, as the server runs best as 1 server per CPU core.

### Servers get deployed in the following mannner:
1. Open **HoNfigurator-launcher.bat** ``as Administrator``
2. Fill in the basic information requirements (defaults will be remembered):
3. Make sure your Discord ID is provided, this is the 12 digit number found by right clicking your name in the members list in discord and selecting ``Copy ID``
4. Select to deploy single or all servers.
5. Servers will automatically start and you will receive a message from your bot with the next steps.
6. Servers will be each assigned to their own CPU core, and given a ``low`` process priority unless a game is running, in which case it is set to ``realtime``

#### Example: If 2 total servers selected
This will configure and deploy 2x hon servers in the following SERVER_HOME locations: 
```
<hon_directory>\instances\hon_server_1\		= SERVER_1_HOME
<hon_directory>\instances\hon_server_2\		= SERVER_2_HOME
```
``startup.cfg`` is automatically created for each server and deployed to the appropriate "HOME" location for that HoN server.

Networking details such as the server ports will be automatically assigned based on the server number.

- server 1: ``server port 10000``
- server 2: ``server port 11000``
- etc

A list of ports will be provided at the end of deployment so you can port forward if required.

## Adminbot - Discord Integration
Upon success of creating the required directories and configurations, HoNfigurator will deploy a python discord bot ``sdc.py`` and relevant config files, to the home directory of each server.

```Example: <hon_directory>\hon_server_1\Documents\Heroes of Newerth x64\game\logs\sdc```

Windows Services will be automatically created, configured & started for each adminbot, and automatically started. There is no manual starting of servers required.
The HoN Server Registration API will also be created and started if it doesn't exist already. This registers the game server on the masterserver.

Adminbot resides in each ``SERVER_HOME`` directory, and it will act as a layer of security and monitoring for each server.

Adminbot parses game log files, looks out for sinister events, and gives real-time game status updates to discord guilds via embedded messages. The purpose of this is to provide game server security and a "window" into any running games on your servers so that it is easily visible from just looking at the discord chat where it is deployed.

### Security/Uptime/Availability Features
- [x] After a game has finished, or a lobby has been closed, server is automatically restarted.
- [x] If someone tries to start games on your server with invalid parameters (such as an invalid map/mode) this can crash your server.
		- Server restarts in this instance, and saves a log with the clients IP address for analysis so they may be blocked if required.
- [ ] Other DDOS events in the logs can be captured and also trigger an automatic server restart + automatically ban the IP in windows firewall (not on by default)

### Embedded Message Features
- [x] Links are embedded into these messages for handy things such as the honmasterserver.com website, a hon client fix that will fix client side HoN configuration and a link to a HoN Server Portal discord where all of the deployed bots will be assigned to their allocated region. This will make HoN feel alive.
- [x] "Reacts" can be used by users on discord to perform backend administration on individual game servers.
	- (🔁) Restart 		``Anyone as long as no one is connected to the server.``
	- (🔼) Start		``Anyone as long as no one is connected to the server.``
	- (🔽) Stop 		``Anyone as long as no one is connected to the server.``
	- (🛑) Force Stop	``Only allocated Discord admin roles.``
- [x] Total games played
- [x] Last restart time
- [x] In Lobby information such as (map, host, mode, spots left)
- [x] In game information such as (match in progress, elapsed time)

### How to Use
- In discord, create a channel for server status updates. This should be dedicated to use by the bot.
- Use the ``!portalhelp`` command to be sent an overview of the available commands. The commands will be customised to your set up.
- ![bothelp](https://user-images.githubusercontent.com/82205454/183851795-3bad4f0b-dca9-496f-96c3-8719dabb873e.png)
- Use the ``!createlinks <identifier>`` command  in the discord channel which you wish to receive updates in.
- Repeat the above to any other discord guilds or channels where you also want the server status displayed.
- All subscribed channels will be kept up to date with the same server status messages. And personalised event logs sent to your inbox
- ![server-status](https://user-images.githubusercontent.com/82205454/184099721-7ae4bf14-1769-46cd-8258-5f60bf93dce3.png)
- ![events](https://user-images.githubusercontent.com/82205454/184092512-5f141db7-627e-4851-a0cf-35a5ee7b4056.png)

## Installation
These are to be performed on game servers only.

### Prerequisites
Details on how to clone a repository found here: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository
1. **Clone** this github repository to a location on the server. This will be the central point where updates can be pushed out from, and where the HoNfigurator will run from.
	- ``git clone https://github.com/frankthetank001/honfigurator``
3. Install basic Hon x64 client - http://honmasterserver.com/Heroes%20of%20Newerth%20x64%20-%20CLEAN.rar
4. Move the ``Heroes of Newerth x64`` folder into ``C:\Program Files\`` or a location of your choice.
5. Install Python from ``honfigurator-main\dependencies\`` folder.
6. Run the Installer for **Python** ``as Administrator``
 	- Use the following options (IMPORTANT):
		- ``custom installation``
		- ``select option to install for all users``
		- ``Add python to path/environment variables``
		- ``disable PATH length constraints``
7. Execute **HoNfigurator-installer.bat** ``as Administrator``
	- This will install ``Python pre-requisites``. Take note of any errors.
8. Retrieve a bot token from: (Discord ID: FrankTheGodDamnMotherFuckenTank#8426)
9. Execute **HoNfigurator-launcher.bat** ``as Administrator``
10. Fill in the basic information requirements (defaults will be remembered):
	- Server host ``(example: T4NK)``
	- Location ``(example: AUSTRALIA)``
	- Region ``(example: AUS)``
	- Total Servers. ``Limited by total CPU cores``
	- Discord Admin Role ``(example: AUS Server Admins)``
	- Discord Bot Token
	- Masterserver host
	- Core Assignment
		- one logical core per server - ``Default``
		- two logical cores per server
	- ``Configure ALL servers`` button
		- Configures all servers within the ``total servers range``
	- ``Configure SINGLE server``
		- Configures single server by selected ``server ID``.
11. Example of full configuration below:
![Config Options](https://user-images.githubusercontent.com/82205454/183896906-13467995-57ba-4022-a7ff-a8df7035f296.png)
