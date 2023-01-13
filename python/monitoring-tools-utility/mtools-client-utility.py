#!/usr/local/bin/python

"""CLI Client utility for interacting with DataDog/Wormly/Zabbix."""

import os
from dotenv import load_dotenv
import time
import pytz
import colorama
from colorama import Back, Style
from simple_term_menu import TerminalMenu
import requests
import json
# from configparser import ConfigParser
from pprint import pprint
from datetime import datetime
from datadog_api_client.v1 import ApiClient, ApiException, Configuration
from datadog_api_client.v1.api import synthetics_api
from datadog_api_client.v1.models import SyntheticsUpdateTestPauseStatusPayload
from datadog_api_client.v1.models import SyntheticsTestPauseStatus
from datadog_api_client.v1.api import downtimes_api
from datadog_api_client.v1.api.downtimes_api import DowntimesApi
from datadog_api_client.v1.model.downtime import Downtime

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


def print_header():
    """Print the Header."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 90)
    print()
    print(Back.GREEN + Style.BRIGHT + " " + "*" * 21 + " DATADOG/WORMLY/ZABBIX CLIENT UTILITY  " + "*" * 21 + "       ")
    print()
    print("=" * 90)
    displayProgressBar()
    print("=" * 90)


def display_menu(config):
    """Display the Menu."""
    title = "DATADOG/WORMLY/ZABBIX CLIENT UTILITY "
    main_menu_title = title + "\n" + "*" * 46
    main_menu_items = ["DataDog", "Wormly", "Zabbix",
                       "Quit"]
    main_menu_cursor = "> "
    main_menu_cursor_style = ("fg_red", "bold")
    main_menu_style = ("bg_red", "fg_yellow")
    main_menu_exit = False

    main_menu = TerminalMenu(
        menu_entries=main_menu_items,
        title=main_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=True,
    )

    datadog_menu_title = title + "=> DataDog\n" + "*" * 46
    datadog_menu_items = ["Synthetic Tests", "Downtimes",
                          "Back to Main Menu", "Quit"]
    datadog_menu_back = False
    datadog_menu = TerminalMenu(
        datadog_menu_items,
        title=datadog_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=True,
    )

    datadog_syn_tests_menu_title = title + "=> Synthetic Tests\n" + "*" * 46
    datadog_syn_tests_menu_items = ["Get All", "Get By Status",
                                    "Pause All", "Un-Pause All", "Pause by ID",
                                    "Un-Pause by ID", "Back to Main Menu",
                                    "Quit"]
    datadog_syn_tests_menu_back = False
    datadog_syn_tests_menu = TerminalMenu(
        datadog_syn_tests_menu_items,
        title=datadog_syn_tests_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=True,
    )

    datadog_downtimes_menu_title = title + "=> Downtimes\n" + "*" * 46
    datadog_downtimes_menu_items = ["Get All", "Get By Status",
                                    "Schedule", "Cancel",
                                    "Back to Main Menu", "Quit"]
    datadog_downtimes_menu_back = False
    datadog_downtimes_menu = TerminalMenu(
        datadog_downtimes_menu_items,
        title=datadog_downtimes_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=True,
    )

    wormly_menu_title = title + "=> Wormly\n" + "*" * 46
    wormly_menu_items = ["Get All Downtimes", "Get Downtimes By HostID",
                         "Schedule All Downtimes", "Schedule Downtime for HostID", "Back to Main Menu", "Quit"]
    wormly_menu_back = False
    wormly_menu = TerminalMenu(
        wormly_menu_items,
        title=wormly_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=True,
    )
    while not main_menu_exit:
        main_sel = main_menu.show()

        if main_sel == 0:
            while not datadog_menu_back:
                datadog_sel = datadog_menu.show()
                if datadog_sel == 0:
                    while not datadog_syn_tests_menu_back:
                        datadog_syn_tests_sel = datadog_syn_tests_menu.show()
                        if datadog_syn_tests_sel == 0:
                            print("Getting All Tests...")
                            print(".......")
                            list_synthetic_tests(config, 'all', False)
                            print()
                            input("Press Enter to return back to Menu...")
                        elif datadog_syn_tests_sel == 1:
                            print("Get By Status..")
                            test_status = ""
                            status = input("Type in:\n1 for 'live'\n2 for 'paused'\n[ OR Press Enter to return back to Menu ] : \n")
                            if status == "1":
                                print("Getting All Live Tests...")
                                test_status = "live"
                            elif status == "2":
                                print("Getting All Paused Tests...")
                                test_status = "paused"
                            else:
                                # datadog_syn_tests_menu_back = True
                                continue
                            list_synthetic_tests(config, test_status, False)
                            print()
                            input("Press Enter to return back to Menu...")
                        elif datadog_syn_tests_sel == 2:
                            print("Pausing All Synthetic Tests...")
                            print("........")
                            pause_unpause_all_synthetic_tests(config, 'paused')
                            print()
                            input("Press Enter to return back to Menu...")
                        elif datadog_syn_tests_sel == 3:
                            print("Un-Pausing All Synthetic Tests...")
                            print("........")
                            pause_unpause_all_synthetic_tests(config, 'live')
                            print()
                            input("Press Enter to return back to Menu...")
                        elif datadog_syn_tests_sel == 4:
                            print("Pause By ID...")
                            test_id = input("Type in Test ID [ OR Press Enter to return back to Menu ] : \n")
                            if test_id == "":
                                # datadog_syn_tests_menu_back = True
                                continue
                            else:
                                pause_unpause_synthetic_tests(config,
                                                              [test_id],
                                                              'paused')
                            print()
                            input("Press Enter to return back to Menu...")
                        elif datadog_syn_tests_sel == 5:
                            print("UnPause By ID...")
                            test_id = input("Type in Test ID [ OR Press Enter to return back to Menu ] : \n")
                            if test_id == "":
                                # datadog_syn_tests_menu_back = True
                                continue
                            else:
                                pause_unpause_synthetic_tests(config,
                                                              [test_id],
                                                              'live')
                            print()
                            input("Press Enter to return back to Menu...")
                        elif datadog_syn_tests_sel == 6:
                            datadog_syn_tests_menu_back = True
                        elif datadog_syn_tests_sel == 7:
                            datadog_syn_tests_menu_back = True
                            datadog_menu_back = True
                            main_menu_exit = True
                    datadog_syn_tests_menu_back = False
                elif datadog_sel == 1:
                    while not datadog_downtimes_menu_back:
                        datadog_downtimes_sel = datadog_downtimes_menu.show()
                        if datadog_downtimes_sel == 0:
                            print("Getting All Downtimes...")
                            list_downtimes(config, "all")
                            print()
                            input("Press Enter to return back to Menu...")
                        elif datadog_downtimes_sel == 1:
                            print("Get By Status..")
                            print("-"*80)
                            downtime_status = ""
                            # downtime_status = input("Type in Downtime Status {'live', 'scheduled'} [ OR Press Enter to return back to Menu ] : \n")
                            status = input("Type in:\n1 for 'live'\n2 for 'scheduled'\n[ OR Press Enter to return back to Menu ] : \n")
                            if status == "1":
                                print("Live...")
                                downtime_status = "live"
                            elif status == "2":
                                print("Scheduled...")
                                downtime_status = "scheduled"
                            else:
                                # datadog_syn_tests_menu_back = True
                                continue
                            list_downtimes(config, downtime_status)
                            print()
                            input("Press Enter to return back to Menu...")
                        elif datadog_downtimes_sel == 2:
                            print("Schedule...")
                            start = input("Type in Downtime Start [ OR Press Enter to return back to Menu ] : \n")
                            if start == "":
                                # datadog_syn_tests_menu_back = True
                                continue
                            end = input("Type in Downtime End [ OR Press Enter to return back to Menu ] : \n")
                            if end == "":
                                # datadog_syn_tests_menu_back = True
                                continue

                            print("Scheduling Downtime from: (" + start + ") - till: (" + end + ")")

                            start_dt = start.split('T')
                            start_dp = start_dt[0].split('-')
                            start_tp = start_dt[1].split(':')
                            end_dt = end.split('T')
                            end_dp = end_dt[0].split('-')
                            end_tp = end_dt[1].split(':')

                            # Schedule a Downtime
                            downtime_start_datetime = datetime(int(start_dp[0]), int(start_dp[1]),
                                                               int(start_dp[2]), int(start_tp[0]),
                                                               int(start_tp[1]), int(start_tp[2]))

                            downtime_end_datetime = datetime(int(end_dp[0]), int(end_dp[1]),
                                                             int(end_dp[2]), int(end_tp[0]),
                                                             int(end_tp[1]), int(end_tp[2]))

                            print(downtime_start_datetime)
                            print(downtime_end_datetime)

                            # Get the POSIX timestamp values
                            downtime_start = int(downtime_start_datetime.timestamp())
                            downtime_end = int(downtime_end_datetime.timestamp())
                            print(f"Start: {downtime_start}")
                            print(f"End: {downtime_end}")
                            # schedule_downtime(config, downtime_start, downtime_end)
                            print()
                            input("Press Enter to return back to Menu...")
                        elif datadog_downtimes_sel == 3:
                            print("Cancel...")
                            print()
                            input("Press Enter to return back to Menu...")
                        elif datadog_downtimes_sel == 4:
                            datadog_downtimes_menu_back = True
                        elif datadog_downtimes_sel == 5:
                            datadog_downtimes_menu_back = True
                            datadog_menu_back = True
                            main_menu_exit = True
                    datadog_downtimes_menu_back = False
                elif datadog_sel == 2:
                    datadog_menu_back = True
                elif datadog_sel == 3:
                    datadog_menu_back = True
                    main_menu_exit = True
            datadog_menu_back = False
        elif main_sel == 1:
            while not wormly_menu_back:
                wormly_sel = wormly_menu.show()
                if wormly_sel == 0:
                    which_hostids = input("Type 1 for MyJS, 2 for CFS, 3 for Both [ OR Press Enter to return back to Menu  ]: \n")
                    if which_hostids == "1":
                        print("Getting all latest downtimes for MyJS...")
                        get_wormly_downtimes(myjs_hostids, False)
                    elif which_hostids == "2":
                        print("Getting all latest downtimes for CFS...")
                        get_wormly_downtimes(cfs_hostids, False)
                    elif which_hostids == "3":
                        print("Getting all latest downtimes for both MyJS & CFS...")
                        get_wormly_downtimes(myjs_hostids+cfs_hostids, False)
                    else:
                        continue
                    input("Press Enter to Continue...")
                elif wormly_sel == 1:
                    hostid = input("Type in HostID [ OR Press Enter to return back to Menu ] : \n")
                    if hostid == "":
                        continue
                    get_wormly_downtimes([hostid], False)
                    input("Press Enter to Continue...")
                elif wormly_sel == 2:
                    print("Schedule Downtimes for all HostIDs...")
                    results = get_wormly_downtimes([myjs_hostids[0]], True)
                    # print(results)
                    on = input(f"Type in Date (YYYY-MM-DD) [{results[0][myjs_hostids[0]]['on']}] \n[ OR Press Enter to accept the default value]\n[ OR Type 1 to return back to Menu] : \n")
                    if on == "":
                        on = results[0][myjs_hostids[0]]['on']
                    if on == '1':
                        continue
                    start = input(f"Type in Start time [{results[0][myjs_hostids[0]]['start']}]  \n[ OR Press Enter to accept the default value]\n[ OR Type 1 to return back to Menu] : \n")
                    if start == "":
                        start = results[0][myjs_hostids[0]]['start']
                    if start == '1':
                        continue
                    end = input(f"Type in End time [{results[0][myjs_hostids[0]]['end']}]  \n[ OR Press Enter to accept the default value]\n[ OR Type 1 to return back to Menu] : \n")
                    if end == "":
                        end = results[0][myjs_hostids[0]]['end']
                    if end == '1':
                        continue
                    timezone = input(f"Type in TimeZone [{results[0][myjs_hostids[0]]['timezone']}]  \n[ OR Press Enter to accept the default value]\n[ OR Type 1 to return back to Menu] : \n")
                    if timezone == "":
                        timezone = results[0][myjs_hostids[0]]['timezone']
                    if timezone == '1':
                        continue
                    # print(on, start, end, timezone)
                    print()
                    which_hostids = input("Type 1 for MyJS, 2 for CFS, 3 for Both [ OR Press Enter to return back to Menu  ]: \n")
                    if which_hostids == "1":
                        print("Setting downtimes for MyJS...")
                        set_wormly_downtimes(myjs_hostids, start, end, timezone, "ONCEONLY", on)
                    elif which_hostids == "2":
                        print("Setting downtimes for CFS...")
                        set_wormly_downtimes(cfs_hostids, start, end, timezone, "ONCEONLY", on)
                    elif which_hostids == "3":
                        print("Setting downtimes for both MyJS & CFS...")
                        set_wormly_downtimes(myjs_hostids+cfs_hostids, start, end, timezone, "ONCEONLY", on)
                    else:
                        continue
                    input("Press Enter to Continue...")
                elif wormly_sel == 3:
                    print("Schedule Downtimes for HostID")
                    print("-"*80)
                    hid = input("Type in HostID [ OR Press Enter to return back to Menu ] : \n")
                    if hid == "":
                        continue
                    results = get_wormly_downtimes([hid], True)
                    # print(results)
                    on = input(f"Type in Date (YYYY-MM-DD) [{results[0][hid]['on']}] \n[ OR Press Enter to accept the default value]\n[ OR Type 1 to return back to Menu] : \n")
                    if on == "":
                        on = results[0][hid]['on']
                    if on == '1':
                        continue
                    start = input(f"Type in Start time [{results[0][hid]['start']}]  \n[ OR Press Enter to accept the default value]\n[ OR Type 1 to return back to Menu] : \n")
                    if start == "":
                        start = results[0][hid]['start']
                    if start == '1':
                        continue
                    end = input(f"Type in Start time [{results[0][hid]['end']}]  \n[ OR Press Enter to accept the default value]\n[ OR Type 1 to return back to Menu] : \n")
                    if end == "":
                        end = results[0][hid]['end']
                    if end == '1':
                        continue
                    timezone = input(f"Type in Start time [{results[0][hid]['timezone']}]  \n[ OR Press Enter to accept the default value]\n[ OR Type 1 to return back to Menu] : \n")
                    if timezone == "":
                        timezone = results[0][hid]['timezone']
                    if timezone == '1':
                        continue
                    # print(on, start, end, timezone)
                    set_wormly_downtimes([hid], start, end, timezone, "ONCEONLY", on)
                    input("Press Enter to Continue...")
                elif wormly_sel == 4:
                    wormly_menu_back = True
                elif wormly_sel == 5:
                    wormly_menu_back = True
                    main_menu_exit = True
            wormly_menu_back = False
        elif main_sel == 2:
            print("Zabbix Menu..")
            input("Press Enter to Continue...")
        elif main_sel == 3:
            main_menu_exit = True


def main():
    """Entry point of the application."""
    global WORMLY_CONFIG

    env_file = os.path.dirname(os.path.realpath(__file__)) + os.sep + "config/env.mtools"

    load_dotenv(env_file)

    print_header()

    configuration = Configuration()

    display_menu(configuration)


if __name__ == "__main__":
    main()
