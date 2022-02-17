#!/usr/local/bin/python

"""CLI Client utility for interacting with DataDog."""

import os
import sys
import time
import pytz
import argparse
import colorama
from datetime import datetime
from colorama import Back, Style
from datadog_api_client.v1 import ApiClient, ApiException, Configuration
from datadog_api_client.v1.api import synthetics_api
from datadog_api_client.v1.models import SyntheticsUpdateTestPauseStatusPayload
from datadog_api_client.v1.models import SyntheticsTestPauseStatus
from datadog_api_client.v1.api import downtimes_api
from datadog_api_client.v1.api.downtimes_api import DowntimesApi
from datadog_api_client.v1.model.downtime import Downtime
from pprint import pprint

colorama.init(autoreset=True)


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


def list_all_synthetic_tests(config, noprint):
    """List all the synthetic tests."""
    with ApiClient(config) as api_client:
        api_instance = synthetics_api.SyntheticsApi(api_client)
        testIDs = []
        # example, this endpoint has no required or optional parameters
        try:
            # Get the list of all tests
            api_response = api_instance.list_tests()
            # pprint(api_response)
            if not noprint:
                print("-"*80)
                print(f"Total #tests configured is :,\
                {len(api_response['tests'])}")
                print("Details are :")
                print("-"*80)
            for i, test in enumerate(api_response['tests']):
                if not noprint:
                    print("-"*80)
                    print(f"Test #{i+1}")
                    print("-"*80)
                    print(f"Name: {test['name']}")
                    print(f"ID: {test['public_id']}")
                if i != 2:
                    testIDs.append(test['public_id'])
                if not noprint:
                    print(f"TYPE: {test['type']}")
                    print(f"STATUS: {test['status']}")
                    print(f"MESSAGE TO: {test['message']}")
                    print("*"*80)
            return testIDs
        except ApiException as e:
            print("Exception when calling SyntheticsApi->list_tests: %s\n" % e)


def pause_unpause_all_synthetic_tests(config, state):
    """Pause/Unpause all Synthetic tests."""
    testIDs = list_all_synthetic_tests(config, True)
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
                body = SyntheticsUpdateTestPauseStatusPayload(
                    new_status=SyntheticsTestPauseStatus(state),
                )
                try:
                    api_response = api_instance.update_test_pause_status(public_id, body)
                    pprint(api_response)
                except ApiException as e:
                    print("Exception when calling SyntheticsApi->update_test_pause_status: %s\n" % e)


def list_downtimes(config, scope):
    """List all currently scheduled Downtimes."""
    with ApiClient(config) as api_client:
        api_instance = downtimes_api.DowntimesApi(api_client)
        current_only = False
        if scope == 'active':
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
    # CALL THE APIs to fetch results
    print("=" * 80)
    print()
    print(Back.GREEN + Style.BRIGHT + "      " + "*" * 20 + ",\
          DATADOG CLIENT UTILITY  " + "*" * 20 + "       ")
    print()
    print("=" * 80)
    displayProgressBar()
    print("=" * 80)


def argParserConfig():
    """Parse the input arguments."""
    # create parser object
    parser = argparse.ArgumentParser(description="DataDog Client Utility!")
    # defining arguments for parser object
    parser.add_argument("--list_all_syn_tests", action='store_true',
                        help="Get all Synthetic Tests.")
    parser.add_argument("--pause_all_syn_tests", action='store_true',
                        help="Pause all Synthetic tests.")
    parser.add_argument("--unpause_all_syn_tests", action='store_true',
                        help="UnPause all Synthetic tests.")
    parser.add_argument("--pause_syn_test", type=str, nargs=1,
                        metavar="test_id", default=None,
                        help="Pause a Synthetic Test")
    parser.add_argument("--unpause_syn_test", type=str, nargs=1,
                        metavar="test_id", default=None,
                        help="UnPause a Synthetic Test")
    parser.add_argument("--list_downtimes",
                        choices=['all', 'active', 'scheduled'],
                        help="Get all currently active Downtimes.")
    parser.add_argument("--schedule_downtime", type=str, nargs=2,
                        metavar=("start", "end"),
                        help="Schedule a Downtime by specifying,\
                        start and end time")
    return parser


def call_methods(args, config):
    """Invoke the menthods based on the args passed."""
    # calling functions depending on type of argument
    if args.list_all_syn_tests:
        print("Fetching all Synthetic Tests")
        list_all_synthetic_tests(config, False)
    elif args.pause_all_syn_tests:
        print("Pausing all Synthetic Tests")
        print()
        pause_unpause_all_synthetic_tests(config, 'paused')
    elif args.unpause_all_syn_tests:
        print("UnPausing all Synthetic Tests")
        print()
        pause_unpause_all_synthetic_tests(config, 'live')
    elif args.pause_syn_test is not None:
        print("Pausing Synthetic Test with ID: " + args.pause_syn_test[0])
        print()
        pause_unpause_synthetic_tests(config, args.pause_syn_test, 'paused')
    elif args.unpause_syn_test is not None:
        print("UnPausing Synthetic Test with ID: " + args.unpause_syn_test[0])
        print()
        pause_unpause_synthetic_tests(config, args.unpause_syn_test, 'live')
    elif args.list_downtimes:
        print(f"Fetching {args.list_downtimes.upper()} Downtimes")
        print()
        list_downtimes(config, args.list_downtimes)
    elif args.schedule_downtime is not None:
        start = args.schedule_downtime[0]
        end = args.schedule_downtime[1]
        print("Scheduling Downtime from: (" + start + "),\
                               - till: (" + end + ")")

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
        schedule_downtime(config, downtime_start, downtime_end)


def print_footer():
    """Print the Footer."""
    print()
    print("=" * 80)


def main():
    """Entry point of the application."""
    # check_and_install_dependencies()

    parser = argParserConfig()

    # parse the arguments from standard input
    args = parser.parse_args()

    # print help message and exit if no arguments passed in
    if not len(sys.argv) > 1:
        parser.print_help()
        sys.exit()

    print_header()

    configuration = Configuration()

    call_methods(args, configuration)

    print_footer()


if __name__ == "__main__":
    main()
