import os

def clear_scr():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')

def get_names(admin_login=False):
    clear_scr()
    print("Admin Login" if admin_login else "User Login")
    while True:
        try:
            name = input("Enter your name : ")
            password = int(input("Enter your password : "))
            clear_scr()
            break
        except ValueError:
            clear_scr()
            print("Invalid Input")
            print("Enter the correct name and password !\n")
    return [name, password]

def check_values(user, password, database):
    for keys, values in database.items():
        if user == keys and password == values:
            return True
    return False

def auth_user(database, name, password, admin=False):
    if admin:
        return True if check_values(name, password, database) else False
    if not admin:
        return True if check_values(name, password, database) else False

def find_balance(deno, bal=0):
    for keys, vals in deno.items():
        bal += keys*vals
    return bal

def return_bal(amt, bal=0, vals=[2000, 1000, 500, 200, 100]):
    for i in range(len(amt)):
        bal += vals[i]*amt[i]
    return bal


def validate_deno(deno, available_deno):
    max_threshold = {2000: 500, 1000: 500, 500: 500, 200: 500, 100: 500}
    for index, (val) in enumerate(max_threshold):
        if deno[index] + available_deno[val] > max_threshold[val]:
            return False
    return True

def update_money(old, new, updated={}):
    for index, (key, value) in enumerate(old.items()):
        updated[key] = value + new[index]
    return updated

def change_pin(database, name, new_pin):
    database[name] = new_pin
    return database

def get_money():
    clear_scr()
    print("Enter the deno below")
    print("2000 1000 500 200 100\n")
    demonimations = list(map(int, input().split()))
    return demonimations

def generate_deno(amt, deno=[], vals=[2000, 1000, 500, 200, 100]):
    for i in vals:
        deno.append(amt//i)
        amt = amt % i
    return deno

def validate_transfer(name, amount, balance_database, threshold):
    return True if amount < balance_database[name] and threshold[name]+amount < 200000 else False

def transfer_funds(from_name, to_name, amount, balance_database):
    balance_database[from_name] = balance_database[from_name] - amount
    balance_database[to_name] = balance_database[to_name] + amount
    return balance_database

def validate_atm_funds(amount, available_deno):
    return amount < find_balance(available_deno)

def get_send_details():
    while True:
        try:
            name = input("Enter the name of the person you want to transfer : ")
            amount = int(input("Enter the amount : "))
            break
        except ValueError:
            clear_scr()
            print("Invalid amount")
    clear_scr()
    return [name, amount]

# Stored Data
stored_admin_data = {"Kaushik": 12345}
stored_user_data = {"ks": 123, "ck": 1234, "cp": 12345}
available_deno = {2000: 20, 1000: 20, 500: 40, 200: 50, 100: 100}
available_bal = {"ks": 250000, "ck": 300000, "cp": 500500}
max_user_threshold = {"ks": 0, "ck": 0, "cp": 0}

# Driver Code
clear_scr()
while True:
    print("ATM Application")
    try:
        user_choice = int(input("1. Admin Login\n2. User Login\n3. Exit\n"))
    except ValueError:
        continue
    if user_choice == 3:
        clear_scr()
        exit()

    if user_choice == 1:
        name, password = get_names(admin_login=True)
        if (auth_user(stored_admin_data, name, password, admin=True)):
            clear_scr()
            print("Welcome admin {}!".format(name))

            while True:
                admin_choice = int(
                    input("1. Add Money\n2. Check Balance\n3. Exit \n"))

                if admin_choice == 1:
                    deno = get_money()
                    if validate_deno(deno, available_deno):
                        clear_scr()
                        print("Amount Updated")
                        available_deno = update_money(
                            available_deno, deno)
                    else:
                        clear_scr()
                        print("Reached maximum threshold")
                    print("available Balance : {}/-".format(find_balance(available_deno)))

                if admin_choice == 2:
                    clear_scr()
                    print("available Balance : {}/-".format(find_balance(available_deno)))

                if admin_choice == 3:
                    clear_scr()
                    break

        else:
            print("Invalid adminname or password")

    if user_choice == 2:
        name, password = get_names()
        if (auth_user(stored_user_data, name, password)):
            clear_scr()
            print("Welcome user {}!".format(name))
            while True:
                while True:
                    try:
                        choice = int(input("1. Add Money\n2. Check Balance\n3. Update Pin\n4. transfer money\n5. Withdraw money\n6. Exit\n"))
                        break
                    except ValueError:
                        clear_scr()
                        print("Invalid Entry")

                if choice == 1:
                    deno = get_money()
                    clear_scr()
                    print(
                        "Previous Balance : {}/-".format(available_bal[name]))
                    available_bal[name] = available_bal[name] + \
                        return_bal(deno)
                    print(
                        "Amount to be Added : {}/-".format(return_bal(deno)))
                    print(
                        "Your current balance is : {}/-".format(available_bal[name]))

                if choice == 2:
                    clear_scr()
                    print(
                        "Your current balance is : {}/-".format(available_bal[name]))

                if choice == 3:
                    clear_scr()
                    while True:
                        try:
                            new_pin = int(input("Enter new pin: \n"))
                            break
                        except ValueError:
                            clear_scr()
                            print("Invalid pin")

                    stored_user_data = change_pin(stored_user_data, name, new_pin)
                    print("PIN successfully updated")

                if choice == 4:
                    clear_scr()
                    transfer_name, amount = get_send_details()
                    if not validate_atm_funds(amount, available_deno):
                        clear_scr()
                        print("Insufficient funds in atm. Sorry for the inconvenience")
                    else:
                        if validate_transfer(name, amount, available_bal, max_user_threshold):
                            if transfer_name in available_bal.keys():
                                print("Successfully transfered {}/- to {}".format(amount, transfer_name))
                                available_bal = transfer_funds(name, transfer_name, amount, available_bal)
                                print("New Balance : {}".format(available_bal[name]))
                            else:
                                print("No such name as {}. Make sure that you've entered it properly".format(transfer_name))

                        else:
                            clear_scr()
                            print("Insuffient Funds or maximum limit reached")
                            print("Your Balance : {}\nAmount : {} ".format(available_bal[name], amount))
                            print("Total Amount transfered : {}".format(max_user_threshold[name]))

                if choice == 5:
                    clear_scr()
                    while True:
                        try:
                            amount = int(
                                input("Enter the amount you want to withdraw : "))
                            break
                        except:
                            clear_scr()
                            print("Invalid amount")
                    if available_bal[name] < amount:
                        clear_scr()
                        print("Insufficient Funds")
                        continue
                    if not validate_atm_funds(amount, available_deno):
                        clear_scr()
                        print(
                            "Insufficient funds in atm. Sorry for the inconvenience")
                    else:
                        clear_scr()
                        available_bal[name] -= amount
                        print("Amount Withdrawn : {}/-".format(amount))
                        print("New Balance : {}/-".format(available_bal[name]))

                if choice == 6:
                    clear_scr()
                    break

                if choice > 6:
                    clear_scr()
                    print("Invalid Choice")

        else:
            clear_scr()
            print("Invalid username or password")
