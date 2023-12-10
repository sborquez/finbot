
import argparse
import os

# Import the Google Auth library.
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


# Define the scopes required for accessing Gmail API
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/spreadsheets",
]


def setup_credentials(token_file: str, scopes: list[str]) -> Credentials:
    """
    Sets up the credentials for accessing the Gmail API.

    Args:
        token_file: The path to the token file.
        scopes: The scopes required for accessing the Gmail API.

    Returns:
        The credentials for accessing the Gmail API.
    """
    if not os.path.exists(token_file):
        raise FileNotFoundError("The token file does not exist.")
    creds = Credentials.from_authorized_user_file(
        token_file, scopes
    )
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise ValueError("The credentials are invalid.")
        with open(token_file, "w") as token:
            token.write(creds.to_json())
    return creds


def generate_token(credentials_file: str, token_file: str, scopes: list[str] = SCOPES) -> None:
    """
    Generates a new token for accessing the Google Sheets and Gmail APIs.

    Args:
        credentials_file: The path to the credentials file.
        token_file: The path to the token file.
        scopes: The scopes required for accessing the Gmail API.
    """

    # Load client secrets from a file
    flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)

    # Run the OAuth 2.0 authorization flow
    credentials = flow.run_local_server(port=0)

    # Save the credentials to a file
    with open(token_file, "w") as f:
        f.write(credentials.to_json())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a new Gmail token")
    parser.add_argument("--credentials_file", help="Path to the credentials file")
    parser.add_argument("--token_file", help="Path to the token file")
    args = parser.parse_args()

    generate_token(args.credentials_file, args.token_file)
