#!/usr/bin/env python3

import re
import requests
import sqlite3
import os
import stat


def main():
    HOME = os.getenv("HOME")
    LUTRIS_DB_PATH = HOME + "/.local/share/lutris"
    LUTRIS_DB_NAME = "pga.db"
    conn = sqlite3.connect(LUTRIS_DB_PATH + "/" + LUTRIS_DB_NAME)
    c = conn.cursor()
    c.execute("SELECT directory,configpath FROM games WHERE slug='league-of-legends'")
    try:
        directory, configpath = c.fetchone()
        conn.close()
    except Exception:
        print("No league of legends install from lutris found")
        conn.close()
        quit()

    LUTRIS_CONFIG_FOLDER = HOME + "/.config/lutris/games/"
    LUTRIS_LOL_CONFIG_FILE = LUTRIS_CONFIG_FOLDER + configpath + ".yml"

    launchhelper2_sh_path = os.path.join(directory, "launchhelper2.sh")
    launchhelper2_py_path = os.path.join(directory, "launchhelper2.py")
    injector_py_path = os.path.join(directory, "injector.py")

    print("Downloading launchhelper2.sh")
    with open(launchhelper2_sh_path, "w+", encoding="utf-8") as f:
        f.write(
            requests.get(
                "https://raw.githubusercontent.com/nhubaotruong/league-of-legends-linux-garena-script/main/fixes/12.5/launchhelper2.sh"
            ).text
        )
    launchhelper2_sh_st = os.stat(launchhelper2_sh_path)
    os.chmod(launchhelper2_sh_path, launchhelper2_sh_st.st_mode | stat.S_IEXEC)

    print("Downloading launchhelper2.py")
    with open(launchhelper2_py_path, "w+", encoding="utf-8") as f:
        f.write(
            requests.get(
                "https://raw.githubusercontent.com/CakeTheLiar/launchhelper/master/launchhelper2.py"
            ).text
        )

    print("Downloading injector.py")
    with open(injector_py_path, "w+", encoding="utf-8") as f:
        f.write(
            requests.get(
                "https://raw.githubusercontent.com/CakeTheLiar/launchhelper/master/injector.py"
            ).text
        )

    print(f"Updating {LUTRIS_LOL_CONFIG_FILE} with new prelaunch_command")

    with open(LUTRIS_LOL_CONFIG_FILE, "r", encoding="utf-8") as f:
        data = f.read()

    data_fixes = re.sub(
        r"prelaunch_command:\s+(.+)\n",
        f"prelaunch_command: {launchhelper2_sh_path}\n",
        data,
    )
    with open(LUTRIS_LOL_CONFIG_FILE, "w+", encoding="utf-8") as f:
        f.write(data_fixes)

    print("Please install some python dependencies as the fixes requires it")
    print("pip install psutil frida")


if __name__ == "__main__":
    main()
