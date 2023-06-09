# Copyright: (c) 2023, dbi services
# This file is part of YaK core.
# Yak core is free software distributed without any warranty under the terms of the GNU General Public License v3 as published by the Free Software Foundation, https://www.gnu.org/licenses/gpl-3.0.txt
ARG COMMIT_TAG="Default_Value"
ARG COMMIT_SHORT_SHA="Default_Value"
ARG YAKENV_TAG="stable"

FROM registry.gitlab.com/yak4all/yakenv:${YAKENV_TAG}

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

COPY ./install/entry-point.sh /entry-point.sh
COPY ./install/yakhelp.lst /yakhelp.lst
RUN chmod u+x /entry-point.sh
RUN chmod ugo+x /yakhelp.lst
RUN echo CI_COMMIT_TAG: ${COMMIT_TAG}
RUN echo CI_COMMIT_SHORT_SHA: ${COMMIT_SHORT_SHA}
RUN echo YaK version: ${COMMIT_TAG} > /workspace/yak/.version
RUN echo commit short sha: ${COMMIT_SHORT_SHA} >> /workspace/yak/.version

ENV LANG en_US.utf8

ENTRYPOINT ["/entry-point.sh"]
