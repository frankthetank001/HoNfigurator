# Server Monitoring
## Overview
The following covers setting up the required agents in order to have your server monitored by ElasticSearch.

Monitoring servers provides many benefits. Some of them are listed below:
- Server Performance
    - Lag (skipped server frames)
    - Network Packet Loss
    - Server CPU/RAM/Disk Usage
    - Server Network Throughput and Disk IO
- Configuration Overviews
- Player and Server location plotting
- Bandwidth Estimation requirements, based on player activity on your server.

## How Does it Work?
### Hosted by Me
[ElasticSearch](https://www.elastic.co/what-is/elasticsearch) - Data indexing engine  
[Logstash](https://www.elastic.co/guide/en/logstash/current/introduction.html) - Data loading and transformation  
[Kibana](https://www.elastic.co/guide/en/kibana/current/introduction.html) - Dashboard Design, Data Exploration and UI

### Hosted by You

[FileBeat](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-overview.html#:~:text=Filebeat%20is%20a%20lightweight%20shipper,Elasticsearch%20or%20Logstash%20for%20indexing.) - Lightweight log collecter

[MetricBeat](https://www.google.com/search?q=what+is+metricbeat&oq=what+is+metricbeat&aqs=edge..69i57j0i512l3j0i22i30i625j0i22i30j0i22i30i625l2j69i64.2892j0j4&sourceid=chrome&ie=UTF-8) - Lightweight metrics collecter

---

#### 1
- Filebeat collects and ships logs for HoN Servers.
- MetricBeat collects and ships metrics for server statisics (CPU, RAM, NETWORK, IO)
- The data is sent to LogStash (hosted by me)

#### 2
- Logstash analyses, transforms (mutates and filters) the data
- Then sends it to ElasticSearch for indexing.

### 3
- Kibana aggregates the data, creating views, graphs and other pretty things.
- This is what everyone uses to monitor the servers.

## Setup
The setup is simple. Estimated setup time is 5 minutes.

1. Download the [install beats](https://honfigurator.app/install-beats.bat) script
    - This will download and install ``FileBeat`` & ``MetricBeat``
1. Run the file ``install-beats.bat`` from anywhere
1. Observe the output:
    - You will be asked to provide the generated  [Certificate Signing Request](https://www.globalsign.com/en/blog/what-is-a-certificate-signing-request-csr) - ``client.csr`` to me.  
      You can [contact me on Discord](https://discordapp.com/users/197967989964800000) to send me the file.
    - I will provide the ``client.pem`` file requested by the script.
1. Copy the ``client.pem`` file where the script has asked you to place it.
1. Once done, press enter on the script window to finalise the installation.

> **Note** A ``CSR`` (client.csr) is required to receive a ``certificate`` (client.pem), which is used for establishing encrypted communications between two endpoints.  
This is how your server talks securely to mine.

## Start Monitoring!
Visit [HoN ElasticSearch Server Monitoring](https://hon-elk.honfigurator.app:5601)  
> Username: ``readonly``  
Password: ``Provided by me``

Start observing the fascination dashboards.

## Screenshots
