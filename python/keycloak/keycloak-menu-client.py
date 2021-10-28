import json
import os
import shlex
import subprocess
import sys
import time
from configparser import ConfigParser

import colorama
import requests
from colorama import Fore, Back, Style
from requests.auth import HTTPBasicAuth
from simple_term_menu import TerminalMenu

colorama.init(autoreset=True)

KEYCLOAK_CONFIG = {}
AUTH_TOKEN = ""


# def check_and_install_dependencies():
#     if sys.hexversion <= 0x3000000:
#         print("Need Python 3 to execute this... Please install the same and re-run.")
#         sys.exit(0)
#     try:
#         import colorama
#         import requests
#         import simple_term_menu
#     except ImportError or ModuleNotFoundError:
#         print("Installing dependencies : python libraries...")
#         subprocess.run(shlex.split("pip3 install -r requirements.txt"))


def config(filename='keycloak_config.ini', section='keycloak'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    keycloak = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            keycloak[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return keycloak


# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def displayProgressBar():
    # A List of Items
    items = list(range(0, 57))
    l = len(items)

    # Initial call to print 0% progress
    printProgressBar(0, l, prefix='Loading:', suffix='Complete', length=50)
    for i, item in enumerate(items):
        # Do stuff...
        time.sleep(0.02)
        # Update Progress Bar
        printProgressBar(i + 1, l, prefix='Loading:', suffix='Complete', length=50)


def get_token():
    url = KEYCLOAK_CONFIG['base_url'] + "/auth/realms/" + KEYCLOAK_CONFIG['realm'] + "/protocol/openid-connect/token"
    payload = 'grant_type=client_credentials'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(url, headers=headers, data=payload,
                             auth=HTTPBasicAuth(KEYCLOAK_CONFIG['client_id'], KEYCLOAK_CONFIG['client_secret']))

    token = json.loads(response.text)
    # print(token)
    return token["access_token"]


def getUserCount():
    url = KEYCLOAK_CONFIG['base_url'] + "/auth/admin/realms/" + KEYCLOAK_CONFIG['realm'] + "/users/count"

    # print(url)

    payload = {}
    auth = 'Bearer ' + AUTH_TOKEN
    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth
    }

    response = requests.get(url, headers=headers, data=payload)

    # print(response.text)
    return json.loads(response.text)


def get_users(query_params):
    url = KEYCLOAK_CONFIG['base_url'] + "/auth/admin/realms/" + KEYCLOAK_CONFIG['realm'] + "/users" + query_params

    payload = {}
    auth = 'Bearer ' + AUTH_TOKEN
    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth
    }

    response = requests.get(url, headers=headers, data=payload)

    # print(response.text)
    return json.loads(response.text)


def getUsersByName(firstname="", lastname=""):
    # print("Finding users with FirstName=" + firstname + "and LastName=" + lastname)
    # print('=' * 80)
    query_params = "?firstName=" + firstname + "&lastName=" + lastname
    return get_users(query_params)


def getUsersByEmail(email):
    # print("Finding users with email=" + email)
    # print('=' * 80)
    query_params = "?email=" + email
    return get_users(query_params)


def getUserRoles(email):
    user = getUsersByEmail(email)
    if not len(user) > 0:
        print(Fore.RED + "No user with email: '" + email + "' found...")
        sys.exit(0)
    user_id = user[0]['id']
    url = KEYCLOAK_CONFIG['base_url'] + "/auth/admin/realms/" + KEYCLOAK_CONFIG['realm'] + "/users/" + user_id \
          + "/role-mappings/clients/" + KEYCLOAK_CONFIG['client_uuid']
    payload = {}
    auth = 'Bearer ' + AUTH_TOKEN
    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth
    }
    response = requests.get(url, headers=headers, data=payload)
    # print(response.text)
    roles = []
    result = json.loads(response.text)
    for r in result:
        roles.append(r['name'])
    return roles


def getClientRoles():
    url = KEYCLOAK_CONFIG['base_url'] + "/auth/admin/realms/" + KEYCLOAK_CONFIG['realm'] + "/clients/" + \
          KEYCLOAK_CONFIG['client_uuid'] + "/roles"
    auth = 'Bearer ' + AUTH_TOKEN
    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth
    }
    response = requests.get(url, headers=headers)
    # print(response.text)
    return json.loads(response.text)


