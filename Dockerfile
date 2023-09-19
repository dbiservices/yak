# Copyright: (c) 2023, dbi services
# This file is part of YaK core.
# Yak core is free software distributed without any warranty under the terms of the GNU General Public License v3 as published by the Free Software Foundation, https://www.gnu.org/licenses/gpl-3.0.txt
ARG YAKENV_TAG="stable"

FROM registry.gitlab.com/yak4all/yakenv:${YAKENV_TAG}

ARG CI_COMMIT_TAG="stable"
ARG CI_COMMIT_SHORT_SHA="xxxxxx"

# Add user YaK
RUN adduser -D yak -h /workspace
RUN echo "yak ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/yak
RUN echo "Include /workspace/yak/configuration/infrastructure/.ssh/config" >> /etc/ssh/ssh_config

# Workdir
WORKDIR /workspace/yak

# COPY Sources
COPY ./collections /workspace/yak/collections
COPY ./configuration /workspace/yak/configuration
COPY ./inventory /workspace/yak/inventory
COPY ./servers /workspace/yak/servers
COPY ./component_types /workspace/yak/component_types
COPY ./licenses /workspace/yak/lisenses
COPY ./docs /workspace/yak/docs
COPY ./ansible.cfg /workspace/yak
COPY ./COPYING /workspace/yak
COPY ./README.md /workspace/yak

# COPY config
COPY ./install/log-yak.sh /log-yak.sh
RUN chmod u+x /log-yak.sh
COPY ./install/profile.sh /etc/profile.d/yak-profile.sh
RUN chmod ugo+rw /etc/profile
COPY ./install/yakhelp.txt /workspace/yakhelp.txt
RUN chown yak:yak /workspace/yakhelp.txt
COPY ./install/yakhelp.lst /workspace/yakhelp.lst
RUN chown yak:yak /workspace/yakhelp.lst
RUN echo "CI_COMMIT_TAG: $CI_COMMIT_TAG"
RUN echo "CI_COMMIT_SHORT_SHA: $CI_COMMIT_SHORT_SHA"
RUN echo "YaK version: $CI_COMMIT_TAG" > /workspace/yak/.version
RUN echo "commit short sha: $CI_COMMIT_SHORT_SHA" >> /workspace/yak/.version
RUN chown yak:yak /workspace/yak/.version

CMD [ "/log-yak.sh" ]
