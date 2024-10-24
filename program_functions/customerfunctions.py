from .mongovars import customer_collection, log_collection, deku_collection, inventory_collection
import random
from datetime import datetime

def customer_options(customer_username):
    while(True):
        whether_collect_buy = input("\033[1m" + "Would you like to (s)cavenge for more rupees or (v)isit the store? Or (e)xit? " + "\033[0m")
        match (whether_collect_buy.strip().lower()[0]):
            case('s'):
                while(True):
                    choice_scavenge = input("\033[1m" + "Would you like to (b)reak pots in people's houses, (c)ut grass, or (k)ill an enemy to earn more rupees? Or (e)xit? " + "\033[0m")
                    match (choice_scavenge.strip().lower()[0]):
                        case('b'):
                            break_pots(customer_username)
                            continue
                        case('c'):
                            cut_grass(customer_username)
                            continue
                        case('k'):
                            kill_enemy(customer_username)
                            continue
                        case('e'):
                            break
            case('v'):
                    buy_sell_options(customer_username)
            case('e'):
                return

def break_pots(customer_username):
    broken_pots_rupees = random.randint(5, 11)
    customer_collection.update_one( { "user" : customer_username.lower() }, { "$inc" : { "wallet" : broken_pots_rupees } } )
    log_collection.insert_one( { "log" : f"UPDATEd after breaking pots to increase wallet by {broken_pots_rupees}!", "when": datetime.now() } )
    current_wallet = customer_collection.distinct("wallet", { "user" : customer_username.lower() } )
    log_collection.insert_one( { "log" : f"QEURIEd for current amount in wallet after BREAKING POTS!", "when": datetime.now() } )
    print("You broke pots to collect rupees!")
    print(f"{customer_username} your wallet increased by {broken_pots_rupees} rupees and is now {current_wallet[0]} rupees full!")

def cut_grass(customer_username):
    cut_grass = random.randint(1, 14)
    customer_collection.update_one( { "user" : customer_username.lower() }, { "$inc" : { "wallet" : cut_grass } } )
    log_collection.insert_one( { "log" : f"UPDATEd after cutting grass to increase wallet by {cut_grass}!", "when": datetime.now() } )
    current_wallet = customer_collection.distinct("wallet", { "user" : customer_username.lower() } )
    log_collection.insert_one( { "log" : f"QEURIEd for current amount in wallet after CUTTING GRASS!", "when": datetime.now() } )
    print("You cut a patch of tall grass and gathered the rupees that fell out!")
    print(f"{customer_username} your wallet increased by {cut_grass} rupees and is now {current_wallet[0]} rupees full!")

def kill_enemy(customer_username):
    kill_enemy = random.randint(3, 16)
    customer_collection.update_one( { "user" : customer_username.lower() }, { "$inc" : { "wallet" : kill_enemy } } )
    log_collection.insert_one( { "log" : f"UPDATEd after killing enemy to increase wallet by {kill_enemy}!", "when": datetime.now() } )
    current_wallet = customer_collection.distinct("wallet", { "user" : customer_username.lower() } )
    log_collection.insert_one( { "log" : f"QEURIEd for current amount in wallet after KILLING ENEMY!", "when": datetime.now() } )
    enemy_type = ["Amy", "Anubis", "Armos", "Baby Dodongo", "Bari", "Beamos", "Beth", "Big Blade", "Big Deku Baba", "Big Poe", "Big Skulltula", "Biri", "Blade Trap", "Blue Bubble", "Blue Tektite", "Boulder", "Business Scrub", "Club Moblin", "Deku Baba", "Deku Scrub", "Dinolfos", "Dodongo", "Trap Door", "Fire Eye", "Fire Keese", "Flame Wall", "Flat", "Floor Spikes", "Floormaster", "Flying Pot", "Crazy Floor Tile", "Freezard", "Gerudo Guard", "Gibdo", "Gohma Larva", "Gold Skulltula", "Green Bubble", "Guay", "Guillotine", "Ice Keese", "Ice Scythe", "Joelle", "Keese", "Leever", "Like Like", "Lizalfos", "Mad Scrub", "Magma Bomb", "Meg", "Moblin", "Octorok", "Parasitic Tentacle", "Peahat", "Peahat Larva", "Poe", "ReDead", "Red Bubble", "Red Tektite", "Shabom", "Sharp", "Shell Blade", "Skulltula", "Skullwalltula", "Skull Kid", "Spike", "Spiked-Log Trap", "Stalchild", "Stalfos", "Stinger", "Tailpasaran", "Torch Slug", "Toxic Water", "Wallmaster", "White Bubble", "White Wolfos", "Wolfos"]
    your_enemy = random.choice(enemy_type)
    print("You killed an enemy! The enemy you fought was the " + "\033[4m" + f"{your_enemy}" + "\033[0m" + ".")
    print(f"{customer_username} your wallet increased by {kill_enemy} rupees and is now {current_wallet[0]} rupees full!")

