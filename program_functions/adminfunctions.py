from .mongovars import customer_collection, log_collection, deku_collection, inventory_collection
from datetime import datetime

def whether_create_store():
    whether_store_initialize = input("\033[1m" + "Would you like to initialize the store? (Y/n) " + "\033[0m")
    if (whether_store_initialize.lower().startswith("y")):
        initialize_store()
        log_collection.insert_one( { "log" : "Deku store data initialized.", "when": datetime.now() } )
    else:
        print("Store not initialized!")
        log_collection.insert_one( { "log" : "Deku store was not initialized.", "when": datetime.now() } )

def initialize_store():
        deku_collection.delete_many({})
        log_collection.insert_one( { "log" : "Deku store was DELETEd. It is now empty.", "when": datetime.now() } )
        inventory_collection.delete_many({})
        log_collection.insert_one( { "log" : "Customer inventory was DELETEd. It is now empty.", "when": datetime.now() } )

        document_list = [{"item" : "Kokiri Sword", "cost" : 100},
                    {"item" : "Deku Shield", "cost" : 40},
                    {"item" : "Deku Nuts", "cost" : 20},
                    {"item" : "Slingshot", "cost" : 80},
                    {"item" : "Slingshot Bullets", "cost" : 20},
                    {"item" : "Deku Stick (6 pieces)", "cost" : 10},
                    ]

        deku_collection.insert_many(document_list)
        log_collection.insert_one( { "log" : "Deku Store inventory was INSERTed.", "when": datetime.now() } )

def choose_user_editing():
    whether_edit_delete = input("\033[1m" + "Would you like to (e)dit or (d)elete a customer account? Or (n)ot? " + "\033[0m")
    match (whether_edit_delete.strip().lower()[0]):
        case('n'):
            pass
        case('e'):
            admin_editing_inputs()
        case('d'):
            admin_deleting_inputs()

def admin_editing_inputs():            
    while(True):
        customer_user = input("What customer would you like to edit? ")
        if ((customer_collection.count_documents( { "user" : { "$eq": customer_user.lower() } } )) == 0):
            log_collection.insert_one( { "log" : "Queried database for non-existing user during UPDATE!", "when": datetime.now() } )
            print("The customer username you searched for does not exist!")
            continue
        customer_updated_user = input("\033[1m" + "What would you like to edit? The (u)sername or (p)assword? " + "\033[0m")
        match (customer_updated_user.strip().lower()[0]):
            case('u'):
                new_username = input("What username would you like to change this user to? ")
                customer_collection.update_one( { "user" : customer_user.lower() }, { "$set" : { "user" : new_username.lower() } } )
                log_collection.insert_one( { "log" : f"UPDATEd customer username {customer_user} to {new_username}!", "when": datetime.now() } )
                print("Customer username updated!")
                return
            case('p'):
                new_password = input("What would you like to change this customer's password to? ")
                customer_collection.update_one( { "user" : customer_user.lower() }, { "$set" : { "password" : new_password } } )
                log_collection.insert_one( { "log" : f"UPDATEd customer username {customer_user}'s password!", "when": datetime.now() } )
                print("Customer password updated!")
                return

def admin_deleting_inputs():
    while(True):
        customer_user = input("What customer would you like to delete? ")
        if ((customer_collection.count_documents( { "user" : { "$eq": customer_user.lower() } } )) == 0):
            log_collection.insert_one( { "log" : "Queried database for non-existing user during DELETE!", "when": datetime.now() } )
            print("The customer username you searched for does not exist!")
            continue
        customer_collection.delete_one( { "user" : customer_user.lower() } )
        log_collection.insert_one( { "log" : f"DELETEd customer username {customer_user}!", "when": datetime.now() } )
        print(f"Customer username {customer_user} deleted!")
        return
    
def choose_item_editing():
    update_or_delete_store = input("\033[1m" + "Would you like to (a)dd, (e)dit, or (d)elete items from the store? Or (n)ot? " + "\033[0m")
    match (update_or_delete_store.strip().lower()[0]):
        case('n'):
            pass
        case('a'):
            admin_add_item()
        case('e'):
            admin_edit_item()
        case('d'):
            admin_delete_item()
            
def admin_add_item():
    item_to_add = input("What is the name of the item you would like to add? ")
    cost_of_item = input("What is the cost of the item you are adding? ")
    deku_collection.insert_one( { "item" : item_to_add, "cost": int(cost_of_item) } )
    log_collection.insert_one( { "log" : f"ADDed item to store {item_to_add} with cost {cost_of_item}!", "when": datetime.now() } )
    print("\033[1m" + f"You added {item_to_add} to the Deku Store with a cost of {cost_of_item}!" + "\033[0m")

def admin_edit_item():
    while(True):
        store_item_update = input("What item would you like to edit? ")
        if ((deku_collection.count_documents( { "item" : { "$eq": store_item_update } } )) == 0):
            log_collection.insert_one( { "log" : "Queried database for non-existing STORE ITEM during UPDATE!", "when": datetime.now() } )
            print("The item you searched for does not exist!")
            continue
        deku_updated_item = input("\033[1m" + "What would you like to edit? The (i)tem or (c)ost? " + "\033[0m")
        match (deku_updated_item.strip().lower()[0]):
            case('i'):
                new_updated_item = input("What item would you like to change this specific item to? ")
                deku_collection.update_one( { "item" : store_item_update }, { "$set" : { "item" : new_updated_item } } )
                log_collection.insert_one( { "log" : f"UPDATEd item name {store_item_update} to {new_updated_item}!", "when": datetime.now() } )
                print(f"Store item {store_item_update} updated to {new_updated_item}!")
                return
            case('c'):
                new_cost = int(input("What would you like to change this item's cost to? "))
                deku_collection.update_one( { "item" : store_item_update }, { "$set" : { "cost" : new_cost } } )
                log_collection.insert_one( { "log" : f"UPDATEd item {store_item_update}'s cost to {new_cost}!", "when": datetime.now() } )
                print(f"Store item {store_item_update}'s cost updated to {new_cost}!")
                return

def admin_delete_item():
    while(True):
        store_item_delete = input("What item would you like to delete? ")
        if ((deku_collection.count_documents( { "item" : { "$eq": store_item_delete } } )) == 0):
            log_collection.insert_one( { "log" : "Queried database for non-existing STORE ITEM during DELETE!", "when": datetime.now() } )
            print("The item you searched for does not exist!")
            continue
        deku_collection.delete_one( { "item" : store_item_delete } )
        log_collection.insert_one( { "log" : f"DELETEd item {store_item_delete}!", "when": datetime.now() } )
        print(f"Item named {store_item_delete} deleted!")
        return
    
def admin_output_logs():
    output_logs = input("\033[1m" + "Would you like to (o)utput logs, (d)elete all logs? Or (n)ot? " + "\033[0m")
    match (output_logs.strip().lower()[0]):
        case('n'):
            pass
        case('o'):
            all_logs = log_collection.find()
            for log in all_logs:
                print(f"{log['log']:64}" , " | recorded: " + str(log["when"]))
        case('d'):
            log_collection.delete_many({})
            log_collection.insert_one( { "log" : "All logs were DELETEd. The logs are now empty.", "when": datetime.now() } )