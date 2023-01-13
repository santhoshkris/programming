#!/usr/local/bin/python

"""CLI Client utility for interacting with DataDog/Wormly/Zabbix."""

# import pytz
# import requests
# import json
# from configparser import ConfigParser
# from pprint import pprint
import os
from dotenv import load_dotenv
import time
import colorama
from colorama import Back, Style
from simple_term_menu import TerminalMenu
import mtools
import banner
import pages
from datadog_api_client.v1 import Configuration

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


def print_header():
    """Print the Header."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 90)
    print()
    print(Back.GREEN + Style.BRIGHT + " " + "*" * 22 + "     MAINTENANCE/DOWNTIME UTILITY  \
    " + "*" * 22 + "      ")
    print()
    print("=" * 90)
    displayProgressBar()
    print("=" * 90)


def display_menu(config):
    """Display the Menu."""
    title = "MAINTENENACE/DOWNTIME UTILITY"
    main_menu_title = title + "\n" + "*" * 46
    main_menu_items = ["Banner", "Cloudflare/Pages",
                       "DataDog", "Wormly", "Zabbix", "Quit"]
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
                         "Schedule All Downtimes",
                         "Schedule Downtime for HostID",
                         "Back to Main Menu", "Quit"]
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
            print("=> Maintenance Banner")
            print()
            ans = input("Begin upating the files? [Type 'yes' to continue or Press Enter to return back to Menu...]\n")
            if ans == 'yes':
                banner.update_files()
                input("All Done, Press Enter to return back to Menu...")
            else:
                pass
        elif main_sel == 1:
            print("=> Cloudflare/Maintenance Pages")
            print()
            ans = input("Begin upating the files? [Type 'yes' to continue or Press Enter to return back to Menu...]\n")
            if ans == 'yes':
                action = input("Enter the action type: [deploy/undeploy] or Press Enter to return back to Menu...\n")
                if action != "":
                    if action != 'undeploy':
                        scope = input("Enter the scope of changes: [myjs,jdb or all] or Press Enter to return back to Menu...\n")
                        if scope != "":
                            pages.update_files(action, scope)
                            input("All Done, Press Enter to return back to Menu...")
                    else:
                        pages.update_files(action)
                        input("All Done, Press Enter to return back to Menu...")
            else:
                pass
        elif main_sel == 2:
            while not datadog_menu_back:
                datadog_sel = datadog_menu.show()
                if datadog_sel == 0:
                    while not datadog_syn_tests_menu_back:
                        datadog_syn_tests_sel = datadog_syn_tests_menu.show()
                        if datadog_syn_tests_sel == 0:
                            print("Getting All Tests...")
                            print(".......")
                            mtools.list_synthetic_tests(config, 'all', False)
                            print()
                            input("Press Enter to return back to Menu...")
                        elif datadog_syn_tests_sel == 1:
                            print("Get By Status..")
                            test_status = ""
                            status = input("Type in:\n1 for 'live'\n2 for \ 'paused'\n[ OR Press Enter to return back to Menu ] : \n")
                            if status == "1":
                                print("Getting All Live Tests...")
                                test_status = "live"
                            elif status == "2":
                                print("Getting All Paused Tests...")
                                test_status = "paused"
                            else:
                                # datadog_syn_tests_menu_back = True
                                continue
                            mtools.list_synthetic_tests(config, test_status, False)
                            print()
                            input("Press Enter to return back to Menu...")
                        elif datadog_syn_tests_sel == 2:
                            print("Pausing All Synthetic Tests...")
                            print("........")
                            mtools.pause_unpause_all_synthetic_tests(config, 'paused')
                            print()
                            input("Press Enter to return back to Menu...")
                        elif datadog_syn_tests_sel == 3:
                            print("Un-Pausing All Synthetic Tests...")
                            print("........")
                            mtools.pause_unpause_all_synthetic_tests(config, 'live')
                            print()
                            input("Press Enter to return back to Menu...")
                        elif datadog_syn_tests_sel == 4:
                            print("Pause By ID...")
                            test_id = input("Type in Test ID [ OR Press Enter to return back to Menu ] : \n")
                            if test_id == "":
                                # datadog_syn_tests_menu_back = True
                                continue
                            else:
                                mtools.pause_unpause_synthetic_tests(config, [test_id], 'paused')
                            print()
                            input("Press Enter to return back to Menu...")
                        elif datadog_syn_tests_sel == 5:
                            print("UnPause By ID...")
                            test_id = input("Type in Test ID [ OR Press Enter to return back to Menu ] : \n")
                            if test_id == "":
                                # datadog_syn_tests_menu_back = True
                                continue
                            else:
                                mtools.pause_unpause_synthetic_tests(config, [test_id], 'live')
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
                            mtools.list_downtimes(config, "all")
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
                            mtools.list_downtimes(config, downtime_status)
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
                            mtools.schedule_downtime(config, downtime_start, downtime_end)
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
        elif main_sel == 3:
            while not wormly_menu_back:
                wormly_sel = wormly_menu.show()
                if wormly_sel == 0:
                    which_hostids = input("Type 1 for MyJS, 2 for CFS, 3 for Both [ OR Press Enter to return back to Menu  ]: \n")
                    if which_hostids == "1":
                        print("Getting all latest downtimes for MyJS...")
                        mtools.get_wormly_downtimes(mtools.myjs_hostids, False)
                    elif which_hostids == "2":
                        print("Getting all latest downtimes for CFS...")
                        mtools.get_wormly_downtimes(mtools.cfs_hostids, False)
                    elif which_hostids == "3":
                        print("Getting all latest downtimes for both MyJS & CFS...")
                        mtools.get_wormly_downtimes(mtools.myjs_hostids+mtools.cfs_hostids, False)
                    else:
                        continue
                    input("Press Enter to Continue...")
                elif wormly_sel == 1:
                    hostid = input("Type in HostID [ OR Press Enter to return back to Menu ] : \n")
                    if hostid == "":
                        continue
                    mtools.get_wormly_downtimes([hostid], False)
                    input("Press Enter to Continue...")
                elif wormly_sel == 2:
                    print("Schedule Downtimes for all HostIDs...")
                    results = mtools.get_wormly_downtimes([mtools.myjs_hostids[0]], True)
                    # print(results)
                    on = input(f"Type in Date (YYYY-MM-DD) [{results[0][mtools.myjs_hostids[0]]['on']}] \n[ OR Press Enter to accept the default value]\n[ OR Type 1 to return back to Menu] : \n")
                    if on == "":
                        on = results[0][mtools.myjs_hostids[0]]['on']
                    if on == '1':
                        continue
                    start = input(f"Type in Start time [{results[0][mtools.myjs_hostids[0]]['start']}]  \n[ OR Press Enter to accept the default value]\n[ OR Type 1 to return back to Menu] : \n")
                    if start == "":
                        start = results[0][mtools.myjs_hostids[0]]['start']
                    if start == '1':
                        continue
                    end = input(f"Type in End time [{results[0][mtools.myjs_hostids[0]]['end']}]  \n[ OR Press Enter to accept the default value]\n[ OR Type 1 to return back to Menu] : \n")
                    if end == "":
                        end = results[0][mtools.myjs_hostids[0]]['end']
                    if end == '1':
                        continue
                    timezone = input(f"Type in TimeZone [{results[0][mtools.myjs_hostids[0]]['timezone']}]  \n[ OR Press Enter to accept the default value]\n[ OR Type 1 to return back to Menu] : \n")
                    if timezone == "":
                        timezone = results[0][mtools.myjs_hostids[0]]['timezone']
                    if timezone == '1':
                        continue
                    # print(on, start, end, timezone)
                    print()
                    which_hostids = input("Type 1 for MyJS, 2 for CFS, 3 for Both [ OR Press Enter to return back to Menu  ]: \n")
                    if which_hostids == "1":
                        print("Setting downtimes for MyJS...")
                        mtools.set_wormly_downtimes(mtools.myjs_hostids, start, end, timezone, "ONCEONLY", on)
                    elif which_hostids == "2":
                        print("Setting downtimes for CFS...")
                        mtools.set_wormly_downtimes(mtools.cfs_hostids, start, end, timezone, "ONCEONLY", on)
                    elif which_hostids == "3":
                        print("Setting downtimes for both MyJS & CFS...")
                        mtools.set_wormly_downtimes(mtools.myjs_hostids+mtools.cfs_hostids, start, end, timezone, "ONCEONLY", on)
                    else:
                        continue
                    input("Press Enter to Continue...")
                elif wormly_sel == 3:
                    print("Schedule Downtimes for HostID")
                    print("-"*80)
                    hid = input("Type in HostID [ OR Press Enter to return back to Menu ] : \n")
                    if hid == "":
                        continue
                    results = mtools.get_wormly_downtimes([hid], True)
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
                    mtools.set_wormly_downtimes([hid], start, end, timezone, "ONCEONLY", on)
                    input("Press Enter to Continue...")
                elif wormly_sel == 4:
                    wormly_menu_back = True
                elif wormly_sel == 5:
                    wormly_menu_back = True
                    main_menu_exit = True
            wormly_menu_back = False
        elif main_sel == 4:
            print("Zabbix Menu..")
            mtools.get_zabbix_auth_token()
            mtools.get_zabbix_maintenance()
            input("Press Enter to Continue...")
        elif main_sel == 5:
            main_menu_exit = True


def main():
    """Entry point of the application."""
    global WORMLY_CONFIG

    env_file = os.path.dirname(os.path.realpath(__file__)) + os.sep + "config/env.file"

    load_dotenv(env_file)

    print_header()

    configuration = Configuration()

    display_menu(configuration)


if __name__ == "__main__":
    main()
