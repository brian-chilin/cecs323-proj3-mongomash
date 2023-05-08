# used pycharm to install pymongo
from pymongo import MongoClient
from pprint import pprint

def connect():
    CONNECTION_STRING = "mongodb://localhost:27017"
    client = MongoClient(CONNECTION_STRING)
    return client['project3']

def troopLookup(db: MongoClient):
    troopInput = input("Input the number of a troop to retrieve a summary: ")

    if not troopInput.isnumeric():
        print("Troop number should only contain digits")
        return

    troopQuery = [
        {
            "$match": {
                "_id": int(troopInput)
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
        print("No Troop found with that number")
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
            print(2)
        elif choice == '3':
            print(3)
        elif choice == 'q':
            break;