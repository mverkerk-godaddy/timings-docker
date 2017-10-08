"""
Imports the kibana objects into Elasticsearch
:return: True if operation is completed successfully, False otherwise.
"""
import sys
import os
import json

import argparse
import requests

# Test parameter settings
PARSER = argparse.ArgumentParser()

# Common arguments
PARSER.add_argument(
    '-a', '--apihost', action='store', default='localhost',
    help='host/ip address of the timings server (default=localhost)')
PARSER.add_argument(
    '-b', '--apiport', action='store', default='80',
    help='host/ip address of the timings server (default=80)')
PARSER.add_argument(
    '-f', '--eshost', action='store', default='localhost',
    help='host/ip address of the elasticsearch server (default=localhost)')
PARSER.add_argument(
    '-g', '--esport', action='store', default='9200',
    help='port of the elasticsearch server (default=9200)')
PARSER.add_argument(
    '-i', '--kbindex', action='store', default='.kibana',
    help='the kibana index (default=.kibana)')
PARSER.add_argument(
    '-k', '--kbhost', action='store', default='localhost',
    help='host/ip address of the kibana server (default=localhost)')
PARSER.add_argument(
    '-l', '--kbport', action='store', default='5601',
    help='port of the kibana server (default=5601)')

OPTIONS = PARSER.parse_args()

if not len(sys.argv) > 1:
    print(">>> You did not provide any or all of the arguments - " +
          "defaults will be used!")

IMPORT_JSON = json.load(open(os.path.join(os.path.abspath(
    os.path.dirname(__file__)), 'kibana_items.json')))

TEMPLATE_JSON = json.load(
    open(os.path.join(os.path.abspath(
        os.path.dirname(__file__)
        ), 'cicd_template.json')))

PERF_JSON = json.load(
    open(os.path.join(os.path.abspath(
        os.path.dirname(__file__)
        ), 'sample_data.json')))

BASE_IMPORT_URL = 'http://{}:{}'.format(OPTIONS.eshost, OPTIONS.esport)

STRING = ("Starting import to server [{}] on port [{}] to index [{}]".format(
    OPTIONS.eshost, OPTIONS.esport, OPTIONS.kbindex))
print(STRING)
print("=" * len(STRING))


def kb_import():
    """Import dashboards, visualizations and index-patterns into Kibana"""
    try:
        for item in IMPORT_JSON:
            _id = item["_id"]
            _type = item["_type"]
            _source = item["_source"]
            _title = _source["title"]

            if _type == 'index-pattern' and _id == 'cicd-perf':
                if OPTIONS.apiport != '80':
                    api_host = OPTIONS.apihost + ':' + OPTIONS.apiport
                else:
                    api_host = OPTIONS.apihost

                _source['fieldFormatMap'] = _source['fieldFormatMap'].replace(
                    '__api__hostname', api_host)

            response = requests.post(
                BASE_IMPORT_URL + '/' + OPTIONS.kbindex +
                '/' + _type + '/' + _id,
                data=json.dumps(_source),
                headers={'content-type': 'application/json'}
                )

            check_response(response, 'import [' + _type + ']', _title)

    except requests.exceptions.RequestException as err:
        print(err)


def kb_default_index():
    """Set cicd-perf as the default index"""
    try:
        response = requests.put(
            BASE_IMPORT_URL + '/' + OPTIONS.kbindex + '/config/5.6.2',
            data=json.dumps({'defaultIndex': 'cicd-perf'}),
            headers={'content-type': 'application/json'}
            )

        check_response(response, 'default index', 'cicd-perf')

    except requests.exceptions.RequestException as err:
        print(err)

    # $ curl -XPUT -D- 'http://localhost:9200/.kibana/config/5.6.1' \
    #     -H 'Content-Type: application/json' \
    #     -d '{"defaultIndex": "logstash-*"}'


def es_template():
    """Adds basic template for cicd-perf index to ElasticSearch"""
    try:
        response = requests.post(
            BASE_IMPORT_URL + '/_template/cicd-perf',
            data=json.dumps(TEMPLATE_JSON),
            headers={'content-type': 'application/json'}
            )

        check_response(response, 'add template', 'cicd-perf')

    except requests.exceptions.RequestException as err:
        print(err)


def es_sample_data(index, data_type):
    """Adds sample data to main indices (cicd-perf and cicd-perf-res)"""
    doc_type = data_type
    if data_type == 'resource_nav' or data_type == 'resource_uri':
        doc_type = 'resource'

    try:
        response = requests.post(
            BASE_IMPORT_URL + '/' + index + '/' + doc_type + '/',
            data=json.dumps(PERF_JSON[data_type]),
            headers={'content-type': 'application/json'}
            )

        check_response(response, 'add sample data', data_type)

    except requests.exceptions.RequestException as err:
        print(err)


def check_response(response, job, item):
    """Check the request responses and prints results"""
    job_summ = " - job: {} - item: {}".format(job, item)
    if response.ok:
        print("PASS - {}".format(job_summ))
    else:
        print('FAIL - {} - StatusCode: {} - Reason: {}, Error: {}'.format(
            job_summ, response.status_code, response.reason, response.content))


if __name__ == '__main__':
    kb_import()
    kb_default_index()
    es_template()
    es_sample_data('cicd-perf', 'navtiming')
    es_sample_data('cicd-perf-res', 'resource_nav')
    es_sample_data('cicd-perf-res', 'resource_uri')
