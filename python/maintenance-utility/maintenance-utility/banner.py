#!/usr/local/bin/python

"""Setup Maintenance Banner Messages."""

import subprocess
import fileinput
import time
from git import Repo

# Some Globals

MAINT_JS_FILE = "maintenance-update.js"
ID_LANG_FILES = ['View/default/common/l10n/in_ID/header.lng',
                 'View/responsive/common/l10n/in_ID/header.lng',
                 'View/responsive/common/l10n/in_ID/jora-header.lng'
                 ]
EN_LANG_FILES = ['View/default/common/l10n/en_US/header.lng',
                 'View/responsive/common/l10n/en_US/header.lng',
                 'View/responsive/common/l10n/en_US/jora-header.lng'
                 ]
PROP_FILES = ['ant-props/live-id.properties',
              'ant-props/live.properties',
              'ant-props/stage.properties'
              ]

SHOW_BANNER_DAYS_BEFORE = 1
SHOW_STAGING_BANNER_DAYS_BEFORE = 3


def update_files():
    """Update all the required files with the appropriate maint start and end dates."""
    # Initialize the GIT repo
    repo_dir = input("Enter the path to the local MyJS code repo\n")
    repo = Repo(repo_dir)
    repo_dir = repo_dir+'/'
    # print(repo.branches)
    branch_name = input("Enter the branch name..: ")
    print(f"New branch name: {branch_name}")
    print()
    input("Begin creating new branch? .... Press Enter to Continue...")
    print(f"Creating branch {branch_name}...")
    repo.git.checkout('-b', branch_name)
    print()
    maint_start = input("Enter the Maintenance Start Date/Time in this format [2022-05-18T22:30:00]:\n")
    maint_end = input("Enter the Maintenance End Date/Time in this format [2022-05-19T06:30:00]:\n")

    toupdate_start = "const maintenance_start_time = '" + maint_start + "';"
    toupdate_end = "const maintenance_end_time = '" + maint_end + "';"

    # print("To update start: ", toupdate_start)
    # print("To update end: ", toupdate_end)

    print(f"Maint start: {maint_start}, Maint End: {maint_end}")
    print()
    input("Begin updating the files with the above values? .... Press Enter to Continue...")

    # replace the maintenance start and end values in the maintenance-update.js file
    print(f"Updating file : {MAINT_JS_FILE}... ")
    with fileinput.FileInput(repo_dir+MAINT_JS_FILE, inplace=True) as f:
        for line in f:
            if "const maintenance_start_time" in line:
                print(toupdate_start, end='')
                print()
                # print(line.replace("hello", "hello world"), end='')
            elif "const maintenance_end_time" in line:
                print(toupdate_end, end='')
                print()
            else:
                print(line, end='')
        time.sleep(0.5)

    # Run maintenance-update.js file and capture the output for the messages

    result = (subprocess.run(['node', repo_dir+'maintenance-update.js'], capture_output=True, encoding='UTF-8').stdout).split('\n')
    messages = {"en": result[3], "en_id": result[6], "id": result[9]}

    # print("SG...")
    # print(messages['en'])
    # print("ID in English...")
    # print(messages['en_id'])
    # print("ID...")
    # print(messages['id'])

    # messages are ready, replace the content in the lng files

    # ----------------------------------------------------------------------------------
    # Replace in the language files in default/common and responsive/common
    # ----------------------------------------------------------------------------------

    # In all the ID files
    id_msg_string = "LBL_SERVER_MAINTENANCE = Untuk melayani Anda lebih baik, kami akan melakukan maintenance pada " + messages['id'] + ". Selama maintenance, JobStreet.com tidak dapat diakses. Harap waspada terhadap penipuan yang rawan terjadi dengan adanya maintenance ini. Untuk kandidat, hindari undangan interview yang meminta bayaran dalam bentuk apapun (tiket pesawat, akomodasi, dll). Untuk perusahaan, hindari memberikan login ID dan password kepada siapapun dengan alasan apapun dan jangan mengklik link yang mencurigakan. Kami mohon maaf atas ketidaknyamanannya. Terima kasih."

    for idFile in ID_LANG_FILES:
        print(f"Updating file : {idFile}... ")
        with fileinput.FileInput(repo_dir+idFile, inplace=True) as f:
            for line in f:
                if "LBL_SERVER_MAINTENANCE =" in line:
                    print(id_msg_string, end='')
                    print()
                else:
                    print(line, end='')
        time.sleep(0.5)

    # In all the EN files
    en_msg_string_default = "LBL_SERVER_MAINTENANCE = To serve you better, our servers will be undergoing planned maintenance from " + messages['en'] + ". During the maintenance window, JobStreet.com will not be accessible. We regret the inconvenience caused. Kindly do not entertain any request of log-in or password during this exercise. If you receive such request, please contact our Customer Care at  info-my@jobstreet.com immediately."
    en_msg_string_my = "LBL_SERVER_MAINTENANCE_MY = To serve you better, our servers will be undergoing planned maintenance from " + messages['en'] + ". During the maintenance window, JobStreet.com will not be accessible. We regret the inconvenience caused. Kindly do not entertain any request of log-in or password during this exercise. If you receive such request, please contact our Customer Care at  info-my@jobstreet.com immediately."
    en_msg_string_sg = "LBL_SERVER_MAINTENANCE_SG = To serve you better, our servers will be undergoing planned maintenance from " + messages['en'] + ". During the maintenance window, JobStreet.com will not be accessible. We regret the inconvenience caused. Kindly do not entertain any request of log-in or password during this exercise. If you receive such request, please contact our Customer Care at  info-my@jobstreet.com immediately."
    en_msg_string_ph = "LBL_SERVER_MAINTENANCE_PH = To serve you better, our servers will be undergoing planned maintenance from " + messages['en'] + ". During the maintenance window, JobStreet.com will not be accessible. We regret the inconvenience caused. Kindly do not entertain any request of log-in or password during this exercise. If you receive such request, please contact our Customer Care at  info-my@jobstreet.com immediately."
    en_msg_string_id = "LBL_SERVER_MAINTENANCE_ID = In order to serve you better, we are going to run system maintenance on " + messages['en_id'] + ". During the maintenance, JobStreet.com cannot be accessed. Please beware of scam that tends to happen during this time. For candidates, please be careful of interview invitation that involves payment in any form (plane tickets, accommodation, and so on). For hirers, please do not give your Login ID and password to anyone with any reason and please do not click on suspicious link. We apologize for the inconvenience. Thank you for your attention."

    for enFile in EN_LANG_FILES:
        print(f"Updating file : {enFile}... ")
        with fileinput.FileInput(repo_dir+enFile, inplace=True) as f:
            for line in f:
                if "LBL_SERVER_MAINTENANCE_MY =" in line:
                    print(en_msg_string_my, end='')
                    print()
                elif "LBL_SERVER_MAINTENANCE_SG =" in line:
                    print(en_msg_string_sg, end='')
                    print()
                elif "LBL_SERVER_MAINTENANCE_PH =" in line:
                    print(en_msg_string_ph, end='')
                    print()
                elif "LBL_SERVER_MAINTENANCE_ID =" in line:
                    print(en_msg_string_id, end='')
                    print()
                elif "LBL_SERVER_MAINTENANCE =" in line:
                    print(en_msg_string_default, end='')
                    print()
                else:
                    print(line, end='')
        time.sleep(0.5)

    # ----------------------------------------------------------------------------------
    # Replace in properties files
    # ant-props/live-id.properties
    # ant-props/live.properties
    # ant-props/stage.properties
    # ----------------------------------------------------------------------------------

    # maint_start_date = maint_start.split("T")[0].split("-")
    # maint_end_date = maint_start.split("T")[0].split("-")
    # maint_stage_start_date = maint_start.split("T")[0].split("-")
    # maint_stage_end_date = maint_start.split("T")[0].split("-")
    # maint_start_date.reverse()
    # maint_end_date.reverse()
    # maint_stage_start_date.reverse()
    # maint_stage_end_date.reverse()
    # maint_start_date[0] = str(int(maint_start_date[0])-SHOW_BANNER_DAYS_BEFORE)
    # maint_stage_start_date[0] = str(int(maint_stage_start_date[0])-SHOW_STAGING_BANNER_DAYS_BEFORE)

    # # print(f"For Staging using this start date: {maint_stage_start_date}")

    # update_props_start = "config.app.serverMaintenance.startDate = " + "'" + "-".join(maint_start_date) + " " + "00:00:00" + "'"
    # update_props_end = "config.app.serverMaintenance.endDate =  " + "'" + "-".join(maint_end_date) + " " + "22:00:00" + "'"

    # update_stage_props_start = "config.app.serverMaintenance.startDate = " + "'" + "-".join(maint_stage_start_date) + " " + "00:00:00" + "'"
    # update_stage_props_end = "config.app.serverMaintenance.endDate =  " + "'" + "-".join(maint_stage_end_date) + " " + "22:00:00" + "'"

    # for pFile in PROP_FILES:
    #     print(f"Updating file : {pFile}... ")
    #     if "stage." in pFile:
    #         staging = True
    #     else:
    #         staging = False
    #     with fileinput.FileInput(repo_dir+pFile, inplace=True) as f:
    #         for line in f:
    #             if "config.app.serverMaintenance.startDate =" in line:
    #                 if staging:
    #                     print(update_stage_props_start, end='')
    #                     print()
    #                 else:
    #                     print(update_props_start, end='')
    #                     print()
    #             elif "config.app.serverMaintenance.endDate =" in line:
    #                 if staging:
    #                     print(update_stage_props_end, end='')
    #                     print()
    #                 else:
    #                     print(update_props_end, end='')
    #                     print()
    #             else:
    #                 print(line, end='')
        # time.sleep(0.5)
    print()
    input("Files updated... Push to Git Repo ? .... Press Enter to Continue...")
    repo.git.add('--all')
    commit_msg = input("Enter the Git Commit message: \n")
    repo.git.commit('-m', commit_msg)
    repo.git.push('--set-upstream', 'origin', branch_name)
    origin = repo.remote(name='origin')
    origin.push()


def main():
    """Entry point."""
    # git_begin()

    update_files()

    # git_complete()


if __name__ == "__main__":
    main()
