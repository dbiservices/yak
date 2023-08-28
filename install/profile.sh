# Environment
export OCI_USE_NAME_AS_IDENTIFIER=true

# Aliases
alias ll='ls -ltra'
alias uc='unset YAK_CORE_COMPONENT'
alias cdh='cd ~/yak'
alias cdc='cd ~/yak/component_types'
alias cdcc='cd ~/yak/configuration/components'
alias cdci='cd ~/yak/configuration/infrastructure'
alias cdcii='cd ~/yak/configuration/infrastructure/@yak_dev_infrastructure'
alias cds='cd ~/yak/servers'
alias startdemo='cd ~/yak; ~/yak/configuration/demo_scripts/startdemo.sh'

# Functions
sc() { export YAK_CORE_COMPONENT="$1"; }
aig() { cd ~/yak && ansible-inventory --graph "$1"; cd - > /dev/null; }
aigv() { cd ~/yak && ansible-inventory --graph "$1" --vars; cd - > /dev/null; }
aih() { cd ~/yak && ansible-inventory --host "$1"; cd - > /dev/null; }
apdp() { cd ~/yak && ansible-playbook servers/deploy.yml -e target="$1"; cd - > /dev/null; }
apdps() { cd ~/yak && ansible-playbook servers/deploy.yml --tags=server -e target="$1"; cd - > /dev/null; }
apdpr() { cd ~/yak && ansible-playbook servers/deploy.yml --tags=requirements -e target="$1"; cd - > /dev/null; }
apdc() { cd ~/yak && ansible-playbook servers/decommission.yml -e target="$1"; cd - > /dev/null; }
gen_secret() { ssh-keygen -b 4096 -m PEM -t rsa -f sshkey -q -N ""; }
yakhelp() { cat ${HOME}/yakhelp.lst | more; }

# SSH Config
YAK_LOCAL_SSH="${HOME}/yak/configuration/infrastructure/.ssh"
if [ ! -d "${YAK_LOCAL_SSH}" ]; then
    mkdir -p ${YAK_LOCAL_SSH}
    touch ${YAK_LOCAL_SSH}/config
fi

# OCI Config
if [ ! -d "${HOME}/.oci" ]; then
    mkdir ${HOME}/.oci
    touch ${HOME}/.oci/config
fi

## Reset to normal: \033[0m
NORM="\033[0m"
## Change Color to White
WHITE="\033[1;37m"
function whiteLog {
    MSG="$@"
    echo  -e "${WHITE}$MSG${NORM} "
}

echo
echo "INFO: type 'yakhelp' to display the help of YAK"
echo

# Display YaK Demo environement infos
if [ "${YAK_DEMO}" = true ]; then
    mv ${HOME}/yak/configuration/infrastructure/demo_aws/linux ${HOME}/yak/configuration/infrastructure/demo_aws/linux-$(hostname -s)
    clear
    cat /yakhelp.txt
fi

# Go to project directory
cd /workspace/yak
