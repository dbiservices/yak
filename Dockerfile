FROM alpine:3.18

# Metadata params
ARG ANSIBLE_VERSION
ENV ANSIBLE_VERSION=${ANSIBLE_VERSION:-8.3.0}
ARG ANSIBLE_LINT_VERSION
ENV ANSIBLE_LINT_VERSION=${ANSIBLE_LINT_VERSION:-6.17.2}
ARG ANSIBLE_RUNNER_VERSION
ENV ANSIBLE_RUNNER_VERSION=${ANSIBLE_RUNNER_VERSION:-2.3.3}

# GitLab params
ARG CI_COMMIT_TAG="stable"
ARG CI_COMMIT_SHORT_SHA="xxxxxx"

# Setup
RUN apk --update --no-cache add \
        ca-certificates \
        openssh-client \
        openssl \
        python3 \
        py3-cryptography \
        rsync \
        sshpass \
        shadow \
        sudo

RUN apk --update add \
        --virtual .build-deps \
        py3-pip \
        python3-dev \
        libffi-dev \
        openssl-dev \
        build-base \
        gcc musl-dev cargo make \
        curl \
        && pip3 install --upgrade \
                pip \
                cffi \
                pyyaml==5.3.1 \
                ruamel.yaml \
        # Ansible
        && pip3 install \
                ansible==${ANSIBLE_VERSION} \
                ansible-lint==${ANSIBLE_LINT_VERSION} \
                ansible-runner==${ANSIBLE_RUNNER_VERSION} \
        ## AWS Deps
        && pip3 install boto3 \
        ## Azure Deps (TODO: remove az cli when possible)
        && pip3 install azure-cli
        # && pip3 install -r /usr/lib/python3.11/site-packages/ansible_collections/azure/azcollection/requirements-azure.txt \
        ## Oracle OCI Deps
        && mkdir -p /etc/ansible/collections \
        && ansible-galaxy collection install oracle.oci --collections-path /etc/ansible/collections \
        && pip3 install -r /etc/ansible/collections/ansible_collections/oracle/oci/requirements.txt \
        ## Cleanup
        && apk del .build-deps \
        && rm -rf /var/cache/apk/*

# Add user YaK
RUN adduser -D yak -h /workspace
RUN echo "yak ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/yak
RUN echo "Include /workspace/yak/configuration/infrastructure/.ssh" >> /etc/ssh/ssh_config

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
COPY ./install/profile.sh /etc/profile
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
