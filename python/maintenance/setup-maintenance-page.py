#!/usr/local/bin/python

"""Setup Maintenance Pages for Jobstreet and JobsDB."""

import subprocess
import fileinput
import time
from git import Repo
import sys

# Some Globals

repo = ""
branch_name = ""
WORKER_ROUTES_JOBSTREET_FILE = "worker-routes-jobstreet.tf"
WORKER_ROUTES_JOBSDB_FILE = "worker-routes-jobsdb.tf"
WORKER_ROUTES_MAINTENANCE_FILE = "worker-routes-maintenance.tf"


def git_begin():
    """GIT initialize."""
    # repo = Repo.clone_from('git@github.com:seekasia/myjs.git', '.')
    repo = Repo('.')
    print(repo.branches)
    branch_name = input("Enter the branch name..: ")
    print(branch_name)
    print(f"Creating branch {branch_name}...")
    repo.git.checkout('-b', branch_name)


def update_files(scope):
    """Update the worker routes."""
    if scope == "all":
        with open(WORKER_ROUTES_JOBSTREET_FILE, 'w'):
            pass
        with open(WORKER_ROUTES_JOBSDB_FILE, 'w'):
            pass
        with fileinput.FileInput(WORKER_ROUTES_MAINTENANCE_FILE, inplace=True) as f:
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
        with open(WORKER_ROUTES_JOBSTREET_FILE, 'w'):
            pass
        with fileinput.FileInput(WORKER_ROUTES_MAINTENANCE_FILE, inplace=True) as f:
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
        with open(WORKER_ROUTES_JOBSDB_FILE, 'w'):
            pass
        with fileinput.FileInput(WORKER_ROUTES_MAINTENANCE_FILE, inplace=True) as f:
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


def git_complete():
    """GIT Complete."""
    input("Begin pushing into Git Repo ? .... Press Enter to Continue...")
    repo.git.add('--all')
    repo.git.commit('-m', 'maint page from py script')
    repo.git.push('--set-upstream', 'origin', branch_name)
    origin = repo.remote(name='origin')
    origin.push()


def main():
    """Entry point."""
    # git_begin()

    if len(sys.argv) < 2:
        print("Need a scope value...")
        sys.exit(1)

    update_files(sys.argv[1])

    # git_complete()


if __name__ == "__main__":
    main()
