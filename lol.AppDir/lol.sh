#!/bin/sh

HERE="$(dirname "$(readlink -f "${0}")")"
LUTRIS_DB="$HOME/.local/share/lutris/pga.db"
RIOT_SERVICES_EXE="RiotClientServices.exe"
LOL_GAME_CONFIG_PATH="$(find "$HOME/.config/lutris/games" -type f -name "$("$HERE"/usr/bin/sqlite3 "$LUTRIS_DB" "SELECT configpath FROM games WHERE slug='league-of-legends'").*")"

kill_lol_processes() {
    if [ "$(pgrep -f "[L]eague.*.exe")" ]; then
        pgrep -f "[L]eague.*.exe" | xargs kill -9
    fi
    if [ "$(pgrep -f "[R]iot.*.exe")" ]; then
        pgrep -f "[R]iot.*.exe" | xargs kill -9
    fi
}

case "$1" in
"help")
    echo "USAGE: Run this program with no arguments to play LOL. Else:"
    echo "      install         install Garena and LOL environment to play"
    echo "                      use SKIP_INSTALL_GARENA env to skip Garena"
    echo "                      use SKIP_INSTALL_LOL env to skip LOL"
    echo "      help            print usage"
    ;;
"install")
    if [ "$SKIP_INSTALL_GARENA" != "1" ]; then
        echo "Installing Garena, close lutris when done"
        env LUTRIS_SKIP_INIT=1 lutris -i https://raw.githubusercontent.com/nhubaotruong/league-of-legends-linux-garena-script/main/garena.json
    fi

    # Install LOL
    if [ "$SKIP_INSTALL_LOL" != "1" ]; then
        echo "Installing LOL env, close lutris when done"
        wget "https://lutris.net/api/installers/league-of-legends-standard-launch-help?format=json" -O /tmp/lol.json
        "$HERE"/usr/bin/yq e -i 'del(.results[0].script.files[0]) | del(.results[0].script.installer[0]) | del(.results[0].script.installer[1])' /tmp/lol.json
        env LUTRIS_SKIP_INIT=1 lutris -i /tmp/lol.json
    fi
    ;;
"config")
    GARENA_WINE_PREFIX="$("$HERE"/usr/bin/sqlite3 "$LUTRIS_DB" "SELECT directory FROM games WHERE slug='garena'")"
    if [ "$GARENA_WINE_PREFIX" = "" ]; then
        echo "No Garena install from lutris found"
        exit
    fi
    EXEC_PATH="$(find "$GARENA_WINE_PREFIX" -type f -name "$RIOT_SERVICES_EXE")"
    if [ "$EXEC_PATH" = "" ]; then
        echo "Garena LOL isn't installed in $GARENA_WINE_PREFIX"
        exit
    fi

    "$HERE"/usr/bin/yq e -i ".game.exe=\"$EXEC_PATH\"" "$LOL_GAME_CONFIG_PATH"
    ;;
"")
    echo "The script will wait for a $RIOT_SERVICES_EXE process to show up to get it's token. So go to the Garena client and press Play"
    echo ""
    kill_lol_processes
    until [ "$(pidof $RIOT_SERVICES_EXE)" ]; do
        sleep 2
    done
    RIOT_PROCESS="$(ps -p "$(pidof $RIOT_SERVICES_EXE)" -o args | sed 1d)"
    RIOT_ARGS="--${RIOT_PROCESS#*--}"
    kill_lol_processes
    "$HERE"/usr/bin/yq e -i ".game.args=\"$RIOT_ARGS\"" "$LOL_GAME_CONFIG_PATH"
    GAME_ID="$("$HERE"/usr/bin/sqlite3 "$LUTRIS_DB" "SELECT id FROM games WHERE slug='league-of-legends'")"
    echo "Garena token got from $RIOT_SERVICES_EXE: $RIOT_ARGS"
    echo ""
    echo "Starting game with config:"
    echo "- Wine version: $("$HERE"/usr/bin/yq e '.wine.version' "$LOL_GAME_CONFIG_PATH")"
    echo "- Executable: $("$HERE"/usr/bin/yq e '.game.exe' "$LOL_GAME_CONFIG_PATH")"
    echo "- Wineprefix: $("$HERE"/usr/bin/yq e '.game.prefix' "$LOL_GAME_CONFIG_PATH")"
    echo ""
    echo "If this is your first time running LOL since reboot, a pop up will appear, chose the first or second option then enter your password"
    echo ""
    echo "It's a workaround by the lutris community"
    lutris lutris:rungameid/"$GAME_ID"
    ;;
esac
