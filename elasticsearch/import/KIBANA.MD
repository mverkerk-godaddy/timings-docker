# KIBANA

We provide a set of index-patterns, dashboards and visualizations for Kibana that you can easily import!

## Python script import.py

To run this script, use the following command:

```
$ python ./import.py {ip/>host} {port} {kibana index}
```

where:

{ip/host}        ->  The ip address or hostname of your elasticsearch server/cluster (default is 'localhost')
{port}           ->  The port of your elasticsearch server/cluster (default is '9200')
{kibana index}   ->  The name of your kibana index (default is '.kibana')
