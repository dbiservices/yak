#!/bin/bash
#-------------------------------------------------------------------------------
# FILE:  startdemo.sh
#
# PURPOSE: Script to execute Yak demo with the different Cloud Provider
#
# PARAMETERS: aws, azure, oci
#
# NOTE: Test 
#-------------------------------------------------------------------------------
# $Author: Herve Schweitzer $
# $Release: #RELEASE_VERSION 
#-------------------------------------------------------------------------------
. /workspace/yak/configuration/demo_scripts/lib_log.sh
START_TIME=$(date +%s)
#HUMAN_NOW=$(date +'%d%m%Y_%H%M%S')
#UUID=$(cat /proc/sys/kernel/random/uuid)
#mkdir -p .log
#echo "New VM creation: $HUMAN_NOW" > .log/$UUID.log

# print the usage of this script
function usage()
{
	echo
	whiteLog " NAME"
   echo "   startdemo -  YaK demo"
   echo ""
   whiteLog " SYNOPSIS"
   echo ""
	echo "   This script will run a demo of the YaK for AWS"
	echo "   YaK is build to work for main cloud providers: "
   echo "   Oracle OCI, Microsoft AZURE and Amazon AWS"
   echo "   This demo works only for AWS currently"
   echo ""
	whiteLog " USAGE"
   echo "   startdemo [aws|azure|oci]"
   echo ""
	whiteLog " NOTE"
	echo "   Only AWS is allowed for this demo"
   echo " "
   whiteLog " CREDITS"
   echo "   YaK is distributed and written by dbi services "
   echo " "

}

function step_time() {

   local MSG="$@"
   local END_TIME=$(date +%s)
   runtime=$(($END_TIME - $START_TIME))
   runtime_human="$((runtime / 60))m:$((runtime % 60))s"
#   echo "Duration $runtime_human: $MSG" >> .log/$UUID.log

}

# No parameter provided at all, this can not work
if [ "$#" -eq 0 ]; then
    usage
    exit
fi

scriptname="$(basename $0)"
dir=`dirname $0`

function not_available ()
{
   echo ""
   whiteLog " Only AWS is allowed for this demo"
   echo ""
}


