#!/bin/bash
#-------------------------------------------------------------------------------
# FILE:  startdemo.sh
#
# PURPOSE: Script to execute Yak Demo with the different Cloud Provider
#
# PARAMETERS: AWS, OCI, AZURE
#
# NOTE:
#-------------------------------------------------------------------------------
# $Author: Herve Schweitzer $
# $Release: #RELEASE_VERSION 
#-------------------------------------------------------------------------------

# print the usage of this script
usage()
{
	echo "This script will run a Demo of the YaK for the selected provider"
	echo 
	echo "      $ startdemo.sh [AWS|OCI|AZURE]"
	echo
}

# No parameter provided at all, this can not work
if [ "$#" -eq 0 ]; then
    usage
    exit
fi

scriptname="$(basename $0)"
dir=`dirname $0`

start_aws_demo()
{
   echo 
   echo "STEP 1"
   echo "-------------------------------------------------------------------------------------"
   echo "         To create a Machine on AWS, an  environment configuration must exist"
   echo "   In our case we will use the environment DEMO under ./configuration/infrastructure"
   echo
   echo "cat $HOME/yak/configuration/infrastructure/demo/variables.yml" 
   echo
   read -p "Press enter to continue"
   echo
   cat $HOME/yak/configuration/infrastructure/demo/variables.yml
   echo

   echo
   read -p "Press enter to continue"
   echo "STEP 2"
   echo "-------------------------------------------------------------------------------------"
   echo "       Then a Machine configuration must exist under this environment "
   echo
   echo "cat $HOME/yak/configuration/infrastructure/demo/linux-$(hostname -s)/variables.yml" 
   echo
   read -p "Press enter to continue"
   echo
   cat $HOME/yak/configuration/infrastructure/demo/linux-$(hostname -s)/variables.yml
   echo

   echo
   read -p "Press enter to continue"
   echo "STEP 3"
   echo "-------------------------------------------------------------------------------------"
   echo "    Now you can display your ansible inventory to check if everything is correct  "
   echo
   echo "ansible-inventory --host demo/linux-$(hostname -s)" 
   echo
   read -p "Press enter to continue"
   echo
ansible-inventory --host demo/linux-$(hostname -s)
   echo

   echo
   read -p "Press enter to continue"
   echo "STEP 4"
   echo "-------------------------------------------------------------------------------------"
   echo "         Now you must set your authentification method "
   echo "  to have the privileges to create and configure the instance" 
   echo "  In our case it's not mandatory as we set permanent keys"
   echo
   echo "export AWS_ACCESS_KEY_ID=ASI********2E7"
   echo "export AWS_SECRET_ACCESS_KEY=PE************UNaHGu2"
   echo "export AWS_SESSION_TOKEN=IQoJb3JpZ2luX*******4+vfWexbFF3cKg="
   echo 
   read -p "Press enter to continue"

   echo
   read -p "Press enter to continue"
   echo "STEP 5"
   echo "-------------------------------------------------------------------------------------"
   echo "    Now you are ready to create your host including storage configuration"
   echo
   echo "ansible-playbook servers/deploy.ymk -e target=demo/linux-$(hostname -s)" 
   echo
   read -p "Press enter to continue"
   echo
ansible-playbook servers/deploy.yml -e target=demo/linux-$(hostname -s)
   echo
   
   echo
   read -p "Press enter to continue"
   echo "Last Step"
   echo "-------------------------------------------------------------------------------------"
   echo "           you can connect your created server "
   echo "    and check that the storage is correclty configured"
   echo "    please exit the session when checked with df -h"
   echo
   echo "ssh demo/linux-$(hostname -s)" 
   echo "df -h"
   echo "exit" 
   echo
   read -p "Press enter to continue"
   echo
ssh demo/linux-$(hostname -s) 
   echo
   echo 
   echo "Cleanup step"
   echo "-------------------------------------------------------------------------------------"
   echo "           Now your can decommission your created server "
   echo
   echo "ansible-playbook servers/decommission.yml -e target=demo/linux-$(hostname -s)" 
   echo
   read -p "Press enter to continue"
   echo
ansible-playbook servers/decommission.yml -e target=demo/linux-$(hostname -s)
   echo
   echo
   echo "Please close this DEMO session with \"exit\" before leaving"
   echo
}

###############
# Main Programm
###############

if [[ $1 == AWS  ]]; then
   start_aws_demo 
else
   usage 
fi
