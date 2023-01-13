#!/usr/local/bin/python

"""Module for interacting with DataDog/Wormly/Zabbix."""

import os
import time
import pytz
import colorama
import requests
import json
# from configparser import ConfigParser
from datetime import datetime
from datadog_api_client.v1 import ApiClient, ApiException, Configuration
from datadog_api_client.v1.api import synthetics_api
from datadog_api_client.v1.models import SyntheticsUpdateTestPauseStatusPayload
from datadog_api_client.v1.models import SyntheticsTestPauseStatus
from datadog_api_client.v1.api import downtimes_api
from datadog_api_client.v1.api.downtimes_api import DowntimesApi
from datadog_api_client.v1.model.downtime import Downtime

ZABBIX_AUTH_TOKEN = ""

myjs_hostids = [
    "36304",  # MYJS Docswap - ds-mfs (SG2)
    "43899",  # MYJS Docswap - ds-mfs (SG2) Load Average
    "36303",  # MYJS Docswap - ds-myjs (SG1)
    "36306",  # MYJS Docswap - ds-myjs-id
    "36307",  # MYJS Docswap - ds-myjs-idck
    "40396",  # MYJS OWA
    "45770",  # MYJS OWA - Preprosessing Schedule
    "52739",  # MYJS Serverchat
    "17943",  # MYJS WebServer
    "18151",  # MYJS WebServer (ID)
    "58102",  # MYJSDB centralmyjs transfer
]

cfs_hostids = [
    "70542",  # Jobsdb TH MSite
    "54589",  # Jobsdb TH DesktopSite
    "70641",  # Jobsdb MobileAppApi
    "54252",  # Jobsdb HK DesktopSite
]

colorama.init(autoreset=True)


# def config_reader(filename='./config/mtools_config.ini', section='wormly'):
#     """Read in the config file to fetch the required API KEY details."""
#     # create a parser
#     parser = ConfigParser()
#     # read config file
#     parser.read(filename)

#     # get section, default to postgresql
#     details = {}
#     if parser.has_section(section):
#         params = parser.items(section)
#         for param in params:
#             details[param[0]] = param[1]
#     else:
#         raise Exception(f'Section {section} not found in the {filename} file')

#     return details


# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1,
                     length=100, fill='█', printEnd="\r"):
    """Create a Simple progress bar."""
    percent = ("{0:." + str(decimals) + "f}").\
        format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def displayProgressBar():
    """Generate the progress bar and display on screen."""
    # A List of Items
    items = list(range(0, 57))
    plength = len(items)

    # Initial call to print 0% progress
    printProgressBar(0, plength, prefix='Connecting:', suffix='Complete',
                     length=50)
    for i, item in enumerate(items):
        # Do stuff...
        time.sleep(0.02)
        # Update Progress Bar
        printProgressBar(i + 1, plength, prefix='Connecting:',
                         suffix='Complete', length=50)


def get_zabbix_auth_token():
    """Get AUTH Token for Zabbix API."""
    global ZABBIX_AUTH_TOKEN
    url = os.getenv('ZABBIX_API_URL_TH')
    uname = os.getenv('ZABBIX_ADMIN_USER')
    passwd = os.getenv('ZABBIX_ADMIN_PASSWD')

    response = requests.post(url,
                             json={
                                    "jsonrpc": "2.0",
                                    "method": "user.login",
                                    "params": {
                                        "user": uname,
                                        "password": passwd
                                    },
                                    "id": 1
                                    })

    # print(response.json())
    ZABBIX_AUTH_TOKEN = response.json()["result"]
    print(ZABBIX_AUTH_TOKEN)


def get_zabbix_hosts():
    """Get currently configured maintenance windows."""
    url = os.getenv('ZABBIX_API_URL_TH')

    response = requests.post(url,
                             json={
                                    "jsonrpc": "2.0",
                                    "method": "maintenance.get",
                                    "params": {
                                        "output": "extend",
                                        "selectGroups": "extend",
                                        "selectTimeperiods": "extend",
                                        "selectTags": "extend"
                                    },
                                    "auth": ZABBIX_AUTH_TOKEN,
                                    "id": 1
                                   }
                             )

    print(response.json())


