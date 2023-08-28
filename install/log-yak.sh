#!/bin/sh
# Copyright: (c) 2023, dbi services
# This file is part of YaK core.
# Yak core is free software distributed without any warranty under the terms of the GNU General Public License v3 as published by the Free Software Foundation, https://www.gnu.org/licenses/gpl-3.0.txt

if [ ! -z "${YAK_DEV_GID}" -a ! -z "${YAK_DEV_UID}" ]; then
    usermod -u ${YAK_DEV_UID} yak
    groupmod  -g ${YAK_DEV_GID} yak
fi

su - yak
