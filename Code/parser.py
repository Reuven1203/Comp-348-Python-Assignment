def readFile(filename):
    with open(filename, "r") as file:
        db = file.readlines()
    return tokenizeFile(db)


def tokenizeFile(db):
    databaseList = []
    for line in db:
        item = line.split('|')
        finalItem = item[len(item) - 1]
        lastChar = finalItem[-1:]
        if lastChar == '\n':
            item[len(item) - 1] = finalItem[:-1]
        databaseList.append(item)
    return databaseList


def parseListToDict(db):
    databaseDict = {}
    for item in db:
        key = item[0].strip()
        value = [item[1].strip(), item[2].strip(), item[3].strip()]
        databaseDict[key] = value
    return databaseDict


def parseItemToString(name, item):
    return name.strip() + "|" + item[0] + "|" + item[1] + "|" + item[2]


def parseStringToItem(item):
    item = item.split('|')
    finalItem = item[len(item) - 1]
    lastChar = finalItem[-1:]
    if lastChar == '\n':
        item[len(item) - 1] = finalItem[:-1]
    return item
