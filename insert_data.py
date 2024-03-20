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

        with open('f1_GP_info_2024.csv', newline='', encoding='utf-8') as file:
            csv_data = csv.reader(file)
            for row in csv_data:
                if row[0] == 'GP_id':
                    continue
                GPs.append((row[1], row[2], row[3], row[4], row[5], row[6]))

        # remove duplicates
        GPs = list(set(GPs))

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

        with open('f1_drivers_info_2024.csv', newline='', encoding='utf-8') as file:
            csv_data = csv.reader(file)
            for row in csv_data:
                if row[0] == 'driver_id':
                    continue
                drivers.append((row[1], row[2], row[3]))

        # remove duplicates
        drivers = list(set(drivers))

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

    def insert_driver_countries(self):

        country_ids = self.get_country_ids()
        driver_ids = self.get_driver_ids()

        query = "INSERT INTO land_driver (land_id, driver_id) VALUES (%s, %s)"

        driver_countries = []
        driver_countries_ids = []

        with open('f1_country_of_driver_2023.csv', newline='', encoding='utf-8') as file:
            csv_data = csv.reader(file)
            for row in csv_data:
                if row[1] == 'Country_of_driver':
                    continue
                driver_countries.append((row[0], row[1]))
        
        with open('f1_country_of_driver_2024.csv', newline='', encoding='utf-8') as file:
            csv_data = csv.reader(file)
            for row in csv_data:
                if row[1] == 'Country_of_driver':
                    continue
                driver_countries.append((row[0], row[1]))
        
        # remove duplicates
        driver_countries = list(set(driver_countries))
        test = 1        

        for driver_country in driver_countries:
            driver_id = next((number for number, name in driver_ids if name == driver_country[0]), None)
            country_id = next((number for number, name in country_ids if name == driver_country[1]), None)
            # update driver_countries_ids with the driver_id and country_id
            driver_countries_ids.append((country_id, driver_id))

        self.cursor.executemany(query, driver_countries_ids)
        self.mydb.commit()

    def insert_constructors(self):

        query = "INSERT INTO constructor (land_id, name) VALUES (%s, %s)"

        country_ids = self.get_country_ids()

        constructors = []
        constructors_ids = []

        with open('f1_constructor_info_2023.csv', newline='', encoding='utf-8') as file:
            csv_data = csv.reader(file)
            for row in csv_data:
                if row[0] == 'constructor_id':
                    continue
                constructors.append((row[1],row[3],))
        
        with open('f1_constructor_info_2024.csv', newline='', encoding='utf-8') as file:
            csv_data = csv.reader(file)
            for row in csv_data:
                if row[0] == 'constructor_id':
                    continue
                constructors.append((row[1],row[3],))

        # remove duplicates
        constructors = list(set(constructors))

        for constructor in constructors:
            country_id = next((number for number, name in country_ids if name == constructor[0]), None)
            constructors_ids.append((country_id, constructor[1]))

        self.cursor.executemany(query, constructors_ids)
        self.mydb.commit()

    def insert_constructor_driver(self):
    
            query = "INSERT INTO constructor_driver (driver_id, constructor_id) VALUES (%s, %s)"
    
            constructor_ids = self.get_constructor_ids()
            driver_ids = self.get_driver_ids()
    
            constructor_driver = []
            constructor_driver_ids = []
    
            with open('f1_constructor_driver_2023.csv', newline='') as file:
                csv_data = csv.reader(file)
                for row in csv_data:
                    if row[0] == 'constructor_name':
                        continue
                    constructor_driver.append((row[0], row[1]))
            
            with open('f1_constructor_driver_2024.csv', newline='') as file:
                csv_data = csv.reader(file)
                for row in csv_data:
                    if row[0] == 'constructor_name':
                        continue
                    constructor_driver.append((row[0], row[1]))
    
            # remove duplicates
            constructor_driver = list(set(constructor_driver))
    
            for cd in constructor_driver:
                constructor_id = next((number for number, name in constructor_ids if name == cd[0]), None)
                driver_id = next((number for number, name in driver_ids if name == cd[1]), None)
                constructor_driver_ids.append((driver_id, constructor_id))

            self.cursor.executemany(query, constructor_driver_ids)
            self.mydb.commit()
    
    def insert_statuses(self):

        query = "INSERT INTO status (status) VALUES (%s)"
        
        statuses = [
            ('NC',),
            ('DNF',),
            ('DNQ',),
            ('DSQ',),
            ('DNS',),
            ('EX',),
            ('WD',),
        ]

        self.cursor.executemany(query, statuses)
        self.mydb.commit()

    def insert_points_race(self):
        
        query = "INSERT INTO points (driver_id, pointsrace_id, gp_id, status_id, pole, fastest_lap) VALUES (%s, %s, %s, %s, %s, %s)" 
        #INSERT INTO points (driver_id, pointsrace_id, gp_id, status_id, pole, fastest_lap) VALUES (23, 13, 1, 1, 'False', 'False')
        
        GP_ids = self.get_GP_ids()
        driver_ids = self.get_driver_ids()
        status_ids = self.get_status_ids()
        points_race_ids = self.get_points_race_ids()
        
        points = []
        points_ids = []
        
        with open('f1_points_race_2023.csv', newline='', encoding='utf-8') as file:
            csv_data = csv.reader(file)
            for row in csv_data:
                if row[0] == 'Type_race':
                    continue
                points.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

        with open('f1_points_race_2024.csv', newline='', encoding='utf-8') as file:
            csv_data = csv.reader(file)
            for row in csv_data:
                if row[0] == 'Type_race':
                    continue
                points.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

        for point in points:
            driver_id = next((number for number, name in driver_ids if name == point[1]), None)
            gp_id = next((number for number, name in GP_ids if name == point[4]), None)
            status_id = next((number for number, name in status_ids if name == point[3]), None)
            value = point[2]
            if value == '0' or value == '':
                points_id = None
            else:
                points_id = next((race_id for race_id, position, race_type in points_race_ids if position == int(point[2]) and race_type == point[0]), None)
            pole_position = point[5]
            fastest_lap = point[6]
            points_ids.append((driver_id, points_id, gp_id, status_id, pole_position, fastest_lap,  ))
 
        self.cursor.executemany(query, points_ids)
        self.mydb.commit()

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

    def get_driver_ids(self):
        query = "SELECT id, name FROM driver"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_constructor_ids(self):
        query = "SELECT id, name FROM constructor"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_status_ids(self):
        query = "SELECT id, status FROM status"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_points_race_ids(self):
        query = "SELECT id, place, racetype FROM points_race"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_GP_ids(self):
        query = "SELECT id, circuit_name FROM GP"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert_all_data(self):
        self.insert_countries()
        self.insert_GPs()
        self.insert_functions()
        self.insert_drivers_info()
        self.insert_driver_countries()
        self.insert_constructors()
        self.insert_constructor_driver()
        self.insert_points_race()
