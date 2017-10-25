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

$ cd timings-docker
```

### Step 2. Run docker-compose

You can start up the multi-container environments like this:

```shell
$ docker-compose up -d
Starting elasticsearch ...
Starting elasticsearch ... done
Starting kibana ...
Starting kibana ... done
Starting timings ...
Starting timings ... done
...
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

Follow these steps:

## From the docker host

If you want to run the script from the docker host (needs `python` and the `requests` module to be installed):

```shell
$ python import/import.py
>>> You did not provide any or all of the arguments - defaults will be used!
Starting import to server [localhost] on port [9200] to index [.kibana]
=======================================================================
PASS -  - job: import [index-pattern] - item: cicd-perf-res
PASS -  - job: import [index-pattern] - item: cicd-perf
PASS -  - job: import [index-pattern] - item: cicd-perf-errorlog
...
...
```

## From inside the elasticsearch container

If you want to run the python script inside the elasticsearch container:

- Find the container ID of the elasticseach container (5896572dec79 in the below example):

```shell
$ docker ps
CONTAINER ID        IMAGE                  COMMAND                  CREATED             STATUS              PORTS                                            NAMES
404fea2319a2        docker_kibana          "/bin/sh -c /usr/l..."   20 minutes ago      Up 19 minutes       0.0.0.0:5601->5601/tcp                           kibana
5896572dec79        docker_elasticsearch   "/bin/bash bin/es-..."   24 minutes ago      Up 19 minutes       0.0.0.0:9200->9200/tcp, 0.0.0.0:9300->9300/tcp   elasticsearch
```

- Run the import script

```shell
$ docker exec -it 5896572dec79 python import/import.py
>>> You did not provide any or all of the arguments - defaults will be used!
Starting import to server [localhost] on port [9200] to index [.kibana]
=======================================================================
PASS -  - job: import [index-pattern] - item: cicd-perf-res
PASS -  - job: import [index-pattern] - item: cicd-perf
PASS -  - job: import [index-pattern] - item: cicd-perf-errorlog
...
...
```

Now go and check out Kibana to make sure everything looks A-OK!