#!/bin/bash

# Log preparation status
echo "Preparing image..."

# Check virtual environment is activated
if [[ -z "${VIRTUAL_ENV}" ]] ; then
    echo "Please activate your virtual environment then re-run script"
    exit 1
fi

# Prepare image
bash $PROJECT_ROOT/scripts/network/delete_all_wifi_connections.sh

sudo rm -f $PROJECT_ROOT/data/registration