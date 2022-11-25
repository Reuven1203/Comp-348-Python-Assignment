# connect to server

import socket
import os

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999


def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def displayMenu():
    clearTerminal()
    print("Python Menu\n\n")
    print("1. Find Customer")
    print("2. Add Customer")
    print("3. Delete Customer")
    print("4. Update Customer age")
    print("5. Update Customer address")
    print("6. Update Customer phone number")
    print("7. Print report")
    print("8. Exit")
    return promptChoice()


def promptChoice():
    try:
        choice = int(input("Enter choice: "))
        if choice < 1 or choice > 8:
            raise ValueError
        return choice
    except ValueError:
        print("Invalid choice")
        return promptChoice()


def promptName(choice=1):
    name = input("Enter customer name: ")
    if name.strip() == '':
        print("Invalid name")
        return promptName(choice)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except socket.error:
        print("Could not connect to server\nProgram will now exit")
        exit()
    req = choice, name
    client.send(str(req).encode('utf-8'))
    res = client.recv(1024).decode('utf-8')
    if res == 'False':
        print("Customer does not exist")
        return promptName(choice)
    if choice == 2 and res == '100':
        print("Customer already exists")
        return promptName(choice)
    return name


def promptAge():
    try:
        age = int(input("Enter customer age: "))
    except ValueError:
        print("Invalid age")
        return promptAge()
    if age < 1:
        print("Invalid age")
        return promptAge()
    return age


def promptAddress():
    address = input("Enter customer address: ")
    if address.strip() == '':
        print("Invalid address")
        return promptAddress()
    return address


def promptPhone():
    phone = input("Enter customer phone number: ")
    if phone.strip() == '':
        print("Invalid phone number")
        return promptPhone()
    return phone


def findCustomer():
    print("Which customer would you like to find?")
    customer = promptName()
    return 1, customer


def addCustomer():
    print("Adding customer")
    name = promptName(2)
    if name == '':
        return
    age = str(promptAge())
    address = promptAddress()
    phone = promptPhone()
    return 2, name + '|' + age + '|' + address + '|' + phone


def deleteCustomer():
    print("Which customer would you like to delete?")
    customer = promptName()
    return 3, customer


def updateCustomerAge():
    name = promptName(4)
    print("What is the new age?")
    age = promptAge()
    return 4, [name, age]


def updateCustomerAddress():
    name = promptName(5)
    address = promptAddress()
    return 5, [name, address]


def updateCustomerPhone():
    name = promptName(6)
    phone = promptPhone()
    return 6, [name, phone]


def printReport():
    print('Printing report\n\n')
    return 7, None


def processChoice(choice):
    if choice == 1:
        return findCustomer()
    elif choice == 2:
        return addCustomer()
    elif choice == 3:
        return deleteCustomer()
    elif choice == 4:
        return updateCustomerAge()
    elif choice == 5:
        return updateCustomerAddress()
    elif choice == 6:
        return updateCustomerPhone()
    elif choice == 7:
        return printReport()
    elif choice == 8:
        print("Goodbye")
        exit()


def sendRequest(choice):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except socket.error:
        print("Could not connect to server\nProgram will now exit")
        exit()
    client.send(str(choice).encode('utf-8'))
    response = client.recv(1024).decode('utf-8')
    if response != 'False':
        print("--------------\n\n" + response + "\n\n--------------")
    input('Press enter to continue')
    client.close()


def executeProgram():
    while True:
        choice = displayMenu()
        if choice == 8:
            print("Goodbye")
            break
        sendRequest(processChoice(choice))


executeProgram()
