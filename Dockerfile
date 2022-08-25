FROM registry.gitlab.com/yak4all/yakenv:1.0.0

# COPY Sources
COPY ./collections /workspace/yak/collections/
COPY ./configuration /workspace/yak/configuration/
COPY ./inventory /workspace/yak/inventory/
COPY ./servers /workspace/yak/servers/
COPY ./licenses /workspace/yak/lisenses
COPY ./ansible.cfg /workspace/yak/
COPY ./COPYING /workspace/yak/
COPY ./README.md /workspace/yak/
COPY ./YAK_SETUP.md /workspace/yak/

COPY ./install/entry-point.sh /entry-point.sh
COPY ./install/yakhelp.lst /yakhelp.lst
RUN chmod u+x /entry-point.sh
RUN chmod ugo+x /yakhelp.lst
ENV LANG en_US.utf8

ENTRYPOINT ["/entry-point.sh"]
