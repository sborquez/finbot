#!/bin/bash
source ./settings.sh

# Delete Pub/Sub
gcloud pubsub schemas delete $data-stream_schema-id
