# timings-docker

This repo provides **docker-compose** support for the node/express based [**TIMINGS API**](https://github.com/godaddy/timings) only! **This is not the API itself** but merely a collection of scripts and configuration files to run the API in a docker based environment. For details about the API itself, please check out the repo here: [https://github.com/godaddy/timings](https://github.com/godaddy/timings).

Also, see the FAQ section in the Wiki for more help & tips: https://github.com/Verkurkie/timings-docker/wiki/FAQ-page.

## Installation

### System requirements:

- Linux or Windows based OS with the following pre-requisites:

  - Docker and docker-compose
    - Docker: https://docs.docker.com/engine/installation/
    - Docker-compose: https://docs.docker.com/compose/install/
  - Windows Subsystem for Linux (Windows only)
    - To support the `wait-for-it.sh` script (until we have a PowerShell equivalent)
    - More info: https://msdn.microsoft.com/en-us/commandline/wsl/install-win10 and https://msdn.microsoft.com/commandline/wsl/install-on-server
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

### Step 2. Create a custom config file

It is recommended that you create a custom config file. You can copy the sample config file (`./timings-docker/timings/config/.config_sample.js`) and:

- save it in a location of your choice (example: `/etc/perfconfig.js`)
- edit the file according to your needs - see also here: [https://github.com/godaddy/timings/blob/master/CONFIG.MD](https://github.com/godaddy/timings/blob/master/CONFIG.MD)
- update `./timings-docker/docker-compose.yml` file and **uncomment** the _volume_ entry for the config file:

```yaml
  volumes
  # - /your/custom/config.js:/src/.config.js  <<< uncomment & update this line!
  - ./timings/logs:/src/logs
```

**If you don't use a custom config file, the API will use default values**. Settings such as the ElasticSearch host (`ES_HOST`), Kibana host (`KB_HOST`), etc. don't need to be included because they are already defined in the docker-compose yaml file.

### Step 3. Prepping the docker host

Before you can run the API you may have to make a few modifications to your docker host:

#### Add user to `docker` group [Linux only]

You have to add your user account to the `docker` group and logging out & back in again. If you don't do this, you have to run `docker-compose` with `sudo` which is not recommended! You can use the following command:

```shell
usermod -aG docker ${USER}
```

#### Custom elasticsearch data directory

This is optional. By defaults, the elasticsearch container will use the `timings-docker/elasticsearch/data` directory on the **docker host** to store its data. If you want to use a different location, you need to edit the `volumes` section of the `timings-docker/docker-compose.yml` file and point to the desired location:

```yaml
  elasticsearch:
    ...
    volumes:
      - ./elasticsearch/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml
      - ./elasticsearch/data:/usr/share/elasticsearch/data [ <<-- edit this line ]
      - ./elasticsearch/logs:/var/log/elasticsearch
    ...
```

#### Set permissions for the elasticsearch data directory [Linux only]

You need to set the required permissions to the `elasticsearch/data` directory by running these commands:

```shell
$ sudo chown 1000:1000 ./elasticsearch/data
$ sudo chmod 775 ./elasticsearch/data
```

### Step 4. Starting up the API
You should now be able to run the environment by running `docker-compose up` from the `timings-docker` folder.

**NOTE:** The first time you run this or when you use the `--build` argument, Docker will (re-)build the containers! The output will look different and the entire process will take a bit longer to complete. You should use the `--build` argument every time one of the docker images is updated!

```shell
$ docker-compose up
Starting elasticsearch ... done
Starting kibana ... done
Starting timings ... done
Attaching to elasticsearch, kibana, timings
elasticsearch    | [2018-03-12T16:11:33,741][INFO ][o.e.n.Node               ] [] initializing ...
...
timings          | debug: [Elasticsearch] - elasticsearch:9200 - [WAIT] waiting for Elasticsearch healthy state ...
timings          | debug: [timings API] - LTDV-MVERKERK:80 - [READY] v1.1.9 - using config: [defaults] - Could not find or access config file, or no file provided

... [ELK messages]

timings          | debug: [Elasticsearch] - elasticsearch:9200 - [PORTCHECK] - port 9200 is live ...
timings          | debug: [Elasticsearch] - elasticsearch:9200 - [HEALTHCHECK] - status is [GREEN] ...
timings          | debug: [Elasticsearch] - elasticsearch:9200 - [READY] - [Elasticsearch v.5.6.2] is up!
timings          | debug: [Elasticsearch] - elasticsearch:9200 - [UPGRADE] checking if upgrades are needed ...
timings          | debug: [Elasticsearch] - elasticsearch:9200 - [UPGRADE] upgrading Kibana items ... [Force: undefined - New: true - Upgr: false]

... [more ELK messages]

timings          | debug: [Elasticsearch] - elasticsearch:9200 - [IMPORT] - imported/updated 48 Kibana item(s)!
timings          | debug: [Elasticsearch] - elasticsearch:9200 - Template [cicd-perf] exists/created: true

... [log continues ...]
```

Above example is showing the main log output messages of the [timings] service that you should look for! During the first startup, you should see the line that says `imported/updated [xx] Kibana item(s)`! This confirms that the API waited for Elasticsearch to be healthy and it imported the main Kibana dashboards and visualizations into Elasticsearch.

### Step 5. Test the apps

After the containers have started, you can test the apps by browsing to the following:

|App|Link|
|-|-|
|timings|http://your_server
|elasticsearch|http://your_server:9200|
|kibana|http://your_server:5601|

### Step 6. Validate Kibana

Now go and check out Kibana to make sure everything looks A-OK! Navigate to your Kibana server and go to:

#### Management -> Saved Objects (should see a number of dashboards and visualizations)

![Kibana Saved Objects - after API startup & import](/img/kb_saved_objects.jpg)

-or-

#### Visualize (should see a list of visualizations)

![Kibana Saved Objects - after API startup & import](/img/kb_visualizations.jpg)

-or-

#### Dashboard -> TIMINGS-Dashboard (should see an empty dashboard)

Since you most probably haven't submitted any test results to the API yet, the main dashboard (http://{kibana host}/app/kibana#/dashboard/TIMINGS-Dashboard) is working but still empty:

![Kibana empty Dashboard](/img/kb_dashboard.jpg)

Time to start running your tests and submit data to the API and your dashboard should start showing some data!
