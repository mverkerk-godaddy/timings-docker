# timings-docker

This repo provides **docker-compose** support for the node/express based [**TIMINGS API**](https://github.com/godaddy/timings) only! **This is not the API itself** but merely a collection of scripts and configuration files to run the API in a docker based environment. For details about the API itself, please check out the repo here: [https://github.com/godaddy/timings](https://github.com/godaddy/timings).

Also, see the FAQ section in the Wiki for more help & tips: [https://github.com/Verkurkie/timings-docker/wiki/FAQ-page](https://github.com/Verkurkie/timings-docker/wiki/FAQ-page).

## IMPORTANT

**> IF YOU ARE UPDATING YOUR INSTALLATION OF THIS REPO, PLEASE READ THE [UPDATING.md](./docs/UPDATING.md) DOCUMENT!!**

## Usage

Before jumping into the installation & usage of this repo and the associated Docker container, please read the following notes.
It is really crucial that you understand Docker and `docker-compose`, especially when upgrading this repo!!

- When you start the Docker infrastructure for the first time, a number of folders is created for logs and data files:

  ```no-lang
  [host folder]
    /elasticsearch
      /data
    /kibana
      /data
    /timings
      /logs
  ```

- As you use the API, elasticsearch data is stored on the local file system of the Docker Host! The data can be found in the `./elasticsearch/data/nodes/` folder
- When you upgrade this repo, there is a possibility that the `docker-compose.yml` file is pointing at newer versions of Elasticsearch and Kibana
  - ==>> in this scenario, please read the [UPDATING.md](./docs/UPDATING.md) document!
  - **please make sure that you have migrated your elasticsearch data when upgrading to a new MAJOR version of elasticsearch/kibana!**

Last but not least, please reference the [system requirements](#system-requirements) to check if your system meets the needs.

### Step 1. Clone it

Clone this repo to a folder of your choice:

```lang-console
$ git clone git@github.com/godaddy/timings-docker.git
Cloning into 'timings-docker'...
...
$ cd timings-docker
```

### Step 2. Configure it

It is recommended that you create a custom config file. You can copy the sample config file (`./timings-docker/timings/config/sample_default.json`) and:

- save it in a location of your choice (example: `/etc/timings/timings.json`)
- edit the file according to your needs - see also here: [https://github.com/godaddy/timings/blob/master/CONFIG.MD](https://github.com/godaddy/timings/blob/master/CONFIG.MD)

### Step 3. Run it

You should now be able to run the environment by running:

```lang-console
$ CONFIGFILE=/etc/timings/timings.json docker-compose up
WARNING: The HOSTNAME variable is not set. Defaulting to a blank string.
Starting elasticsearch ... done
Starting kibana        ... done
Starting timings       ... done
Attaching to elasticsearch, kibana, timings
timings          | [2021-03-01T09:33:45.171Z][info] - timings API - LOGGING - logs files stored in: ["/src/logs"]
timings          | [2021-03-01T09:33:45.175Z][info] - timings API - LOGGING - log level: INFO
timings          | [2021-03-01T09:33:45.514Z][info] - timings API - CONFIG - Using config ["/src/.config.js"]
timings          | [2021-03-01T09:33:45.514Z][info] - timings API - STATUS - Server v1.4.5 is running at http://08ed9a9ac258:80
timings          | [2021-03-01T09:33:45.522Z][info] - Elasticsearch - UTILS - [PORTCHECK] waiting for host [elasticsearch] at port [9200] ...
elasticsearch    | [2021-03-01T09:33:48,685][INFO ][o.e.n.Node               ] [66ca5bd94595] version[7.11.1], pid[7], build[default/docker/ff17057114c2199c9c1bbecc727003a907c0db7a/2021-02-15T13:44:09.394032Z], OS[Linux/4.19.128-microsoft-standard/amd64], JVM[AdoptOpenJDK/OpenJDK 64-Bit Server VM/15.0.1/15.0.1+9]
elasticsearch    | [2021-03-01T09:33:48,690][INFO ][o.e.n.Node               ] [66ca5bd94595] JVM home [/usr/share/elasticsearch/jdk], using bundled JDK [true]
... [more elasticsearch messages]

timings          | [2021-03-01T09:34:04.367Z][info] - Elasticsearch - UTILS - [HEALTHCHECK] status [yellow] of host [elasticsearch] is OK!
timings          | [2021-03-01T09:34:04.378Z][info] - Elasticsearch - UTILS - [INFO] found elastic v7.11.1 ...
timings          | [2021-03-01T09:34:04.426Z][info] - Elasticsearch - UTILS - [UPDATE] API and ELK are up-to-date!
```

Above example is showing the main log output messages of the [timings] service that you should look for! During the first startup, you should ultimately see a line that says `[UPDATE] API and ELK are up-to-date!` or `[TEMPLATE] created/updated [cicd-perf]` in case the API was updated! This confirms that the API waited for Elasticsearch to be healthy and it updated the template for `cicd-perf*` in Elasticsearch.

```bash
$ CONFIGFILE=/etc/timings/timings.json docker-compose up
```

**NOTE:** The first time you install this or when you use the `pull / --build` argument(s), Docker will (re-)build the containers! The output will look different and the entire process will take a bit longer to complete.

You should use `CONFIGFILE=/etc/timings/timings.json docker-compose pull && docker-compose up --build` every time the timings images is updated. This ensures you're getting the latest container!

### Step 4. Check it

After the containers have started, you can test the app by browsing to the following URLs (where `hostname` is the name of you Docker host system):

|Service|Link|
|-|-|
|timings|http://hostname
|elasticsearch|http://hostname:9200|
|kibana|http://hostname:5601|

## Other considerations

Depending on your host system, you may need to make some further adjustments or you can consider a few optional settings. Keep reading below.

### Update docker-compose file [optional]

Instead of using the `CONFIGFILE` variable to start docker-compose, you can reference your config file in the `docker-compose.yml` file:

- Update `./timings-docker/docker-compose.yml` and **uncomment + edit** the _volumes_ section for the `timings` service to map your config file to the container's `/src/config/default.json` file:

```yaml
  volumes
  volumes:
    - "${CONFIGFILE}:/src/config/default.json"   <<-- edit this line
    - ./timings/logs:/timings/logs
```

**If you don't use a custom config file, the API will use default values**. Settings such as the ElasticSearch host (`ES_HOST`), Kibana host (`KB_HOST`), etc. don't need to be included because they are already defined in the docker-compose yaml file.

### Host specific settings

Before you can run the API you may have to make a few modifications to your docker host:

#### Add user to `docker` group [Linux only]

You have to add your user account to the `docker` group and logging out & back in again. If you don't do this, you have to run `docker-compose` with `sudo` which is not recommended! You can use the following command:

```lang-console
sudo usermod -aG docker ${USER}
```

#### Custom elasticsearch data directory [optional]

This is optional. By defaults, the elasticsearch container will use the `timings-docker/elasticsearch/data` directory on the **docker host** to store its data. If you want to use a different location, you can edit the `volumes` section of the `timings-docker/docker-compose.yml` file and point to the desired location:

```yaml
  elasticsearch:
    ...
    volumes:
      - ./elasticsearch/data:/usr/share/elasticsearch/data    <<-- edit this line
    ...
```

#### Set permissions for the data & logging directories [Linux only]

You need to set the necessary read/write permissions to the data and logging directories! Depending on how you are running docker-compose, the permissions may look different

In this example, we're setting full permissions on all of the directories:

```lang-console
$ sudo chmod 777 ./elasticsearch/data
$ sudo chmod 777 ./kibana/data
$ sudo chmod 777 ./timings/logs
```

## System requirements

- Linux or Windows based OS with the following pre-requisites:

  - Docker and docker-compose
    - Docker: [https://docs.docker.com/engine/installation/](https://docs.docker.com/engine/installation/)
    - Docker-compose: [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)
  - Windows Subsystem for Linux (Windows only)
    - To support the `wait-for-it.sh` script (until we have a PowerShell equivalent)
    - More info: [https://msdn.microsoft.com/en-us/commandline/wsl/install-win10](https://msdn.microsoft.com/en-us/commandline/wsl/install-win10) and [https://msdn.microsoft.com/commandline/wsl/install-on-server](https://msdn.microsoft.com/commandline/wsl/install-on-server)
- Min. 4GB memory for elasticsearch (8+GB is recommended)
- Storage space for elasticsearch data
  - required amount depends on test frequency. As an indicator, running the API for ~6 mo at GoDaddy with ~40,000 tests/day produced ~170Gb of data.
  - storage can also be mounted remotely (see [here](#custom-elasticSearch-data-directory-optional))
