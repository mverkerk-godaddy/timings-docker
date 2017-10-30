# timings-docker

Docker support for the node/express based **TIMINGS API**. See more here: [https://github.com/godaddy/timings](https://github.com/godaddy/timings).

We **HIGHLY** recommend running the TIMINGS API along with ElasticSearch and Kibana in a containerized environment! This repo has everything you need to get this setup!

## Installation

Rcommendations:

- Linux based OS such as Centos 7

- Min. 8GB memory

### Step 1. Clone this repo

Clone this repo to a folder of your choice:

```shell
$ git clone git@github.com/godaddy/timings-docker.git
Cloning into 'timings-docker'...
...
...

$ cd timings-docker
```

### Step 2. Run docker-compose

You can start up the multi-container environments like this:

```shell
$ docker-compose up
Starting elasticsearch ...
Starting elasticsearch ... done
Starting kibana ...
Starting kibana ... done
Starting timings ...
Starting timings ... done
Attaching to elasticsearch, kibana, timings
timings          | wait-for-it.sh: waiting 30 seconds for elasticsearch:9200
elasticsearch    | [2017-10-30T22:59:12,238][INFO ][o.e.n.Node               ] [] initializing ...
...
```

Notice that the timings service first runs the `wait-for-it.sh` script. This ensures that the timings service waits (up to 30 secs) for elasticsearch to start!

The following line in the output indicates that the timings service is up and running:

```shell
...
timings          | debug: TIMINGS API [prod] is running on port 80
...
```

### Step 3. Test the apps

After the containers have started, you can test the apps by browsing to the following:

|App|Link|
|-|-|
|timings|http://your_server
|ElasticSearch|http://your_server:9200|
|Kibana|http://your_server:5601|

### Step 4. Import Kibana assets

**IMPORTANT:** To add Kibana assets, run the `import.py` script from (a) the docker host or (b) **inside** the elasticsearch container! This script will add dashboards, visualizations and index-patters for Kibana. It will even set the default index so you don't have to worry about anything!

The script resides in the `timings-docker/elasticsearch/import/` directory and accepts the following arguments:

```shell
$ python elasticsearch/import/import.py --help
usage: import.py [-h] [-a APIHOST] [-b APIPORT] [-f ESHOST] [-g ESPORT]
                 [-i KBINDEX] [-k KBHOST] [-l KBPORT]

optional arguments:
  -h, --help            show this help message and exit
  -a APIHOST, --apihost APIHOST
                        host/ip address of the timings server
                        (default=localhost)
  -b APIPORT, --apiport APIPORT
                        host/ip address of the timings server (default=80)
  -f ESHOST, --eshost ESHOST
                        host/ip address of the elasticsearch server
                        (default=localhost)
  -g ESPORT, --esport ESPORT
                        port of the elasticsearch server (default=9200)
  -i KBINDEX, --kbindex KBINDEX
                        the kibana index (default=.kibana)
  -k KBHOST, --kbhost KBHOST
                        host/ip address of the kibana server
                        (default=localhost)
  -l KBPORT, --kbport KBPORT
                        port of the kibana server (default=5601)
```

You can run the script from the command line on the docker host or from inside the elasticsearch container. To run from the host, you need to make sure that `Python` and the `requests` module are installed! The container already has these pre-installed.

#### Running the script from the docker host

Run the following from the command line:

```shell
$ python elasticsearch/import/import.py [-f ESHOST -g ESPORT ...]
>>> You did not provide any or all of the arguments - defaults will be used!
Starting import to server [localhost] on port [9200] to index [.kibana]
=======================================================================
PASS -  - job: import [index-pattern] - item: cicd-perf-res
PASS -  - job: import [index-pattern] - item: cicd-perf
PASS -  - job: import [index-pattern] - item: cicd-perf-errorlog
...
...
```

Note that the script assumes [localhost] and [9200] when no arguments are provided!

#### Running the script from inside the elasticsearch container

You first need to get the elasticsearch container ID (in below example, the ID is: **9836a8281d73**):

```shell
$ docker ps
CONTAINER ID        IMAGE                         COMMAND                  CREATED             STATUS              PORTS                                            NAMES
adb19f15c820        timingsdocker_timings         "./wait-for-it.sh ..."   9 minutes ago       Up 9 minutes        0.0.0.0:80->80/tcp                               timings
df10a60e2ef4        timingsdocker_kibana          "/bin/sh -c /usr/l..."   3 hours ago         Up 9 minutes        0.0.0.0:5601->5601/tcp                           kibana
9836a8281d73        timingsdocker_elasticsearch   "/bin/bash bin/es-..."   3 hours ago         Up 9 minutes        0.0.0.0:9200->9200/tcp, 0.0.0.0:9300->9300/tcp   elasticsearch
```

Then you can run the script using docker's `exec` command:

```shell
$ docker exec -it 9836a8281d73 python ./import/import.py [-f ESHOST -g ESPORT ...]
>>> You did not provide any or all of the arguments - defaults will be used!
Starting import to server [localhost] on port [9200] to index [.kibana]
=======================================================================
PASS -  - job: import [index-pattern] - item: cicd-perf-res
PASS -  - job: import [index-pattern] - item: cicd-perf
PASS -  - job: import [index-pattern] - item: cicd-perf-errorlog
...
...
```

Note that the script uses [localhost] and [9200] when no arguments are provided!

Now go and check out Kibana to make sure everything looks A-OK!