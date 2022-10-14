#!/bin/bash
# Copyright: (c) 2022, dbi services
# This file is part of YaK core.
# Yak core is free software distributed without any warranty under the terms of the GNU General Public License v3 as published by the Free Software Foundation, https://www.gnu.org/licenses/gpl-3.0.txt

YAK_USER_HOME="/workspace"

# User create with proper UID/GID at run time
if ! id yak > /dev/null 2>&1; then

    if [ -z "${YAK_DEV_GID}" -o -z "${YAK_DEV_UID}" ]; then
        echo "INFO: Creating group yak => groupadd yak"
        groupadd yak
        echo "INFO: Creating user yak  => useradd -M -d ${YAK_USER_HOME} -g yak -s /bin/bash yak"
        useradd -M -d ${YAK_USER_HOME} -g yak -s /bin/bash yak
    else
        echo "INFO: Creating group yak => groupadd -g ${YAK_DEV_GID} yak"
        groupadd -g ${YAK_DEV_GID} yak
        echo "INFO: Creating user yak  => useradd -u ${YAK_DEV_UID} -M -d ${YAK_USER_HOME} -g yak -s /bin/bash yak"
        useradd -u ${YAK_DEV_UID} -M -d ${YAK_USER_HOME} -g yak -s /bin/bash yak
    fi

    # Environment
    echo "cd ${YAK_USER_HOME}/yak" >> ${YAK_USER_HOME}/.bashrc
    echo "export OCI_USE_NAME_AS_IDENTIFIER=true" >> ${YAK_USER_HOME}/.bashrc

    # Alias
    echo "alias ll='ls -latr'" >> ${YAK_USER_HOME}/.bashrc
    echo "alias cdci='cd ${YAK_USER_HOME}/yak/configuration/infrastructure'" >> ${YAK_USER_HOME}/.bashrc
    echo "alias cdcii='cd ${YAK_USER_HOME}/yak/configuration/infrastructure/@yak_dev_infrastructure'" >> ${YAK_USER_HOME}/.bashrc
    echo "alias cdct='cd ${YAK_USER_HOME}/yak/configuration/template'" >> ${YAK_USER_HOME}/.bashrc
    echo "alias cdh='cd ${YAK_USER_HOME}/yak'" >> ${YAK_USER_HOME}/.bashrc
    echo "alias cdr='cd ${YAK_USER_HOME}/yak/roles'" >> ${YAK_USER_HOME}/.bashrc
    echo "alias cds='cd ${YAK_USER_HOME}/yak/servers'" >> ${YAK_USER_HOME}/.bashrc
    echo "alias startdemo='cd ${YAK_USER_HOME}/yak;${YAK_USER_HOME}/yak/configuration/demo_scripts/startdemo.sh'" >> ${YAK_USER_HOME}/.bashrc
    echo 'aig() { cd ~/yak && ansible-inventory --graph "$1"; cd - > /dev/null; }' >> ${YAK_USER_HOME}/.bashrc
    echo 'aigv() { cd ~/yak && ansible-inventory --graph "$1" --vars; cd - > /dev/null; }' >> ${YAK_USER_HOME}/.bashrc
    echo 'aih() { cd ~/yak && ansible-inventory --host "$1"; cd - > /dev/null; }' >> ${YAK_USER_HOME}/.bashrc
    echo 'apdp() { cd ~/yak && ansible-playbook servers/deploy.yml -e target="$1"; cd - > /dev/null; }' >> ${YAK_USER_HOME}/.bashrc
    echo 'apdps() { cd ~/yak && ansible-playbook servers/deploy.yml --tags=server -e target="$1"; cd - > /dev/null; }' >> ${YAK_USER_HOME}/.bashrc
    echo 'apdpr() { cd ~/yak && ansible-playbook servers/deploy.yml --tags=requirements -e target="$1"; cd - > /dev/null; }' >> ${YAK_USER_HOME}/.bashrc
    echo 'apdc() { cd ~/yak && ansible-playbook servers/decommission.yml -e target="$1"; cd - > /dev/null; }' >> ${YAK_USER_HOME}/.bashrc
    echo 'gen_secret() { ssh-keygen -b 4096 -m PEM -t rsa -f sshkey -q -N ""; }' >> ${YAK_USER_HOME}/.bashrc
    echo 'yakhelp() { cat /yakhelp.lst | more; }' >> ${YAK_USER_HOME}/.bashrc

    chown yak:yak ${YAK_USER_HOME}
    chown yak:yak ${YAK_USER_HOME}/.bashrc

    if [ ! -d "${YAK_USER_HOME}/.ssh" ]; then
       mkdir ${YAK_USER_HOME}/.ssh
       chown yak:yak -R ${YAK_USER_HOME}/.ssh
    fi

    if [ ! -d "${YAK_USER_HOME}/.oci" ]; then
       mkdir ${YAK_USER_HOME}/.oci
       touch ${YAK_USER_HOME}/.oci/config
       chown yak:yak -R ${YAK_USER_HOME}/.oci
    fi

    YAK_LOCAL_SECRETS="${YAK_USER_HOME}/yak/configuration/infrastructure/secrets"
    if [ ! -d "${YAK_LOCAL_SECRETS}" ]; then
        mkdir -p ${YAK_LOCAL_SECRETS}
    fi
    chmod 700 ${YAK_USER_HOME}/yak/configuration/infrastructure/secrets

    YAK_LOCAL_SSH="${YAK_USER_HOME}/yak/configuration/infrastructure/.ssh"
    if [ ! -d "${YAK_LOCAL_SSH}" ]; then
        mkdir -p ${YAK_LOCAL_SSH}
        touch ${YAK_LOCAL_SSH}/config
    fi

    # Use Yak local ssh config file
    echo "Include ${YAK_LOCAL_SSH}/config" >> /etc/ssh/ssh_config

    #Set the correct privilege for the yak files
    chown yak:yak -R ${YAK_USER_HOME}/yak

    # Sudo
    if [ "${YAK_ENABLE_SUDO}" = true ]; then
       echo 'yak ALL=(ALL:ALL) NOPASSWD: ALL' > /etc/sudoers.d/yak
    fi

    ## Reset to normal: \033[0m
    NORM="\033[0m"
    ## Change Color to White
    WHITE="\033[1;37m"
    function whiteLog {
       MSG="$@"
       echo  -e "${WHITE}$MSG${NORM} "
    }

    clear
    echo
    echo "INFO: type 'yakhelp' to display the help of YAK"
    echo

    # Display YaK Demo environement infos
    if [ "${YAK_DEMO}" = true ]; then
       mv ${YAK_USER_HOME}/yak/configuration/infrastructure/demo_aws/linux ${YAK_USER_HOME}/yak/configuration/infrastructure/demo_aws/linux-$(hostname -s)
       clear
       echo "==========================================================="
       echo
       echo " Type 'yakhelp' to display the help of YaK"
       echo
       echo " As of demo this environment has some restriction"
       echo
       echo " The servers:"
       echo "  - provisioning allows only instance_type=t3.micro "
       echo "  - are automatically destroyed after 4h"
       echo "  - storage size can't be extended"
       echo
       echo " Disclaimer:"
       echo "    The instances created by the YaK are delivered as is, "
       echo "    dbi-services is not responsible for the use that could be made "
       echo "    of them outside the YaK demonstration environment"
       echo
       whiteLog  " Type \"startdemo aws\" and then press ENTER"
       echo
       echo " This demo will deploy and configure a Debian 11.4 server "
       echo "       Including additional storage on AWS Cloud"
       echo
       echo "==========================================================="
       echo
   fi
fi
su - yak --pty -c "$@"
cd /workspace/yak


