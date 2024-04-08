# finbot
A tiny bot that will help you to track your finances.

## TODOs:

- [x] Read emails from Gmail
- [ ] Read from a pdf file
- [ ] Read from a file
- [ ] Read from a Pub/Sub
- [x] Write to a file
- [x] Write to Google Sheets
- [ ] write to  Pub/Sub
- [ ] Write to a firestore database
- [ ] Write to a SQL database
- [ ] Use a serverless framework with Google Cloud Functions

## Setup

### Ubuntu

```bash
conda create -n fb python=3.11
conda activate fb
pip install -r requirements.txt

# Install google cloud sdk
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init

# Install protobuf compiler
sudo apt install -y protobuf-compiler
```

### Windows 11

```powershell
conda create -n fb python=3.11
conda activate fb
pip install -r requirements.txt

# Install google cloud sdk
Invoke-WebRequest -Uri https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe -OutFile gcloudsdk.exe
.\gcloudsdk.exe

# Install protobuf compiler
choco install protoc
```

## Usage

Check the `.vscode/launch.json` file for the usage of the scripts.

## References

* [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
* [Gmail API](https://developers.google.com/gmail/api/quickstart/python)
* [Protobuf](https://developers.google.com/protocol-buffers)
<!-- * [Google Sheets API](https://developers.google.com/sheets/api/quickstart/python) -->