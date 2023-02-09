<img align="right" width="120" height="120" style="margin-top: -15px;margin-right:20px" src="https://i.ibb.co/hZHLy2K/honico.png">


# HoNfigurator
## Overview

HoNFigurator is a GUI based HoN Server configuration and management tool.

It provides an easy way to visually deploy, manage and monitor servers with performance in mind.

Servers can be deployed as either a managed (**windows application**) or unmanaged (**windows service**).

Servers are monitored closely for changes in state, and intelligent actions are taken to increase or reduce the priority that the operating system should give to each server.

Additionally, alerts are configured to notify you when something is wrong and requires your attention.

The idea is to completely maximise the performance potential, for hosting on a variety of different hardware. And provide confidence in monitoring & management for unattended operation.

## How Does it Work?
HoNfigurator allocates an isolated directory for each server. Here, the server configuration and logs are stored.

A watchdog, called **adminbot** is created by HoNfigurator for each desired HoN Server Instance, and resides in the associated directory.

**adminbot** will run at all times, as either:
- a Windows Application, or
- a Windows Service

When deployed, **adminbot** can either start the HoN Server, or attach itself to the existing HoN Server process (if one is already running).

From here, HoN Server Logs are parsed and analysed, and the following actions are taken.
#### Performance Tweaks
- Process priority and CPU affinity is assigned appropriately to in-game or idle instances
- Restrictive modes are applied, such as dissallowing bot games.
- Crashed instances are automatically recovered
- Stuck matches / idle lobbies are terminated.

#### Alerting & Events
Discord is used as a messaging platform, so that HoNfigurator can send messages to you when something is wrong.

|  Events (no @mention) |  Alerts (@mention) |
| ------------ | ------------ |
| Server First Start  | Lag Spike of more than ``x`` seconds / last 5 min |
| Match Started | Server crashed unexpectedly |

