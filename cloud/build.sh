#!/bin/bash
# This file is for setting up the cloud project.
source ./settings.sh

# 1. Setup the project
echo "1. Setup the project  $project_id"

# Setup APIs
echo "Setup APIs"
# Check if the project exists
if gcloud projects list | grep -q $project_id; then
    echo "Project $project_id exists"
    gcloud config set project $project_id
else
    echo "Project $project_id does not exist"
    echo "Creating project $project_id"
    gcloud projects create $project_id
    gcloud config set project $project_id
    gcloud services enable logging.googleapis.com \
                        eventarc.googleapis.com \
                        cloudfunctions.googleapis.com \
                        cloudbuild.googleapis.com \
                        artifactregistry.googleapis.com
    gcloud components update
fi

# Setup permisions
# This step is temporal. I should use some S.A. approach.
echo "Setup permisions"
gcloud auth application-default login

