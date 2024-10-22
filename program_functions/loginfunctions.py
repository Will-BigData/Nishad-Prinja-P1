from .mongovars import customer_collection, log_collection, admin_collection
from datetime import datetime

def adminLogin():
    while(True):
        adminUsername = input("Enter your username: ")
        adminPassword = input("Enter your password: ")

        find_admin = admin_collection.count_documents( { "$and": [ {"user" : {"$eq": adminUsername.lower()} }, {"password" : {"$eq" : adminPassword}} ] })
        log_collection.insert_one( { "log" : "Counted records of matching Admin/password!", "when": datetime.now() } )

        if (find_admin > 0):
            print("You have successfully logged in!")
            log_collection.insert_one( { "log" : "Admin logged in!", "when": datetime.now() } )
            return True
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
        if (find_customer > 0):
            print ("You have successfully logged in!")
            log_collection.insert_one( { "log" : "Customer logged in!", "when": datetime.now() } )
            return True, customerUsername
        else:
            print("Invalid username or password, please try again.")
            log_collection.insert_one( { "log" : "Rejected login. Customer entered invalid information!", "when": datetime.now() } )
            continue