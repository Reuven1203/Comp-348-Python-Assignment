import socket
import parser
import os
PORT = 9999
FILE = "data.txt"
HOST = socket.gethostbyname(socket.gethostname())


def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def startServer():
    print("Server is starting...")
    serverStarting = True
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while serverStarting:
        try:
            server.bind((HOST, PORT))
            print("Server started")
            serverStarting = False
            return server
        except socket.error as e:
            print("Server failed to start")
            print(e)
            print("Trying again...")
            print("Please wait...")
            clearTerminal()


def executeServer():
    server = startServer()
    while True:
        server.listen(5)
        print("Server is listening")
        client, address = server.accept()
        print("Client connected")
        encodedChoice = client.recv(1024)
        choice = encodedChoice.decode('utf-8')
        if choice[1] != "7" and choice[1] != '2' and not customerExists(choice[5:-2]):
            print("Choice received: " + choice)
            print("Customer does not exist")
            client.send("False".encode('utf-8'))
            client.close()
            continue
        elif choice[1] == "2" and customerExists(choice[5:-2]):
            print("Customer already exists")
            client.send("100".encode('utf-8'))
            client.close()
            continue
        elif choice[1] != "7":
            print("Customer exists")
            client.send("True".encode('utf-8'))
            client.close()
        if choice[1] != '7':
            client, address = server.accept()
            encodedChoice = client.recv(1024)
        choice = encodedChoice.decode('utf-8')
        print("Choice received: " + choice)
        res = processChoice(choice)
        # print("Response:\n" + res)
        client.send(res.encode('utf-8'))
        client.close()
        print("Client disconnected")


def customerExists(name):
    if name in database:
        return True
    else:
        return False


def findCustomer(name):
    if name in database:
        return parser.parseItemToString(name, database[name])
    else:
        return name + " not found in database"


def addCustomer(item):
    print("Adding customer : " + item)
    item = parser.parseStringToItem(item)
    if item[0] in database:
        return item[0] + " already exists in database"
    else:
        database[item[0]] = item[1:]
        return item[0] + " added to database"


def deleteCustomer(name):
    if name in database:
        del database[name]
        return name + " deleted"
    else:
        return name + " not found in database"


def updateCustomer(choice, parsedVal):
    name = parsedVal.split(',')[0][1:-1]
    updatedValue = parsedVal.split(',')[1][1:].replace("'", "")
    print(updatedValue + " is the updated value")
    if name in database:
        database[name][int(choice) - 4] = updatedValue
        return name + " updated -> " + parser.parseItemToString(name, database[name])
    else:
        return name + " not found in database"


def printReport():
    report = "Printing report\n\n"
    for key in sorted(database, key=str.lower):
        report += parser.parseItemToString(key, database[key]) + '\n'
    return report


def processChoice(returnedVal):
    parsedVal = returnedVal[5:-2]
    if returnedVal[1] == "1":
        return findCustomer(parsedVal)
    elif returnedVal[1] == "2":
        return addCustomer(parsedVal)
    elif returnedVal[1] == "3":
        return deleteCustomer(parsedVal)
    elif returnedVal[1] == "4" or returnedVal[1] == "5" or returnedVal[1] == "6":
        return updateCustomer(returnedVal[1], parsedVal)
    elif returnedVal[1] == "7":
        return printReport()


def fetchDB(filename):
    print("Fetching database")
    try:
        return parser.readFile(filename)
    except FileNotFoundError:
        print("Database not found")
        return {}


database = parser.parseListToDict(fetchDB(FILE))
executeServer()
