#! /usr/bin/env bash
set -eou pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

username=$(cat $SCRIPT_DIR/../.env | grep POSTGRES_USER | cut -d "=" -f 2)
password=$(cat $SCRIPT_DIR/../.env | grep POSTGRES_PASSWORD | cut -d "=" -f 2)
db=$(cat $SCRIPT_DIR/../.env | grep POSTGRES_DB | cut -d "=" -f 2)

psql "postgresql://$username:$password@localhost:5431/$db"
