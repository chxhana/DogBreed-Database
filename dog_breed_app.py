#!/usr/bin/env python3

'''A template for a simple app that interfaces with a database on the class server.
This program is complicated by the fact that the class database server is behind a firewall and we are not allowed to
connect directly to the MySQL server running on it. As a workaround, we set up an ssh tunnel (this is the purpose
of the DatabaseTunnel class) and then connect through that. In a more normal database application setting (in
particular if you are writing a database app that connects to a server running on the same computer) you would not
have to bother with the tunnel and could just connect directly.'''
'''import MySQLdb'''
import mysql.connector
import os.path
from db_tunnel import DatabaseTunnel
import math

# Default connection information (can be overridden with command-line arguments)
# Change these as needed for your app. (You should create a token for your database and use its username
# and password here.)
DB_NAME = "ndh1226_dog_breed"
DB_USER = "token_1c36"
DB_PASSWORD = "wQvvg1STFxOsZ8b6"

# SQL queries/statements that will be used in this program (replace these with the queries/statements needed
# by your program)

# Use "%s" as a placeholder for where you will need to insert values (e.g., user input)
ADD_NEW_BREED = """
    INSERT INTO Breed (name, size, cost, energyLevel, coatType, originCountry) VALUES (%s, %s, %s, %s, %s, %s)
"""

ADD_NEW_COUNTRY = """
    INSERT INTO Country (name, continent) VALUES (%s, %s)
"""

ADD_NEW_COAT_TYPE = """
    INSERT INTO CoatType (text, hairYield) VALUES
    (%s, %s)
"""

ADD_HEALTH_CONCERN = """
    INSERT INTO HealthConcern (text) VALUES (%s)
"""

ADD_BREED_HEALTH_CONCERN = """
    INSERT INTO HasHealthConcern (breedId, healthConcernId) VALUES (%s, %s)
"""

GET_ALL_BREEDS = """
    SELECT name
    FROM Breed
"""

GET_INFO_FOR_BREED_BY_NAME = """
    SELECT name, size, cost, energyLevel, coatType, originCountry
    FROM Breed
    WHERE name LIKE %s
"""

GET_BREED_ID_BY_NAME = """
    SELECT id FROM Breed WHERE name LIKE %s
"""

GET_ALL_HEALTH_CONCERNS = """
    SELECT id, text FROM HealthConcern
"""

GET_HEALTH_CONCERN_ID_BY_NAME = """
    SELECT id FROM HealthConcern WHERE text like %s
"""

GET_COAT_TYPES = """
    SELECT id as identifier, text as type, hairYield as "hair-yield" 
    FROM CoatType
"""

GET_COAT_ID = """
    SELECT id
    FROM CoatType
    WHERE text LIKE %s
"""

GET_COAT = """
    SELECT *
    FROM CoatType
    WHERE id = %s
"""

GET_BREED_HEALTH_CONCERNS = """
    SELECT text as 'health-concern'
    FROM HealthConcern
        INNER JOIN HasHealthConcern ON HealthConcern.id = HasHealthConcern.healthConcernId
        INNER JOIN Breed ON Breed.id = HasHealthConcern.breedId
    WHERE Breed.name LIKE %s
"""

GET_CONTINENT_OF_COUNTRY = """
    SELECT Continent
    FROM Country
    WHERE country LIKE %s
"""

GET_AVAILABLE_COUNTRIES = """
    SELECT name, continent
    FROM Country
"""

GET_COUNTRY_ID = """
    SELECT id
    FROM Country
    WHERE name LIKE %s
"""

GET_COUNTRY_INFO = """
    SELECT *
    FROM Country
    WHERE id = %s
"""

GET_TOTAL_BREEDS = """
    SELECT COUNT(*)
    FROM Breed
"""

DROP_BREED_BY_NAME = """
    DELETE FROM Breed
    WHERE name LIKE %s
"""

DROP_HEALTH_CONCERN = """
    DELETE FROM HealthConcern
    WHERE id = %s
"""

DROP_HEALTH_CONCERN_FOR_BREED = """
    DELETE FROM HasHealthConcern
    WHERE breedId = %s AND healthConcernId = %s
"""

