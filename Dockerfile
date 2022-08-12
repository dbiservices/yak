FROM debian:11.4

RUN  apt-get update \
     && apt-get dist-upgrade -y \
     && mkdir -p /dev /usr/share/ansible/collections \
     && apt-get install bash sudo git wget curl unzip python3-pip jq vim tree iputils-ping traceroute dnsutils -y \
     # Terraform
     # ---------
     && TERRAFORM_VERSION=`curl -s https://checkpoint-api.hashicorp.com/v1/check/terraform | jq -r -M '.current_version'` \
     && wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
     && unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /usr/local/bin \
     # Ansible
     # -------
     && pip3 install ansible \
     && pip3 install ansible-runner \
     # Oracle OCI Ansible collection
     # ------------------------------
     && mkdir -p /etc/ansible/collections \
     && ansible-galaxy collection install oracle.oci --collections-path /etc/ansible/collections \
     # Azure Ansible Collection
     # ------------------------
     && pip3 install -r /usr/local/lib/python3.9/dist-packages/ansible_collections/azure/azcollection/requirements-azure.txt \
     # Install Windows Remote Manager
     # ------------------------------
     && pip3 install pywinrm \
     # AWS CLI
     # -------
     && pip3 install boto3 \
     && pip3 install boto \
     && pip3 install ansible-lint \
     && pip3 install requests \
     && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
     && unzip awscliv2.zip \
     && ./aws/install \
     # Oracle OCI-CLI
     # --------------
     && pip3 install oci-cli \
     # Cleanup
     # -------
     && rm -f *.zip

# COPY Sources
COPY ./collections /workspace/yak/collections/
COPY ./configuration /workspace/yak/configuration/
COPY ./inventory /workspace/yak/inventory/
COPY ./servers /workspace/yak/servers/
COPY ./ansible.cfg /workspace/yak/

COPY ./install/entry-point.sh /entry-point.sh
COPY ./install/yakhelp.lst /yakhelp.lst
RUN chmod u+x /entry-point.sh
RUN chmod ugo+x /yakhelp.lst
ENV LANG en_US.utf8

ENTRYPOINT ["/entry-point.sh"]
