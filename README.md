# finbot
A tiny bot that will help you to track your finances.


## Setup

```bash
conda create -n finbot python=3.11
conda activate finbot
pip install -r requirements.txt

# Install google cloud sdk
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init

# Install protobuf compiler
sudo apt install -y protobuf-compiler
```