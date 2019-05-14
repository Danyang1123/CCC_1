#!/bin/bash
chmod 600 resources/nectarssh.key
. ./openrc.sh; ansible-playbook nectar.yaml
# If instaling web and data servers separately
# # ansible-playbook webserver.yaml
# # ansible-playbook dataserver.yaml