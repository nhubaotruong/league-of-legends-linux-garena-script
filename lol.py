import psutil
import os
import yaml
import sqlite3

riot_service_process_name = "RiotClientServices.exe"

# Don't need these if using lutris
HOME = os.getenv("HOME")
# WINEPREFIX create by https://lutris.net/games/league-of-legends/
launchhelper = HOME + "/Games/league-of-legends/launchhelper.sh"
WINEPREFIX = HOME + "/Games/league-of-legends"

# Game install location
game_path = (
    HOME
    + "/Games/league-of-legends/drive_c/Garena/Games/32787/Riot Client/RiotClientServices.exe"
)

# Wine lol download from lutris
wine_exe = HOME + "/.local/share/lutris/runners/wine/lutris-lol-5.5-2-x86_64/bin/wine"

# Use gamemode
use_gamemoderun = True

# Enable esync
use_esync = True

# Enable fsync
use_fsync = True


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
LUTRIS_CONFIG_FOLDER = HOME + "/.config/lutris/games/"
# LUTRIS_LOL_CONFIG_FILE = glob.glob(LUTRIS_CONFIG_FOLDER + "league*.yml")[0]
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

lutris_db_path = HOME + "/.local/share/lutris"
lutris_db_name = "pga.db"
conn = sqlite3.connect(lutris_db_path + "/" + lutris_db_name)
c = conn.cursor()
c.execute("SELECT id FROM games WHERE slug='league-of-legends'")
try:
    game_id =  c.fetchone()[0]
except Exception:
    print("No league of legends install from lutris found")
    quit()

conn.close()

print(f"lutris game id: {game_id}")
launch_command = f"lutris lutris:rungameid/{game_id}"
os.system(launch_command)

# Kill Garena
# os.system("wineserver -k")

# Start game using correct setup
# Keep in mind the client will take awhile to start, after that you can play like normal
# No garena while playing though
# launch_command = f'env WINEPREFIX={WINEPREFIX} WINEESYNC={1 if use_esync else 0} WINEFSYNC={1 if use_fsync else 0} {"gamemoderun " if use_gamemoderun else ""}"{wine_exe}" "{game_path}" {riot_argument} & "{launchhelper}"'
# os.system(launch_command)

