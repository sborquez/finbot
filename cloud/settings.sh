# !/bin/bash
# Use this file to define the project variables

# Project id
export project_id='finbot-data'

# PubSub for data stream ingestion
export data_stream_topic_id='finbot-data-stream'
export data_stream_schema_id='transaction-schema'
export data_stream_schema_type='PROTOCOL_BUFFER'
export data_stream_schema_definition='../protobuff/definitions/transaction_v1.proto'

# FireStore
# export firestore_enable=true
# export firestore_region='nam5'
# export database_id='sensors-data'