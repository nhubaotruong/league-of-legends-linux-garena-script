import yaml
import sqlite3
import os

def main():
    riot_service_process_name = "RiotClientServices.exe"
    HOME = os.getenv("HOME")

    LUTRIS_DB_PATH = HOME + "/.local/share/lutris"
    LUTRIS_DB_NAME = "pga.db"
    conn = sqlite3.connect(LUTRIS_DB_PATH + "/" + LUTRIS_DB_NAME)
    c = conn.cursor()
    c.execute("SELECT configpath,directory FROM games WHERE slug='garena'")
    try:
        configpath, directory = c.fetchone()
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
        exec_path = ""
        for root, _, files in os.walk(directory):
            for file in files:
                if file == riot_service_process_name:
                    exec_path = os.path.join(root, file)
        if not exec_path:
            print("League of legends cannot be found in Garena folder")
            quit()
        try:
            game_config['game']['exe'] = exec_path
            yaml.dump(game_config, f, default_flow_style=False)
        except Exception as err:
            print(err)
            quit()

if __name__ == '__main__':
    main()