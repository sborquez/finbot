import os

from googleapiclient.discovery import build

import finbot_core.py.transaction_v1_pb2 as transaction_v1_pb2
import finbot_stream.google_credentials as google_credentials


def write_to_file(transactions: list[transaction_v1_pb2.Transaction], output_file: str) -> None:
    """
    Writes a list of Transaction Protobufs to a file.

    Args:
        transactions: A list of Transaction Protobufs.
        output_file: The output CSV file to write the data to.
    """
    print("Writing to file...")
    header = [
        'uuid', 'checked', 'date', 'income', 'expense', 'account', 'installment_type',
        'description', 'category',  'subcategory'
    ]
    if not os.path.exists(output_file):
        with open(output_file, "w") as f:
            f.write(",".join(header) + "\n")
    # read uuids
    with open(output_file, "r") as f:
        uuids = set(map(lambda row: row.split(",")[0], f.readlines()[1:]))

    # write new transactions
    with open(output_file, "a") as f:
        for transaction in filter(lambda transaction: transaction.uuid not in uuids, transactions):
            f.write(",".join([
                transaction.uuid,
                "FALSE",
                transaction.date,
                str(transaction.amount) if transaction.type == transaction_v1_pb2.TransactionType.INCOME else "",
                str(transaction.amount) if transaction.type == transaction_v1_pb2.TransactionType.EXPENSE else "",
                transaction.account_alias,
                str(transaction.installment_type),
                transaction.description,
                "",
                ""
            ]) + "\n")


def write_to_google_sheet(transactions: list[transaction_v1_pb2.Transaction], spreadsheet_id: str, token_file: str) -> None:
    """
    Writes a list of Transaction Protobufs to a Google Sheet.

    Args:
        transactions: A list of Transaction Protobufs.
        sheet: The Google Sheet to write the data to.
    """
    print("Writing to Google Sheet...")
    # Setup Credentials
    creds = google_credentials.setup_credentials(token_file, google_credentials.SCOPES)

    # Connect to Google Sheets API
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    # Find the last row
    result = (
        sheet
        .values()
        .get(
            spreadsheetId=spreadsheet_id,
            range="FinBot!A1:A",
        )
        .execute()
    )
    last_row = len(result.get("values", [])) + 1
    uuids = set(map(lambda row: row[0], result.get("values", [])))

    # Build the body
    header = [
        'uuid', 'checked', 'date', 'income', 'expense', 'account', 'installment_type',
        'description', 'category',  'subcategory'
    ]
    values = []
    if last_row == 1:
        values.append(header)

    for transaction in filter(lambda transaction: transaction.uuid not in uuids, transactions):
        values.append([
            str(transaction.uuid),
            "FALSE",
            transaction.date,
            str(transaction.amount).replace('.', ',') if transaction.type == transaction_v1_pb2.TransactionType.INCOME else "",
            str(transaction.amount).replace('.', ',') if transaction.type == transaction_v1_pb2.TransactionType.EXPENSE else "",
            transaction.account_alias,
            str(transaction.installment_type),
            transaction.description,
            "",
            ""
        ])
    write_rows = len(values)
    response = (
        sheet
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            valueInputOption="USER_ENTERED",
            range=f"FinBot!A{last_row}:{chr(ord('A') + len(header) - 1)}{last_row + write_rows - 1}",
            body={
               "values": values
            },
        )
        .execute()
    )
    print('Sheet successfully Updated')
