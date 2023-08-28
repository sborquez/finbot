# !/bin/bash

# Create a schema
echo "Create a schema"
gcloud pubsub schemas create $data_stream_schema_id \
        --type=$data_stream_schema_type \
        --definition-file=$data_stream_schema_definition
gcloud pubsub schemas describe $data_stream_schema_id

# # Create a topic with a schema
# echo "Create a topic with a schema"
# gcloud pubsub topics create $topic_id \
#         --message-encoding=BINARY \
#         --schema=$data_stream_schema_id
