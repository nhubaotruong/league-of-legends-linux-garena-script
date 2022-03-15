#!/usr/bin/env python3

import psutil
import os
import yaml
import sqlite3
import re
import time


def find_process_id_by_name(processName):
    """
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    """
    # Iterate over the all the running process
    while True:
        time.sleep(1)
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=["cmdline", "name", "pid"])
                # Check if process name contains the given name string.
                if processName.lower() in pinfo["name"].lower():
                    return pinfo
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass


def kill_old_league_and_riot_process():
    RIOT_AND_LEAGUE_PROCESS_REGEX = re.compile("(league|riot).*\.exe", flags=re.I)
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=["name", "pid"])
            # Check if process name contains the given name string.
            if RIOT_AND_LEAGUE_PROCESS_REGEX.search(pinfo.get("name")):
                print(
                    f"Found old process still running: {pinfo.get('name')}, pid: {pinfo.get('pid')}"
                )
                p = psutil.Process(pinfo.get("pid"))
                p.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


def main():
    riot_service_process_name = "RiotClientServices.exe"

    print(
        f"The script will wait for a {riot_service_process_name} process to show up to get it's token. So go to the Garena client and press Play"
    )
    kill_old_league_and_riot_process()

    # Get RiotClientServices.exe process
    riot_process = find_process_id_by_name(riot_service_process_name)

    # Programmatically get RiotClientServices.exe arguments
    try:
        riot_argument = " ".join(riot_process.get("cmdline", [])[1:]).strip()
    except Exception:
        print("Cannot get Garena Token")

    # Exit if no riot_argument is found
    if not riot_argument:
        quit()

    print(f"Garena token got from {riot_service_process_name}: {riot_argument}")

    # Kill the current RiotClientServices.exe
    p = psutil.Process(riot_process.get("pid"))
    p.kill()

    # Start game using lutris
    HOME = os.getenv("HOME")

    LUTRIS_DB_PATH = HOME + "/.local/share/lutris"
    LUTRIS_DB_NAME = "pga.db"
    conn = sqlite3.connect(LUTRIS_DB_PATH + "/" + LUTRIS_DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id,configpath FROM games WHERE slug='league-of-legends'")
    try:
        game_id, configpath = c.fetchone()
        conn.close()
    except Exception:
        print("No league of legends install from lutris found")
        conn.close()
        quit()

    LUTRIS_CONFIG_FOLDER = HOME + "/.config/lutris/games/"
    LUTRIS_LOL_CONFIG_FILE = LUTRIS_CONFIG_FOLDER + configpath + ".yml"

    with open(LUTRIS_LOL_CONFIG_FILE, "r") as f:
        try:
            game_config = yaml.load(f, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)
            quit()

    with open(LUTRIS_LOL_CONFIG_FILE, "w") as f:
        game_config["game"]["args"] = riot_argument
        try:
            yaml.dump(game_config, f, default_flow_style=False)
        except yaml.YAMLError as exc:
            print(exc)
            quit()

    print("Starting game with current config:")
    print(f"- Wine version: {game_config.get('wine',{}).get('version')}")
    print(f"- Executable: {game_config.get('game',{}).get('exe')}")
    print(f"- Wineprefix: {game_config.get('game',{}).get('prefix')}")

    print(
        "If this is your first time running LOL since reboot, a pop up will appear, chose the first or second option then enter your password\n"
    )
    print("It's a workaround by the lutris community\n")
    print("Ignore the lines below, they are not actually error\n")
    launch_command = f"lutris lutris:rungameid/{game_id}"
    os.system(launch_command)


if __name__ == "__main__":
    main()
