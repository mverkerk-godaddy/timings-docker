# **IMPORTANT NOTICE:**

You can specify the location of your own API config by using the `CONFIGFILE` environment variable!

If you don't specify your own config, the API will use the sample config: `./timings/config/.config_sample.js`

-- end of notice --

# timings-docker

This repo provides **docker-compose** support for the node/express based [**TIMINGS API**](https://github.com/godaddy/timings) only! **This is not the API itself** but merely a collection of scripts and configuration files to run the API with Docker. For details about the API itself, please check out its repo here: [https://github.com/godaddy/timings](https://github.com/godaddy/timings).

Also, see the FAQ section in the Wiki for more help & tips: https://github.com/Verkurkie/timings-docker/wiki/FAQ-page.

## Installation

System requirements:

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

You can store your config file anywhere on the host system, just make sure you set `CONFIGFILE={path}` variable before the docker-compose command! The config file **must be in JavaScript format** (be sure to export the config with `module.exports`). A sample JS file is provided in this repo (`/timings/config/.config_sample.js`). 

You do not have to specify `ES_HOST` and `KB_HOST` in the config file - they are configured in the `docker-compose.yml` file!

### Step 3. Starting up the API

You should now be able to run the docker environment with the following command (example):

```shell
$ CONFIGFILE=/etc/.perfconfig.js docker-compose up [--build]
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

### Step 5. Validate Kibana

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
