import csv
import sqlite3

# ------------Data List----------------------------------

obj_list = []

# -----------Data List trimmed----------------------------
finallist = []

connection = sqlite3.connect('WorldCities.db')
c = connection.cursor()


# ----------CSV Input-------------
def fileIO():
    try:
        with open('worldcities.csv', encoding="utf8") as iniFile:
            scanner = csv.reader(iniFile)
            counter = 0
            for row in scanner:

                if counter == 0:
                    counter += 1
                    continue
                else:

                    counter += 1
                    obj_list.append(row)

        iniFile.close()
    # Checking if mentioned file exist or not
    except IOError:
        print('File not Found')
        print('Please make sure file is in the location')
        exit()


# ------------Table creation-------------------------------
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS worldcities(city TEXT, country TEXT)')


# --------------Data entry---------------------------------
def data_entry(city, country):
    c.execute("INSERT INTO worldcities(city, country) VALUES(?, ?)",
              (city, country))


# --------------Data fetch from the database----------------
def fetch(final_str):
    c.execute(final_str)
    record_objects = c.fetchall()
    return record_objects


# ------------Display function------------------------------
def display_with_filter():
    req = input("Enter column/columns you wanna filter (city, country): ").split(' ')
    ini_string = "SELECT * FROM worldcities WHERE "

    for x in req:
        if x == "city" or x == "country":
            inp = input("Enter value for " + x + " : ")
            str_formation = x + " == " + "'" + inp + "'" + " AND "
            ini_string = ini_string + str_formation
            final_str = ini_string[:len(ini_string) - 5]
            record_objects = fetch(final_str)
            if len(record_objects) == 0:
                print("No record with such value exists")
            else:
                for row in record_objects:
                    print(row[0])
                    finallist.append(row[0])
                for r in sorted(finallist):
                    print(r)
                finallist.clear()
        else:
            finallist.clear()
            print("\nchoose from the option please given ....\n")


# -------------------To save changes in database-------------
def change_save():
    connection.commit()


# -------------------To disconnect the database-------------
def disconnect():
    c.close()
    connection.close()


# If required tha use this function to create table in database.
def databaseTable_Creation():
    fileIO()
    create_table()

    for row in obj_list:
        data_entry(row[0], row[1])
    change_save()
    disconnect()


# --------------------------Main Logic----------------------


choice = "y"
while choice == "y":
    display_with_filter()
    choice = input("\n\nIf want to continue press y and enter: ")

disconnect()


