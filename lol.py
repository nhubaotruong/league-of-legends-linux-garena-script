import psutil
import os
import yaml
import sqlite3

def findProcessIdByName(processName):
    """
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    """
    # Iterate over the all the running process
    while True:
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=["cmdline", "name", "pid"])
                # Check if process name contains the given name string.
                if processName.lower() in pinfo["name"].lower():
                    return pinfo
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

def main():
    riot_service_process_name = "RiotClientServices.exe"

    # Get RiotClientServices.exe process
    riot_process = findProcessIdByName(riot_service_process_name)

    # Programmatically get RiotClientServices.exe arguments
    try:
        riot_argument = " ".join(riot_process.get("cmdline", [])[1:]).strip()
    except Exception:
        print("Cannot get Garena Token")
    
    # Exit if no riot_argument is found
    if not riot_argument:
        quit()

    print(riot_argument)

    # Kill the current RiotClientServices.exe
    p = psutil.Process(riot_process.get("pid"))
    p.kill()

    # Start game using lutris
    HOME = os.getenv("HOME")
    LUTRIS_CONFIG_FOLDER = HOME + "/.config/lutris/games/"
    LUTRIS_LOL_CONFIG_FILE = LUTRIS_CONFIG_FOLDER + os.popen(f'ls {LUTRIS_CONFIG_FOLDER} | grep -i -E league.*.yml').read().strip()
    
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
    
    LUTRIS_DB_PATH = HOME + "/.local/share/lutris"
    LUTRIS_DB_NAME = "pga.db"
    conn = sqlite3.connect(LUTRIS_DB_PATH + "/" + LUTRIS_DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id FROM games WHERE slug='league-of-legends'")
    try:
        game_id =  c.fetchone()[0]
        conn.close()
    except Exception:
        print("No league of legends install from lutris found")
        conn.close()
        quit()
    
    print(f"lutris game id: {game_id}")
    launch_command = f"lutris lutris:rungameid/{game_id}"
    os.system(launch_command)
    

if __name__ == '__main__':
    main()