# Those who cannot start LOL after the 11.17 update check here: [Update to newer wine-lol version](#update-new-wine-lol)
# Instructions for getting the latest wine-lol are [here](https://old.reddit.com/r/leagueoflinux/comments/pb4wqy/did_the_upgrade_to_cef91_as_part_of_1117_break/hab2oe0/)
# You can also refer to [r/leagueoflinux](https://www.reddit.com/r/leagueoflinux/) for frequent updates regarding the game on linux

# Note: This is the way I personally use to start LOL on Linux, through lutris. The code for starting game without Lutris is still in the script though
## Wine Dependency (Maybe redundant, but just to be sure nothing goes wrong)
**Source:** [https://www.gloriouseggroll.tv/how-to-get-out-of-wine-dependency-hell/](https://www.gloriouseggroll.tv/how-to-get-out-of-wine-dependency-hell/)

### Antergos/Manjaro/Arch derivatives (enable multilib in pacman.conf):
```
sudo pacman -Sy
sudo pacman -S wine-staging winetricks
sudo pacman -S giflib lib32-giflib libpng lib32-libpng libldap lib32-libldap gnutls lib32-gnutls mpg123 lib32-mpg123 openal lib32-openal v4l-utils lib32-v4l-utils libpulse lib32-libpulse alsa-plugins lib32-alsa-plugins alsa-lib lib32-alsa-lib libjpeg-turbo lib32-libjpeg-turbo libxcomposite lib32-libxcomposite libxinerama lib32-libxinerama ncurses lib32-ncurses opencl-icd-loader lib32-opencl-icd-loader libxslt lib32-libxslt libva lib32-libva gtk3 lib32-gtk3 gst-plugins-base-libs lib32-gst-plugins-base-libs vulkan-icd-loader lib32-vulkan-icd-loader cups samba dosbox
```
### Solus:
```
sudo eopkg install wine wine-devel wine-32bit-devel winetricks
```
### Ubuntu:
```
wget -nc https://dl.winehq.org/wine-builds/winehq.key
sudo apt-key add winehq.key
sudo apt-add-repository 'https://dl.winehq.org/wine-builds/ubuntu/'
sudo apt update
sudo apt install --install-recommends winehq-staging
sudo apt install winetricks
```
### Fedora:

Enable RPM Fusion repo
```
sudo dnf install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
```
```
sudo dnf install lutris wine winetricks
```

```
sudo dnf groupinstall "C Development Tools and Libraries"
sudo dnf groupinstall "Development Tools"
```
## Install Lutris
**Follow Lutris official docs here:** [https://lutris.net/downloads/](https://lutris.net/downloads/)

## Install Garena and LOL from Lutris
**Garena:** [https://lutris.net/games/garena/](https://lutris.net/games/garena/)

**Note for Garena:** After installing Garena, do not login, close the window

**LOL:** [https://lutris.net/games/league-of-legends/](https://lutris.net/games/league-of-legends/)

**Note for LOL:** when the installer for LOL NA comes up, just close it, you don't need to install it, we just need the environment

## Install LOL from Garena
Open Garena from lutris and install LOL like you normally do on Windows. 

Also, enable **Disable proxy when browsing** for better Garena experience (it sucks by default)

![Garena setting](images/garena.png)

## Config LOL Lutris
Change the default Executable in Riot LOL(the default LOL Installation for Lutris) to **LeagueClient.exe** (thanks to [abiswas97](https://github.com/abiswas97)) from the LOL-Garena installed location. For example:

> /home/nhubao/Games/league-of-legends/drive_c/Games/32787/LeagueClient/LeagueClient.exe

![Lutris setting](images/lutris_new.png)

## Start the game
* Download the python script (lol.py)
* Install the dependencies:
```
pip3 install psutil pyyaml
```
* Start Garena
* Open terminal, ```cd``` into the directory where you have saved this project(Ex: /home/nhubao/league-of-legends-linux-garena-script-main) and run the script
```
python3 lol.py
```
* Return to Garena and press **Play**
* Wait for a while, it may take some time load in

## Result
![LOL on Linux](images/result.png)

## Update new wine-lol (This is not the wine-lol package in the AUR)
- It currently only have prebuilt for Ubuntu/Debian based and PKGBUILD for arch based: https://github.com/ekistece/wine-lol
- After installing both `wine-lol` and `wine-lol-glibc`, change the wine version of LOL in lutris to custom and enter this path: `/opt/wine-lol/bin/wine`

## Disclaimer
* If the game crash with some message that saids `core dump...` just press `OK` and wait a bit, the game will continue at the exact state