DROP_COAT_TYPE = """
    DELETE FROM CoatType
    WHERE id = %s
"""

DROP_COUNTRY_BY_ID = """
    DELETE FROM Country
    WHERE id = %s
"""

GET_AVERAGE_PRICE_BY_COAT = """
    SELECT text, AVG(cost)
    FROM Breed INNER JOIN CoatType ON Breed.coatType = CoatType.id
    GROUP BY text
"""

GET_BREEDS_MORE_EXPENSIVE_THAN_AVERAGE = """
    SELECT name, cost
    FROM Breed
    WHERE cost > (SELECT AVG(cost) FROM Breed)
"""

UPDATE_COAT_TYPE_FOR_BREED = """
    UPDATE Breed
    SET coatType = %s
    WHERE id = %s
"""

UPDATE_ORIGIN_COUNTRY_FOR_BREED = """
    UPDATE Breed
    SET originCountry = %s
    WHERE id = %s
"""


# If you change the name of this class (and you should) you also need to change it in main() near the bottom
class DatabaseApp:
    '''A simple Python application that interfaces with a database.'''

    def __init__(self, dbHost, dbPort, dbName, dbUser, dbPassword):
        self.dbHost, self.dbPort = dbHost, dbPort
        self.dbName = dbName
        self.dbUser, self.dbPassword = dbUser, dbPassword

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.close()

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.dbHost, port=self.dbPort, database=self.dbName,
            user=self.dbUser, password=self.dbPassword,
            use_pure=True,
            autocommit=True,
        )
        self.cursor = self.connection.cursor(buffered=True)

    def close(self):
        self.connection.close()

    def runApp(self):
        print(f"Welcome to the Dog Breed Database!")

        while True:
            print("\nHere are all the available breeds:")
            breeds = self.get_all_breeds()
            if not breeds:
                print("\t(No breeds registered)")
            else:
                for breed in breeds:
                    print(f"\t{breed}")
            print(f"{self.get_total_breeds()} breeds total\n")

            print("What would you like to do?")
            print("\tS) Research/edit a breed\n\tA) Add a new breed\n\tD) Drop a breed\n\tC) See average price of "
                  "a breed by each coat type\n\tG) See which breeds are more expensive than average\n\tQ) Quit")
            user_input = input("Your answer: ").lower().strip()
            if user_input == 'q':
                break

            elif user_input == 's':
                self.select_breed_process(breeds)

            elif user_input == 'a':
                self.create_breed_process(breeds)

            elif user_input == 'd':
                self.drop_breed_process(breeds)

            elif user_input == 'c':
                self.print_average_price_by_coat()

            elif user_input == 'g':
                self.print_breeds_more_expensive()

            else:
                print("Not a valid input")

    def select_breed_process(self, breeds):
        while True:
            breed_name = input("Enter the name of the breed you want to select: ").title().strip()

            if not breeds:
                print("You don't have any breeds to search for")
                return

            if breed_name not in breeds:
                print("This breed isn't in the database")
                continue
            break

        breed_info = self.search_for_breed_by_name(breed_name)
        self.print_readable_breed_info(breed_info)
        while True:

            print("\nWhat would you like to do now?")
            print("H) View/Edit this breed's health concerns")
            print("C) Change this breed's coat type")
            print("O) Change this breed's origin country")
            print("V) Re-display this breed's information")
            print("Q) Go back to the main page")
            answer = input("Your answer: ").lower().strip()

            if answer == 'q':
                return

            elif answer == 'v':
                breed_info = self.search_for_breed_by_name(breed_name)  # In case the info was updated
                self.print_readable_breed_info(breed_info)

            elif answer == 'h':
                self.health_concern_process(breed_name)

            elif answer == 'c':
                current_coat = self.get_coat_info(breed_info[4])[1]
                self.change_coat_process(breed_name, current_coat)

            elif answer == 'o':
                if breed_info[5]:
                    current_origin_country = self.get_country_info(breed_info[5])[1]
                else:
                    current_origin_country = None
                self.change_origin_country_process(breed_name, current_origin_country)

            else:
                print("Type a correct answer")
                continue

    def change_origin_country_process(self, breed_name, current_origin_country):
        while True:
            all_countries_and_continents = self.get_available_countries()
            print(f"\nCurrent origin country: {current_origin_country}")
            print("Type the name of the country, if it isn't in the database, you will be able to add it")
            print("Type 'V' to view all countries")
            print("Type 'D' to delete countries")
            print("Type 'Q' to go back")
            answer = input("Your answer: ").title().strip()

            if not answer:
                print("Type a correct answer")
                continue

            if answer == current_origin_country:
                print("This is already the origin country for this breed")
                continue

            if answer == 'Q':
                return

            if answer == 'D':
                self.delete_country_process()
                continue

            if answer == 'V':
                print()
                for country_continent in all_countries_and_continents:
                    print(f"\t{country_continent[0]}, {country_continent[1]}")
                continue

            countries = [location[0] for location in all_countries_and_continents]
            if answer in countries:
                country_id = self.get_country_id(answer)
                breed_id = self.get_breed_id(breed_name)
                self.update_country(breed_id, country_id)
                print(f"Origin country updated to {answer}")
                return

            return_code = self.add_country_process(answer)

            if return_code == -1:
                continue

            yes_no = input(
                "Do you want to do this process again? If not the country that you added will be used. y/n: ").lower().strip()

            if yes_no == 'y':
                country_id = self.get_country_id(answer)
                breed_id = self.get_breed_id(breed_name)
                self.update_country(breed_id, country_id)

    def add_country_process(self, country_name):
        while True:
            print("Country is not in database, you can add it here")
            continent = input("Type the name of the continent this country is in, or 'Q' to go back: ").title()

            if continent == 'Q':
                return -1

            if not continent:
                print("Type a valid answer")
                continue
            self.add_new_country(country_name, continent)
            return

    def delete_country_process(self):
        while True:
            country_to_delete = input("Country to delete (type 'Q' to go back): ").title()

            if country_to_delete == 'Q':
                return

            if country_to_delete not in [location[0] for location in self.get_available_countries()]:
                print("That country isn't in the database")
                continue

            country_to_delete_id = int(self.get_country_id(country_to_delete))
            self.drop_country(country_to_delete_id)
            yes_no = input("Country deleted. Would you like to do this again? y/n: ").lower()
            if yes_no != 'y':
                break

    def change_coat_process(self, breed_name, current_coat):
        while True:
            all_coat_type_names = self.get_coat_type_names()
            print(f"\nCurrent coat: {current_coat}")
            print("Type the name of the coat, if it isn't in the database, you will be able to add it")
            print("Type 'V' to view all coats")
            print("Type 'D' to delete coats")
            print("Type 'Q' to go back")
            answer = input("Your answer: ").title()

            if not answer:
                print("Type a correct answer")
                continue

            if answer == current_coat:
                print("Coat is already used by this breed")
                continue

            if answer == 'Q':
                return

            if answer == 'D':
                self.delete_coat_process()
                continue

            if answer == 'V':
                available_coat_types = self.get_coat_types()
                print()
                for available_coat in available_coat_types:
                    print(f"\tType: {available_coat[1]}, {available_coat[2]} hair yield")
                continue

            if answer not in all_coat_type_names:
                self.add_coat(answer)
                continue

            breed_id = self.get_breed_id(breed_name)
            coat_id = self.get_coat_id(answer)
            self.update_coat(breed_id, coat_id)

    def health_concern_process(self, breed_name):
        while True:
            print("\nV) View health concerns for this breed")
            print("A) Add health concerns for this breed")
            print("D) Delete health concerns for this breed")
            print("Q) Go back")
            answer = input("Your answer: ").lower()

            if answer == 'q':
                break

            if answer == 'v':
                breed_health_concerns = self.get_breed_health_concerns(breed_name)

                if not breed_health_concerns:
                    print(f"No health concerns entered for {breed_name}s")
                    continue

                for health_concern in breed_health_concerns:
                    print(health_concern)

            elif answer == 'a':
                self.add_health_concern_process(breed_name)

            elif answer == 'd':
                self.delete_health_concern_for_breed_process(breed_name)

            else:
                print("Type a valid answer")

    def delete_health_concern_for_breed_process(self, breed_name):
        while True:
            print("\nType the name of the health concern you'd like to delete ")
            print("Type 'V' to view all health concern for this breed")
            print("Type 'Q' to go back")
            answer = input("Your answer: ").title()

            if answer == 'Q':
                return

            breed_health_concerns = self.get_breed_health_concerns(breed_name)

            if answer == 'V':
                if not breed_health_concerns:
                    print(f"No health concerns entered for {breed_name}s")
                    continue

                for health_concern in breed_health_concerns:
                    print(health_concern)
                continue

            if answer not in breed_health_concerns:
                print(f"This isn't a health concern for {breed_name}")
                continue

            self.drop_breed_health_concern(self.get_breed_id(breed_name), self.get_health_concern_id(answer))
            print(f"{answer} was removed")
            yes_no = input("Would you like to drop another health concern? y/n: ").lower()
            if yes_no == 'n':
                return

    def add_health_concern_process(self, breed_name):
        while True:
            all_health_concerns = self.get_all_health_concerns()
            print("\nHere are the available health concerns in the database:")
            if all_health_concerns:
                for concern in all_health_concerns:
                    print(concern)
            else:
                print("(There are no health concerns in the database)")

            print(f"\nType in the name of the health concern you'd like to attribute to {breed_name}s")
            print("If the concern isn't in the database, you will be able to add it once you've enter it")
            print("You can also type 'delete' to delete a health concern or 'Q' to go back")

            answer = input("Your answer: ").title()

            if answer == 'Q':
                return

            if answer == "Delete":
                self.delete_health_concern_process(all_health_concerns)
                return

            self.add_health_concern_to_breed_helper(breed_name, answer)
            yes_no = input("Would you like to add more health concerns? y/n: ").lower()
            if yes_no == 'n':
                return

    def add_health_concern_to_breed_helper(self, breed_name, concern_name):
        breed_health_concerns = self.get_breed_health_concerns(breed_name)
        if concern_name in breed_health_concerns:
            print(f"This is already listed as a health concern for {breed_name}s")
            return

        health_concerns = self.get_all_health_concerns()
        if concern_name not in health_concerns:
            yes_no = input("This health concern isn't in the database, do you want to add it? y/n: ").lower().strip()
            if yes_no == 'y':
                self.add_health_concern(concern_name)
                self.add_health_concern_for_breed(self.get_breed_id(breed_name),
                                                  self.get_health_concern_id(concern_name))
                print(f"Health concern added to the database and {breed_name}s")
        else:
            self.add_health_concern_for_breed(self.get_breed_id(breed_name), self.get_health_concern_id(concern_name))

    def delete_health_concern_process(self, all_health_concerns):
        while True:
            health_concern_to_delete = input("Type the name of the health concern you want to "
                                             "delete or type 'Q' to go back: ").title()
            if health_concern_to_delete == "Q":
                break

            if health_concern_to_delete not in all_health_concerns:
                print("This health concern isn't in the database")
                continue

            concern_id = self.get_health_concern_id(health_concern_to_delete)
            self.drop_health_concern(concern_id)
            print(f"{health_concern_to_delete} was deleted from the database")

            answer = input("Are there any other concerns you'd like to delete? y/n: ").lower()
            if answer == 'n':
                return

    def create_breed_process(self, breeds):
        while True:
            try:
                name = input("Enter the name of the breed or type Q to cancel: ").title().strip()

                if name == "Q":
                    return

                if not name:
                    print("No value entered")
                    continue

                if name in breeds:
                    print("Breed is already in the database")
                    continue

                print("Enter size of breed using the following sizes:\n1) Small\n2) Medium\n3) Large\n4) Very Large")
                size = int(input("Your answer: "))
                cost = int(input("Average/estimated cost of the breed: "))
                energy_level = int(input("Energy level of the breed on a scale from 1-10: "))

                if cost not in range(0, 1000000) or size not in range(1, 5) or energy_level not in range(1, 11):
                    print("One or more of the fields weren't correct values")
                    continue

            except ValueError:
                print("One or more of the fields weren't correct values")
                continue

            break

        coat_id = self.get_coat_id_process()
        if coat_id == -1:
            return

        country_id = self.get_country_id_process()
        if country_id == -1:
            return

        self.add_new_breed(name, size, cost, energy_level, coat_id, country_id)
        print(f"\n{name} successfully added to the database!")

        yes_no = input(
            f"Would you like to add any health concerns for {name}s? You can add them later as well. y/n: ").lower()

        if yes_no == 'y':
            self.add_health_concern_process(name)

    def print_readable_breed_info(self, breed_info):
        sizes = {1: "Small", 2: "Medium", 3: "Large", 4: "Very large"}
        print(f"\nSize: {sizes[breed_info[1]]}")
        print(f"Estimated Price: ${breed_info[2]}")
        print(f"Energy Level: {breed_info[3]}/10")
        coat_info = self.get_coat_info(breed_info[4])
        print(f"Coat Type: {coat_info[1]}, {coat_info[2]} hair yield")
        if breed_info[5]:
            origin_country_info = self.get_country_info(breed_info[5])
            print(f"Origin Country: {origin_country_info[1]}, {origin_country_info[2]}")
        else:
            print("Origin Country: Undetermined")

    def get_coat_id_process(self):
        while True:
            available_coat_types = self.get_coat_types()
            print("These are the available coat types:\n")
            for available_coat in available_coat_types:
                print(f"\tType: {available_coat[1]}, {available_coat[2]} hair yield")

            print("\nEnter the breed's coat type (everything before the comma), if it isn't listed you can add it")
            print("Type 'D' to delete a coat type")
            print("Type 'Q' to return to the main menu")
            answer = input("Your answer: ").title().strip()

            if not answer:
                print("Type in a correct answer")
                continue

            if answer == 'Q':
                return -1

            all_coat_type_names = self.get_coat_type_names()

            if answer == 'D':
                self.delete_coat_process()
                continue

            if answer not in all_coat_type_names:
                if self.add_coat(answer) == -1:
                    continue
                yes_no = input(
                    "Would you like to do this process again? If not the coat that was made will be used. y/n: ").lower().strip()
                if yes_no == 'y':
                    continue

            return self.get_coat_id(answer)

    def add_coat(self, coat_name):
        print("This coat type isn't in the database, you'll be able to add it here")
        while True:
            hair_yield = input("Enter the hair yield of this coat type, or type 'Q' to go back: ").title().strip()

            if hair_yield == 'Q':
                return -1

            if not hair_yield:
                print("Type a correct value")
                continue
            break
        self.add_coat_type(coat_name, hair_yield)
        print("Coat added to the database")

    def delete_coat_process(self):
        all_coat_type_names = self.get_coat_type_names()
        while True:
            coat_to_delete = input("Enter the coat type to be deleted, or type 'Q' to go back: ").title().strip()

            if coat_to_delete == 'Q':
                return -1

            if coat_to_delete not in all_coat_type_names:
                print("Not a valid coat")
                continue
            try:
                self.drop_coat_type(self.get_coat_id(coat_to_delete))
            except Exception as e:
                print("This coat is used by other breeds, you'll need to change their coats to perform this action")
                continue
            print("Coat was deleted")
            break

    def get_country_id_process(self):
        while True:
            countries_continents = self.get_available_countries()
            country_name = input("\nType the name of the breed's origin country\ntype 'V' to see a list "
                                 "of countries in the database\ntype 'D' to remove a country from "
                                 "the database\ntype 'None' if you want to skip this step\n"
                                 "if the country isn't available it will be added\n"
                                 "Type 'Q' if you want to return to the main menu\n"
                                 "Your answer: ").title().strip()

            if not country_name:
                continue

            if country_name == 'Q':
                return -1

            if country_name == 'V':
                for country in countries_continents:
                    print(f"{country[0]}, {country[1]}")
                continue

            if country_name == 'D':
                self.delete_country_process()
                continue

            if country_name == 'None':
                return None

            if country_name in [location[0] for location in countries_continents]:
                return self.get_country_id(country_name)

            return_code = self.add_country_process(country_name)

            if return_code == -1:
                # They changed their mind
                continue

            yes_no = input(
                "Do you want to do this process again? If not the country that you added will be used. y/n: ").lower()

            if yes_no == 'n':
                return self.get_country_id(country_name)

    def drop_breed_process(self, breeds):
        name = input("Enter a the name of the breed you want to remove or type q to cancel: ").title().strip()

        if name == 'Q':
            return

        if name not in breeds:
            print(f"{name} wasn't in the database")
        else:
            self.drop_breed(name)
            print(f"{name} was removed from the database.")

    def search_for_breed_by_name(self, breed_name):
        self.cursor.execute(GET_INFO_FOR_BREED_BY_NAME, ("%" + breed_name + "%",))

        breed_info = []
        for info in self.cursor:
            breed_info.append(info)
        return breed_info[0]

    def print_average_price_by_coat(self):
        self.cursor.execute(GET_AVERAGE_PRICE_BY_COAT)

        print("")
        for row in self.cursor:
            print(f"\t{row[0]}: ${round(row[1], 2)}")

    def print_breeds_more_expensive(self):
        self.cursor.execute(GET_BREEDS_MORE_EXPENSIVE_THAN_AVERAGE)

        print("")
        for row in self.cursor:
            print(f"{row[0]}: ${round(row[1], 2)}")

    def add_new_breed(self, breed_name, size, cost, energy_level, coat_type, origin_country):
        self.cursor.execute(ADD_NEW_BREED, (breed_name, size, cost, energy_level, coat_type, origin_country,))

    def add_new_country(self, country_name, continent_name):
        self.cursor.execute(ADD_NEW_COUNTRY, (country_name, continent_name,))

    def add_coat_type(self, coat_type, hair_yield):
        self.cursor.execute(ADD_NEW_COAT_TYPE, (coat_type, hair_yield,))

    def add_health_concern(self, text):
        self.cursor.execute(ADD_HEALTH_CONCERN, (text,))

    def add_health_concern_for_breed(self, breed_id, health_concern_id):
        self.cursor.execute(ADD_BREED_HEALTH_CONCERN, (breed_id, health_concern_id,))

        health_concerns = []
        for concern in self.cursor:
            health_concerns.append(concern[1])
        return health_concerns

    def get_breed_id(self, breed_name):
        self.cursor.execute(GET_BREED_ID_BY_NAME, ("%" + breed_name + "%",))
        return self.cursor.next()[0]

    def get_all_health_concerns(self):
        self.cursor.execute(GET_ALL_HEALTH_CONCERNS)

        health_concerns = []
        for concern in self.cursor:
            health_concerns.append(concern[1])
        return health_concerns

    def get_health_concern_id(self, health_concern_name):
        self.cursor.execute(GET_HEALTH_CONCERN_ID_BY_NAME, ("%" + health_concern_name + "%",))
        return self.cursor.next()[0]

    def get_coat_types(self):
        self.cursor.execute(GET_COAT_TYPES)

        coats = []
        for coat in self.cursor:
            coats.append(coat)
        return coats

    def get_coat_type_names(self):
        self.cursor.execute(GET_COAT_TYPES)

        coats = []
        for coat in self.cursor:
            coats.append(coat[1])
        return coats

    def get_coat_info(self, coat_id):
        self.cursor.execute(GET_COAT, (coat_id,))

        return self.cursor.next()

    def get_coat_id(self, coat_type):
        self.cursor.execute(GET_COAT_ID, ("%" + coat_type + "%",))

        return self.cursor.next()[0]

    def get_all_breeds(self):
        self.cursor.execute(GET_ALL_BREEDS)

        breeds = []
        for breed in self.cursor:
            breeds.append(breed[0])
        return breeds

    def get_breed_health_concerns(self, breed_name):
        self.cursor.execute(GET_BREED_HEALTH_CONCERNS, ("%" + breed_name + "%",))

        health_concerns = []
        for concern in self.cursor:
            health_concerns.append(concern[0])
        return health_concerns

    def get_available_countries(self):
        self.cursor.execute(GET_AVAILABLE_COUNTRIES)

        countries = []
        for country in self.cursor:
            countries.append(country)
        return countries

    def get_continent(self, country):
        self.cursor.execute(GET_CONTINENT_OF_COUNTRY, (country,))

        return self.cursor.next()[0]

    def get_country_id(self, name):
        self.cursor.execute(GET_COUNTRY_ID, (name,))

        return self.cursor.next()[0]

    def get_country_info(self, country_id):
        self.cursor.execute(GET_COUNTRY_INFO, (country_id,))

        return self.cursor.next()

    def get_total_breeds(self):
        self.cursor.execute(GET_TOTAL_BREEDS)

        return self.cursor.next()[0]

    def drop_breed(self, breed_name):
        self.cursor.execute(DROP_BREED_BY_NAME, ("%" + breed_name + "%",))

    def drop_country(self, country_id):
        self.cursor.execute(DROP_COUNTRY_BY_ID, (country_id,))

    def drop_coat_type(self, coat_id):
        self.cursor.execute(DROP_COAT_TYPE, (coat_id,))

    def drop_health_concern(self, health_concern_id):
        self.cursor.execute(DROP_HEALTH_CONCERN, (health_concern_id,))

    def drop_breed_health_concern(self, breed_id, health_concern_id):
        self.cursor.execute(DROP_HEALTH_CONCERN_FOR_BREED, (breed_id, health_concern_id,))

    def update_coat(self, breed_id, coat_id):
        self.cursor.execute(UPDATE_COAT_TYPE_FOR_BREED, (coat_id, breed_id,))

    def update_country(self, breed_id, country_id):
        self.cursor.execute(UPDATE_ORIGIN_COUNTRY_FOR_BREED, (country_id, breed_id,))


