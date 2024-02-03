"""
Script Name: wwma.py

This script provides functions to automate sending birthday, holiday messages, customized messages and photos to a list of contact (can be filtered through tags) via WhatsApp Web.

It utilizes the selenium to automate this process. The contact can be updated and retrieved in and from a local directory or Azure Cosmos DB for MongoDB
"""

from time import sleep
import jsonpickle as jp
from datetime import datetime as dt
from config.const import PATH, DOCUMENT_ID
from urllib.parse import quote
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from platform import system
from config.mongodb_context import get_collection
import config.mongodb_context as db
from bson import ObjectId


def generate_time():
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
    msg = input("Enter your msg here\n(If you want to add someone's name, type zzzz as a placeholder)\n> ")
    return msg


def generate_users_from_local():
    """Generate all user details and put them in a list

    The list consists of: user key, user name, user phone number, user's birthday

    Returns:
        list: A list of user details [key, name, phone number, birthday]
    """
    with open(PATH) as f:
        content = f.read()
        users = jp.decode(content)
        user_list = []
        for key, value in users.items():
            user_info = [key, value["name"], value["number"],
                         dt.strptime(value["bday"], "%Y-%m-%d").date()]
            user_list.append(user_info)
    return user_list


def generate_users_from_db():
    """Retrieve users' details from local MongoDB database
    
    Returns:
        list: A list of user details [key, name, phone number, birthday]
    """
    collecion = get_collection()
    data_raw = collecion.find_one()
    user_list = []
    for i, (key, value) in enumerate(data_raw.items()):
        if i == 0:
            continue
        user_info = [key, value["name"], value["number"], dt.strptime(value["bday"], "%Y-%m-%d").date()]
        user_list.append(user_info)
    return user_list
    
    
def send_msg(user, msg):
    """send automated message via WhatsApp Web to a phone number.

    Args:
        user (list): user details including user key, user name, user phone number and user birthday.
        msg (str): message to be sent
    """
    # w.sendwhatmsg(user[2], msg, dt.now().hour, dt.now().minute+1, wait_time=15, tab_close=True, close_time=5)

    # Using selenium: set option so I don't have to login with QR code each time
    dir_path = os.getcwd()
    profile = os.path.join(dir_path, "profile", "wpp")
    ops = webdriver.ChromeOptions()
    ops.add_argument(f"user-data-dir={profile}")
    ops.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Load message and send
    driver = webdriver.Chrome(options=ops)
    driver.maximize_window()
    driver.get(f"https://web.whatsapp.com/send?phone={user[2]}&text={msg}")
    # driver.implicitly_wait(5)
    # send_btn = driver.find_element(By.CSS_SELECTOR, 'button[data-tab="11"]')
    selector = "#main > footer > div._2lSWV._3cjY2.copyable-area > div > span:nth-child(2) > div > div._1VZX7 > div._2xy_p._3XKXx > button"
    # selector2 = 'button[data-tab="11"]'
    send_btn = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
    driver.implicitly_wait(5)
    send_btn.click()
    sleep(5)
    driver.quit()

    # w.sendwhatmsg(user[2], msg, dt.now().hour, dt.now().minute+1, wait_time=30, tab_close=False)
    # sleep(5)
    # k.press_and_release('ctrl+w')
    # sleep(2)
    # k.press_and_release("enter")

    # caption optinal for the photo
    # w.sendwhats_image(user[2], "Scripts/WhatsApp_Web_Automation/bday1.jpg", wait_time=20, tab_close=False)
    # sleep(6)
    # k.press_and_release('ctrl+w')
    # sleep(2)


def increment_year(user):
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


# def update_year_to_cloud(user):
#     data = generate_users_from_db()
#     data_split = user[3].strftime("%Y-%m-%d").split("-")
#     data_split_year_increment = str(int(data_split[0])+1)
#     data_split_month = data_split[1]
#     data_split_day = data_split[2]

#     bday_year_increment_update = f"{
#         data_split_year_increment}-{data_split_month}-{data_split_day}"

#     data[user[0]]["bday"] = bday_year_increment_update
    
#     collection = db.get_collection()
#     collection.update_one({"_id": ObjectId(DOCUMENT_ID)}, {"$set": data})
#     return data