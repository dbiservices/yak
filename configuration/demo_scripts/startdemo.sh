#!/bin/bash
#-------------------------------------------------------------------------------
# FILE:  startdemo.sh
#
# PURPOSE: Script to execute Yak Demo with the different Cloud Provider
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
	whiteLog " NAME "
   echo "   startdemo -  YaK demo"
   echo ""
   whiteLog " SYNOPSIS"
   echo ""
	echo "   This script will run a Demo of the YaK for AWS"
	echo "   YaK is build to work for main cloud providers: "
   echo "   Oracle OCI, Microsoft AZURE and Amazon AWS"
   echo "   This demo works only for AWS currently"
   echo ""
	whiteLog " USAGE:"
   echo "   startdemo [aws|azure|oci]"
   echo ""
	whiteLog " NOTE:"
	echo "   Only AWS is allowed for this DEMO"
   echo " "
   whiteLog " CREDITS:"
   echo "   Yak is distributed and written by dbi services "
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
   whiteLog " Only AWS is allowed for this DEMO"
   echo ""
}


function start_demo ()
{
   echo 
   blueLog "STEP 1#9: Provider description."
   whiteLog "-------------------------------------------------------------------------------------"
   echo "   To create a Machine on AWS, an environment configuration must exist"
   echo "   The environment DEMO is located under under ./configuration/infrastructure"
   echo
   greenLog "Executed command: "
   whiteLog "cat $HOME/yak/configuration/infrastructure/demo_${provider}/variables.yml" 
   echo
   read -p "Press enter to continue: "
   echo
   cat $HOME/yak/configuration/infrastructure/demo_${provider}/variables.yml
   echo
   read -p "Press enter to continue: "
   echo
   step_time "STEP 1"

   blueLog "STEP 2#9: Machine variables."
   whiteLog "-------------------------------------------------------------------------------------"
   echo "   The Machine configuration is located under ./configuration/infrastructure"
   echo
   greenLog "Executed command: "
   whiteLog "cat $HOME/yak/configuration/infrastructure/demo_${provider}/linux-$(hostname -s)/variables.yml" 
   echo
   read -p "Press enter to continue: "
   echo
   cat $HOME/yak/configuration/infrastructure/demo_${provider}/linux-$(hostname -s)/variables.yml
   echo
   read -p "Press enter to continue: "
   echo
   step_time "STEP 2"


   blueLog "STEP 3#9: Component variables."
   whiteLog "-------------------------------------------------------------------------------------"
   echo "   The component configuration is located under ./configuration/infrastructure"
   echo
   greenLog "Executed command: "
   whiteLog "cat $HOME/yak/configuration/infrastructure/demo_${provider}/linux-$(hostname -s)/PG/variables.yml" 
   echo
   whitelog "based on the template file located on  ./configuration/templates/linux/storage/postgresql_instance.yml"
   echo
   read -p "Press enter to continue: "
   echo
   cat $HOME/yak/configuration/infrastructure/demo_${provider}/linux-$(hostname -s)/PG/variables.yml
   echo
   read -p "Press enter to continue: "
   echo
   step_time "STEP 3"

   blueLog "STEP 4#8. DEMO Inventory"
   whiteLog "--------------------------------------------------------------------------------------"
   echo "    Display the ansible inventory  "
   echo
   greenLog "Executed command: "
   whiteLog "ansible-inventory --graph" 
   echo
   read -p "Press enter to continue: "
   echo
   ansible-inventory --graph
   echo
   read -p "Press enter to continue: "
   echo
   step_time "STEP 4"

   blueLog "STEP 5#9. DEMO inventory for the used VM"
   whiteLog "--------------------------------------------------------------------------------------"
   echo "    Display the ansible inventory from your machine  "
   echo
   greenLog "Executed command: "
   whiteLog "ansible-inventory --host demo_${provider}/linux-$(hostname -s)" 
   echo
   read -p "Press enter to continue: "
   echo
   ansible-inventory --host demo_${provider}/linux-$(hostname -s)
   echo
   read -p "Press enter to continue: "
   echo
   step_time "STEP 5"

   blueLog "STEP 6#9"
   whiteLog "-------------------------------------------------------------------------------------"
   echo "   Set the authentification method "
   echo "   to have the privileges to create and configure the instance" 
   echo "   For DEMO AWS this is done by exportingg AWS provided variables:"
   echo
   greenLog "Executed command: "
   whiteLog "export AWS_ACCESS_KEY_ID=ASI********2E7"
   whiteLog "export AWS_SECRET_ACCESS_KEY=PE************UNaHGu2"
   whiteLog "export AWS_SESSION_TOKEN=IQoJb3JpZ2luX*******4+vfWexbFF3cKg="
   echo 
   read -p "Press enter to continue: "
   echo
   step_time "STEP 6"

   blueLog "STEP 7#9. VM Creation."
   whiteLog "-------------------------------------------------------------------------------------"
   echo "   Now you are ready to create your host including storage configuration"
   echo
   greenLog "Executed command: "
   whiteLog "ansible-playbook servers/deploy.yml -e target=demo_${provider}/linux-$(hostname -s)" 
   echo
   read -p "Press enter to continue: "
   echo
   ansible-playbook servers/deploy.yml -e target=demo_${provider}/linux-$(hostname -s)
   echo
   read -p "Press enter to continue: "
   step_time "STEP 7"

   blueLog "STEP 8#9. SSH connection to created VM"
   whiteLog "-------------------------------------------------------------------------------------"
   echo "   At this step the VM was created. An SSH connection will be made."
   echo "   Check that VM and the storage is correclty configured"
   echo "   Please exit the session when finished."
   echo
   greenLog "Executed command: "
   whiteLog "ssh demo_${provider}/linux-$(hostname -s)" 
   echo
   read -p "Press enter to continue: "
   echo
   ssh demo_${provider}/linux-$(hostname -s) 
   echo 
   step_time "STEP 8"

   blueLog "STEP 9#9 Machine Cleanup."
   whiteLog "-------------------------------------------------------------------------------------"
   redLog   " Machine Decommissioning. You can press CTRL-C now if you want to keep the Machine"
   redlog   " In any case the Machine will be destroyed in 4h. "
   echo
   greenLog "Executed command: "
   whiteLog "ansible-playbook servers/decommission.yml -e target=demo_${provider}/linux-$(hostname -s)" 
   echo
   read -p "Press enter to continue: "
   echo
   ansible-playbook servers/decommission.yml -e target=demo_${provider}/linux-$(hostname -s)
   echo
   step_time "STEP 9"

   blueLog "End."
   whiteLog "-------------------------------------------------------------------------------------"
   whiteLog "   Close this DEMO session with \"exit\" before leaving"
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