def main():
    import sys
    '''Entry point of the application. Uses command-line parameters to override database connection settings, then invokes runApp().'''
    # Default connection parameters (can be overridden on command line)
    params = {
        'dbname': DB_NAME,
        'user': DB_USER,
        'password': DB_PASSWORD
    }

    needToPrintHelp = False

    # Parse command-line arguments, overriding values in params
    i = 1
    while i < len(sys.argv) and not needToPrintHelp:
        arg = sys.argv[i]
        isLast = (i + 1 == len(sys.argv))

        if arg in ("-h", "-help"):
            needToPrintHelp = True
            break

        elif arg in ("-dbname", "-user", "-password"):
            if isLast:
                needToPrintHelp = True
            else:
                params[arg[1:]] = sys.argv[i + 1]
                i += 1

        else:
            print("Unrecognized option: " + arg, file=sys.stderr)
            needToPrintHelp = True

        i += 1

    # If help was requested, print it and exit
    if needToPrintHelp:
        printHelp()
        return

    try:
        with \
                DatabaseTunnel() as tunnel, \
                DatabaseApp(
                    dbHost='localhost', dbPort=tunnel.getForwardedPort(),
                    dbName=params['dbname'],
                    dbUser=params['user'], dbPassword=params['password']
                ) as app:

            try:
                app.runApp()
            except mysql.connector.Error as err:
                print("\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", file=sys.stderr)
                print("SQL error when running database app!\n", file=sys.stderr)
                print(err, file=sys.stderr)
                print("\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", file=sys.stderr)

    except mysql.connector.Error as err:
        print("Error communicating with the database (see full message below).", file=sys.stderr)
        print(err, file=sys.stderr)
        print("\nParameters used to connect to the database:", file=sys.stderr)
        print(f"\tDatabase name: {params['dbname']}\n\tUser: {params['user']}\n\tPassword: {params['password']}",
              file=sys.stderr)
        print("""
(Did you install mysql-connector-python and sshtunnel with pip3/pip?)
(Are the username and password correct?)""", file=sys.stderr)


def printHelp():
    print(f'''
Accepted command-line arguments:
    -help, -h          display this help text
    -dbname <text>     override name of database to connect to
                       (default: {DB_NAME})
    -user <text>       override database user
                       (default: {DB_USER})
    -password <text>   override database password
    ''')


if __name__ == "__main__":
    main()
