#!/bin/bash
# This file is for setting up the cloud project.
source ./settings.sh

# Delete previus schema
gcloud pubsub schemas delete $data_stream_schema_id

# Create a schema
gcloud pubsub schemas create $data_stream_schema_id \
        --type=$data_stream_schema_type \
        --definition-file=$data_stream_schema_definition
gcloud pubsub schemas describe $data_stream_schema_id

# Update the topic with a schema
# gcloud pubsub topics update $topic_id \
#     --schema=$schema_id \
#     --message-encoding=BINARY