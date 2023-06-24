#!/usr/bin/env bash
source ./bin/utils.sh

set -e
environment=$1

env_check "$environment"

echo "About to deploy a new revision to $1"

tag=$(get_tag)
hash=$(get_hash)

if [ "$environment" == "production" ]; then
  echo "Releasing to production"
  #gcloud run services update --image "$tag" --region=asia-southeast1 prod-peppermint-api --update-env-vars STATIC_URL="https://cdn.peppermint-api.com/web/$hash/"
  #gcloud run services update --image "$tag" --region=asia-southeast1 prod-peppermint-worker --update-env-vars STATIC_URL="https://cdn.peppermint-api.com/web/$hash/"
  url="https://ecosystem-commons.com"
fi

if [ "$environment" == "staging" ]; then
  echo "Releasing to staging"
  gcloud run services update --image "$tag" --region=asia-southeast1 dev-commons-api --update-env-vars STATIC_URL="https://cdn.ecosystem-commons.com/web/$hash/"
  gcloud run services update --image "$tag" --region=asia-southeast1 dev-commons-tasks --update-env-vars STATIC_URL="https://cdn.ecosystem-commons.com/web/$hash/"
  url="https://ecosystem-commons.dev"
fi

curl -X POST --data-urlencode \
  "payload={\"channel\": \"#proj_ecosystem_commons\", \"username\": \"Cosmic Owl\", \"text\": \"Released $tag to $url.\", \"icon_emoji\": \":owl:\"}" \
  "https://hooks.slack.com/services/$SLACK_WEBHOOK_SECRET"
