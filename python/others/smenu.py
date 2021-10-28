#!/usr/bin/env python3
"""
Demonstration example for GitHub Project at
https://github.com/IngoMeyer441/simple-term-menu

This code only works in python3. Install per

    sudo pip3 install simple-term-menu

"""
import time

from simple_term_menu import TerminalMenu


def main():
    print()
    print("KEYCLOAK CLIENT UTITLITY...")
    print()
    main_menu_title = ""
    main_menu_items = ["Find Users", "Enable/Disable User", "User Roles", "Send Email Actions", "Get LDAP Config for User", "Quit"]
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
        clear_screen=False,
    )

    find_user_menu_title = "  Find Users\n"
    find_user_menu_items = ["by Email", "by First Name", "by Last Name", "Back to Main Menu"]
    find_user_menu_back = False
    find_user_menu = TerminalMenu(
        find_user_menu_items,
        title=find_user_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=False,
    )

    enable_disable_menu_title = "  Enable/Disable Users\n"
    enable_disable_menu_items = ["Enable", "Disable", "Back to Main Menu"]
    enable_disable_menu_back = False
    enable_disable_menu = TerminalMenu(
        enable_disable_menu_items,
        title=enable_disable_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=False,
    )

    user_roles_menu_title = "  User Roles\n"
    user_roles_menu_items = ["Get User Roles", "Add Role to User", "Remove Role from User", "Back to Main Menu"]
    user_roles_menu_back = False
    user_roles_menu = TerminalMenu(
        user_roles_menu_items,
        title=user_roles_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=False,
    )

    send_email_actions_menu_title = "  Send Email Actions\n"
    send_email_actions_menu_items = ["Send Verification", "Send Update Password", "Back to Main Menu"]
    send_email_actions_menu_back = False
    send_email_actions_menu = TerminalMenu(
        send_email_actions_menu_items,
        title=send_email_actions_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=False,
    )

    while not main_menu_exit:
        main_sel = main_menu.show()

        if main_sel == 0:
            while not find_user_menu_back:
                find_user_sel = find_user_menu.show()
                if find_user_sel == 0:
                    print("by Email Selected")
                    time.sleep(2)
                elif find_user_sel == 1:
                    print("by First Name Selected")
                    time.sleep(2)
                elif find_user_sel == 2:
                    print("by Last Name Selected")
                    time.sleep(2)
                elif find_user_sel == 3:
                    find_user_menu_back = True
                    print("Back Selected")
            find_user_menu_back = False
        elif main_sel == 1:
            while not enable_disable_menu_back:
                enable_disable_sel = enable_disable_menu.show()
                if enable_disable_sel == 0:
                    print("Enable Selected")
                    time.sleep(2)
                elif enable_disable_sel == 1:
                    print("Disable Selected")
                    time.sleep(2)
                elif enable_disable_sel == 2:
                    enable_disable_menu_back = True
                    print("Back Selected")
            enable_disable_menu_back = False
        elif main_sel == 2:
            while not user_roles_menu_back:
                user_roles_sel = user_roles_menu.show()
                if user_roles_sel == 0:
                    print("Get User Roles")
                    time.sleep(2)
                elif user_roles_sel == 1:
                    print("Add User Role")
                    time.sleep(2)
                elif user_roles_sel == 2:
                    print("Remove User Role")
                    time.sleep(2)
                elif user_roles_sel == 3:
                    user_roles_menu_back = True
                    print("Back Selected")
            user_roles_menu_back = False
        elif main_sel == 3:
            while not send_email_actions_menu_back:
                send_email_actions_sel = send_email_actions_menu.show()
                if send_email_actions_sel == 0:
                    print("Send Verification")
                    time.sleep(2)
                elif send_email_actions_sel == 1:
                    print("Send Update Password")
                    time.sleep(2)
                elif send_email_actions_sel == 2:
                    send_email_actions_menu_back = True
                    print("Back Selected")
            send_email_actions_menu_back = False
        elif main_sel == 4:
            print("Get LDAP Selected")
            time.sleep(2)
        elif main_sel == 5:
            main_menu_exit = True
            print("Quit Selected")


if __name__ == "__main__":
    main()
