import pymongo
from pymongo import MongoClient
from datetime import datetime
import random
import json

def main():

    # Connect to server
    uri = "mongodb://localhost:27017/"
    client = MongoClient(uri)

    logging_db = client["pystore_logs"]
    log_collection = logging_db["logs"]   

    log_collection.insert_one( { "log" : "Connecting to MongoDB Database!", "when": datetime.now() } )

    admin_database = client["admin"]
    admin_collection = admin_database["admins"]

    customer_db = client["customer"]
    customer_collection = customer_db["customers"]

    deku_store_db = client["deku_store"]
    deku_collection = deku_store_db["deku_items"] 

    inventory_db = client["inventory_storage"]
    inventory_collection = inventory_db["inventory"]

    def create_admin():
        document_list = [{"user" : "zelda", "password" : "pwd"},
                     {"user" : "link", "password" : "password"}]

        admin_collection.insert_many(document_list)
        log_collection.insert_one( { "log" : "Updated records with new admin accounts!", "when": datetime.now() } )

    initialize_admins = input("\033[1m" + "Would you like to create the admin users? (Y/n) " + "\033[0m")
    if (initialize_admins.lower().startswith("y")):
        create_admin()
        log_collection.insert_one( { "log" : "Admin roles created!", "when": datetime.now() } )
    else:
        pass

    #Role selection
    role = int(input("\033[1m" + "Select your role: [Admin = 1, Customer = 2] " + "\033[0m"))    

    def adminLogin():
        adminUsername = input("Enter your username: ")
        adminPassword = input("Enter your password: ")

        find_admin = admin_collection.count_documents( { "$and": [ {"user" : {"$eq": adminUsername.lower()} }, {"password" : {"$eq" : adminPassword}} ] })
        log_collection.insert_one( { "log" : "Counted records of matching Admin/password!", "when": datetime.now() } )
        # print(find_admin)
        if (find_admin):
            print("You have successfully logged in!")
            log_collection.insert_one( { "log" : "Admin logged in!", "when": datetime.now() } )
            return find_admin
        else:
            print("Invalid username or password, please try again.")
            log_collection.insert_one( { "log" : "Invalid password entered for Admin!", "when": datetime.now() } )

    def customerRegistration():  
        while(True):
            customerUsername = input("What is your desired username?: ")
            customerPassword = input("What is your desired password?: ")

            if ((customer_collection.count_documents( { "user" : { "$eq": customerUsername.lower() } } )) != 0):
                log_collection.insert_one( { "log" : "Queried database for existing user!", "when": datetime.now() } )
                print("Already a user by this name!")
                log_collection.insert_one( { "log" : "Customer tried to register with username already in database!", "when": datetime.now() } )
            else:
                customer_collection.insert_one( { "user" : customerUsername.lower(), "password" : customerPassword, "wallet" : 0 } )
                log_collection.insert_one( { "log" : "Database insert procedure executed for new customer username/password!", "when": datetime.now() } )
                print("You have successfully created an account!")
                log_collection.insert_one( { "log" : "Customer created an account!", "when": datetime.now() } )
                return
            
    def customerLogin():
        while(True):
            customerUsername = input("Enter your username: ")
            customerPassword = input("Enter your password: ")
            find_customer = customer_collection.count_documents( { "$and": [ {"user" : {"$eq": customerUsername.lower()} }, {"password" : {"$eq" : customerPassword}} ] })
            log_collection.insert_one( { "log" : "Counted records of matching customer/password!", "when": datetime.now() } )
            # print(find_customer)
            if (find_customer):
                print ("You have successfully logged in!")
                log_collection.insert_one( { "log" : "Customer logged in!", "when": datetime.now() } )
                return find_customer, customerUsername
            else:
                print("Invalid username or password, please try again.")
                log_collection.insert_one( { "log" : "Rejected login. Customer entered invalid information!", "when": datetime.now() } )
                continue
    
    def initialize_store():
        document_list = [{"item" : "Kokiri Sword", "cost" : 100},
                    {"item" : "Deku Shield", "cost" : 40},
                    {"item" : "Deku Nuts", "cost" : 20},
                    {"item" : "Slingshot", "cost" : 80},
                    {"item" : "Slingshot Bullets", "cost" : 20},
                    {"item" : "Deku Stick (6 pieces)", "cost" : 10},
                    ]

        deku_collection.insert_many(document_list)

    admin_logged_in = 0
    customer_logged_in = 0

    if (role == 1):
        admin_logged_in = adminLogin()
    elif (role == 2):
        registration = input("\033[1m" + "Are you a registered customer? [Yes/No] " + "\033[0m")
        if (registration.lower().startswith("n")):
            customerRegistration()
        else:
            customer_logged_in, customer_username = customerLogin()
            # print(customer_logged_in)
            # print(customer_username)
    elif (role != 1 or role != 2):
        print("Invalid selection!")
        log_collection.insert_one( { "log" : "Invalid selection of user role.", "when": datetime.now() } )

    if (admin_logged_in):
        whether_store_initialize = input("\033[1m" + "Would you like to initialize the store? (Y/n) " + "\033[0m")
        if (whether_store_initialize.lower().startswith("y")):
            initialize_store()
            log_collection.insert_one( { "log" : "Deku store data initialized.", "when": datetime.now() } )
        else:
            print("Store not initialized!")
            log_collection.insert_one( { "log" : "Deku store was not initialized.", "when": datetime.now() } )
        
        whether_edit_delete = input("\033[1m" + "Would you like to (e)dit or (d)elete a customer account? Or (n)ot? " + "\033[0m")
        match (whether_edit_delete.strip().lower()[0]):
            case('n'):
                pass
            case('e'):
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
            case('d'):
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
        
        update_or_delete_store = input("\033[1m" + "Would you like to (a)dd, (e)dit, or (d)elete items from the store? Or (n)ot? " + "\033[0m")
        match (update_or_delete_store.strip().lower()[0]):
            case('n'):
                pass
            case('a'):
                item_to_add = input("What is the name of the item you would like to add? ")
                cost_of_item = input("What is the cost of the item you are adding? ")
                deku_collection.insert_one( { "item" : item_to_add, "cost": int(cost_of_item) } )
                log_collection.insert_one( { "log" : f"ADDed item to store {item_to_add} with cost {cost_of_item}!", "when": datetime.now() } )
                print("\033[1m" + f"You added {item_to_add} to the Deku Store with a cost of {cost_of_item}!" + "\033[0m")
            case('e'):
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
            case('d'):
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
        output_logs = input("\033[1m" + "Would you like to (o)utput logs Or (n)ot? " + "\033[0m")
        match (output_logs.strip().lower()[0]):
            case('n'):
                pass
            case('o'):
                all_logs = log_collection.find()
                for log in all_logs:
                    print(log["log"], " | recorded: " + str(log["when"]))


    if (customer_logged_in):
            while(True):
                whether_collect_buy = input("\033[1m" + "Would you like to (s)cavenge for more rupees or (b)uy items? Or (e)xit? " + "\033[0m")
                match (whether_collect_buy.strip().lower()[0]):
                    case('s'):
                        while(True):
                            choice_scavenge = input("\033[1m" + "Would you like to (b)reak pots in people's houses, (c)ut grass, or (k)ill an enemy to earn more rupees? Or (e)xit? " + "\033[0m")
                            match (choice_scavenge.strip().lower()[0]):
                                case('b'):
                                    broken_pots_rupees = random.randint(5, 11)
                                    customer_collection.update_one( { "user" : customer_username.lower() }, { "$inc" : { "wallet" : broken_pots_rupees } } )
                                    log_collection.insert_one( { "log" : f"UPDATEd after breaking pots to increase wallet by {broken_pots_rupees}!", "when": datetime.now() } )
                                    current_wallet = customer_collection.distinct("wallet", { "user" : customer_username.lower() } )
                                    log_collection.insert_one( { "log" : f"QEURIEd for current amount in wallet after BREAKING POTS!", "when": datetime.now() } )
                                    print("You broke pots to collect rupees!")
                                    print("\n")
                                    print(f"{customer_username} your wallet increased by {broken_pots_rupees} rupees and is now {current_wallet[0]} rupees full!")
                                    continue
                                case('c'):
                                    cut_grass = random.randint(1, 14)
                                    customer_collection.update_one( { "user" : customer_username.lower() }, { "$inc" : { "wallet" : cut_grass } } )
                                    log_collection.insert_one( { "log" : f"UPDATEd after cutting grass to increase wallet by {cut_grass}!", "when": datetime.now() } )
                                    current_wallet = customer_collection.distinct("wallet", { "user" : customer_username.lower() } )
                                    log_collection.insert_one( { "log" : f"QEURIEd for current amount in wallet after CUTTING GRASS!", "when": datetime.now() } )
                                    print("You cut a patch of tall grass and gathered the rupees that fell out!")
                                    print("\n")
                                    print(f"{customer_username} your wallet increased by {cut_grass} rupees and is now {current_wallet[0]} rupees full!")
                                    continue
                                case('k'):
                                    kill_enemy = random.randint(3, 16)
                                    customer_collection.update_one( { "user" : customer_username.lower() }, { "$inc" : { "wallet" : kill_enemy } } )
                                    log_collection.insert_one( { "log" : f"UPDATEd after killing enemy to increase wallet by {kill_enemy}!", "when": datetime.now() } )
                                    current_wallet = customer_collection.distinct("wallet", { "user" : customer_username.lower() } )
                                    log_collection.insert_one( { "log" : f"QEURIEd for current amount in wallet after KILLING ENEMY!", "when": datetime.now() } )
                                    enemy_type = ["Amy", "Anubis", "Armos", "Baby Dodongo", "Bari", "Beamos", "Beth", "Big Blade", "Big Deku Baba", "Big Poe", "Big Skulltula", "Biri", "Blade Trap", "Blue Bubble", "Blue Tektite", "Boulder", "Business Scrub", "Club Moblin", "Deku Baba", "Deku Scrub", "Dinolfos", "Dodongo", "Trap Door", "Fire Eye", "Fire Keese", "Flame Wall", "Flat", "Floor Spikes", "Floormaster", "Flying Pot", "Crazy Floor Tile", "Freezard", "Gerudo Guard", "Gibdo", "Gohma Larva", "Gold Skulltula", "Green Bubble", "Guay", "Guillotine", "Ice Keese", "Ice Scythe", "Joelle", "Keese", "Leever", "Like Like", "Lizalfos", "Mad Scrub", "Magma Bomb", "Meg", "Moblin", "Octorok", "Parasitic Tentacle", "Peahat", "Peahat Larva", "Poe", "ReDead", "Red Bubble", "Red Tektite", "Shabom", "Sharp", "Shell Blade", "Skulltula", "Skullwalltula", "Skull Kid", "Spike", "Spiked-Log Trap", "Stalchild", "Stalfos", "Stinger", "Tailpasaran", "Torch Slug", "Toxic Water", "Wallmaster", "White Bubble", "White Wolfos", "Wolfos"]
                                    your_enemy = random.choice(enemy_type)
                                    print(f"You killed an enemy! The enemy you fought was the {your_enemy}.")
                                    print("\n")
                                    print(f"{customer_username} your wallet increased by {kill_enemy} rupees and is now {current_wallet[0]} rupees full!")
                                    continue
                                case('e'):
                                    break

                    
                    case('b'):
                        while(True):
                            entire_store = deku_collection.find()
                            entire_inventory = inventory_collection.find()
                            log_collection.insert_one( { "log" : f"QEURIEd for ENTIRE STORE!", "when": datetime.now() } )
                            # print(entire_store)
                            store_decision = input("\033[1m" + "Would you like to (b)uy or (s)ell? Or (e)xit? " + "\033[0m")
                            match(store_decision.strip().lower()[0]):
                                case('b'):
                                    # pass
                                    print("These are the items we have for sale in the Deku Store!")
                                    for item in entire_store:
                                        print(item["item"], " | cost: " + str(item["cost"]))
                                    current_wallet = customer_collection.distinct("wallet", { "user" : customer_username.lower() } )
                                    log_collection.insert_one( { "log" : f"QEURIEd for current amount in wallet during TRANSACTION!", "when": datetime.now() } )
                                    print(f"Your wallet has {current_wallet[0]} rupees!")
                                    item_bought = input("What item would you like to buy? ")
                                    if ((deku_collection.count_documents( { "item" : { "$eq": item_bought } } )) == 0):
                                        log_collection.insert_one( { "log" : "Queried database for non-existing STORE ITEM during TRANSACTION!", "when": datetime.now() } )
                                        print("The item you searched for does not exist!")
                                        continue
                                    item_to_buy = deku_collection.distinct("cost", { "item" : item_bought } )
                                    log_collection.insert_one( { "log" : f"QEURIEd for item cost during TRANSACTION!", "when": datetime.now() } )
                                    # print(item_to_buy[0])
                                    if (current_wallet[0] - item_to_buy[0] < 0):
                                        print("You do not have enough money to buy this!")
                                        print("\n")
                                        log_collection.insert_one( { "log" : f"WARNED customer that he/she has INSUFFICIENT FUNDS!", "when": datetime.now() } )
                                        continue
                                    else:
                                        customer_collection.update_one( { "user" : customer_username.lower() }, { "$inc" : { "wallet" : -item_to_buy[0] } } )
                                        wallet_after_sale = customer_collection.distinct("wallet", { "user" : customer_username.lower() } )
                                        log_collection.insert_one( { "log" : f"QUERIEd customer wallet AFTER TRANSACTION!", "when" : datetime.now() } )
                                        print(f"Your wallet now has {wallet_after_sale[0]} rupees!")
                                        log_collection.insert_one( { "log" : f"UPDATEd customer wallet to reflect his/her purchase!", "when": datetime.now() } )
                                        inventory_collection.insert_one( { "item" : item_bought, "sell_price" : item_to_buy[0] - int(item_to_buy[0] * .2) } )
                                        log_collection.insert_one( { "log" : f"UPDATEd customer inventory with item and sale value!", "when": datetime.now() } )
                                        deku_collection.delete_one( { "item" : item_bought } )
                                        log_collection.insert_one( { "log" : f"DELETEd purchased item from the Deku Store's items!", "when": datetime.now() } )
                                case('s'):
                                    print("These are the items you have in your inventory to sell to the Deku Store!")
                                    for item in entire_inventory:
                                        print(item["item"], " | sale value: " + str(item["sell_price"]))
                                    current_sell_wallet = customer_collection.distinct("wallet", { "user" : customer_username.lower() } )
                                    print(f"Your wallet has {current_sell_wallet[0]} rupees!")
                                    log_collection.insert_one( { "log" : f"QEURIEd for current amount in wallet during SALE!", "when": datetime.now() } )
                                    item_selling = input("What item would you like to sell? ")
                                    if ((inventory_collection.count_documents( { "item" : { "$eq": item_selling } } )) == 0):
                                        log_collection.insert_one( { "log" : "Queried database for non-existing STORE ITEM during SALE!", "when": datetime.now() } )
                                        print("The item you searched for does not exist!")
                                        continue
                                    item_to_sell = inventory_collection.distinct("sell_price", { "item" : item_selling } )
                                    log_collection.insert_one( { "log" : f"QEURIEd for item cost during SALE!", "when": datetime.now() } )
                                    customer_collection.update_one( { "user" : customer_username.lower() }, { "$inc" : { "wallet" : item_to_sell[0] } } )
                                    wallet_after_sale = customer_collection.distinct("wallet", { "user" : customer_username.lower() } )
                                    log_collection.insert_one( { "log" : f"QUERIEd customer wallet AFTER SALE!", "when" : datetime.now() } )
                                    print(f"Your wallet now has {wallet_after_sale[0]} rupees!")
                                    log_collection.insert_one( { "log" : f"UPDATEd customer wallet to reflect his/her sale of item!", "when": datetime.now() } )
                                    deku_collection.insert_one( { "item" : item_selling, "cost" : item_to_sell[0] + int(item_to_sell[0] * .3) } )
                                    log_collection.insert_one( { "log" : f"UPDATEd Deku Store with item and sale value!", "when": datetime.now() } )
                                    inventory_collection.delete_one( { "item" : item_selling } )
                                    log_collection.insert_one( { "log" : f"DELETEd purchased item from the inventory of items!", "when": datetime.now() } )

                                case('e'):
                                    break

                    case('e'):
                        return
        

    client.close()

if __name__ == '__main__':
    main()

    