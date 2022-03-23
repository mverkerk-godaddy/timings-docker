# Upgrading from v5.x to v6.x

## Upgrade Kibana [Do this first!]

### You will be performing this step in your current v5.x version of Kibana

- Please perform all 4 of the steps mentioned on this page: [https://www.elastic.co/guide/en/kibana/6.7/migrating-6.0-index.html](https://www.elastic.co/guide/en/kibana/6.7/migrating-6.0-index.html)

## Upgrade Elasticsearch

### Copy data and migrate

Just for peace of mind:

- your current data is located in `./elasticsearch/data`
- you will make a copy of your data to sub-directories inside the `./upgrade` directory
- only upon successful migration, you will copy the upgraded data back to the original `./elasticsearch/data` directory

OK, let's go ...

- **step 1**
  - Stop your current docker-compose environment
- **step 2**
  - Make sure the `./upgrade/data_v6` is empty
  - Copy the entire `nodes` directory from `./elasticsearch/data` to `./upgrade/data_v6`
- **step 3**
  - To prevent any file level permission issues, set full permissions on the `./upgrade/data_v6` directory:

  ```bash
  $ sudo chown -R $USER:$USER ./upgrade/data_v6
  $ sudo chmod 777 -R ./upgrade/data_v6
  ```

- **step 4**
  - Start up an Elasticsearch/Kibana v6.x environment by running the following command from the `timings-docker` folder:

  ```bash
  $ docker-compose -f ./upgrade/docker-compose-elk-v6.yml up --remove-orphans
  ```

  > Note: this runs Elasticsearch and Kibana (version 6.8.23) WITHOUT the timings API!

- **step 5**
  - After Elasticsearch and Kibana have fully started (and your data has been migrated), you can navigate to Kibana at `http://{your_host}:5601` for some **important**  post-migration steps...
  - Note: if you see a message like this: `FATAL  Error: Index .kibana belongs to a version of Kibana that cannot be automatically migrated. Reset it or use the X-Pack upgrade assistant.` then you have most likely skipped the Kibana upgrade ... see here: [Upgrade Kibana](#upgrade-kibana-do-this-first)

## Post-migration

After the data migration, a few more items need to be updated in Kibana.

### You can perform these steps using Kibana's "Dev Tools" feature**

- **step 1** - Update the [cicd-perf] template

  Run the following command:

  ```no-lang
  PUT _template/cicd-perf?include_type_name=true
  {
    "order": 0,
    "version": 145,
    "index_patterns": [
      "cicd-perf-*",
      "cicd-resource-*",
      "cicd-errorlog-*"
    ],
    "settings": {
      "index": {
        "number_of_shards": "1"
      }
    },
    "mappings": {
      "doc": {
        "dynamic_templates": [
          {
            "string_fields": {
              "mapping": {
                "norms": false,
                "ignore_above": 512,
                "index": true,
                "store": false,
                "type": "keyword"
              },
              "match_mapping_type": "string",
              "match": "*"
            }
          },
          {
            "long_fields": {
              "mapping": {
                "store": false,
                "type": "long"
              },
              "match_mapping_type": "long",
              "match": "*"
            }
          }
        ],
        "_meta": {
          "api_version": "1.4.5"
        }
      }
    },
    "aliases": {}
  }
  ```

- **step 2**
  - Check Kibana to validate that the migration worked:
    - You can use the Discover feature to see if your data looks OK
    - You can use the Dashboards feature to see if your visualizations look OK

## Next steps

**=> next step: UPGRADE TO V7 ... follow the instructions here:** [UPDATING from 6 to 7](./UPDATING_6_to_7.md)
