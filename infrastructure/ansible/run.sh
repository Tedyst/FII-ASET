#!/bin/bash

exec ansible-playbook playbooks/main.yml -i inventory.yml --vault-password-file secrets.pass
