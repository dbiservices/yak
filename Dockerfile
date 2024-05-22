# Copyright: (c) 2023, dbi services
# This file is part of YaK core.
# Yak core is free software distributed without any warranty under the terms of the GNU General Public License v3 as published by the Free Software Foundation, https://www.gnu.org/licenses/gpl-3.0.txt
ARG YAKENV_TAG="stable"

FROM registry.gitlab.com/yak4all/yakenv:${YAKENV_TAG}

ARG CI_COMMIT_TAG="stable"
ARG CI_COMMIT_SHORT_SHA="yak:2.0.0-ee 0.1"

# COPY Sources
COPY ./ReleaseNotes /runner/project/ReleaseNotes
COPY ./collections /runner/project/collections
COPY ./configuration /runner/project/configuration
COPY ./install /runner/project/install
COPY ./inventory /runner/project/inventory
COPY ./servers /runner/project/servers
COPY ./component_types /runner/project/component_types
COPY ./licenses /runner/project/lisenses
COPY ./docs /runner/project/docs
COPY ./ansible.cfg /runner/project
COPY ./COPYING /runner/project
COPY ./README.md /runner/project

COPY ./install/entry-point.sh /entry-point.sh
COPY ./install/yakhelp.lst /yakhelp.lst
RUN chmod u+x /entry-point.sh
RUN chmod ugo+x /yakhelp.lst
RUN echo "CI_COMMIT_TAG: $CI_COMMIT_TAG"
RUN echo "CI_COMMIT_SHORT_SHA: $CI_COMMIT_SHORT_SHA"
RUN echo "YaK version: $CI_COMMIT_TAG" > /runner/project/.version
RUN echo "commit short sha: $CI_COMMIT_SHORT_SHA" >> /runner/project/.version
RUN apt-get update && apt-get install -y locales sshpass && sed -i 's/^# *\(en_US.UTF-8\)/\1/' /etc/locale.gen && locale-gen 
ENV LANG en_US.utf8 
