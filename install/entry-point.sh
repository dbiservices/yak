#!/bin/bash

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

    echo "alias ll='ls -latr'" >> ${YAK_USER_HOME}/.bashrc
    echo "alias cdci='cd ${YAK_USER_HOME}/yak/configuration/infrastructure'" >> ${YAK_USER_HOME}/.bashrc
    echo "alias cdct='cd ${YAK_USER_HOME}/yak/configuration/template'" >> ${YAK_USER_HOME}/.bashrc
    echo "alias cdh='cd ${YAK_USER_HOME}/yak'" >> ${YAK_USER_HOME}/.bashrc
    echo "alias cdr='cd ${YAK_USER_HOME}/yak/roles'" >> ${YAK_USER_HOME}/.bashrc
    echo "alias cds='cd ${YAK_USER_HOME}/yak/servers'" >> ${YAK_USER_HOME}/.bashrc
    echo "cd ${YAK_USER_HOME}/yak" >> ${YAK_USER_HOME}/.bashrc
    echo 'aig() { cd ~/yak && ansible-inventory --graph "$1"; cd - > /dev/null; }' >> ${YAK_USER_HOME}/.bashrc
    echo 'aih() { cd ~/yak && ansible-inventory --host "$1"; cd - > /dev/null; }' >> ${YAK_USER_HOME}/.bashrc
    echo 'apsdp() { cd ~/yak && ansible-playbook servers/deploy.yml -e target="$1"; cd - > /dev/null; }' >> ${YAK_USER_HOME}/.bashrc
    echo 'apsr() { cd ~/yak && ansible-playbook servers/deploy.yml --tag=component_requirements -e target="$1"; cd - > /dev/null; }' >> ${YAK_USER_HOME}/.bashrc
    echo 'apsdc() { cd ~/yak && ansible-playbook servers/decommission.yml -e target="$1"; cd - > /dev/null; }' >> ${YAK_USER_HOME}/.bashrc
    echo 'gen_secret() { ssh-keygen -b 4096 -m PEM -t rsa -f sshkey -q -N ""; }' >> ${YAK_USER_HOME}/.bashrc
    echo 'yakhelp() { cat /yakhelp.lst | more; }' >> ${YAK_USER_HOME}/.bashrc
    echo
    echo "INFO: type 'yakhelp' to display the help of YAK"
    echo
    mkdir ${YAK_USER_HOME}/.oci
    touch ${YAK_USER_HOME}/.oci/config
    chown yak:yak ${YAK_USER_HOME}
    chown yak:yak ${YAK_USER_HOME}/.bashrc
    chown yak:yak -R ${YAK_USER_HOME}/.oci

    YAK_LOCAL_SECRETS="${YAK_USER_HOME}/yak/configuration/infrastructure/secrets"
    if [ ! -d "${YAK_LOCAL_SECRETS}" ]; then
        mkdir -p ${YAK_LOCAL_SECRETS}
    fi
    chmod -R 700 ${YAK_USER_HOME}/yak/configuration/infrastructure/secrets

    YAK_LOCAL_SSH="${YAK_USER_HOME}/yak/configuration/infrastructure/ssh"
    if [ ! -d "${YAK_LOCAL_SSH}" ]; then
        mkdir -p ${YAK_LOCAL_SSH}
        touch ${YAK_LOCAL_SSH}/config 
    fi

    chown yak:yak -R ${YAK_USER_HOME}/yak
    ln -s ${YAK_LOCAL_SSH} ${YAK_USER_HOME}/.ssh
    # Sudo
    if [ "${YAK_ENABLE_SUDO}" = true ]; then
       echo 'yak ALL=(ALL:ALL) NOPASSWD: ALL' > /etc/sudoers.d/yak
    fi
fi

su - yak --pty -c "$@"
