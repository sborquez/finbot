"""
Gmail Source
------------

This file will contain the code that will extract data from the Gmail API.

In this file, we will create a extract_gmail_data function that will extract
the data from the gmail API and return a list of Transaction Protobufs.

We will also create a function that will take a list of Transaction Protobufs
and write them to a file and/or to a Google Sheet.
"""
import os
import sys

# TODO: Check if this work with Cloud Functions
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import base64
import datetime
import json
import re
from typing import Callable, Dict, List, Optional

# # Import the Google Auth library.
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Import the Transaction Protobuf.
import finbot_core.py.transaction_v1_pb2 as transaction_v1_pb2

TOKEN_FILE = os.environ.get("TOKEN_FILE", "token.json")
ACCOUNT_DATA_FILE = os.environ.get("ACCOUNT_DATA", "account_data.json")
with open(ACCOUNT_DATA_FILE, "r") as f:
    ACCOUNT_DATA = json.load(f)


def parse_bancochile_email(mail: dict) -> Optional[transaction_v1_pb2.Transaction]:
    """
    Extracts data from a Banco Chile email.

    Args:
        mail: A dict representing the email. The dict is in the format returned by
            the Gmail API.

    Returns:
        A Transaction Protobuf.
    """
    # Get data from headers
    subject = None
    owner_email = None
    for header in mail["payload"]["headers"]:
        if header["name"] == "Subject":
            subject = header["value"]
        elif header["name"] == "To":
            owner_email = re.search(r"<(.*)>", header["value"]).group(1)

    # Get data from body
    print(f"Parsing: {subject}")
    if subject == "Compra con Tarjeta de Crédito":
        content = mail["snippet"]
        pattern = re.compile(
            r"(.*?): Te informamos que se ha realizado una compra por \$(?P<amount>[\d.]+) con Tarjeta de Crédito \*\*\*\*(?P<account>\d{4}) en (?P<description>[^0-9]+) el (?P<date>\d{2}/\d{2}/\d{4} \d{2}:\d{2})."
        )
        match = pattern.search(content).groupdict()
        if not match:
            return None

        # Build Transaction Protobuf
        transaction = transaction_v1_pb2.Transaction()
        transaction.account_owner_email = owner_email

        account_uuid = match["account"]
        transaction.account_uuid = account_uuid
        transaction.account_alias = ACCOUNT_DATA[owner_email][account_uuid].get("alias", None)
        transaction.account_type = transaction_v1_pb2.AccountType.CREDIT_CARD
        transaction.account_bank = "Banco de Chile"
        transaction.account_currency = ACCOUNT_DATA[owner_email][account_uuid].get("currency", None)

        date = datetime.datetime.strptime(match["date"],  "%d/%m/%Y %H:%M")
        transaction.date = date.strftime("%Y-%m-%d")
        transaction.gdate_time = date.strftime("%Y-%m-%dT%H:%M:%S")

        transaction.amount = float(match["amount"])
        transaction.type = transaction_v1_pb2.TransactionType.EXPENSE
        transaction.description = match["description"]

        transaction.installment_type = transaction_v1_pb2.InstallmentType.SINGLE
        # transaction.installment = 1
        # transaction.total_installments = 1
        # transaction.total_amount = transaction.amount

        transaction.uuid = str(hash(owner_email + transaction.gdate_time + content))
    else:
        print(f"Unknown subject: {subject}")
        # content = mail["payload"]["parts"][0]["body"]["data"]
        transaction = None

    return transaction


PARSERS: Dict[str, Callable[[dict], Optional[transaction_v1_pb2.Transaction]]] = {
    "enviodigital@bancochile.cl": parse_bancochile_email,
}


def extract_gmail_data(date: Optional[str] = None, senders: List[str] = ["enviodigital@bancochile.cl"]) -> List[transaction_v1_pb2.Transaction]:
    """
    Extracts data from the Gmail API.

    Args:
        date: The date to extract the data from. If None, then extract today's
            data. The date is in the format YYYY-MM-DD.

    Returns:
        A list of Transaction Protobufs.
    """
    # Setup Credentials
    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
    if not os.path.exists(TOKEN_FILE):
        raise FileNotFoundError("The token file does not exist.")
    creds = Credentials.from_authorized_user_file(
        TOKEN_FILE, SCOPES
    )
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise ValueError("The credentials are invalid.")
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    # Build query 
    if not date:
        print("No date provided.")
        date = datetime.date.today().strftime("%Y-%m-%d")
    query = f"after:{date}"

    if senders:
        query += " AND ("
        for sender in senders:
            query += f"from:{sender} OR "
        query = query[:-4] + ")"
    print(query)

    # Call the Gmail API
    transactions = []
    try:
        service = build("gmail", "v1", credentials=creds)
        results = service.users().messages().list(userId="me", q=query).execute()
        messages = results.get("messages", [])
        if not messages:
            print("No messages found.")
            return []
        else:
            print(f"Found {len(messages)} messages.")
        print("Parsing messages...")
        for message in messages:
            msg = service.users().messages().get(userId="me", id=message["id"]).execute()
            from_email = next(filter(lambda header: header["name"] == "From", msg["payload"]["headers"]))["value"]
            from_email = re.search(r"<(.*)>", from_email).group(1)
            transaction = PARSERS[from_email](msg)
            if transaction:
                print(transaction)
                # TODO: Mark message as read 
                transactions.append(transaction)
            else:
                print("No transaction found.")

    except errors.HttpError as error:
        print(f"An error occurred: {error}")

    return transactions


def write_to_file(transactions: List[transaction_v1_pb2.Transaction]) -> None:
    """
    Writes a list of Transaction Protobufs to a file.

    Args:
        transactions: A list of Transaction Protobufs.
    """
    pass


def write_to_google_sheet(transactions: List[transaction_v1_pb2.Transaction]) -> None:
    """
    Writes a list of Transaction Protobufs to a Google Sheet.

    Args:
        transactions: A list of Transaction Protobufs.
    """
    pass


def main(
    date: Optional[str] = None, senders: List[str] = ["enviodigital@bancochile.cl"],
    output_file: Optional[str] = None, sheet: Optional[str] = None) -> None:
    """
    Extracts data from the Gmail API and writes it to a file and/or to a Google
    Sheet.

    Args:
        output_file: The output file to write the data to.
        sheet: The Google Sheet to write the data to.
    """
    transactions = extract_gmail_data(date, senders)
    if output_file:
        write_to_file(transactions)
    if sheet:
        write_to_google_sheet(transactions)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Extracts data from the Gmail API.")
    parser.add_argument(
        "-d", "--date",
        help="The date to extract the data from. If None, then extract today's data. The date is in the format YYYY-MM-DD.")
    parser.add_argument(
        "-q", "--senders",
        nargs="*",  # 0 or more arguments
        default=["enviodigital@bancochile.cl"],
        help="The senders to extract the data from.")
    parser.add_argument(
        "-o", "--output_file",
        help="The output file to write the data to.")
    parser.add_argument(
        "-s", "--sheet",
        help='The Google Sheet to write the data to.')
    args = parser.parse_args()

    main(args.date, args.senders, args.output_file, args.sheet)
