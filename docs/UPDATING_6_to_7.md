# Upgrading from v6.x to v7.x

**Perform the Kibana upgrade instructions first!**

## Kibana

- Please follow the instructions from this page: [https://www.elastic.co/guide/en/kibana/6.7/migrating-6.0-index.html](https://www.elastic.co/guide/en/kibana/6.7/migrating-6.0-index.html)

## Elasticsearch

### Copy data and migrate

For clarity, the directory of your previous installation is called `{src}` and the new directory is called `{dst}`

- **step 1**
  - Stop your current docker-compose environment
- **step 2**
  - Copy the entire contents of the `nodes` folder from `{src}/upgrade/data_v6` to `{dst}/upgrade/data_v7`
- **step 3**
  - To prevent any file level permissions issues, set full permissions on the `{dst}` directory:

  ```bash
  $ sudo chown -R $USER:$USER ./upgrade/data_v7
  $ sudo chmod 777 -R ./upgrade/data_v7
  ```

- **step 4**
  - Start up an Elasticsearch/Kibana v7.x environment by running the following command from the `timings-docker` folder:

  ```bash
  $ docker-compose -f ./upgrade/docker-compose-elk-v7.yml up --remove-orphans
  ```

  > Note: this only runs Elasticsearch and Kibana (version 7.17.0) and NOT the timings API!

- **step 5**
  - After Elasticsearch and Kibana have fully started (and your data has been migrated), you can navigate to Kibana at `http://{your_host}:5601` for the post-migration steps...

### Post-migration

After the data migration, a few more items need to be updated in Elasticsearch.
**You can perform these steps using Kibana's "Dev Tools" feature**

- **step 1** - Update the [cicd-perf] template

  Using the Dev Tools feature in Kibana, run the following commands:

  ```no-lang
  DELETE _template/cicd-perf
  ```

  ```no-lang
  PUT _index_template/cicd-perf?include_type_name=true
  {
    "version": 145,
    "index_patterns": [
      "cicd-perf-*",
      "cicd-resource-*",
      "cicd-errorlog-*"
    ],
    "template": {
      "settings": {
        "index": {
          "refresh_interval": "30s",
          "number_of_shards": "1",
          "number_of_replicas": "1"
        }
      },
      "mappings": {
        "dynamic_date_formats": [
          "strict_date_optional_time",
          "yyyy/MM/dd HH:mm:ss Z||yyyy/MM/dd Z"
        ],
        "dynamic": true,
        "_source": {
          "excludes": [],
          "includes": [],
          "enabled": true
        },
        "date_detection": true,
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
          "api_version": 145
        }
      }
    }
  }
  ```

- **step 2** - Reindex the [cicd-*] indices

  This step turns the the indices into new "typeless" indices. This also prepares them for the upgrade to v7.x!

  Using the Dev Tools feature of Kibana, run the following command:

  ```no-lang
  ???

  ```

- **step 3**
  - Check Kibana to validate that the migration worked:
    - You can use the Discover feature to see if your data looks OK
    - You can use the Dashboards feature to see if your visualizations look OK

## Next steps

**=> next step: RESTART TIMINGS-API ... you can follow the last steps here:** [UPDATING](./UPDATING.md#check-out-your-upgraded-api)
