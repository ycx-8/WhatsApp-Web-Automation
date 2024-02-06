"""Provides functions to automate sending birthday, holiday messages, customized text messages and photos to a list of contact (can be filtered through tags) via WhatsApp Web.

It utilizes the selenium to automate this process. The contact can be updated and retrieved in and from a local directory or Azure Cosmos DB for MongoDB. The images and text messages can be retrieved from Azure Blob Storage or locally.
"""

from time import sleep
from datetime import datetime as dt
from const import CONTACT_PATH_LOCAL, DOCUMENT_ID, TEMP_PATH
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import context as db
from bson import ObjectId
import generator as gen
from encrydecry import encrypt_json, decrypt_json
import seutil as se
    
    
def send_txtmsg(user: list, msg=""):
    """Send automated message via WhatsApp Web to a phone number.

    Args:
        user (list): user details including user key, user name, user phone number and user birthday.
        msg (str): message to be sent.
    """
    driver = se.open_whatsapp_web(user=user, msg=msg)
    se.click_send_btn(driver=driver)
    driver.quit()
    

def send_photo(user, msg=""):
    """Send photo via WhatsApp Web to a phone number.

    Args:
        user (list): User's details
        msg (str, optional): Caption for the photo which is optional. Defaults to "".
    """
    driver = se.open_whatsapp_web(user=user, msg=msg)

    se.click_plus_btn_in_chat(driver=driver)
    
    photos_btn_selector = "#main > footer > div._2lSWV._3cjY2.copyable-area > div > span:nth-child(2) > div > div._2xy_p._1bAtO > div._1OT67 > div > span > div > ul > div > div:nth-child(2) > li > div"
    photo_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, photos_btn_selector))
    )
    photo_btn.click()
    
    sleep(3)
    try:
        file_upload_selector = "#main > footer > div._2lSWV._3cjY2.copyable-area > div > span:nth-child(2) > div > div._2xy_p._1bAtO > div._1OT67 > div > span > div > ul > div > div:nth-child(2) > li > div > input[type=file]"
        file_upload = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, file_upload_selector))
        )
        file_upload.send_keys(os.path.abspath("resources/bday_memeDOWNLOAD.jpg"))
        sleep(3)
        se.click_send_photo_btn(driver=driver)
        sleep(6)
        driver.quit()
    except TimeoutError as e:
        print(f"Exception: {e}")
  

def send_documents(user, msg=""):
    pass
  

def update_year_in_local(user: list):
    """Increment user's birthday year by one after birthday message is sent and update list of user details (json)

    Args:
        user (list): user details including user key, user name, user phone number and user birthday.
    """
    with open(CONTACT_PATH_LOCAL, "r") as f:
        decrypt_json(CONTACT_PATH_LOCAL)
        data = json.load(f)
    
    bday_year_increment_update = increment_year(user)
    data[user[0]]["bday"] = bday_year_increment_update
    
    with open(CONTACT_PATH_LOCAL, "w") as f:
        json.dump(data, f, indent=2)
    encrypt_json(CONTACT_PATH_LOCAL)
    return data


def update_year_in_cloud(user: list):
    """_summary_

    Args:
        user (_type_): _description_

    Returns:
        _type_: _description_
    """
    with open(TEMP_PATH, "r") as f:
        data = json.load(f)

    bday_year_increment_update = increment_year(user)
    data[user[0]]["bday"] = bday_year_increment_update
    
    with open(TEMP_PATH, "w") as f:
        json.dump(data, f, indent=2)
        
    # If you go into Azure Cosmos DB for MongoDB account (RU) Data Explorer sometimes you have refresh the entire tab (rather than just the refresh button for the document) to see the updated results. This is probably a bug from Microsoft :(
    collection = db.get_collection()
    collection.update_one({"_id": ObjectId(DOCUMENT_ID)}, {"$set": data})
    return data