![image](https://user-images.githubusercontent.com/82205454/217794598-8b084a09-bea4-4cee-9694-eb6ea0b22bc3.png)

> One message block is sent per server, acting as a **server companion**.  
There is only ever one message block per server, to prevent clutter.  
Message content is "edited" to prevent excess notifications.

> A dynamically built link to [ElasticSearch Monitoring](#monitoring) is included in the message

#### Monitoring
Additionally, as an optional add-on, servers can be monitored via agents deployed to collect and upload logs to ElasticSearch.
> Any HoN server can be monitored. It doesn't have to be hosted by HoNfigurator.
 
ElasticSearch is an enterprise open source data indexing tool, which includes data transformations and data analytics. With my experience in ElasticSearch and parsing data, I have been able to create beautiful dashboards to monitor your server performance and other's experience on your server.

Lag per Match             |  Player Map
:-------------------------:|:-------------------------:
![](https://user-images.githubusercontent.com/82205454/217789201-03ab77d3-3708-4c9f-afbd-690562aad501.png)  |  ![](https://user-images.githubusercontent.com/82205454/217789506-8eda9cea-b7e7-40c4-99fa-607056a8208f.png)

> Link to above: [ElasticSearch Monitoring Dashboard](https://hon-elk.honfigurator.app:5601)
> 
How-To Guide - [Monitoring Setup Guide]()

> Username and Password provided - [Contact me](https://discordapp.com/users/197967989964800000)

## Discord Integration
HoNfigurator integrates with discord by registering a **Bot Token**.

A **Bot Token** is a secret key which allows the **adminbot** watchdogs deployed by **HoNfigurator** to connect to Discord.

By connecting to Discord, each **adminbot** instance is able to send you (the owner) a rolling event log.

The event log is split into two halves, **events** and **alerts**.

|  Events |  Alerts |
| ------------ | ------------ |
| Server Starting  | Lag Spike of more than 5s / last 5 min  |
| Match Started | Server crashed unexpectedly |

- Bot owner ID (Your discord ID, 12 digit number) - [find discord ID](https://techswift.org/2020/04/22/how-to-find-your-user-id-on-discord/#:~:text=In%20any%20Discord%20server%2C%20click,to%20see%20your%20User%20ID.)
- Bot Token (Secret): Retrieve this from @FrankTheGodDamnMotherFuckenTank#8426

## How Do I Use it?
Complete the [Installation Steps](#installation) first.
1.  Open **HoNfigurator.exe**
1. Complete the **Base Settings** tab
	1. Fill in the basic server info requirements.
1. Complete the **Server Setup** tab
 	1. Decide on the total server count
 	1. Select to configure either a group of servers or all servers
1. **Server Administartion** tab
 	1. Monitor the configured servers.


## Installation
### Prerequisites
###### Server Requirements
1. Dedicated server, or a Virtual Machine with dedicated cores.
1. Minimum 1GB RAM per HoN Server
1. Windows OS.
	1. Either standard Windows Server / Windows 10-11, or
	1. Optimised Windows OS for gaming - https://atlasos.net/ (a suggestion only)
1. [Further requirements](https://github.com/Unofficial-kongor/Server-hosting/blob/main/basics/system-and-infra.md) - CPU and Network

###### Downloads
1. [Server Binaries](https://wasserver/wasserver)
	1. These files are not affiliated with HoNfigurator, however they are required to host servers.
2. [HoNfigurator Installation Script](https://raw.githubusercontent.com/frankthetank001/HoNfigurator/main/utilities/honfigurator-installer.bat) - ``Right click > save link as``

#### Install HoNfigurator
1. Copy ``HoNfigurator-Installer.bat`` to a location where HoNfigurator should be installed to. Such as ``C:\Program Files``
1. Run ``HoNfigurator-Installer.bat``
	1. This should launch an installer like below:
	![image](https://user-images.githubusercontent.com/82205454/187016190-3192a4be-b35f-48ee-992e-819db303a778.png)
	1. It may take some time to install Chocolatey.
	1. When prompted, you may opt to install a clean HoN client.	Answer (**y/n**) to the prompt.
	1. When the install is complete, HoNfigurator will open.

#### Prepare Server Files
Merge the [Server Binaries](https://wasserver/wasserver) with the **HoN Install Directory**
1. **HoN Install Directory** is either:
	1. an existing installation, or
	1. the downloaded HoN Client from the previous step.
1. Copy the following files
	1. ``wasserver\hon_x64.exe`` ``wasserver\k2_x64.dll`` ``wasserver\proxy.exe`` ``wasserver\proxymanager.exe`` >> **HoN Install Directory**
	1. ``wasserver\cgame_x64.dll`` ``wasserver\game_shared_x64.dll`` ``wasserver\game_x64.dll`` >> **HoN Install Directory\game**

#### Once HoNfigurator is open, Obtain the following information:

#### Fill in the server requirements (defaults will be remembered):
- Server host - ``(example: T4NK)``
- Location - ``(example: AUSTRALIA)``
- Region - ``(example: AU)``
- Total Servers  - ``Limited by total CPU cores``
- HoN Directory - ``Ensure you provide the correct path``
	- You must also obtain required server binaries yourself.
- Discord Owner ID - ``obtained in step 1``
- Discord Bot Token - ``obtained in step 1``
- Masterserver host - ``selectable option between two different master servers``
- Core Assignment
	- one logical core per server - ``Default``
	- two logical cores per server
	- two servers per logical core - ``for very strong CPUs only``
- Networking details
	- Starting Game Port - ``Default 10000``
	- Starting Voice Port - ``Default 10060``
	- the value to increment the port number by for each subsequent server - ``Default 1``

#### Running HoNfigurator
- ``Configure ALL servers`` button
	- Configures all servers within the ``total servers range`` with the selected settings.
- ``Configure SINGLE server``
	- Configures a single server by selected ``server ID`` with the selected settings.
- ``Update HoNfigurator``
	- Updates HoNfigurator with the latest updates from GitHub.
	- It's important to stay in the loop with the most recent updates, especially with a changing HoN environment, updates are frequently being pushed.
	- Updates will occur automatically when launching.

#### Post Configuration
- Observe the output of HoNfigurator, althought it will automatically configure windows firewall, it will advise which ports must be opened (port forward) in your network firewall.
- Updates
	- It is safe to configure servers when there are games in progress. Restarts will be scheduled if HoNfigurator detects a server ``in-game``.
- Discord
	- Invite your bot to your own discord channel. ``@FrankTheGodDamnMotherFuckenTank#8426`` can assist with this.

#### Example of full configuration below:
![Config Options](https://user-images.githubusercontent.com/82205454/187016509-54870053-4eee-483e-86ec-d3bf31904c6d.png)

To launch HoNfigurator again in the future, simply run ``HoNfigurator.exe`` from ``C:\Program Files\HoNfigurator`` or wherever you installed it to.
You may also create a shortcut to this on your desktop.
