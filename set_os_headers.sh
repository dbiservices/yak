#!/bin/bash

# Variables
pattern_to_search='^[ ]?#[ ]?Copyright:[ ]?\(c\)[ ]?[0-9]{4}[ ]?,[ ]?dbi services'
header="Copyright: (c) $(date +"%Y"), dbi services, distributed without any warranty under the terms of the GNU General Public License v3"
search_from='./manifest.yml ./collections/ansible_collections/yak ./servers ./configuration ./inventory'

# Program

## YAML files
for file in $(find ${search_from} -type f -name "*.yml"); do
    if [ $(egrep -c "${pattern_to_search}" ${file}) -eq 0 ]; then
        echo "Headering file '${file}'"
        sed -i "1 i# ${header}" ${file}
    fi
done

## Python files
for file in $(find ${search_from} -type f -name "*.py"); do
    if [ $(egrep -c "${pattern_to_search}" ${file}) -eq 0 ]; then
        echo "Headering file '${file}'"
        if [ $(head -1 ${file} | egrep -c "#\!/.*python") -eq 1 ]; then
            sed -i "2 i# ${header}" ${file}
        else
            sed -i "1 i# ${header}" ${file}
        fi
    fi
done