function start_demo ()
{
   echo 
   blueLog "STEP 1#11: Provider description"
   whiteLog "-------------------------------------------------------------------------------------"
   echo "   To Provision a server on AWS, a Cloud provider configuration must exist"
   echo "   The environment demo_aws is located under ./configuration/infrastructure"
   echo
   greenLog "Executed command: "
   whiteLog "cat $HOME/yak/configuration/infrastructure/demo_${provider}/variables.yml" 
   echo
   read -p "Press enter to continue "
   echo
   cat $HOME/yak/configuration/infrastructure/demo_${provider}/variables.yml
   echo
   read -p "Press enter to continue "
   echo
   step_time "STEP 1"

   blueLog "STEP 2#11: server variables"
   whiteLog "-------------------------------------------------------------------------------------"
   echo "   The server configuration is located under the Provider environment "
   echo "   ./configuration/infrastructure/demo_aws"
   echo
   greenLog "Executed command: "
   whiteLog "cat $HOME/yak/configuration/infrastructure/demo_${provider}/linux-$(hostname -s)/variables.yml" 
   echo
   read -p "Press enter to continue "
   echo
   cat $HOME/yak/configuration/infrastructure/demo_${provider}/linux-$(hostname -s)/variables.yml
   echo
   read -p "Press enter to continue "
   echo
   step_time "STEP 2"

   blueLog "STEP 3#11: Component variables"
   whiteLog "-------------------------------------------------------------------------------------"
   echo "   The Component configuration is located under a separated directory structure"
   echo "   ./configuration/components"
   echo
   greenLog "Executed command: "
   whiteLog "cat $HOME/yak/configuration/components/COMP/variables.yml" 
   echo
   read -p "Press enter to continue "
   echo
   cat $HOME/yak/configuration/components/COMP/variables.yml
   echo
   read -p "Press enter to continue "
   echo
   step_time "STEP 3"

   blueLog "STEP 4#11. Display the Ansible inventory"
   whiteLog "--------------------------------------------------------------------------------------"
   echo
   greenLog "Executed command: "
   whiteLog "ansible-inventory --graph" 
   echo
   read -p "Press enter to continue "
   echo
   ansible-inventory --graph
   echo
   read -p "Press enter to continue "
   echo
   step_time "STEP 4"

   blueLog "STEP 5#11. Display the Ansible Host inventory"
   whiteLog "--------------------------------------------------------------------------------------"
   echo
   greenLog "Executed command: "
   whiteLog "ansible-inventory --host demo_${provider}/linux-$(hostname -s)" 
   echo
   read -p "Press enter to continue "
   echo
   ansible-inventory --host demo_${provider}/linux-$(hostname -s)
   echo
   read -p "Press enter to continue "
   echo
   step_time "STEP 5"

   blueLog "STEP 6#11. Set the authentification method"
   whiteLog "-------------------------------------------------------------------------------------"
   echo "   To have the privileges to create and configure the server" 
   echo "   For this demo on ${provider} it is done by exporting the ${provider} provided variables"
   echo
   greenLog "Executed command: "
   whiteLog "export AWS_ACCESS_KEY_ID=ASI********2E7"
   whiteLog "export AWS_SECRET_ACCESS_KEY=PE************UNaHGu2"
   whiteLog "export AWS_SESSION_TOKEN=IQoJb3JpZ2luX*******4+vfWexbFF3cKg="
   echo 
   read -p "Press enter to continue "
   echo
   step_time "STEP 6"

   blueLog "STEP 7#11. Set Inventory to the component"
   whiteLog "-------------------------------------------------------------------------------------"
   echo "   To deploy an server including the disk of the component configuration COMP "
   echo "   The inventory must be set to the component"
   echo
   greenLog "Executed command: "
   whiteLog "sc COMP" 
   whiteLog "ansible-inventory --graph" 
   echo
   read -p "Press enter to continue "
   echo
   sc COMP
   ansible-inventory --graph
   echo
   read -p "Press enter to continue "
   step_time "STEP 7"

   blueLog "STEP 8#11. Server creation"
   whiteLog "-------------------------------------------------------------------------------------"
   echo "   Now you are ready to create your host including storage configuration"
   echo
   greenLog "Executed command: "
   whiteLog "ansible-playbook servers/deploy.yml -e target=demo_${provider}/linux-$(hostname -s)" 
   echo
   read -p "Press enter to continue "
   echo
   ansible-playbook servers/deploy.yml -e target=demo_${provider}/linux-$(hostname -s)
   echo
   read -p "Press enter to continue "
   step_time "STEP 8"

   blueLog "STEP 9#11. SSH connection to created server"
   whiteLog "-------------------------------------------------------------------------------------"
   echo "   At this step the server is created and an SSH connection will be made"
   echo "   Check the server and the storage if it is correctly configured"
   whiteLog "   Please type "exit" and ENTER to close the session when you are done"
   echo
   greenLog "Executed command: "
   whiteLog "ssh demo_${provider}/linux-$(hostname -s)" 
   echo
   read -p "Press enter to continue "
   echo
   ssh demo_${provider}/linux-$(hostname -s) 
   echo 
   step_time "STEP 9"
   
   blueLog "STEP 10#11 SSH connection from your PC"
   whiteLog "-------------------------------------------------------------------------------------"
   whiteLog "   If you want to connect from your PC"
   whiteLog "   You can use the below information, and copying the content of the sshkey file"
   echo
   greenLog "Executed command: "
   whiteLog "cat configuration/infrastructure/.ssh/config" 
   echo
   read -p "Press enter to continue "
   echo
   cat configuration/infrastructure/.ssh/config
   echo
   read -p "Press enter to continue "
   step_time "STEP 10"

   blueLog "STEP 11#11 Server Decommissioning"
   whiteLog "-------------------------------------------------------------------------------------"
   redLog   "   If you Press ENTER the server will be destroyed"
   redLog   "   But you can press CTRL-C now if you want to keep the server"
   redLog   "   In any case the server will be destroyed in 4h. "
   echo
   greenLog "Executed command: "
   whiteLog "ansible-playbook servers/decommission.yml -e target=demo_${provider}/linux-$(hostname -s)" 
   echo
   read -p "Press enter to continue "
   echo
   ansible-playbook servers/decommission.yml -e target=demo_${provider}/linux-$(hostname -s)
   echo
   step_time "STEP 11"

   blueLog "End."
   whiteLog "-------------------------------------------------------------------------------------"
   whiteLog "   Close this demo session with \"exit\" before leaving"
   echo
   step_time "END"
}

###############
# Main Programm
###############
clear
if [[ $1 == AWS || $1 == aws ]]; then
   provider=aws
   start_demo
elif [[ $1 == OCI || $1 == oci ]]; then
   provider=oci
   not_available
elif [[ $1 == AZURE || $1 ==  azure ]]; then
   provider=azure
   not_available
else
   usage 
fi