def getRoleRepr(role):
    client_roles = getClientRoles()
    for r in client_roles:
        # print(role)
        if role in r.values():
            return r


def addRemoveUserRoles(email, role, flag):
    user = getUsersByEmail(email)
    if not len(user) > 0:
        print(Fore.RED + "No user with email: '" + email + "' found...")
        sys.exit(0)
    user_id = user[0]['id']
    role_repr = getRoleRepr(role)
    url = KEYCLOAK_CONFIG['base_url'] + "/auth/admin/realms/" + KEYCLOAK_CONFIG['realm'] + "/users/" + user_id \
          + "/role-mappings/clients/" + KEYCLOAK_CONFIG['client_uuid']
    payload = json.dumps([role_repr])
    # print(payload)
    auth = 'Bearer ' + AUTH_TOKEN
    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth
    }
    if flag:
        response = requests.post(url, headers=headers, data=payload)
    else:
        response = requests.delete(url, headers=headers, data=payload)

    if response.ok:
        if flag:
            print("Role : " + role + " successfully added to user : " + email)
        else:
            print("Role : " + role + " successfully removed from user : " + email)
    else:
        if flag:
            print("Failed adding Role : " + role + " to user : " + email + str(
                response.status_code) + " " + response.text)
        else:
            print("Failed removing Role : " + role + " from user : " + email + str(
                response.status_code) + " " + response.text)


def getUserLDAPConf(email):
    # print("Finding LDAP Config for user =" + email)
    result = getUsersByEmail(email)
    if not len(result) > 0:
        print(Fore.RED + "No user with email: '" + email + "' found...")
        sys.exit(0)
    if 'attributes' in result[0].keys():
        return result[0]['attributes']['LDAP_ENTRY_DN']
    else:
        return "No LDAP Configuration found for user"


def enableDisableUser(email, flag):
    url = KEYCLOAK_CONFIG['base_url'] + "/auth/admin/realms/" + KEYCLOAK_CONFIG['realm'] + "/users/"
    user = getUsersByEmail(email)
    if not len(user) > 0:
        print(Fore.RED + "No user with email: '" + email + "' found...")
        sys.exit(0)
    user_id = user[0]['id']
    url = url + user_id
    # print(url)
    if flag:
        payload = {'enabled': True}
    else:
        payload = {'enabled': False}
    auth = 'Bearer ' + AUTH_TOKEN
    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth
    }
    response = requests.put(url, headers=headers, data=json.dumps(payload))
    if response.ok:
        if flag:
            print("Successfully enabled user: " + email)
        else:
            print("Successfully disabled user: " + email)
    else:
        if flag:
            print("Enabling user: " + email + "failed..." + str(response.status_code) + " " + response.text)
        else:
            print("Disabling user: " + email + "failed..." + str(response.status_code) + " " + response.text)


def sendActionsEmailToUser(email, action):
    url = KEYCLOAK_CONFIG['base_url'] + "/auth/admin/realms/" + KEYCLOAK_CONFIG['realm'] + "/users/"
    user = getUsersByEmail(email)
    if not len(user) > 0:
        print(Fore.RED + "No user with email: '" + email + "' found...")
        sys.exit(0)
    # if not user[0]['enabled']:
    #     print("User : " + email + "not enabled. Enabling user now...")
    #     enableDisableUser(email, True)
    user_id = user[0]['id']
    url = url + user_id + '/execute-actions-email'
    exec_action = ""
    if action == "update_pass":
        exec_action = "UPDATE_PASSWORD"
    elif action == "verify_email":
        exec_action = "VERIFY_EMAIL"
    payload = [exec_action]
    auth = 'Bearer ' + AUTH_TOKEN
    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth
    }
    response = requests.put(url, headers=headers, data=json.dumps(payload))
    if response.ok:
        print("Successfully sent " + action + " email to user: " + email)
    else:
        print("Sending update password email to user: " + email + "failed..." + str(
            response.status_code) + " " + response.text)


# def sendVerifyEmailToUser(email):
#     url = KEYCLOAK_CONFIG['base_url'] + "/auth/admin/realms/" + KEYCLOAK_CONFIG['realm'] + "/users/"
#     user = getUsersByEmail(email)
#     if not user[0]['enabled']:
#         print("User : " + email + "not enabled. Enabling user now...")
#         enableDisableUser(email, True)
#     user_id = user[0]['id']
#     url = url + user_id + '/send-verify-email'
#     payload = {}
#     auth = 'Bearer ' + AUTH_TOKEN
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': auth
#     }
#     response = requests.put(url, headers=headers, data=json.dumps(payload))
#     if response.ok:
#         print("Successfully sent verification email to user: " + email)
#     else:
#         print("Sending verification email to user: " + email + "failed..." + str(response.status_code) + " " + response.text)


