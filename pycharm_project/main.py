# used pycharm to install pymongo
from pymongo import MongoClient
from pprint import pprint

def connect():
    CONNECTION_STRING = "mongodb://localhost:27017"
    client = MongoClient(CONNECTION_STRING)
    return client['project3']

def troopLookup(db: MongoClient):
    troopInput = input("Input Troop's number to retrieve a summary of: ")

    if not troopInput.isnumeric():
        print("Troop number should only contain digits")
        return
    troopInput = int(troopInput)

    troopQuery = [
        {
            "$match": {
                "_id": troopInput
            }
        },
        {
            "$project": {
                "_id": 1,
                "founding_date": 1,
                "community": 1,
                "scouts": 1,
                "volunteers": 1
            }
        }
    ]
    result = list(db["troops"].aggregate(troopQuery))
    if not result:
        print("Troop #" + str(troopInput) + " not found")
        return
    result = result[0]
    print(result)
    print("Overview for Troop #" + str(result['_id']) + ":")
    print("Founded: " + str(result['founding_date'].date()))
    print("Community: " + result['community'])
    print("Scouts: ", end='')
    for i, scout in enumerate(result['scouts']):
        if i != 0:
            print(', ', end='')
        print(scout['firstname'] + ' ' + scout['lastname'], end='')
    print()
    print("Volunteers: ", end='')
    for i, volunteer in enumerate(result['volunteers']):
        if i != 0:
            print(', ', end='')
        print(volunteer['firstname'] + ' ' + volunteer['lastname'], end='')
    print() # since for loop ended without a newline

def scoutLookup(db: MongoClient):
    # firstname & lastname
    fnInput = input("First name (caps matter): ")
    lnInput = input("Last name  (caps matter): ")

    scoutQuery = [
        {
            '$unwind': {
                'path': '$scouts',
                'includeArrayIndex': 'string',
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$match': {
                'scouts.firstname': fnInput,
                'scouts.lastname': lnInput
            }
        }, {
            '$project': {
                'founding_date': 0,
                'community': 0,
                'volunteers': 0
            }
        }
    ]

    result = list(db["troops"].aggregate(scoutQuery))
    if not result:
        print(fnInput + " " + lnInput + " not found")
        return
    result = result[0]['scouts']
    print(result)

    print("Detailed view for " + result['firstname'] + ' ' + result['lastname'] + ':')
    print("Birthday: " + str(result['birthday'].date()))
    print("Grade level: " + result['gradelevel'])

    print("Adults: ")
    for adult in result['adults']:
        print("  -" + adult['firstname'] + ' ' + adult['lastname'])
    if not result['adults']:
        print(" (no adults found)")

    print("Allotments: ")
    for allotment in result['allotments']:
        print("  -" + str(allotment['deliverydate'].date()))
        for cookies in allotment['cookies']:
            print("     •" + str(cookies['boxes']) + " boxes of " + cookies['cookietype'])
    if not result['allotments']:
        print(" (no allotments found)")

def salesReport(db: MongoClient):
    troopInput = input("Input the number of a troop to retrieve a sales report: ")

    if not troopInput.isnumeric():
        print("Troop number should only contain digits")
        return
    troopInput = int(troopInput)

    srQuery = [
        {
            '$match': {
                '_id': troopInput
            }
        }, {
            '$unwind': {
                'path': '$scouts',
                'includeArrayIndex': 'string',
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$unwind': {
                'path': '$scouts.allotments',
                'includeArrayIndex': 'string',
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$unwind': {
                'path': '$scouts.allotments.cookies',
                'includeArrayIndex': 'string',
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$lookup': {
                'from': 'cookietypes',
                'localField': 'scouts.allotments.cookies.cookieid',
                'foreignField': '_id',
                'as': 'cookie'
            }
        }, {
            '$unwind': {
                'path': '$cookie',
                'includeArrayIndex': 'string',
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$project': {
                'scouts': 1,
                'cookie': 1,
                'totalvalue': {
                    '$multiply': [
                        '$scouts.allotments.cookies.boxes', '$cookie.price'
                    ]
                }
            }
        }, {
            '$group': {
                '_id': '$scouts._id',
                'firstname': {
                    '$min': '$scouts.firstname'
                },
                'lastname': {
                    '$min': '$scouts.lastname'
                },
                'totalvalue': {
                    '$sum': '$totalvalue'
                }
            }
        }, {
            '$project': {
                'firstname': 1,
                'lastname': 1,
                'totalvalue': 1
            }
        }
    ]

    result = list(db["troops"].aggregate(srQuery))
    for scout in result:
        print(scout['firstname'] + ' ' + scout['lastname'] + '\n   Total Value: ' + str(scout['totalvalue']))
    if not result:
        print("(no scouts to show)")


if __name__ == "__main__":

    db = connect()

    """ example:
    cookieTypes = [
        {
            "$project": {
                "_id": 1,
                "name": 1,
                "price": 1,
                "ingredients": 1
            }
        }
    ]
    results = db["cookietypes"].aggregate(cookieTypes)
    pprint(list(results))
    """

    while True:
        # main menu loop. menu ->
        choice = input("1) Troop Lookup\n2) Scout Lookup\n3) Sales Report\nQ) quit\nEnter 1, 2, 3, or q: ").lower()
        if choice == '1':
            troopLookup(db)
            print()
        elif choice == '2':
            scoutLookup(db)
            print()
        elif choice == '3':
            salesReport(db)
            print()
        elif choice == 'q':
            break;