#!/bin/bash
# Copyright: (c) 2023, dbi services
# This file is part of YaK core.
# Yak core is free software distributed without any warranty under the terms of the GNU General Public License v3 as published by the Free Software Foundation, https://www.gnu.org/licenses/gpl-3.0.txt

git_action="${1}"
if [[ -z ${1} ]]; then
    git_action="pull"
fi

if [[ "${git_action}" == "push" ]]; then
    commit_message="${2}"
    git_command_1="git add -A"
    git_command_2="git commit -m"
    git_command_3="git push"
elif [[ "${git_action}" == "pull" ]]; then
    git_command_1="git pull"
    git_command_2=""
    git_command_3=""
elif [[ "${git_action}" == "status" ]]; then
    git_command_1="git status"
    git_command_2=""
    git_command_3=""
fi

# Components
mkdir -p ./components
for src in $(cat ./manifest.yml | egrep '\- src:' | awk '{ print $3}'); do
    repo_name="$(basename ${src} | awk -F '.' '{ print $1}')"
    if [ -d ./components/${repo_name}/.git ]; then
        echo "## ${git_action}ing component '${repo_name}'..."
        cd ./components/${repo_name}
        ${git_command_1}
        if [[ ! -z "${git_command_2}" ]]; then
            ${git_command_2} "${commit_message}"
            ${git_command_3}
        fi
        cd ../..
    else
        echo "## Cloning component '${repo_name}'..."
        echo "git clone ${src} ./components/${repo_name}"
        git clone ${src} ./components/${repo_name}
    fi
done

# Development infrastructure
for infra_name in yak_dev_infrastructure; do
    if [ -d ./configuration/infrastructure/@${infra_name}/.git ]; then
        echo "## ${git_action}ing infrastructure '${infra_name}'..."
        cd ./configuration/infrastructure/@${infra_name}
        ${git_command_1}
        if [[ ! -z "${git_command_2}" ]]; then
            ${git_command_2} "${commit_message}"
            ${git_command_3}
        fi
        cd ../../..
    else
        echo "## Cloning infrastructure '${infra_name}'..."
        echo "git clone git@gitlab.com:dbiservices/yak/${infra_name}.git ./configuration/infrastructure/@${infra_name}"
        git clone git@gitlab.com:dbiservices/yak/${infra_name}.git ./configuration/infrastructure/@${infra_name}
    fi
done
