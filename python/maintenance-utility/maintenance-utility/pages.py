#!/usr/local/bin/python

"""Setup Maintenance Pages for Jobstreet and JobsDB."""

import fileinput
import time
from git import Repo
import sys

# Some Globals

WORKER_ROUTES_JOBSTREET_FILE = "worker-routes-jobstreet.tf"
WORKER_ROUTES_JOBSDB_FILE = "worker-routes-jobsdb.tf"
WORKER_ROUTES_MAINTENANCE_FILE = "worker-routes-maintenance.tf"
README_FILE = "README.md"

JDB_OTHER_MAINT_ROUTING = '''
## ------
## Other JDB
## ------
resource "cloudflare_worker_route" "jobsdb_msite_maintenance" {
  zone_id     = var.cloudflare_jobsdb_com_zone_id
  pattern     = "m.jobsdb.com/*"
  script_name = "maintenance-routing"
  depends_on  = ["cloudflare_worker_script.maintenance-routing"]
}

resource "cloudflare_worker_route" "jobsdb_rms_maintenance" {
  zone_id     = var.cloudflare_jobsdb_com_zone_id
  pattern     = "rms.jobsdb.com/*"
  script_name = "maintenance-routing"
  depends_on  = ["cloudflare_worker_script.maintenance-routing"]
}

resource "cloudflare_worker_route" "jobsdb_rms_th_maintenance" {
  zone_id     = var.cloudflare_jobsdb_co_th_zone_id
  pattern     = "rms.jobsdb.co.th/*"
  script_name = "maintenance-routing"
  depends_on  = ["cloudflare_worker_script.maintenance-routing"]
}
'''
JOBSTREET_GLOBAL_MAINT = '''
## ------
## JobStreet (global)
## ------
resource "cloudflare_worker_route" "jobstreet_global_maintenance" {
  zone_id     = var.cloudflare_jobstreet_com_zone_id
  pattern     = "*.jobstreet.com/*"
  script_name = "maintenance-routing"
  depends_on  = ["cloudflare_worker_script.maintenance-routing"]
}

'''


