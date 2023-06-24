#!/usr/bin/env bash

function get_hash() {
  hash=$(git rev-parse --short HEAD)
  echo "$hash"
}

function get_tag() {
  tag=asia-southeast1-docker.pkg.dev/ecosystem-commons/ecosystem-commons/app:$(date +%y.%m.%d)-$(get_hash)
  echo "$tag"
}

function env_check() {
  if [ "$1" != "production" ] && [ "$1" != "staging" ]; then
    echo "Build environment is not one of production or staging"
    exit 1
  fi
}

function var_check() {
  if [ -z "$1" ]; then
    echo "Variable $2 is not set."
    exit 1
  fi
}
