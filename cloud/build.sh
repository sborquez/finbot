#!/bin/bash
# This file is for setting up the cloud project.
source ./settings.sh

# Steps:
# Some steps are required once. So you can commented if it is necessary.

# 1. Setup the project
echo "1. Setup the project  $project_id"
bash ./build_steps/01_setup.sh

# 2. Setup PubSubs
echo "2. Setup PubSubs"	
bash ./build_steps/02_pubsub.sh

# # 3. Setup FireStore
# # This step is optional. Denpends on the "enable_firestore" variable in variables.sh
# if [ $enable_firestore = true ]; then
#     # a. Create FireStore database
#     echo "6.a Create FireStore database"
#     # gcloud firestore databases create --region=$cluster_zone
# else
#     echo "FireStore is disabled. Skipping step 6."
# fi
