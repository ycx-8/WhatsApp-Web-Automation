"""
Script Name: msgsender.py

This script provides functions to automate sending birthday, holiday messages, customized messages and photos to a list of contact (can be filtered through tags) via WhatsApp Web.

It utilizes the selenium to automate this process. The contact can be updated and retrieved in and from a local directory or Azure Cosmos DB for MongoDB
"""

from time import sleep
from datetime import datetime as dt
from const import PATH, DOCUMENT_ID, TEMP_PATH
from urllib.parse import quote
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import mongodb_context as db
from bson import ObjectId
import generator as gen
    
    
def send_txtmsg(user, msg):
    """send automated message via WhatsApp Web to a phone number.

    Args:
        user (list): user details including user key, user name, user phone number and user birthday.
        msg (str): message to be sent
    """
    # Using selenium: set option so I don't have to login with QR code each time for session persistence.
    dir_path = os.getcwd()
    profile = os.path.join(dir_path, "profile", "wpp")
    ops = webdriver.ChromeOptions()
    ops.add_argument(f"user-data-dir={profile}")
    ops.add_experimental_option('excludeSwitches', ['enable-logging'])
    link = f"https://web.whatsapp.com/send?phone={user[2]}&text={msg}"

    # Load message and send
    driver = webdriver.Chrome(options=ops)
    driver.maximize_window()
    driver.get(link)
    selector = "#main > footer > div._2lSWV._3cjY2.copyable-area > div > span:nth-child(2) > div > div._1VZX7 > div._2xy_p._3XKXx > button"
    send_btn = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
    driver.implicitly_wait(5)
    send_btn.click()
    # change sleep time for demo purposes
    sleep(5)
    driver.quit()


def update_year_in_local(user):
    """Increment user's birthday year by one after birthday message is sent and update list of user details (json)

    Args:
        user (list): user details including user key, user name, user phone number and user birthday.
    """
    with open(PATH, "r") as f:
        data = json.load(f)
        data_split = user[3].strftime("%Y-%m-%d").split("-")
        data_split_year_increment = str(int(data_split[0])+1)
        data_split_month = data_split[1]
        data_split_day = data_split[2]

    bday_year_increment_update = f"{
        data_split_year_increment}-{data_split_month}-{data_split_day}"

    data[user[0]]["bday"] = bday_year_increment_update

    with open(PATH, "w") as f:
        json.dump(data, f, indent=2)

    return data


def update_year_in_cloud(user):
    """_summary_

    Args:
        user (_type_): _description_

    Returns:
        _type_: _description_
    """
    with open(TEMP_PATH, "r") as f:
        data = json.load(f)
        data_split = user[3].strftime("%Y-%m-%d").split("-")
        data_split_year_increment = str(int(data_split[0])+1)
        data_split_month = data_split[1]
        data_split_day = data_split[2]

    bday_year_increment_update = f"{
        data_split_year_increment}-{data_split_month}-{data_split_day}"

    data[user[0]]["bday"] = bday_year_increment_update
    with open(TEMP_PATH, "w") as f:
        json.dump(data, f, indent=2)
        
    # If you go into Azure Cosmos DB for MongoDB account (RU) Data Explorer you have refresh the entire tab (rather than just the refresh button for the document) to see the updated results. This is probably a bug from Microsoft.
    collection = db.get_collection()
    collection.update_one({"_id": ObjectId(DOCUMENT_ID)}, {"$set": data})
    return data


def send_bday_msgs_from_local(user_list):
    """Send customized automated birthday messages to a list of contacts

    Args:
        user_list (dict): the contact list to go through in order to send automated messages.

    Returns:
        dict: updated contact list.
    """
    current_date = gen.generate_cur_date()["current date"]
    updated_data = {}
    for user in user_list:
        # Custom message
        msg = f"Happy Birthday {user[1]}! Hope you have a good one!"

        # If bday matches:
        if current_date == user[3]:
            send_txtmsg(user, msg)
            updated_data = update_year_in_local(user)
            print(f"It is {user[1]}'s bday today! Msg sent")
        else:
            print(f"NOT {user[1]}'s bday today")
    return updated_data


def send_bday_msgs_from_cloud(user_list):
    """Send customized automated birthday messages to a list of contacts

    Args:
        user_list (dict): the contact list to go through in order to send automated messages.

    Returns:
        dict: updated contact list.
    """
    current_date = gen.generate_cur_date()["current date"]
    updated_data = {}
    for user in user_list:
        # Custom message
        msg = f"Happy Birthday {user[1]}! Hope you have a good one!"

        # If bday matches:
        if current_date == user[3]:
            send_txtmsg(user, msg)
            updated_data = update_year_in_cloud(user)
            print(f"It is {user[1]}'s bday today! Msg sent")
        else:
            print(f"NOT {user[1]}'s bday today")
    return updated_data


def send_holiday_msgs(user_list):
    """_summary_

    Args:
        user_list (_type_): _description_
    """
    current_date = gen.generate_cur_date()["current date"]
    current_date_to_compare = dt(int(dt.now().year), int(
        dt.now().month), int(dt.now().day)).date()
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
            

def send_custom_msg(user_list):
    """_summary_

    Args:
        user_list (_type_): _description_
    """
    msg = gen.generate_msg()
    for user in user_list:
        msg_customized = msg.replace("zzzz", user[1])
        send_txtmsg(user, msg_customized)
        
