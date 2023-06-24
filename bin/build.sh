#!/usr/bin/env bash
source ./bin/utils.sh

set -e

tag=$(get_tag)
hash=$(get_hash)

docker build . --tag "$tag"
docker push "$tag"

mkdir -p "$hash"
export STATIC_ROOT="$hash"

./manage.py collectstatic --noinput

gsutil -m cp -r "$hash/*" "gs://cdn.ecosystem-commons.com/web/$hash/"

rm -rf "$hash"