def get_zabbix_maintenance():
    """Get currently configured maintenance windows."""
    url = os.getenv('ZABBIX_API_URL_TH')

    response = requests.post(url,
                             json={
                                    "jsonrpc": "2.0",
                                    "method": "maintenance.get",
                                    "params": {
                                        "output": "extend",
                                        "selectGroups": "extend",
                                        "selectTimeperiods": "extend",
                                        "selectTags": "extend"
                                    },
                                    "auth": ZABBIX_AUTH_TOKEN,
                                    "id": 1
                                   }
                             )

    print(response.json())


def get_wormly_downtimes(hostids, noprint):
    """Get latest set downtime from Wormly for the HostID(s)."""
    results = []
    print("-"*80)
    for host in hostids:
        url = "https://api.wormly.com/?key=" + os.getenv('key') + "&cmd=getScheduledDowntimePeriods&response=json&hostid=" + host

        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        if not noprint:
            print("-"*80)
            print(f"Lastest Downtime for HostID: {host}")
            print("-"*80)
        response = requests.get(url, headers=headers, data=payload)
        data = json.loads(response.text)['periods'][-1]
        results.append({host: data})
        if not noprint:
            print(f"On: {data['on']}")
            print(f"Start: {data['start']}")
            print(f"End: {data['end']}")
            print(f"TimeZone: {data['timezone']}")
            print("-"*80)
            time.sleep(0.2)
    if noprint:
        return results
    # print(response.text)


def set_wormly_downtimes(hostids, start, end, timezone, recurrence, on):
    """Set downtimes in Wormly for the HostID(s)."""
    for host in hostids:
        url = "https://api.wormly.com/?key=" + os.getenv('key') + "&cmd=setScheduledDowntimePeriod&response=json&hostid=" + host + "&start=" + start + "&end=" + end + "&timezone=" + timezone + "&recurrence=" + recurrence + "&on=" + on

        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        # print(url)

        response = requests.get(url, headers=headers, data=payload)
        data = json.loads(response.text)
        # pprint(data)
        if data["errorcode"] == 0:
            print(f"Downtime scheduled successfully for HostID: {host}")


def list_synthetic_tests(config, scope, noprint):
    """List all the synthetic tests."""
    with ApiClient(config) as api_client:
        api_instance = synthetics_api.SyntheticsApi(api_client)
        testIDs = []
        tests_in_scope = []
        # example, this endpoint has no required or optional parameters
        try:
            # Get the list of all tests
            api_response = api_instance.list_tests()
            # pprint(api_response)
            for i, test in enumerate(api_response['tests']):
                if not noprint:
                    if scope == 'live' and str(test['status']) == 'live':
                        tests_in_scope.append(test)
                    elif scope == 'paused' and str(test['status']) == 'paused':
                        tests_in_scope.append(test)
                    elif scope == 'all':
                        tests_in_scope.append(test)
                else:
                    if i != 2:
                        testIDs.append(test['public_id'])
            if noprint:
                return testIDs

            print("-"*80)
            if scope == 'all':
                print(f"Total #tests configured is : \
                {len(tests_in_scope)}")
            else:
                print(f"Total {scope} tests are : \
                {len(tests_in_scope)}")
            print("Details are :")
            print("-"*80)
            j = 1
            for i, t in enumerate(tests_in_scope):
                print("-"*80)
                if j > 3:
                    j = 1
                    print()
                    input("Press Enter to Continue...")
                    print()
                print(f"Test #{i+1}")
                print("-"*80)
                print(f"Name: {t['name']}")
                print(f"ID: {t['public_id']}")
                print(f"TYPE: {t['type']}")
                print(f"STATUS: {t['status']}")
                print(f"MESSAGE TO: {t['message']}")
                print("*"*80)
                j += 1
        except ApiException as e:
            print("Exception when calling SyntheticsApi->list_tests: %s\n" % e)


def pause_unpause_all_synthetic_tests(config, state):
    """Pause/Unpause all Synthetic tests."""
    testIDs = list_synthetic_tests(config, all, True)
    # print(testIDs)
    pause_unpause_synthetic_tests(config, testIDs, state)


