#!/usr/bin/env python3

import os
import shutil


def main():
    os.system(
        "env LUTRIS_SKIP_INIT=1 lutris -i https://raw.githubusercontent.com/nhubaotruong/league-of-legends-linux-garena-script/main/garena.json",
    )
    print("Close all lutris window when you're done\n")

    os.system(
        "env LUTRIS_SKIP_INIT=1 lutris -i https://raw.githubusercontent.com/nhubaotruong/league-of-legends-linux-garena-script/main/lol.json"
    )

    print("Close all lutris windows after everything is done\n")

    if shutil.which("pip3"):
        print("Installing python dependencies to user directory")
        os.system("pip3 install --user psutil frida pyyaml")
    else:
        print("Please install python-pip from your distro repo and run")
        print("pip3 install --user psutil frida pyyaml")

    print("")
    print("Open Garena and install LOL, just left the install path as default\n")
    print("After it is done instaling, run\n")
    print(
        "curl https://raw.githubusercontent.com/nhubaotruong/league-of-legends-linux-garena-script/main/config.py | python\n"
    )
    print("to auto configure the Executable for LOL\n")
    print("Or you can just go and manually configure it following the config section\n")
    print(
        "https://github.com/nhubaotruong/league-of-legends-linux-garena-script/tree/main-python#config-lol-lutris\n"
    )


if __name__ == "__main__":
    main()
