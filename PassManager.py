import os
from cryptography.fernet import Fernet

# Generate a new key and save it to a file
key = Fernet.generate_key()
with open('key.key', 'wb') as key_file:
    key_file.write(key)

# Read the key from the file
with open('key.key', 'rb') as key_file:
    key = key_file.read()

fernet = Fernet(key)

encColon = fernet.encrypt(":".encode())

def WriteToFile(name, password):
    manager = open("passManager.txt", "a")

    encName = fernet.encrypt(name.encode())
    encPassword = fernet.encrypt(password.encode())

    manager.write(f"{encName.decode()}{encColon.decode()} {encPassword.decode()}\n")

    manager.close()

    print(f"Added password \"{name}: {password}\"")
    
    startOver = input("Would you like to start over? (yes/no): ").lower()

    if startOver == "yes":
        os.system("cls")
        main()
    elif startOver == "no":
        print("")

def GetFromFile():
    with open("passManager.txt", "r") as manager:
        lines = manager.readlines()

    print("\nHere is a list of all of your saved passwords: \n")
    for line in lines:
        encName, encPassword = line.strip().split(encColon.decode())
        decName = fernet.decrypt(encName.encode()).decode()
        decPassword = fernet.decrypt(encPassword.encode()).decode()
        print(f"{decName}: {decPassword}")

    startOver = input("Would you like to start over? (yes/no): ").lower()

    if startOver == "yes":
        os.system("cls")
        main()
    elif startOver == "no":
        print("")

def DeleteFromFile(name):
    with open("passManager.txt", "r") as manager:
        lines = manager.readlines()

    encName = fernet.encrypt(name.encode())

    found = False
    for line in lines:
        line_encName, _ = line.strip().split(encColon.decode())
        line_decName = fernet.decrypt(line_encName.encode()).decode()
        if line_decName == name:
            print(f"Is this the password you are trying to delete: \"{line_decName}\"? (yes/no)")
            confirmation = input().lower()
            if confirmation == "yes":
                lines.remove(line)
                found = True
                break
    
    if not found:
        print("Password not found.")
        return

    with open("passManager.txt", "w") as manager:
        manager.writelines(lines)
    print("Password deleted.")

    startOver = input("Would you like to start over? (yes/no): ").lower()

    if startOver == "yes":
        os.system("cls")
        main()
    elif startOver == "no":
        print("")

def main():
    try:
        manager = open("passManager.txt", "x")
    except:
        pass

    print("Would you like to add a new password or access current ones?")
    choice = input("\"Write\" for new password, \n\"Access\" to see current passwords, \nor \"Delete\" to delete a password: ")

    choice = choice.lower()

    if choice == "access":
        GetFromFile()
    elif choice == "write":
        nameOfPassword = input("What is the name of the password: ")
        password = input(f"What is the password for \"{nameOfPassword}\": ")

        WriteToFile(nameOfPassword, password)
    elif choice == "delete":
        nameOfPassword = input("What is the name of the password you want to be deleted: ")

        DeleteFromFile(nameOfPassword)
    else:
        print("That is not one of the options.")
        print("Please pick either Write, Access, or Delete")

        input("")

main()