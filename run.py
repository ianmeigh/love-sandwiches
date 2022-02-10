import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")

# sales = SHEET.worksheet("sales")
# data = sales.get_all_values()
# print(data)


def get_sales_data():
    """
    Get sales figures input from the user
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10, 20, 30, 40, 50, 60\n")

        data_str = input("Enter your data here: ")
        sales_data = (data_str.replace(" ", "")).split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data


def validate_data(values):
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    try:
        values = [int(value) for value in values]
        number_of_columns = get_num_columns_in_worksheet("sales")

        if len(values) != number_of_columns:
            raise ValueError(
                f"Exactly {number_of_columns} values required "
                f"you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again\n")
        return False
    else:
        return True


def update_worksheet(data, worksheet):
    """
    Update specified worksheet, add new row with the list data provided.
    """
    print("Updating sales worksheet...\n")

    try:
        valid_worksheet_names = ["sales", "surplus", "stock"]
        if not (worksheet in valid_worksheet_names):
            raise ValueError(
                "Incorrect worksheet name entered, couldn't update.."
            )
    except ValueError as e:
        print(f"Internal error: {e}")
    else:
        worksheet_to_update = SHEET.worksheet(worksheet)
        worksheet_to_update.append_row(data)
        print(f"{worksheet.capitalize()} worksheet appended successfully.\n")


def calculate_surplus_data(sales_data):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    surplus_data = [
        int(stock) - sales for stock, sales in zip(stock_row, sales_data)
    ]

    return surplus_data


def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data
    as a list of lists.
    """

    sales = SHEET.worksheet("sales")
    number_of_columns = get_num_columns_in_worksheet("sales")

    columns = []
    for i in range(1, number_of_columns + 1):
        num_items_per_column = len(sales.col_values(i))
        column_excluding_header = sales.col_values(i)[1:num_items_per_column]
        last_5_entries = column_excluding_header[-5:]
        columns.append(last_5_entries)

    return columns


def get_num_columns_in_worksheet(worksheet):
    """
    Get the number of columns from the specified worksheet, allowing
    new sandwich types to be added.
    """
    worksheet_to_check = SHEET.worksheet(worksheet)
    return len(worksheet_to_check.row_values(1))


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")


print("Welcome to Love Sandwiches Data Automation\n")
# main()
sales_columns = get_last_5_entries_sales()
pprint(sales_columns)
