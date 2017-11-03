# timings-docker

Docker support for the node/express based **TIMINGS API**. See more here: [https://github.com/godaddy/timings](https://github.com/godaddy/timings).

We **HIGHLY** recommend running the TIMINGS API along with ElasticSearch and Kibana in a containerized environment! This repo has everything you need to get this setup!

## Installation

System requirements:

- Linux or Windows based OS with the following pre-requisites:

  - Docker and docker-compose
    - Docker: https://docs.docker.com/engine/installation/
    - Docker-compose: https://docs.docker.com/compose/install/
  - Windows Subsystem for Linux (Windows only)
    - To support the `wait-for-it.sh` script (until we have a PowerShell equivalent)
    - More info: https://msdn.microsoft.com/en-us/commandline/wsl/install-win10 and https://msdn.microsoft.com/commandline/wsl/install-on-server
  - [Optional] Python and the `requests` module
    - To support running the `import.py` script from the docker host (see [here](#running-the-script-from-the-docker-host))
    - Python: http://docs.python-guide.org/en/latest/
    - requests: http://docs.python-requests.org/en/master/user/install/
- Min. 4GB memory for elasticsearch (8+GB is recommended)
- Storage space for elasticsearch data
  - required amount amount depends on test frequency. As an indicator, running the API for ~6 mo at GoDaddy with ~40,000 tests/day produced ~170Gb of data.
  - storage can also be mounted remotely (see [here](#custom-elasticSearch-data-directory-optional))

### Step 1. Clone this repo

Clone this repo to a folder of your choice:

```shell
$ git clone git@github.com/godaddy/timings-docker.git
Cloning into 'timings-docker'...
...
...

$ cd timings-docker
```

### Step 2. Prepping the docker host

Before you can run the API you may have to make a few modifications to your docker host:

#### Add user to `docker` group [Linux only]

You have to add your user account to the `docker` group and logging out & back in again. If you don't do this, you have to run `docker-compose` with `sudo` which is not recommended! You can use the following command:

```shell
usermod -aG docker ${USER}
```

#### Custom elasticsearch data directory

This is optional. By defaults, the elasticsearch container will use the `timings-docker/elasticsearch/data` directory on the **docker host** to store its data. If you want to use a different location, you need to edit the `volumes` section of the `timings-docker/docker-compose.yml` file and point to the desired location.

```yaml
  elasticsearch:
    ...
    volumes:
      - ./elasticsearch/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml
      - ./elasticsearch/logs:/var/log/elasticsearch
      - ./elasticsearch/data:/var/lib/elasticsearch
    ...
```

#### Set permissions for the elasticsearch data directory [Linux only]

You need to set the required permissions to the `elasticsearch/data` directory by running these commands:

```shell
$ sudo chown 1000:1000 ./elasticsearch/data
$ sudo chmod 775 ./elasticsearch/data
```

#### Configure the API for Kibana

<span style="color:red">**IMPORTANT:**</span> Please configure the full hostname of the Kibana server in the API's config file with the `config.env.KB_HOST` setting. See review here [API config](https://github.com/godaddy/timings/blob/master/CONFIG.MD). Without this setting, the waterfall pages may not function properly!

### Step 3. Starting up the API

You should now be able to run the docker environment with the following command:

```shell
$ docker-compose up [--build]
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

**NOTE:** The first time you run this or when you use the `--build` argument, Docker will (re-)build the containers! The output will look different and the entire process will take longer to complete. You should use the `--build` argument every time one of the docker images is updated!

Notice that the timings service first runs the `wait-for-it.sh` script. This ensures that the timings service waits (up to 30 secs) for elasticsearch to start!

The following line in the output indicates that the timings service is up and running:

```shell
...
timings          | debug: TIMINGS API [prod] is running on port 80
...
```

### Step 4. Test the apps

After the containers have started, you can test the apps by browsing to the following:

|App|Link|
|-|-|
|timings|http://your_server
|ElasticSearch|http://your_server:9200|
|Kibana|http://your_server:5601|

### Step 5. Setup Kibana

**IMPORTANT:** After startup, Kibana is completely empty - there are no dashboards, visualizations, default index, etc.:

![Empty Kibana](/img/kb_before_import.jpg)

#### The import script

<span style="color:red">**IMPORTANT:**</span> it is important that you **specify the full hostname of the API server** using the `-a` or `--apihost` argument! If you don't, the script will assume `localhost` and the waterfall links will not work for remote users!!

To add objects to Kibana, run the `timings-docker/elasticsearch/import/import.py` script. You can do this [from the docker host](#running-the-script-from-the-docker-host) or [from **inside** the elasticsearch container](#running-the-script-from-inside-the-elasticsearch-container)! This script will add dashboards, visualizations and index-patters for Kibana. It will even set the default index so you don't have to worry about a thing!

The script resides in the `timings-docker/elasticsearch/import/` directory and accepts several arguments.

Also, if elasticsearch is running on a remote server/cluster, you have to specify the full hostname and port using the `-f` or `--eshost` argument (and if the port is not 9200, use the `-g` or `--esport` argument).

```shell
$ python elasticsearch/import/import.py --help
usage: import.py [-h] [-a APIHOST] [-b APIPORT] [-f ESHOST] [-g ESPORT] [-i KBINDEX] [-k KBHOST] [-l KBPORT]

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

#### Running the script from the docker host

To run from the host, you need to make sure that `Python` and the `requests` module are installed! The container already has them pre-installed. Run the following from the command line:

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

Use this ID to run the script with docker's `exec` command:

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

### Step 6. Validate Kibana objects

Now go and check out Kibana to make sure everything looks A-OK! Navigate to your Kibana server and go to:

#### Management -> Saved Objects (should see a number of dashboards and visualizations)

![Kibana Saved Objects - after import](/img/kb_saved_objects.jpg)

-or-

#### Visualize (should see a list of visualizations)

![Kibana Saved Objects - after import](/img/kb_visualizations.jpg)

-or-

#### Dashboard -> TIMINGS-Dashboard (should see an empty dashboard)

Since you most probably haven't submitted any test results to the API yet, the main dashboard (http://{kibana host}/app/kibana#/dashboard/TIMINGS-Dashboard) is working but still empty:

![Kibana empty Dashboard](/img/kb_dashboard.jpg)

Time to start running your tests and submit data to the API and your dashboard should start showing some data!
