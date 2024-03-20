import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import math

class Import_data_class():

    def __init__(self, year):
        self.year = year
        self.tables = self.request_tables(self.year)

    def request_tables(self, year):
        url = "https://nl.wikipedia.org/wiki/Formule_1_in_" + str(self.year)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        tables = soup.find_all('table', {'class': 'wikitable'})
        return tables
    
    def change_year(self, year):
        self.year = year
        self.tables = self.request_tables(self.year)

    def get_driver_names(self):
        tables = self.tables
        driver_info = []
        driver_id = 0
        if self.year == 2024:
            table = tables[5]
        else:
            table = tables[6]
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skipping the header row
            cur_driver_info = {}
            data = row.find_all('td')
            if data:  # Check if there is data in the row
                # give id to driver
                cur_driver_info.update({'Driver_id': driver_id})
                driver_id += 1
                driver_function = 'coureur'
                cur_driver_info.update({'Driver_function': driver_function})
                driver_name = data[1].text.strip()  # Adjust the index if needed
                cur_driver_info.update({'Driver_name': driver_name})
                driver_info.append(cur_driver_info)
        return driver_info

    def get_driver_dob(self, driver_info):
        
        base_url = "https://nl.wikipedia.org/wiki/" 
        for i in range(0, len(driver_info)):
            driver_name = driver_info[i]['Driver_name'] 
            url = base_url + driver_name.replace(' ', '_')
            # wtf george russell and charles leclerc have a different page name
            if driver_name == 'George Russell' or driver_name == 'Charles Leclerc':
                url = url + '_(autocoureur)'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Improved search for 'Geboren', using partial text match and ignoring case
            th = soup.find('th', text=lambda t: t and 'geboren' in t.lower())

            # Check if a matching th tag was found
            if th:
                dob_full_text = th.find_next('td').text.strip()
                # Search for the first occurrence of four consecutive digits in the dob_full_text
                self.year_match = re.search(r'\d{4}', dob_full_text)
                if self.year_match:
                    # Find the position where the self.year starts
                    self.year_start_pos = self.year_match.start()
                    # Cut the string to include everything up to the self.year
                    dob = dob_full_text[:self.year_start_pos+4]  # Include the self.year itself

                    # get month from date example 'maart'
                    month = re.search(r'[a-zA-Z]+', dob).group(0)
                    month = self.change_month_to_number(month)
                    # get day from date
                    day = re.search(r'\d+', dob).group(0)
                    # add leading zero to day if needed
                    if len(day) == 1:
                        day = '0' + day
                    # add leading zero to month if needed
                    if len(str(month)) == 1:
                        month = '0' + str(month)
                    # get year from dob
                    year = re.search(r'\d{4}', dob).group(0)
                    dob = year + '-' + str(month) + '-' + day

                    driver_info[i].update({'Driver_date_of_birth': dob})
        
        return driver_info

    def get_driver_info(self):
        names = self.get_driver_names()
        return self.get_driver_dob(names)

    def save_driver_info_to_csv(self):
        df = pd.DataFrame(self.get_driver_info(), columns=['Driver_id', 'Driver_function', 'Driver_name', 'Driver_date_of_birth'])
        if self.year == 2024:
            file_path = os.path.join(os.getcwd(), 'f1_drivers_info_2024.csv')
        else:    
            file_path = os.path.join(os.getcwd(), 'f1_drivers_info_2023.csv')
        df.to_csv(file_path, index=False)

    def get_GP_basic_info(self):
        table = self.tables[0]
        GP_info = []
        GP_id = 0
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skipping the header row
            cur_GP_info = {}
            data = row.find_all('td')
            if data:  # Check if there is data in the row
                cur_GP_info.update({'GP_id': GP_id})
                GP_id += 1
                GP_country = data[1].text.strip()  # GP country
                # remove 'GP van ' from GP_country
                GP_country = re.sub(r'GP van ', '', GP_country)
                cur_GP_info.update({'GP_country_id': GP_country})
                GP_nr = data[0].text.strip()  # GP number
                cur_GP_info.update({'GP_nr': GP_nr})
                GP_circuit = data[2].text.strip()  # GP Circuit name
                cur_GP_info.update({'GP_circuit': GP_circuit})
                GP_place = data[3].text.strip() # GP place
                cur_GP_info.update({'GP_place': GP_place})
                
                GP_date_string = data[4].text.strip()
                # get month from date example 'maart'
                month = re.search(r'[a-zA-Z]+', GP_date_string).group(0)
                month = self.change_month_to_number(month)
                # get day from date
                day = re.search(r'\d+', GP_date_string).group(0)
                # add leading zero to day if needed
                if len(day) == 1:
                    day = '0' + day
                # add leading zero to month if needed
                if len(str(month)) == 1:
                    month = '0' + str(month)
                GP_date = str(self.year) + '-' + str(month) + '-' + day
                cur_GP_info.update({'GP_date': GP_date})
                GP_info.append(cur_GP_info)
        return GP_info

    def change_month_to_number(self, month):
        case = {
            'januari': 1,
            'februari': 2,
            'maart': 3,
            'april': 4,
            'mei': 5,
            'juni': 6,
            'juli': 7,
            'augustus': 8,
            'september': 9,
            'oktober': 10,
            'november': 11,
            'december': 12
        }
        return case.get(month, 'Invalid month')

    def get_GP_length(self, GP_info):
        base_url = "https://nl.wikipedia.org/wiki/"
        for i in range(0, len(GP_info)):
            url = base_url + GP_info[i]['GP_circuit'].replace(' ', '_')
            if GP_info[i]['GP_circuit'] == 'Albert Park Circuit':
                url = base_url + 'Albert_Park_Street_Circuit'
            if GP_info[i]['GP_circuit'] == 'Silverstone Circuit':
                url = base_url + 'Silverstone_(circuit)'
            if GP_info[i]['GP_circuit'] == 'Circuit of The Americas':
                url = base_url + 'Circuit_of_the_Americas'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # Improved search for 'Lengte' using partial text match and ignoring case
            th = soup.find('th', text=lambda t: t and 'lengte' in t.lower())
            # Check if a matching th tag was found
            if th:
                length = th.find_next('td').text.strip()
                # if length contains [1], remove it
                length = re.sub(r'\[.*\]', '', length)
                # if length contains km, remove it
                length = re.sub(r' km', '', length)
                # if length contains a comma, remove it
                length = re.sub(r',', '', length)
                GP_info[i].update({'GP_length': length})
            else:
                GP_info[i].update({'GP_length': 'Not found'})
        return GP_info
        
    def get_GP_country(self, GP_info):
        # get GP country name. Use name with underscore for wikipedia search
        base_url = "https://nl.wikipedia.org/wiki/Grand_Prix_Formule_1_van_"
        for i in range(0, len(GP_info)):
            url = base_url + GP_info[i]['GP_country_id'].replace(' ', '_')
            response = requests.get(url)
            df = pd.read_html(response.text, match='Land')[0]
            row_index = df[df.columns[0]].eq('Land').idxmax()
            value_in_next_column = df.iloc[row_index, df.columns.get_loc(df.columns[1]) + 1]
            GP_info[i].update({'GP_country_id': value_in_next_column})

            # for now all countries_IDs are not set yet
            #GP_info[i].update({'GP_country_id': 'Not set yet'})
        return GP_info

    def get_GP_info(self):
        GP_info = self.get_GP_basic_info()
        GP_info = self.get_GP_length(GP_info)
        return self.get_GP_country(GP_info)

    def save_GP_info_to_csv(self):
        df = pd.DataFrame(self.get_GP_info(), columns=['GP_id', 'GP_country_id', 'GP_nr', 'GP_circuit', 'GP_place', 'GP_date', 'GP_length'])
        if self.year == 2024:
            file_path = os.path.join(os.getcwd(), 'f1_GP_info_2024.csv')
        else:    
            file_path = os.path.join(os.getcwd(), 'f1_GP_info_2023.csv')
        df.to_csv(file_path, index=False)

    def get_country_info(self):
        base_url = "https://nl.wikipedia.org/wiki/Grand_Prix_Formule_1_van_"
        Country_info = []
        Country_id = 0
        
        table = self.tables[0]
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skipping the header row
            data = row.find_all('td')
            if data:  # Check if there is data in the row
                countr_name_raw = data[1].text.strip()  # GP country
                # remve 'GP van ' from GP_country
                country_name_for_search = re.sub(r'GP van ', '', countr_name_raw)
                cur_country_info = {}
                cur_country_info.update({'Country_id': Country_id})
                Country_id += 1
                url = base_url + country_name_for_search.replace(' ', '_')
                response = requests.get(url)
                df = pd.read_html(response.text, match='Land')[0]
                row_index = df[df.columns[0]].eq('Land').idxmax()
                value_in_next_column = df.iloc[row_index, df.columns.get_loc(df.columns[1]) + 1]
                cur_country_info.update({'Country_name': value_in_next_column})
                cur_country_info.update({'Country_photo_path': 'media/'+value_in_next_column.replace(' ', '_')+'.PNG'})
                Country_info.append(cur_country_info)
        one_off_country = {'Country_id': 1000, 'Country_name': 'Zwitserland', 'Country_photo_path': 'media/Zwitserland.PNG'}
        Country_info.append(one_off_country)
        return Country_info

    def save_country_info_to_csv(self):
        df = pd.DataFrame(self.get_country_info(), columns=['Country_id', 'Country_name', 'Country_photo_path'])
        if self.year == 2024:
            file_path = os.path.join(os.getcwd(), 'f1_country_info_2024.csv')
        else:    
            file_path = os.path.join(os.getcwd(), 'f1_country_info_2023.csv')
        df.to_csv(file_path, index=False) 

    def get_status(self):
        base_url = "https://nl.wikipedia.org/wiki/Formule_1_in_"
        url = base_url + str(self.year)

        Status_info = []

        response = requests.get(url)
        df = pd.read_html(response.text, match='Coureur')[3]
        df_Coureur = df['Coureur']
        for i in range(0, len(df_Coureur)):
            status = df.loc[i]
            status = status.sort_index()
            status = status.drop(['Pos.', 'Nr.', 'Coureur', 'Punten']) # remove crap
            status = status.dropna() # remove NaN
            for j in range(0, len(status)):
                current_status_info = {}
                current_status_info.update({'Driver': df_Coureur.loc[i, 'Coureur']})
                current_status_info.update({'GP': status.index[j][1]})
                cur_status = status.values[j]
                current_status_info.update({'Status': 'Null'})
                if 'NC' in cur_status:
                    current_status_info.update({'Status': 'NC'})
                    cur_status = cur_status.replace('NC', '')
                if 'DNF' in cur_status:
                    current_status_info.update({'Status': 'DNF'})
                    cur_status = cur_status.replace('DNF', '')
                if 'DNQ' in cur_status:
                    current_status_info.update({'Status': 'DNQ'})
                    cur_status = cur_status.replace('DNQ', '')
                if 'DSQ' in cur_status:
                    current_status_info.update({'Status': 'DSQ'})
                    cur_status = cur_status.replace('DSQ', '')
                if 'DNS' in cur_status:
                    current_status_info.update({'Status': 'DNS'})
                    cur_status = cur_status.replace('DNS', '')
                if 'EX' in cur_status:
                    current_status_info.update({'Status': 'EX'})
                    cur_status = cur_status.replace('EX', '')
                if 'WD' in cur_status:
                    current_status_info.update({'Status': 'WD'})
                    cur_status = cur_status.replace('WD', '')
                
                if 'S' in cur_status:
                    current_status_info.update({'Fastest_lap': True})
                    cur_status = cur_status.replace('S', '')
                else:
                    current_status_info.update({'Fastest_lap': False})
                if 'P' in cur_status:
                    current_status_info.update({'Pole_position': True})
                    cur_status = cur_status.replace('P', '')
                else:
                    current_status_info.update({'Pole_position': False})

                Status_info.append(current_status_info)
        return Status_info

    def save_status_info_to_csv(self):
        df = pd.DataFrame(self.get_status(), columns=['Driver', 'GP', 'Status', 'Fastest_lap', 'Pole_position'])
        if self.year == 2024:
            file_path = os.path.join(os.getcwd(), 'f1_status_info_2024.csv')
        else:    
            file_path = os.path.join(os.getcwd(), 'f1_status_info_2023.csv')
        df.to_csv(file_path, index=False)

    def get_country_of_driver(self, driver_info):

        country_of_driver = []

        base_url = "https://nl.wikipedia.org/wiki/" 
        for i in range(0, len(driver_info)):
            current_country_of_driver = {}
            second_current_country_of_driver = {}
            driver_name = driver_info[i]['Driver_name'] 
            current_country_of_driver.update({'Driver_name': driver_name})
            url = base_url + driver_name.replace(' ', '_')
            # wtf george russell and charles leclerc have a different page name
            if driver_name == 'George Russell' or driver_name == 'Charles Leclerc':
                url = url + '_(autocoureur)'
            response = requests.get(url)
            df = pd.read_html(response.text, match='Nationaliteit')[0]
            row_index = df[df.columns[0]].eq('Nationaliteit').idxmax()
            value_in_next_column = df.iloc[row_index, df.columns.get_loc(df.columns[1]) + 1]
            # check if string contains 'xa0' and split it into two values
            check_for_xa0 = value_in_next_column.find(u'\xa0')
            if value_in_next_column == 'Verenigd Koninkrijk België':
                value_in_next_column = 'Verenigd Koninkrijk '+u'\xa0'+ 'België'
                check_for_xa0 = 1
            if check_for_xa0 != -1:
                first_value_in_next_column = value_in_next_column.split(u'\xa0')[0]
                # remove trailing whitespace
                first_value_in_next_column = first_value_in_next_column.rstrip()
                current_country_of_driver.update({'Country_of_driver': first_value_in_next_column})
                country_of_driver.append(current_country_of_driver)

                second_current_country_of_driver.update({'Driver_name': driver_name})
                second_value_in_next_column = value_in_next_column.split(u'\xa0')[1]
                second_value_in_next_column = second_value_in_next_column.replace(u'\xa0', '')
                second_current_country_of_driver.update({'Country_of_driver': second_value_in_next_column})
                country_of_driver.append(second_current_country_of_driver)
            else:
                current_country_of_driver.update({'Country_of_driver': value_in_next_column})
                country_of_driver.append(current_country_of_driver)

        return country_of_driver

    def save_country_of_driver_to_csv(self):
        df = pd.DataFrame(self.get_country_of_driver(self.get_driver_info()), columns=['Driver_name', 'Country_of_driver'])
        if self.year == 2024:
            file_path = os.path.join(os.getcwd(), 'f1_country_of_driver_2024.csv')
        else:    
            file_path = os.path.join(os.getcwd(), 'f1_country_of_driver_2023.csv')
        df.to_csv(file_path, index=False)

    def get_points_race(self):
        
        GP_info = self.get_GP_country()

        races_left = 0

        if self.year == 2024:
            races_left = len(GP_info) - 2 

        points_race = []
        # get GP country name. Use name with underscore for wikipedia search
        base_url = "https://nl.wikipedia.org/wiki/Grand_Prix_Formule_1_van_"
        for i in range(0, len(GP_info)-races_left):
            
            url = base_url + GP_info[i]['GP_country_id'].replace(' ', '_') + '_' + str(self.year)
            response = requests.get(url)
            df = pd.read_html(response.text)
            df_circuit_name = df[0]
            row_index = df_circuit_name[df_circuit_name.columns[0]].eq('Circuit').idxmax()
            circuit_name = df_circuit_name.iloc[row_index, df_circuit_name.columns.get_loc(df_circuit_name.columns[1]) + 1]

            row_index = df_circuit_name[df_circuit_name.columns[0]].eq('Pole position').idxmax()
            pole_position = df_circuit_name.iloc[row_index + 1, df_circuit_name.columns.get_loc(df_circuit_name.columns[1]) + 1]
            # remove everything within brackets
            pole_position = re.sub(r'\([^)]*\)', '', pole_position)
            pole_position = pole_position.rstrip()

            row_index = df_circuit_name[df_circuit_name.columns[0]].eq('Snelste ronde').idxmax()
            fastest_lap = df_circuit_name.iloc[row_index + 1, df_circuit_name.columns.get_loc(df_circuit_name.columns[1]) + 1]
            # remove everything within brackets
            fastest_lap = re.sub(r'\([^)]*\)', '', fastest_lap)
            fastest_lap = fastest_lap.rstrip()


            df_races = pd.read_html(response.text, match='Rondes')
            if len(df_races) > 1:
                df_sprint = df_races[0]
                df_GP = df_races[1]
                for i in range(0, len(df_sprint)-1):
                    current_points_race = {}
                    # get driver name
                    driver = df_sprint.iloc[i, 2]
                    # get position
                    position = df_sprint.iloc[i, 0]
                    current_points_race.update({'Type_race': 'Sprint'})
                    current_points_race.update({'Driver': driver})
                    # check if position is a number
                    if position.isdigit():
                        current_points_race.update({'Position': position})
                        current_points_race.update({'Status': 'Null'})
                    else:
                        current_points_race.update({'Position': 'Null'})
                        current_points_race.update({'Status': position})
                    current_points_race.update({'Circuit': circuit_name})
                    current_points_race.update({'Fastest_lap': 'False'})
                    current_points_race.update({'Pole_position': 'False'})
                    points_race.append(current_points_race)
            
            
            else:
                df_GP = df_races[0]
             
            for i in range(0, len(df_GP)-1):
                    current_points_race = {}
                    # get driver name
                    driver = df_GP.iloc[i, 2]
                    # get position
                    position = df_GP.iloc[i, 0]
                    current_points_race.update({'Type_race': 'GP'})
                    current_points_race.update({'Driver': driver})
                    # check if position is a number
                    if position.isdigit():
                        current_points_race.update({'Position': position})
                        current_points_race.update({'Status': 'Null'})
                    else:
                        current_points_race.update({'Position': 'Null'})
                        current_points_race.update({'Status': position})
                    current_points_race.update({'Circuit': circuit_name})
                    if driver == pole_position:
                        current_points_race.update({'Pole_position': 'True'})
                    else:
                        current_points_race.update({'Pole_position': 'False'})
                    if driver == fastest_lap:
                        current_points_race.update({'Fastest_lap': 'True'})
                    else:
                        current_points_race.update({'Fastest_lap': 'False'})
                    points_race.append(current_points_race)

        return points_race

    # {'Type_race': 'GP', 'Driver': 'Max Verstappen', 'Position': '1', 'Status': 'Null', 'Circuit': 'Bahrain International Circuit', 'Pole_position': 'False'}
    def save_points_race_to_csv(self):
        df = pd.DataFrame(self.get_points_race(), columns=['Type_race', 'Driver', 'Position', 'Status', 'Circuit', 'Pole_position', 'Fastest_lap'])
        if self.year == 2024:
            file_path = os.path.join(os.getcwd(), 'f1_points_race_2024.csv')
        else:
            file_path = os.path.join(os.getcwd(), 'f1_points_race_2023.csv')
        df.to_csv(file_path, index=False)
    

    def get_GP_country(self):
        table = self.tables[0]
        GP_countries = []
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skipping the header row
            cur_GP_info = {}
            data = row.find_all('td')
            if data:  # Check if there is data in the row
                GP_country = data[1].text.strip()  # GP country
                # remove 'GP van ' from GP_country
                GP_country = re.sub(r'GP van ', '', GP_country)
                cur_GP_info.update({'GP_country_id': GP_country})
                GP_countries.append(cur_GP_info)
        
        return GP_countries