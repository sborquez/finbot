# !/bin/bash

echo cwd: $(pwd)
# Setup APIs
echo "Setup APIs"
gcloud config set project $project_id
gcloud services enable pubsub.googleapis.com \
                       logging.googleapis.com \
                       eventarc.googleapis.com \
                       cloudfunctions.googleapis.com \
                       cloudbuild.googleapis.com \
                       artifactregistry.googleapis.com
gcloud components update

# Setup permisions
# This step is temporal. I should use some S.A. approach.
echo "Setup permisions"
gcloud auth application-default login
read -p "Enter your email address: " email
gcloud projects add-iam-policy-binding $project_id --role=roles/pubsub.admin --member="user:$email"