def update_files(action='deploy', scope='all'):
    """Update the worker routes."""
    repo_dir = input("Enter the path to the local Cloudflare-Workers code repo\n")
    if repo_dir == '':
        return
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
    print("Updating files...")
    time.sleep(1)
    if action == 'deploy':
        if scope == "all":
            with open(repo_dir+WORKER_ROUTES_JOBSTREET_FILE, 'w'):
                pass
            with open(repo_dir+WORKER_ROUTES_JOBSDB_FILE, 'w'):
                pass
            with open(repo_dir+WORKER_ROUTES_MAINTENANCE_FILE, 'r') as f:
                existing_content = f.read()
            with open(repo_dir+WORKER_ROUTES_MAINTENANCE_FILE, 'w') as f:
                f.write(JDB_OTHER_MAINT_ROUTING)
                f.write(JOBSTREET_GLOBAL_MAINT)
            with open(repo_dir+WORKER_ROUTES_MAINTENANCE_FILE, 'a') as f:
                f.write(existing_content)

            with fileinput.FileInput(repo_dir+WORKER_ROUTES_MAINTENANCE_FILE, inplace=True) as f:
                for line in f:
                    if "m.jobsdb.com/maintenance*" in line:
                        print('  pattern     = "m.jobsdb.com/*"', end='')
                        print()
                    elif "rms.jobsdb.com/maintenance*" in line:
                        print('  pattern     = "rms.jobsdb.com/*"', end='')
                        print()
                    elif "rms.jobsdb.co.th/maintenance*" in line:
                        print('  pattern     = "rms.jobsdb.co.th/*"', end='')
                        print()
                    elif "hk.jobsdb.com" in line:
                        print('  pattern     = "hk.jobsdb.com/*"', end='')
                        print()
                    elif "th.jobsdb.com/th/en/maintenance*" in line:
                        print('  pattern     = "th.jobsdb.com/*"', end='')
                        print()
                    elif "www.jobstreet.com.sg/maintenance*" in line:
                        print('  pattern     = "*.jobstreet.com.sg/*"', end='')
                        print()
                    elif "www.jobstreet.com.my/maintenance*" in line:
                        print('  pattern     = "*.jobstreet.com.my/*"', end='')
                        print()
                    elif "www.jobstreet.com.ph/maintenance*" in line:
                        print('  pattern     = "*.jobstreet.com.ph/*"', end='')
                        print()
                    elif "www.jobstreet.co.id/maintenance*" in line:
                        print('  pattern     = "*.jobstreet.co.id/*"', end='')
                        print()
                    else:
                        print(line, end='')
        elif scope == "myjs":
            with open(repo_dir+WORKER_ROUTES_JOBSTREET_FILE, 'w'):
                pass
            with open(repo_dir+WORKER_ROUTES_MAINTENANCE_FILE, 'r') as f:
                existing_content = f.read()
            with open(repo_dir+WORKER_ROUTES_MAINTENANCE_FILE, 'w') as f:
                f.write(JOBSTREET_GLOBAL_MAINT)
            with open(repo_dir+WORKER_ROUTES_MAINTENANCE_FILE, 'a') as f:
                f.write(existing_content)
            with fileinput.FileInput(repo_dir+WORKER_ROUTES_MAINTENANCE_FILE, inplace=True) as f:
                for line in f:
                    if "www.jobstreet.com/maintenance*" in line:
                        print('  pattern     = "*.jobstreet.com/*"', end='')
                        print()
                    elif "www.jobstreet.com.sg/maintenance*" in line:
                        print('  pattern     = "*.jobstreet.com.sg/*"', end='')
                        print()
                    elif "www.jobstreet.com.my/maintenance*" in line:
                        print('  pattern     = "*.jobstreet.com.my/*"', end='')
                        print()
                    elif "www.jobstreet.com.ph/maintenance*" in line:
                        print('  pattern     = "*.jobstreet.com.ph/*"', end='')
                        print()
                    elif "www.jobstreet.co.id/maintenance*" in line:
                        print('  pattern     = "*.jobstreet.co.id/*"', end='')
                        print()
                    else:
                        print(line, end='')
        elif scope == "jdb":
            with open(repo_dir+WORKER_ROUTES_JOBSDB_FILE, 'w'):
                pass
            with open(repo_dir+WORKER_ROUTES_MAINTENANCE_FILE, 'r') as f:
                existing_content = f.read()
            with open(repo_dir+WORKER_ROUTES_MAINTENANCE_FILE, 'w') as f:
                f.write(JDB_OTHER_MAINT_ROUTING)
            with open(repo_dir+WORKER_ROUTES_MAINTENANCE_FILE, 'a') as f:
                f.write(existing_content)
            with fileinput.FileInput(repo_dir+WORKER_ROUTES_MAINTENANCE_FILE, inplace=True) as f:
                for line in f:
                    if "m.jobsdb.com/maintenance*" in line:
                        print('  pattern     = "m.jobsdb.com/*"', end='')
                        print()
                    elif "rms.jobsdb.com/maintenance*" in line:
                        print('  pattern     = "rms.jobsdb.com/*"', end='')
                        print()
                    elif "rms.jobsdb.co.th/maintenance*" in line:
                        print('  pattern     = "rms.jobsdb.co.th/*"', end='')
                        print()
                    elif "hk.jobsdb.com" in line:
                        print('  pattern     = "hk.jobsdb.com/*"', end='')
                        print()
                    elif "th.jobsdb.com/th/en/maintenance*" in line:
                        print('  pattern     = "th.jobsdb.com/*"', end='')
                        print()
                    else:
                        print(line, end='')
        else:
            print("Valid scope required...")
            sys.exit(1)
    elif action == 'undeploy':
        with open(repo_dir+README_FILE, 'a') as f:
            f.write('-')
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
    if len(sys.argv) < 3:
        print("Need an action and a scope value...")
        sys.exit(1)

    update_files(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
