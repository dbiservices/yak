## Reset to normal: \033[0m
NORM="\033[0m"

## Colors:
BLACK="\033[0;30m"
GRAY="\033[1;30m"
RED="\033[0;31m"
LRED="\033[1;31m"
GREEN="\033[0;32m"
LGREEN="\033[1;32m"
YELLOW="\033[0;33m"
LYELLOW="\033[1;33m"
BLUE="\033[0;34m"
LBLUE="\033[1;34m"
PURPLE="\033[0;35m"
PINK="\033[1;35m"
CYAN="\033[0;36m"
LCYAN="\033[1;36m"
LGRAY="\033[0;37m"
WHITE="\033[1;37m"

function redLog {
    MSG="$@"
    echo -e "${RED}$MSG${NORM} "
}

function yellowLog {
    MSG="$@"
    echo  -e "${YELLOW}$MSG${NORM} "
}

function blueLog {
    MSG="$@"
    echo  -e "${LBLUE}$MSG${NORM} "
}

function greenLog {
    MSG="$@"
    echo  -e "${LGREEN}$MSG${NORM} "
}

function whiteLog {
    MSG="$@"
    echo  -e "${WHITE}$MSG${NORM} "
}
