import mysql.connector
import Import_data
import csv

class database_connection():
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database = "F1dab",
            )
        self.cursor = self.mydb.cursor()

    def insert_countries_csv(self):
        query = "INSERT INTO land (name) VALUES (%s)"

        countries = []

        with open('f1_country_info_2023.csv', 'r') as file:
            csv_data = csv.reader(file)
            for row in csv_data:
                if row[1] == 'Country_name':
                    continue
                countries.append((row[1],))

        self.cursor.executemany(query, countries)
        self.mydb.commit()

    def insert_countries_scraper(self):
        query = "INSERT INTO land (name) VALUES (%s)"

        countries = []

        data = Import_data.Import_data_class(2023)
        country_info = data.get_country_info()
        for i in range(len(country_info)):
            if country_info[i]['Country_name'] not in countries:
                countries.append(country_info[i]['Country_name'])

        data = Import_data.Import_data_class(2024)
        country_info = data.get_country_info()
        for i in range(len(country_info)):
            if country_info[i]['Country_name'] not in countries:
                countries.append(country_info[i]['Country_name'])

        country_tuple = []
        for i in range(len(countries)):
            country_tuple.append((countries[i],))

        self.cursor.executemany(query, country_tuple)
        self.mydb.commit()

    def get_countries(self):
        query = "SELECT * FROM land"
        self.cursor.execute(query)
        return self.cursor.fetchall()

db_con = database_connection()

db_con.insert_countries_scraper()
print(db_con.get_countries())