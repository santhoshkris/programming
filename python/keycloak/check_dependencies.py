import sys
import subprocess
import shlex

def check_and_install_dependencies():
    if sys.hexversion <= 0x3000000:
        print("Need Python 3 to execute this... Please install the same and re-run.")
        sys.exit(0)
    try:
        import colorama
        import requests
        import simple_term_menu
    except ImportError or ModuleNotFoundError:
        print("Installing dependencies : python libraries...")
        subprocess.check_output(shlex.split("pip3 install -r requirements.txt"), stderr=subprocess.STDOUT)

    print()
    print("All good, everything looks fine now. You can run the keycloak client utility...")
    print("By running   - python ./keycloak-cli-client.py  for the CLI version")
    print("OR           - python ./keycloak-menu-client.py for the Menu version")
    print()

check_and_install_dependencies()