def print_user_list(users):
    char_repeat_count = 80
    print("# of Users returned : ", len(users))
    print('-' * char_repeat_count)
    print("User Details : ")
    print('-' * char_repeat_count)
    for i, u in enumerate(users):
        print("User : Index -> ", i + 1)
        print("     userid: ", u['id'])
        print("     username: ", u['username'])
        print("     Full Name: ", end='')
        if 'firstName' in u.keys():
            print(u['firstName'], end='')
        if 'lastName' in u.keys():
            print(" " + u['lastName'])
        print("     User enabled ?:", u['enabled'])
        print("     User email verified ?:", u['emailVerified'])
        print('-' * char_repeat_count)


def print_header():
    os.system('cls' if os.name == 'nt' else 'clear')
    # CALL THE APIs to fetch results
    print("=" * 80)
    print()
    print(Back.GREEN + Style.BRIGHT + "      " + "*" * 20 + "  KEYCLOAK CLIENT UTILITY  " + "*" * 20 + "       ")
    print()
    print("=" * 80)
    displayProgressBar()
    print("=" * 80)


def print_footer():
    print()
    print("=" * 80)


def display_menu():
    title = "KEYCLOAK CLIENT UTILITY "
    main_menu_title = title + "\n" + "*" * 46
    main_menu_items = ["Search for Users", "Enable/Disable User", "User Roles", "Send Email Actions",
                       "Get LDAP Config for User", "Quit"]
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

    find_user_menu_title = title + "=> Search for Users\n" + "*" * 46
    find_user_menu_items = ["by Email", "by First Name", "by Last Name", "Back to Main Menu", "Quit"]
    find_user_menu_back = False
    find_user_menu = TerminalMenu(
        find_user_menu_items,
        title=find_user_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=True,
    )

    enable_disable_menu_title = title + "=> Enable/Disable User\n" + "*" * 46
    enable_disable_menu_items = ["Enable", "Disable", "Back to Main Menu", "Quit"]
    enable_disable_menu_back = False
    enable_disable_menu = TerminalMenu(
        enable_disable_menu_items,
        title=enable_disable_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=True,
    )

    user_roles_menu_title = title + "=> User Roles\n" + "*" * 46
    user_roles_menu_items = ["Get User Roles", "Add Role to User", "Remove Role from User", "Back to Main Menu", "Quit"]
    user_roles_menu_back = False
    user_roles_menu = TerminalMenu(
        user_roles_menu_items,
        title=user_roles_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=True,
    )

    send_email_actions_menu_title = title + "=> Send Email Actions\n" + "*" * 46
    send_email_actions_menu_items = ["Send Verification", "Send Update Password", "Back to Main Menu", "Quit"]
    send_email_actions_menu_back = False
    send_email_actions_menu = TerminalMenu(
        send_email_actions_menu_items,
        title=send_email_actions_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=True,
    )

    while not main_menu_exit:
        main_sel = main_menu.show()

        if main_sel == 0:
            while not find_user_menu_back:
                find_user_sel = find_user_menu.show()
                if find_user_sel == 0:
                    email = input("Type in User's Email [ OR Press Enter to return back to Menu ] : \n")
                    if email == "":
                        find_user_menu_back = True
                    else:
                        print_user_list(getUsersByEmail(email))
                        input("Press Enter to Continue...")
                elif find_user_sel == 1:
                    fname = input("Type in User's First Name [ OR Press Enter to return back to Menu ] : \n")
                    if fname == "":
                        find_user_menu_back = True
                    else:
                        print_user_list(getUsersByName(firstname=fname))
                        input("Press Enter to Continue...")
                elif find_user_sel == 2:
                    lname = input("Type in User's Last Name [ OR Press Enter to return back to Menu ] : \n")
                    if lname == "":
                        find_user_menu_back = True
                    else:
                        print_user_list(getUsersByName(lastname=lname))
                        input("Press Enter to Continue...")
                elif find_user_sel == 3:
                    find_user_menu_back = True
                elif find_user_sel == 4:
                    find_user_menu_back = True
                    main_menu_exit = True
            find_user_menu_back = False
        elif main_sel == 1:
            while not enable_disable_menu_back:
                enable_disable_sel = enable_disable_menu.show()
                if enable_disable_sel == 0:
                    email = input("Type in the User's Email [ OR Press Enter to return back to Menu ] : \n")
                    if email == "":
                        enable_disable_menu_back = True
                    else:
                        enableDisableUser(email, True)
                        print()
                        input("Press Enter to Continue...")
                elif enable_disable_sel == 1:
                    email = input("Type in the User's Email [ OR Press Enter to return back to Menu ] : \n")
                    if email == "":
                        enable_disable_menu_back = True
                    else:
                        enableDisableUser(email, False)
                        print()
                        input("Press Enter to Continue...")
                elif enable_disable_sel == 2:
                    enable_disable_menu_back = True
                elif enable_disable_sel == 3:
                    enable_disable_menu_back = True
                    main_menu_exit = True
            enable_disable_menu_back = False
        elif main_sel == 2:
            while not user_roles_menu_back:
                user_roles_sel = user_roles_menu.show()
                if user_roles_sel == 0:
                    email = input("Type in the User's Email [ OR Press Enter to return back to Menu ] : \n")
                    if email == "":
                        user_roles_menu_back = True
                    else:
                        print("Getting Roles mapped for user: " + email)
                        print()
                        roles = getUserRoles(email)
                        print()
                        print('Assigned Roles : ')
                        for r in roles:
                            print('\t', r)
                        input("Press Enter to Continue...")
                elif user_roles_sel == 1:
                    email = input("Type in the User's Email [ OR Press Enter to return back to Menu ] : \n")
                    if email == "":
                        user_roles_menu_back = True
                    else:
                        role = input("Enter Role to Add: ")
                        addRemoveUserRoles(email, role, True)
                        print()
                        input("Press Enter to Continue...")
                elif user_roles_sel == 2:
                    email = input("Type in the User's Email [ OR Press Enter to return back to Menu ] : \n")
                    if email == "":
                        user_roles_menu_back = True
                    else:
                        role = input("Enter Role to Add: ")
                        addRemoveUserRoles(email, role, False)
                        print()
                        input("Press Enter to Continue...")
                elif user_roles_sel == 3:
                    user_roles_menu_back = True
                elif user_roles_sel == 4:
                    user_roles_menu_back = True
                    main_menu_exit = True
            user_roles_menu_back = False
        elif main_sel == 3:
            while not send_email_actions_menu_back:
                send_email_actions_sel = send_email_actions_menu.show()
                if send_email_actions_sel == 0:
                    email = input("Type in the User's Email [ OR Press Enter to return back to Menu ] : \n")
                    if email == "":
                        send_email_actions_menu_back = True
                    else:
                        sendActionsEmailToUser(email, "verify_email")
                        print()
                        input("Press Enter to Continue...")
                elif send_email_actions_sel == 1:
                    email = input("Type in the User's Email [ OR Press Enter to return back to Menu ] : \n")
                    if email == "":
                        send_email_actions_menu_back = True
                    else:
                        sendActionsEmailToUser(email, "update_pass")
                        print()
                        input("Press Enter to Continue...")
                elif send_email_actions_sel == 2:
                    send_email_actions_menu_back = True
                elif send_email_actions_sel == 3:
                    send_email_actions_menu_back = True
                    main_menu_exit = True
            send_email_actions_menu_back = False
        elif main_sel == 4:
            email = input("Type in the User's Email [ OR Press Enter to return back to Menu ] : \n")
            if email == "":
                main_menu_back = True
            else:
                print("Getting LDAP config for user: " + email)
                print()
                print(getUserLDAPConf(email))
                print()
                input("Press Enter to Continue...")
        elif main_sel == 5:
            main_menu_exit = True


def main():
    # check_and_install_dependencies()

    print_header()

    # INIT - READ IN KEYCLOAK CONFIG PARAMS
    global KEYCLOAK_CONFIG
    ini_file = os.path.dirname(os.path.realpath(__file__)) + os.sep + "keycloak_config.ini"
    # print(ini_file)
    KEYCLOAK_CONFIG = config(filename=ini_file)

    # GET THE AUTH TOKEN
    global AUTH_TOKEN
    AUTH_TOKEN = get_token()

    display_menu()


if __name__ == "__main__":
    main()
