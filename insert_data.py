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

    def insert_countries(self):
        query = "INSERT INTO land (name) VALUES (%s)"

        countries = []

        with open('f1_country_info_2023.csv', newline='', encoding='utf-8') as file:
            csv_data = csv.reader(file)
            for row in csv_data:
                if row[1] == 'Country_name':
                    continue
                countries.append((row[1],))

        self.cursor.executemany(query, countries)
        self.mydb.commit()

    def insert_GPs(self):
        query = "INSERT INTO GP (land_id, gp_number, circuit_name, location, date, length) VALUES (%s, %s, %s, %s, %s, %s)"

        GPs = []
        GPs_ids = []

        with open('f1_GP_info_2023.csv', newline='', encoding='utf-8') as file:
            csv_data = csv.reader(file)
            for row in csv_data:
                if row[0] == 'GP_id':
                    continue
                GPs.append((row[1], row[2], row[3], row[4], row[5], row[6]))

        # print all GPs on new lines
        #for GP in GPs:
        #    print(GP)

        country_ids = self.get_country_ids()

        # replace all country names with country ids in GPs
        for GP in GPs:
            for country in country_ids:
                if GP[0] == country[1]:
                    GP = (country[0],) + GP[1:]
                    GPs_ids.append(GP)
                    break
        
        # print all GPs on new lines
        #for GP in GPs_ids:
        #    print(GP)


        self.cursor.executemany(query, GPs)
        self.mydb.commit()


    def insert_countries_scraper(self):
        # deprecated
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
        #self.mydb.commit()

    def get_countries(self):
        query = "SELECT * FROM land"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_country_ids(self):
        query = "SELECT id, name FROM land"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_GPs(self):
        query = "SELECT * FROM GP"
        self.cursor.execute(query)
        return self.cursor.fetchall()

db_con = database_connection()

db_con.insert_GPs()
print(db_con.get_GPs())

#db_con.insert_countries()
#print(db_con.get_countries())