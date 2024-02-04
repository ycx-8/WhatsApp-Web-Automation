import msgsender as w
import generator as gen
from const import TEMP_PATH
import os


def main():    
    while True:
        local_or_db = input("Do you want to work with offline storage or Azure CosmosDB?\n1 for offline, 2 for Azure, q to quit\n>> ")
        if local_or_db == "q":
            break
        
        if local_or_db == "1":
            user_list = gen.generate_users_from_local()
            user_op_str = input("1 for bday\n2 for holiday\n3 for custom msg\nq to quit\n>> ")
            if user_op_str == "q":
                continue
            user_op_int = int(user_op_str)
            if user_op_int == 1:
                w.send_bday_msgs_from_local(user_list)
            elif user_op_int == 2:
                w.send_holiday_msgs(user_list)
            elif user_op_int == 3:
                w.send_custom_msg(user_list)
        
        if local_or_db == "2":
            user_list = gen.generate_users_from_mongodb()  
            user_op_str = input("1 for bday\n2 for holiday\n3 for custom msg\nq to quit\n> ")
            if user_op_str == "q":
                continue
            user_op_int = int(user_op_str)
            if user_op_int == 1:
                w.send_bday_msgs_from_cloud(user_list)
            elif user_op_int == 2:
                w.send_holiday_msgs(user_list)
            elif user_op_int == 3:
                w.send_custom_msg(user_list)
                
            
if __name__ == "__main__":
    main()
    if os.path.exists(TEMP_PATH):
        os.remove(TEMP_PATH)
    else:
        print(f"Path does not exist or offline storage was used")