def pause_unpause_synthetic_tests(config, testIDs, state):
    """Pause/UnPause a specific Synthetic test."""
    with ApiClient(config) as api_client:
        api_instance = synthetics_api.SyntheticsApi(api_client)
        if testIDs:
            for id in testIDs:
                public_id = id
                print("Test ID is : ", public_id)
                print("State to set is : ", state)
                time.sleep(1)
                # body = SyntheticsUpdateTestPauseStatusPayload(
                #     new_status=SyntheticsTestPauseStatus(state),
                # )
                # try:
                #     api_response = api_instance.update_test_pause_status(public_id, body)
                #     pprint(api_response)
                # except ApiException as e:
                #     print("Exception when calling SyntheticsApi->update_test_pause_status: %s\n" % e)


def list_downtimes(config, scope):
    """List all currently scheduled Downtimes."""
    with ApiClient(config) as api_client:
        api_instance = downtimes_api.DowntimesApi(api_client)
        current_only = False
        if scope == 'live':
            current_only = True
        try:
            # Get all downtimes
            api_response = api_instance.list_downtimes(current_only=current_only)
            # pprint(api_response)
            if not len(api_response):
                print("No Downtimes found...")
                return
            found_scheduled = False
            print("-"*50)
            for i, dt in enumerate(api_response):
                if scope == 'scheduled':
                    if not dt['disabled']:
                        found_scheduled = True
                        print(f"Downtime #{i+1} :")
                        print("-"*50)
                        print("Disabled: ", dt['disabled'])
                        print("Start (POSIX): ", dt['start'])
                        indatetime1 = datetime.fromtimestamp(int(dt['start']))
                        print(f'Start in local time: {indatetime1}')
                        local1 = pytz.timezone("Asia/Kolkata")
                        toconvert1 = pytz.timezone("Asia/Kuala_Lumpur")
                        localize1 = local1.localize(indatetime1)
                        converted1 = localize1.astimezone(toconvert1)
                        print(f'Start in target timezone: {converted1}')
                        print("End (POSIX): ", dt['end'])
                        indatetime = datetime.fromtimestamp(int(dt['end']))
                        print(f'End in local timezone: {indatetime}')
                        local = pytz.timezone("Asia/Kolkata")
                        toconvert = pytz.timezone("Asia/Kuala_Lumpur")
                        localize = local.localize(indatetime)
                        converted = localize.astimezone(toconvert)
                        print(f'End in target timezone: {converted}')
                        print("TimeZone: ", dt['timezone'])
                        print("Scope: ", dt['scope'])
                        print("Message:  ", dt['message'])
                        print("*"*50)
                else:
                    print(f"Downtime #{i+1} :")
                    print("-"*50)
                    print("Disabled: ", dt['disabled'])
                    print("Start (POSIX): ", dt['start'])
                    indatetime1 = datetime.fromtimestamp(int(dt['start']))
                    print(f'Start in local time: {indatetime1}')
                    local1 = pytz.timezone("Asia/Kolkata")
                    toconvert1 = pytz.timezone("Asia/Kuala_Lumpur")
                    localize1 = local1.localize(indatetime1)
                    converted1 = localize1.astimezone(toconvert1)
                    print(f'Start in target timezone: {converted1}')
                    print("End (POSIX): ", dt['end'])
                    indatetime = datetime.fromtimestamp(int(dt['end']))
                    print(f'End in local timezone: {indatetime}')
                    local = pytz.timezone("Asia/Kolkata")
                    toconvert = pytz.timezone("Asia/Kuala_Lumpur")
                    localize = local.localize(indatetime)
                    converted = localize.astimezone(toconvert)
                    print(f'End in target timezone: {converted}')
                    print("TimeZone: ", dt['timezone'])
                    print("Scope: ", dt['scope'])
                    print("Message:  ", dt['message'])
                    print("*"*50)
            if scope == 'scheduled' and (not found_scheduled):
                print("No SCHEDULED Downtimes found...")
        except ApiException as e:
            print("Exception when calling DowntimesApi->list_downtimes: %s\n" % e)


def schedule_downtime(config, start, end):
    """Schedule Downtime."""
    body = Downtime(
        message="Another TEST - Scheduling Downtime from API",
        start=start,
        end=end,
        timezone="Asia/Kuala_Lumpur",
        scope=["*"],
    )

    with ApiClient(config) as api_client:
        api_instance = DowntimesApi(api_client)
        response = api_instance.create_downtime(body=body)
        # print(response)
        print("Downtime Scheduled...")
