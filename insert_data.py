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

        with open('f1_country_of_driver_2023.csv', newline='', encoding='utf-8') as file:
            csv_data = csv.reader(file)
            for row in csv_data:
                if row[1] == 'Country_of_driver':
                    continue
                countries.append((row[1],))
        
        with open('f1_country_info_2024.csv', newline='', encoding='utf-8') as file:
            csv_data = csv.reader(file)
            for row in csv_data:
                if row[1] == 'Country_name':
                    continue
                countries.append((row[1],))
        
        with open('f1_country_of_driver_2024.csv', newline='', encoding='utf-8') as file:
            csv_data = csv.reader(file)
            for row in csv_data:
                if row[1] == 'Country_of_driver':
                    continue
                countries.append((row[1],))

        # remove duplicates
        countries = list(set(countries))

        self.cursor.executemany(query, countries)
        self.mydb.commit()

    def insert_GPs(self):
        query = "INSERT INTO GP (land_id, gp_number, circuit_name, location, date, length) VALUES (%s, %s, %s, %s, %s, %s)"

        # INSERT INTO GP (land_id, gp_number, circuit_name, location, date, length) VALUES (38, '1080', 'Bahrain International Circuit', 'Sakhir', '2023-03-05', '5412')

        GPs = []
        GPs_ids = []

        # open GP csv
        with open('f1_GP_info_2023.csv', newline='', encoding='utf-8') as file:
            csv_data = csv.reader(file)
            for row in csv_data:
                if row[0] == 'GP_id':
                    continue
                GPs.append((row[1], row[2], row[3], row[4], row[5], row[6]))

        country_ids = self.get_country_ids()

        # replace all country names with country ids and add to GPs_ids
        for GP in GPs:
            for country in country_ids:
                if GP[0] == country[1]:
                    GP = (country[0],) + GP[1:]
                    GPs_ids.append(GP)
                    break

        self.cursor.executemany(query, GPs_ids)
        self.mydb.commit()

    def insert_functions(self):
        query = "INSERT INTO function (name) VALUES (%s)"

        functions = [
            ('coureur',),
            ('testcoureur',),
        ]

        self.cursor.executemany(query, functions)
        self.mydb.commit()

    def insert_drivers_info(self):
        query = "INSERT INTO driver (function_id, name, dateofbirth) VALUES (%s, %s, %s)"

        drivers = []
        drivers_ids = []

        with open('f1_drivers_info_2023.csv', newline='', encoding='utf-8') as file:
            csv_data = csv.reader(file)
            for row in csv_data:
                if row[0] == 'driver_id':
                    continue
                drivers.append((row[1], row[2], row[3]))

        function_ids = self.get_function_ids()

        for driver in drivers:
            for function in function_ids:
                if driver[0] == function[1]:
                    driver = (function[0],) + driver[1:]
                    drivers_ids.append(driver)
                    break
        
        self.cursor.executemany(query, drivers_ids)
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

    def get_function_ids(self):
        query = "SELECT id, name FROM function"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert_all_data(self):
        self.insert_countries()
        self.insert_GPs()
        self.insert_functions()
        self.insert_drivers_info()

db_con = database_connection()

db_con.insert_countries()