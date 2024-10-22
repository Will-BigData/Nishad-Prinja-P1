from pymongo import MongoClient
from datetime import datetime

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