def buy_sell_options(customer_username):
    while(True):
        store_decision = input("\033[1m" + "Would you like to (b)uy or (s)ell? Or (e)xit? " + "\033[0m")
        match(store_decision.strip().lower()[0]):
            case('b'):
                buy_option(customer_username)
            case('s'):
                sell_option(customer_username)
            case('e'):
                break

def buy_option(customer_username):
    entire_store = deku_collection.find()
    log_collection.insert_one( { "log" : f"QEURIEd for ENTIRE STORE!", "when": datetime.now() } )
    print("These are the items we have for sale in the Deku Store!")
    
    for item in entire_store:
        print(item["item"], " | cost: " + str(item["cost"]))

    if (entire_store.retrieved == 0):
        print("\033[1m" + "We have no inventory available for sale!" + "\033[0m")
        return

    current_wallet = customer_collection.distinct("wallet", { "user" : customer_username.lower() } )
    log_collection.insert_one( { "log" : f"QEURIEd for current amount in wallet during TRANSACTION!", "when": datetime.now() } )
    print(f"Your wallet has {current_wallet[0]} rupees!")
    item_bought = input("\033[1m" + "What item would you like to buy? " + "\033[0m")

    if ((deku_collection.count_documents( { "item" : { "$eq": item_bought } } )) == 0):
        log_collection.insert_one( { "log" : "Queried database for non-existing STORE ITEM during TRANSACTION!", "when": datetime.now() } )
        print("The item you searched for does not exist!")
        return
    
    item_to_buy = deku_collection.distinct("cost", { "item" : item_bought } )
    log_collection.insert_one( { "log" : f"QEURIEd for item cost during TRANSACTION!", "when": datetime.now() } )

    if (current_wallet[0] - item_to_buy[0] < 0):
        print("You do not have enough money to buy this!")
        print("\n")
        log_collection.insert_one( { "log" : f"WARNED customer that he/she has INSUFFICIENT FUNDS!", "when": datetime.now() } )
        return
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

def sell_option(customer_username):
    entire_inventory = inventory_collection.find()
    log_collection.insert_one( { "log" : f"QEURIEd for ENTIRE INVENTORY!", "when": datetime.now() } )
    print("These are the items you have in your inventory to sell to the Deku Store!")


    for item in entire_inventory:
        print(item["item"], " | sale value: " + str(item["sell_price"]))

    if (entire_inventory.retrieved == 0):
        print("\033[1m" + "You have no inventory available for sale!" + "\033[0m")
        return
    
    current_sell_wallet = customer_collection.distinct("wallet", { "user" : customer_username.lower() } )
    print(f"Your wallet has {current_sell_wallet[0]} rupees!")
    log_collection.insert_one( { "log" : f"QEURIEd for current amount in wallet during SALE!", "when": datetime.now() } )
    item_selling = input("\033[1m" + "What item would you like to sell? " + "\033[0m")

    if ((inventory_collection.count_documents( { "item" : { "$eq": item_selling } } )) == 0):
        log_collection.insert_one( { "log" : "Queried database for non-existing STORE ITEM during SALE!", "when": datetime.now() } )
        print("The item you searched for does not exist!")
        return
    
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