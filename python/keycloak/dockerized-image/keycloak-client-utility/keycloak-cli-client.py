#!/usr/local/bin/python

import argparse
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


def config(filename='./config/keycloak_config.ini', section='keycloak'):
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
    printProgressBar(0, l, prefix='Connecting:', suffix='Complete', length=50)
    for i, item in enumerate(items):
        # Do stuff...
        time.sleep(0.02)
        # Update Progress Bar
        printProgressBar(i + 1, l, prefix='Connecting:', suffix='Complete', length=50)


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


def argParserConfig():
    # create parser object
    parser = argparse.ArgumentParser(description="KeyCloak Client Utility!")
    # defining arguments for parser object
    parser.add_argument("--get_user_count", action='store_true', 
                        help="Get users by First Name.")
    parser.add_argument("--get_users_by_fname", type=str, nargs=1,
                        metavar="first_name", default=None,
                        help="Get users by First Name.")
    parser.add_argument("--get_users_by_lname", type=str, nargs=1,
                        metavar="last_name", default=None,
                        help="Get users by Last Name.")
    parser.add_argument("--get_users_by_email", type=str, nargs=1,
                        metavar="user_email", default=None,
                        help="Get users by email.")
    parser.add_argument("--get_ldap_conf", type=str, nargs=1,
                        metavar="user_email", default=None,
                        help="Get the LDAP configuration of the user.")
    parser.add_argument("--get_user_roles", type=str, nargs=1,
                        metavar="user_email", default=None,
                        help="Get the Roles mapped to the user.")
    parser.add_argument("--add_user_roles", type=str, nargs=2,
                        metavar=("user_email", "role_to_add"),
                        help="Add Roles to the user.")
    parser.add_argument("--remove_user_roles", type=str, nargs=2,
                        metavar=("user_email", "role_to_remove"),
                        help="Remove Roles from user.")
    parser.add_argument("--enable_user", type=str, nargs=1,
                        metavar="user_email", default=None,
                        help="Enable the user.")
    parser.add_argument("--disable_user", type=str, nargs=1,
                        metavar="user_email", default=None,
                        help="Disable the user.")
    parser.add_argument("--send_verify_email", type=str, nargs=1,
                        metavar="user_email", default=None,
                        help="Send Account Verification Email to the user.")
    parser.add_argument("--send_update_pass_email", type=str, nargs=1,
                        metavar="user_email", default=None,
                        help="Send Update Password Email to the user.")
    return parser


def call_methods(args):
    # calling functions depending on type of argument
    if args.get_user_count:
        print()
        print("Total number of users : " + str(getUserCount()))
    elif args.enable_user is not None:
        print("Enabling user: " + args.enable_user[0])
        print()
        enableDisableUser(args.enable_user[0], True)
    elif args.disable_user is not None:
        print("Disabling user: " + args.disable_user[0])
        print()
        enableDisableUser(args.disable_user[0], False)
    elif args.send_verify_email is not None:
        print("Sending verification email for user: " + args.send_verify_email[0])
        print()
        sendActionsEmailToUser(args.send_verify_email[0], "verify_email")
    elif args.send_update_pass_email is not None:
        print("Sending update password email for user: " + args.send_update_pass_email[0])
        print()
        sendActionsEmailToUser(args.send_update_pass_email[0], "update_pass")
    elif args.get_ldap_conf is not None:
        print("Getting LDAP config for user: " + args.get_ldap_conf[0])
        print()
        print(getUserLDAPConf(args.get_ldap_conf[0]))
    elif args.get_user_roles is not None:
        print("Getting Roles mapped for user: " + args.get_user_roles[0])
        print()
        roles = getUserRoles(args.get_user_roles[0])
        print()
        print('Assigned Roles : ')
        for r in roles:
            print('\t', r)
    elif args.add_user_roles is not None:
        print("Adding Role : " + args.add_user_roles[1] + " to user : " + args.add_user_roles[0])
        print()
        addRemoveUserRoles(args.add_user_roles[0], args.add_user_roles[1], True)
    elif args.remove_user_roles is not None:
        print("Removing Role : " + args.remove_user_roles[1] + " from user : " + args.remove_user_roles[0])
        print()
        addRemoveUserRoles(args.remove_user_roles[0], args.remove_user_roles[1], False)
    elif args.get_users_by_email is not None:
        print("Getting users by email : " + args.get_users_by_email[0])
        print()
        users = getUsersByEmail(args.get_users_by_email[0])
        if not len(users) > 0:
            print(Fore.RED + "No user with email: '" + args.get_users_by_email[0] + "' found...")
            sys.exit(0)
        print_user_list(users)
    elif args.get_users_by_fname is not None:
        print("Getting users by First Name: " + args.get_users_by_fname[0])
        print()
        users = getUsersByName(firstname=args.get_users_by_fname[0])
        if not len(users) > 0:
            print(Fore.RED + "No user with FirstName: '" + args.get_users_by_fname[0] + "' found...")
            sys.exit(0)
        print_user_list(users)
    elif args.get_users_by_lname is not None:
        print("Getting users by Last Name: " + args.get_users_by_lname[0])
        print()
        users = getUsersByName(lastname=args.get_users_by_lname[0])
        if not len(users) > 0:
            print(Fore.RED + "No user with LastName: '" + args.get_users_by_lname[0] + "' found...")
            sys.exit(0)
        print_user_list(users)


def print_footer():
    print()
    print("=" * 80)


def main():
    # check_and_install_dependencies()

    parser = argParserConfig()

    # parse the arguments from standard input
    args = parser.parse_args()

    # print help message and exit if no arguments passed in
    if not len(sys.argv) > 1:
        parser.print_help()
        sys.exit()

    print_header()

    # INIT - READ IN KEYCLOAK CONFIG PARAMS
    global KEYCLOAK_CONFIG
    ini_file = os.path.dirname(os.path.realpath(__file__)) + os.sep + "config/keycloak_config.ini"
    # print(ini_file)
    KEYCLOAK_CONFIG = config(filename=ini_file)

    # GET THE AUTH TOKEN
    global AUTH_TOKEN
    AUTH_TOKEN = get_token()

    call_methods(args)

    print_footer()


if __name__ == "__main__":
    main()