def send_bday_msgs_from_local(user_list, msg: str):
    """Send customized automated birthday messages to a list of contacts

    Args:
        user_list (dict): the contact list to go through in order to send automated messages.

    Returns:
        dict: updated contact list.
    """
    current_date = gen.generate_cur_date()["current date"]
    updated_data = {}
    for user in user_list:
        msg_new = msg.replace("zzzz", user[1])
        
        # check leap year
        if is_leap_year(current_date.year):
            # If today is 02-29, consider it as 02-28 for comparison
            if current_date.month == 2 and current_date.day == 29:
                current_date = dt.date(current_date.year, 2, 28)
            # Adjust the birthdate if it's 02-29 in a non-leap year
            if not is_leap_year(user[3].year):
                user[3] = dt.date(user[3].year, 2, 28)
        
        # If bday matches:
        if current_date == user[3]:
            send_txtmsg(user, msg_new)
            send_photo(user)
            updated_data = update_year_in_local(user)
            print(f"It is {user[1]}'s bday today! Msg sent")
        else:
            print(f"NOT {user[1]}'s bday today")
    return updated_data


def send_bday_msgs_from_cloud(user_list, msg: str):
    """Send customized automated birthday messages to a list of contacts.

    Args:
        user_list (dict): the contact list to go through in order to send automated messages.

    Returns:
        dict: updated contact list.
    """
    current_date = gen.generate_cur_date()["current date"]
    updated_data = {}
    for user in user_list:
        # msg = f"Happy Birthday {user[1]}! Hope you have a good one!"
        msg_new = msg.replace("zzzz", user[1])

        # If bday matches:
        if current_date == user[3]:
            send_txtmsg(user, msg_new)
            send_photo(user)
            updated_data = update_year_in_cloud(user)
            print(f"It is {user[1]}'s bday today! Msg sent")
        else:
            print(f"NOT {user[1]}'s bday today")
    return updated_data


def send_holiday_msgs(user_list):   
    """Send Xmas and NY messages to a list of contacts.

    Args:
        user_list (dict): the contact list to go through in order to send automated messages.
    """
    current_date = gen.generate_cur_date()["current date"]
    # current_date_to_compare = dt(int(dt.now().year), int(dt.now().month), int(dt.now().day)).date()
    # TODO: get holiday messages from Azure Blob Storage.
    for user in user_list:
        if current_date == dt(int(dt.now().year), 12, 25).date():
            msg = f"Merry Xmas {user[1]}! May your holidays be filled with joy and laughter."
            send_txtmsg(user, msg)
        elif current_date == dt(int(dt.now().year), 1, 1).date():
            msg = f"Happy New Year {user[1]}! May your holidays be filled with joy and laughter. Wishing you a happy and prosperous New Year filled with joy and new beginnings!"
            send_txtmsg(user, msg)
        # elif current_date == current_date_to_compare:
        #     msg = f"Happy {dt.now().strftime("%A")} {user[1]}! Hope you have a productive day!"
        #     send_msg(user, msg)
        else:
            print("No holiday today!")
            

def send_custom_msg(user_list: dict):
    """Send customized messages (use placeholders for a person's name). Can be filtered through tag input.
    
    Note: user[4] is the associated tag.

    Args:
        user_list (dict): the contact list to go through in order to send automated messages.
    """
    msg = gen.generate_msg()
    tag_filter = input("Enter a tag to send the msg to selected contacts or type 'all' to send to all:\n> ").lower()
    for user in user_list:
        msg_customized = msg.replace("zzzz", user[1])
        if tag_filter == user[4]:
            send_txtmsg(user, msg_customized)
        if tag_filter == "all":
            send_txtmsg(user, msg_customized)
        if tag_filter != "all" and tag_filter != user[4]:
            print("Enter a valid tag or 'all'!")
            break
        

def increment_year(user: list):
    """Increment year by 1

    Args:
        user (list): a contact's details

    Returns:
        str: updated datetime in yyyy-mm-dd format
    """
    data_split = user[3].strftime("%Y-%m-%d").split("-")
    data_split_year_increment = str(int(data_split[0])+1)
    data_split_month = data_split[1]
    data_split_day = data_split[2]
    return f"{data_split_year_increment}-{data_split_month}-{data_split_day}"


def is_leap_year(year: int):
    """Check if a year is a leap year.
    
    Arg:
        year (int): year.
    
    Returns:
        bool: True if it's a leap year, otherwise False.
    """
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


# ----testing----
# send_photo()