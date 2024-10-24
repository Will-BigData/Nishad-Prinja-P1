import program_functions
from datetime import datetime

def main():
    while(True):
        try:
            role = int(input("\033[1m" + "Select your role: [Admin = 1, Customer = 2] or 3 = exit. " + "\033[0m"))    
        except:
            print("Invalid entry for role selection!")
            continue

        admin_logged_in = False
        customer_logged_in = False

        if (role == 1):
            admin_logged_in = program_functions.adminLogin()
        elif (role == 2):
            registration = input("\033[1m" + "Are you a registered customer? [Yes/No] " + "\033[0m")
            if (registration.lower().startswith("n")):
                program_functions.customerRegistration()
            else:
                customer_logged_in, customer_username = program_functions.customerLogin()
        elif (role == 3):
            break
        elif (role != 1 or role != 2 or role != 3):
            print("Invalid selection!")
            program_functions.log_collection.insert_one( { "log" : "Invalid selection of user role.", "when": datetime.now() } )

        if (admin_logged_in):
            while(True):
                admin_menu = input("\033[1m" + "Would you like to (1) create the store, (2) manage user accounts, (3) manage the Deku Store, (4) output or delete the log outputs? Or (e)xit? " + "\033[0m")
                match(admin_menu):
                    case("1"):
                        program_functions.whether_create_store()
                    case("2"):
                        program_functions.choose_user_editing()
                    case("3"):
                        program_functions.choose_item_editing()
                    case("4"):
                        program_functions.admin_output_logs()
                    case("e"):
                        print("Thanks for managing the system! Goodbye!")
                        break

        if (customer_logged_in):
            program_functions.customer_options(customer_username)

if __name__ == '__main__':
    main()

    