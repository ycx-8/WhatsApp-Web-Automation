import wwma as w
from datetime import datetime as dt
import config.mongodb_context as db
from config.const import DOCUMENT_ID
from bson import ObjectId



def send_bday_msgs(user_list):
    current_date = w.generate_time()["current date"]
    updated_data = {}
    for user in user_list:
        # Custom message
        msg = f"Happy Birthday {user[1]}! Hope you have a good one!"

        # If bday matches:
        if current_date == user[3]:
            w.send_msg(user, msg)
            updated_data = w.increment_year(user)
            print(f"It is {user[1]}'s bday today! Msg sent")
        else:
            print(f"NOT {user[1]}'s bday today")
    return updated_data
            

def send_holiday_msgs(user_list):
    current_date = w.generate_time()["current date"]
    current_date_to_compare = dt(int(dt.now().year), int(
        dt.now().month), int(dt.now().day)).date()
    for user in user_list:
        if current_date == dt(int(dt.now().year), 12, 25).date():
            msg = f"Merry Xmas {user[1]}! May your holidays be filled with joy and laughter."
            w.send_msg(user, msg)
        elif current_date == dt(int(dt.now().year), 1, 1).date():
            msg = f"Happy New Year {user[1]}! May your holidays be filled with joy and laughter. Wishing you a happy and prosperous New Year filled with joy and new beginnings!"
            w.send_msg(user, msg)
        elif current_date == current_date_to_compare:
            msg = f"Happy {dt.now().strftime("%A")} {user[1]}! Hope you have a productive day!"
            w.send_msg(user, msg)


def send_custom_msg(user_list):
    msg = w.generate_msg()
    for user in user_list:
        msg_customized = msg.replace("zzzz", user[1])
        w.send_msg(user, msg_customized)
        

def main():    
    while True:
        local_or_db = input("Do you want to work with offline storage or Azure CosmosDB (sync both contacts stored locally and on the cloud)?\n1 for offline, 2 for Azure, q to quit\n>> ")
        if local_or_db == "q":
            break
        
        if local_or_db == "2":
            user_list = w.generate_users_from_db()  
            user_op_str = input("1 for bday\n2 for holiday\n3 for custom msg\nq to quit\n> ")
            if user_op_str == "q":
                continue
            user_op_int = int(user_op_str)
            if user_op_int == 1:
                updated_data = send_bday_msgs(user_list)
                collection = db.get_collection()
                collection.update_one({"_id": ObjectId(DOCUMENT_ID)}, {"$set": updated_data})
                # w.update_year_to_cloud(user)
            elif user_op_int == 2:
                send_holiday_msgs(user_list)
            elif user_op_int == 3:
                send_custom_msg(user_list)
                
        if local_or_db == "1":
            user_list = w.generate_users_from_local()
            user_op_str = input("1 for bday\n2 for holiday\n3 for custom msg\nq to quit\n>> ")
            if user_op_str == "q":
                continue
            user_op_int = int(user_op_str)
            if user_op_int == 1:
                send_bday_msgs(user_list)
            elif user_op_int == 2:
                send_holiday_msgs(user_list)
            elif user_op_int == 3:
                send_custom_msg(user_list)
            

def main_alt():
    """An alternative to main(): sync both locally stored contact list (as a JSON file) plus that stored in MongoDB as a document.
    """
    msg_sent_count = 0
    # print(f"{msg_sent_count} bday msgs sent today")  # should be 2
    while True:
        user_list = w.generate_users_from_local()  
        user_op_str = input("1 for bday\n2 for holiday\n3 for custom msg\nq to quit\n> ")
        if user_op_str == "q":
            return
        user_op_int = int(user_op_str)
        
        if user_op_int == 1:
            updated_data = send_bday_msgs(user_list, msg_sent_count)
            collection = db.get_collection()
            collection.update_one({"_id": ObjectId(DOCUMENT_ID)}, {"$set": updated_data})
            
        elif user_op_int == 2:
            send_holiday_msgs(user_list)
            
        elif user_op_int == 3:
            send_custom_msg(user_list)


if __name__ == "__main__":
    # main_alt()
    main()