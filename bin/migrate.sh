#!/usr/bin/env bash
source ./bin/utils.sh

set -e
environment=$1
env_check "$environment"
var_check "$PGPORT" "\$PGPORT"

echo "Making sure postgres isn't running on $PGPORT..."

if sudo lsof -i TCP:"$PGPORT" | grep -q 'TCP'; then
  echo "Postgres is already running"
  exit 1
fi

project=$(gcloud config get-value project)

echo "Checking you're on the right project..."
if [ "$project" != "ecosystem-commons" ]; then
  echo "You are working on the wrong project ($project, expected ecosystem-commons)"
  exit 1
fi

if [ "$environment" == "production" ]; then
  echo "Production environment not yet supported."
  exit 1
elif [ "$environment" == "staging" ]; then
  connection=ecosystem-commons:asia-southeast1:ecosystem-commons-dev=tcp:127.0.0.1:$PGPORT
fi

echo "Attempting to connect to $connection..."
cloud_sql_proxy -instances="$connection" >cloud_proxy.log 2>&1 &

echo "Waiting for postgres to respond"
counter=0

while ! nc -z localhost "$PGPORT"; do

  if [[ "$counter" -gt 20 ]]; then
    echo "Tried to connect to postgres $counter times but failed to connect!"
    cat cloud_proxy.log
    exit 1
  fi

  echo "Postgres not online yet... Tried $counter times"
  sleep 1
  counter=$((counter + 1))
done

PGHOST=127.0.0.1 ./manage.py migrate

echo "Killing children..."
pkill -P $$

echo "Removing cloud proxy log..."
rm cloud_proxy.log

echo "Done!"
