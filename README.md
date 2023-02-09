<img align="right" width="120" height="120" style="margin-top: -15px;margin-right:20px" src="https://i.ibb.co/hZHLy2K/honico.png">

# HoNfigurator
<details>
<summary>Table of Contents</summary>

- [Overview](#overview)
- [How Does it Work?](#how-does-it-work)
  * [Performance Tweaks](#performance-tweaks)
  * [Alerting & Events](#alerting--events)
- [Monitoring](#monitoring)
- [How Do I Use it?](#how-do-i-use-it)
- [Installation](#installation)
  * [Prerequisites](#prerequisites)
    + [Server Requirements](#server-requirements)
    + [Downloads](#downloads)
  * [Install HoNfigurator](#install-honfigurator)
  * [Prepare Server Files](#prepare-server-files)
  * [Configure and Start Servers](#configure-and-start-servers)

</details>

---
## Overview

HoNFigurator is a GUI based HoN Server configuration and management tool.

It provides an easy way to visually deploy, manage and monitor servers with performance in mind.

Servers can be deployed as either a managed (**windows application**) or unmanaged (**windows service**).

Servers are monitored closely for changes in state, and intelligent actions are taken to increase or reduce the priority that the operating system should give to each server.

Additionally, alerts are configured to notify you when something is wrong and requires your attention.

The idea is to completely maximise the performance potential, for hosting on a variety of different hardware. And provide confidence in monitoring & management for unattended operation.

---
## How Does it Work?
HoNfigurator allocates an isolated directory for each server. Here, the server configuration and logs are stored.

A watchdog, called **adminbot** is created by HoNfigurator for each desired HoN Server Instance, and resides in the associated directory.

**adminbot** will run at all times, as either:
- a Windows Application, or
- a Windows Service

When deployed, **adminbot** can either start the HoN Server, or attach itself to the existing HoN Server process (if one is already running).

From here, HoN Server Logs are parsed and analysed, and the following actions are taken.

### Performance Tweaks
- Process priority and CPU affinity is assigned appropriately to in-game or idle instances
- Restrictive modes are applied, such as dissallowing bot games.
- Crashed instances are automatically recovered
- Stuck matches / idle lobbies are terminated.

### Alerting & Events
Discord is used as a messaging platform, so that HoNfigurator can send messages to you when something is wrong.

|  Events (no @mention) |  Alerts (@mention) |
| ------------ | ------------ |
| Server First Start  | Lag Spike of more than ``x`` seconds / last 5 min |
| Match Started | Server crashed unexpectedly |

Each server will be accompanied by a **server companion** which will send you messages tracking events and alerts.

The **server companion** is careful not to spam you with notifications. It will only notify on alerts and first time setup.

Existing messages will be edited, to reduce clutter.

<details>
<summary>Click to see images</summary>

![image](https://user-images.githubusercontent.com/82205454/217794598-8b084a09-bea4-4cee-9694-eb6ea0b22bc3.png)

> A dynamically built link to [ElasticSearch Monitoring](#monitoring) is included in the message
</details>

---
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
#### Server Requirements
1. Dedicated server, or a Virtual Machine with dedicated cores.
1. Minimum 1GB RAM per HoN Server
1. Windows OS.
	- Either standard Windows Server / Windows 10-11, or
	- Optimised Windows OS for gaming - https://atlasos.net/
		> **Note** A suggestion only.
1. [Further requirements](https://github.com/Unofficial-kongor/Server-hosting/blob/main/basics/system-and-infra.md) - CPU and Network

#### Downloads
1. [Server Binaries](https://github.com/wasserver/wasserver)
	> **Warning** these files are not affiliated with HoNfigurator, however they are required to host servers.
2. [HoNfigurator Installation Script](https://raw.githubusercontent.com/frankthetank001/HoNfigurator/main/utilities/honfigurator-installer.bat) - ``Right click > save link as``

### Install HoNfigurator
1. Copy ``HoNfigurator-Installer.bat`` to a location where HoNfigurator should be installed to. Such as ``C:\Program Files``
1. Run ``HoNfigurator-Installer.bat``
1. This should launch an installer like below:
	![image](https://user-images.githubusercontent.com/82205454/187016190-3192a4be-b35f-48ee-992e-819db303a778.png)  
	It may take some time to install Chocolatey.
1. When prompted, you may opt to install a clean HoN client.
	- Answer ``y/n`` to the prompt.

> When the install is complete, HoNfigurator will open.  
if there are any issues, please [Contact me](https://discordapp.com/users/197967989964800000)

### Prepare Server Files
Merge the [Server Binaries](https://wasserver/wasserver) with the ``HoN Install Directory``
1. ``HoN Install Directory`` is either:
	- an existing installation, or
	- the downloaded HoN Client from the previous step.
1. Copy the following files
	- ``wasserver\hon_x64.exe`` ``wasserver\k2_x64.dll`` ``wasserver\proxy.exe`` ``wasserver\proxymanager.exe`` >> ``HoN Install Directory``
	- ``wasserver\cgame_x64.dll`` ``wasserver\game_shared_x64.dll`` ``wasserver\game_x64.dll`` >> ``HoN Install Directory\game``

### Configure and Start Servers
You are ready to go!

Please see [How Do I Use it?](#how-do-i-use-it) for steps on configuring and starting servers.

---
## Monitoring
As an optional add-on, servers can be monitored via agents deployed to collect and upload logs to ElasticSearch.
> How-To Guide - [Monitoring Setup Guide](docs/elasticsearch-monitoring-setup.md)

> **Note** any HoN server can be monitored. It doesn't have to be hosted by HoNfigurator.  

ElasticSearch is an enterprise open source data indexing tool, which includes data transformations and data analytics. With my experience in ElasticSearch and parsing data, I have been able to create beautiful dashboards to monitor your server performance and other's experience on your server.

Lag per Match             |  Player Map
:-------------------------:|:-------------------------:
![](https://user-images.githubusercontent.com/82205454/217789201-03ab77d3-3708-4c9f-afbd-690562aad501.png)  |  ![](https://user-images.githubusercontent.com/82205454/217789506-8eda9cea-b7e7-40c4-99fa-607056a8208f.png)

> Link to above: [ElasticSearch Monitoring Dashboard](https://hon-elk.honfigurator.app:5601)  
Username and Password provided - [Contact me](https://discordapp.com/users/197967989964800000)

---
## Epilogue

[Contact me on Discord](https://discordapp.com/users/197967989964800000) • [Issues and Feature Requests](https://github.com/frankthetank001/HoNfigurator/issues)

<img align="right" width="80" height="80" style="margin-top: -15px;margin-right:20px" src="https://i.ibb.co/K0Pw9kg/botmatch.png">
<!-- ![](https://i.ibb.co/K0Pw9kg/botmatch.png) -->

---
