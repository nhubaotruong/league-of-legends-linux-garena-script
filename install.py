import subprocess
import time

def main():
    subprocess.Popen(
        "env LUTRIS_SKIP_INIT=1 lutris -i https://raw.githubusercontent.com/nhubaotruong/league-of-legends-linux-garena-script/main/garena.json",
        shell=True,
    )
    subprocess.Popen(
        "env LUTRIS_SKIP_INIT=1 lutris -i https://lutris.net/api/installers/league-of-legends-standard-launch-help?format=json",
        shell=True,
    )

    command = "zenity --info --no-wrap --text='Close all lutris windows after everything is done'"
    subprocess.run(command, shell=True)

    while True:
        time.sleep(1)
        res = subprocess.run("pgrep -f lutris", shell=True, capture_output=True)
        if res.stdout == b"" and res.stderr == b"":
            break
    
    command2 = "zenity --info --no-wrap --text='Open Garena and install LOL\nThen back to the github (https://github.com/nhubaotruong/league-of-legends-linux-garena-script) for config guide'"
    subprocess.run(command2, shell=True)
    

if __name__ == '__main__':
    main()