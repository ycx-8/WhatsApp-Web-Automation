from datetime import datetime as dt

contact_list = {}


def convert_input_to_date_str(m, d, y=dt.now().year):
    """Convert current year, month and day into the following format: yyyy-mm-dd

    Args:
        m (str): bday month
        d (str): bday day
        y (year, optional): current year. Defaults to dt.now().year.

    Returns:
        str: bday date formatte as yyyy-mm-dd
    """
    # print(f"{y}-{m}-{d}")
    return f"{y}-{m}-{d}"


# while True:
#     # contact_<num> auto increments
#     name = input("Enter 1st name: ")
#     print(name)
#     number = input("Enter phone number (example: +61444666999):\n> ")
#     print(number)
#     bday_month = input("Enter bday month e.g., 07, 12: ")
#     print(bday_month)
#     bday_day = input("Enter bday day e.g., 05, 30: ")

#     pass
