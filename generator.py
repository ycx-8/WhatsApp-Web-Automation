"""Provide functions that generate current date, customized message, contact list from local storage or from Azure Cosmos DB for MongoDB.
"""

from datetime import datetime as dt
from const import CONTACT_PATH_LOCAL, TEMP_PATH
from context import get_collection
import json
from encrydecry import decrypt_json, encrypt_json, is_encrypted


def generate_cur_date():
    """Generate current date

    Returns:
    - dict: A dictionary containing the current date
      ```
      Example:
      {
          'current_date': 'YYYY-MM-DD'
      }
      ```

    Raises:
    - ValueError: If there is an issue retrieving the current date or time.
    """
    try:
        cur_datetime = dt.now().date()
        return {'current date': cur_datetime}
    except Exception as e:
        print(f"An error occurred: {e}")


def generate_msg():
    """Provide user input for the message the user wants to send.

    Returns:
        str: user's custom message.
    """
    msg = input(
        "Enter your msg here\n(If you want to add someone's name, type zzzz as a placeholder)\n> ")
    return msg


def generate_users_from_local():
    """Generate all user details from contact.json stored in the local directory and put them in a list

    The list consists of: contact key, contact name, contact phone number, contact's birthday, contact tag

    Returns:
        list: A list of contact details [key, name, phone number, birthday, tag]
    """
    try:
        if is_encrypted(CONTACT_PATH_LOCAL):
            decrypt_json(CONTACT_PATH_LOCAL)
            with open(CONTACT_PATH_LOCAL) as f:
                data = json.load(f)
            encrypt_json(CONTACT_PATH_LOCAL)
            return convert_contact_dict_to_nested_list(data)
        else:
            print("contacts.json is not encrypted!")
    except Exception as e:
        print(f"An error occurred when trying to load local contact.json: {e}")


def generate_users_from_mongodb():
    """Retrieve users' details from Azure Cosmos DB for MongoDB database and transform them to a nested list of contact information.

    Returns:
        list: A list of contact details [key, name, phone number, birthday, tag]
    """
    data_raw_with_id = get_document_from_azure_mongodb()

    # Omit 1st iteration of _id and add rest of dict to a new dict, then save it to a temp json file for future reads (while the program is still running).
    # TODO: work directly with the data structure received from Azure database, manipulate it to a new dictionary without the _id field.
    data_raw_no_id = {key: value for index,
                      (key, value) in enumerate(data_raw_with_id.items()) if index > 0}
    try:
        with open(TEMP_PATH, 'w') as f:
            json.dump(data_raw_no_id, f, indent=2)
        with open(TEMP_PATH, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"An error occurred when trying to load temp json file: {e}")
        return
    return convert_contact_dict_to_nested_list(data)


def get_document_from_azure_mongodb():
    """Return a document from Azure Cosmos DB for MongoDB as a dictionary.
    
    The dictionary will consists of the document id and the data (which is a list of contact details)

    Returns:
        dict: document id and a list of contact details.
    """
    try:
        collection = get_collection()
        return collection.find_one()
    except Exception as e:
        print(f"An error has occurred when trying to find the document in Azure: {e}")
        return None


def convert_contact_dict_to_nested_list(data):
    """Once data has been retrieved from Azure MongoDB, it is transformed to a nested list in this function.
    
    No need to skip the 1st iteration unlike dealing with contact.json from local directory because we already extracted the json data without _id to the temp file. 

    Args:
        data (dict): a dictionary of contact details

    Returns:
        list: a list of user details [key, name, phone number, birthday, tag]
    """
    contact_list = []    
    for key, value in data.items():
        user_info = [key, value["name"], value["number"],
                     dt.strptime(value["bday"], "%Y-%m-%d").date(), value["tag"]]
        contact_list.append(user_info)
    return contact_list


# -----below for testing-----
# encrypt_json(CONTACT_PATH_LOCAL)
# decrypt_json(CONTACT_PATH_LOCAL)