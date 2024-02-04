"""
Script Name: generator.py

This script provide functions that generate current date, customized message, contact list from local storage and contact list from Azure Cosmos DB for MongoDB.
"""

from datetime import datetime as dt
from const import PATH, TEMP_PATH
from mongodb_context import get_collection
import json


def generate_cur_date():
    """
    Generate current date

    Returns:
    - dict: A dictionary containing the current date
      Example:
      {
          'current_date': 'YYYY-MM-DD'
      }

    Raises:
    - ValueError: If there is an issue retrieving the current date or time.
    """
    try:
        cur_datetime = dt.now().date()
        return {'current date': cur_datetime}
    except Exception as e:
        print(f"An error occurred: {e}")


def generate_msg():
    """Provide user input for the message she wants to send

    Returns:
        str: user's custom message
    """
    msg = input(
        "Enter your msg here\n(If you want to add someone's name, type zzzz as a placeholder)\n> ")
    return msg


def generate_users_from_local():
    """Generate all user details and put them in a list

    The list consists of: user key, user name, user phone number, user's birthday

    Returns:
        list: A list of user details [key, name, phone number, birthday, tag]
    """
    with open(PATH) as f:
        users = json.load(f)
        user_list = []
        for key, value in users.items():
            user_info = [key, value["name"], value["number"],
                         dt.strptime(value["bday"], "%Y-%m-%d").date()]
            user_list.append(user_info)
    return user_list


def generate_users_from_mongodb():
    """Retrieve users' details from local MongoDB database

    Returns:
        list: A list of user details [key, name, phone number, birthday, tag]
    """
    collecion = get_collection()
    data_raw = collecion.find_one()

    # Expensive operation: omit 1st iteration of _id and add rest of dict to a new dict, then save it to a temp json file for future reads
    data_raw_no_id = {key: value for index,
                      (key, value) in enumerate(data_raw.items()) if index > 0}
    with open(TEMP_PATH, 'w') as f:
        json.dump(data_raw_no_id, f, indent=2)
    with open(TEMP_PATH, "r") as f:
        data = json.load(f)

    user_list = []
    # No need to skip the 1st iteration unlike dealing with contact.json from local directory because we already extracted the json data without _id to the temp file. 
    for _, (key, value) in enumerate(data.items()):
        user_info = [key, value["name"], value["number"],
                     dt.strptime(value["bday"], "%Y-%m-%d").date()]
        user_list.append(user_info)

    return user_list