import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os

year = 2024
url = "https://nl.wikipedia.org/wiki/Formule_1_in_" + str(year)

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

tables = soup.find_all('table', {'class': 'wikitable'})

def get_driver_names(tables):
    driver_names = []
    if year == 2024:
        table = tables[5]
    else:
        table = tables[6]
    rows = table.find_all('tr')
    for row in rows[1:]:  # Skipping the header row
        data = row.find_all('td')
        if data:  # Check if there is data in the row
            driver_name = data[1].text.strip()  # Adjust the index if needed
            driver_names.append(driver_name)
    return driver_names

def get_driver_dob(driver_names):
    # get driver date of birth and download foto. Use name with underscore for wikipedia search
    # take a list of driver names and view wikipedia page for each driver
    # example: for name of driver 'Max Verstappen' search https://nl.wikipedia.org/wiki/Max_Verstappen
    # get date of birth and download foto
    
    base_url = "https://nl.wikipedia.org/wiki/" 
    driver_info = []
    for driver_name in driver_names:
        url = base_url + driver_name.replace(' ', '_')
        # wtf george russell and charles leclerc have a different page name
        if driver_name == 'George Russell' or driver_name == 'Charles Leclerc':
            url = url + '_(autocoureur)'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Improved search for 'Geboren', using partial text match and ignoring case
        th = soup.find('th', text=lambda t: t and 'geboren' in t.lower())

        driver_info_dict = {'name': driver_name}

        # Check if a matching th tag was found
        if th:
            dob_full_text = th.find_next('td').text.strip()
            # Search for the first occurrence of four consecutive digits in the dob_full_text
            year_match = re.search(r'\d{4}', dob_full_text)
            if year_match:
                # Find the position where the year starts
                year_start_pos = year_match.start()
                # Cut the string to include everything up to the year
                dob = dob_full_text[:year_start_pos+4]  # Include the year itself
                driver_info_dict['dob'] = dob
            else:
                driver_info_dict['dob'] = 'Not found'
        else:
            driver_info_dict['dob'] = 'Not found'

        driver_info.append(driver_info_dict)

    return driver_info

def save_driver_info_to_csv():
    # convert to .csv files
    df = pd.DataFrame(get_driver_dob(get_driver_names(tables)), columns=['name', 'dob'])

    # Specify the file path for the CSV file
    # get current working directory
    cwd = os.getcwd()
    if year == 2024:
        file_path = os.path.join(cwd, 'f1_drivers_dob_2024.csv')
    else:    
        file_path = os.path.join(cwd, 'f1_drivers_dob_2023.csv')

    # Save the DataFrame to a CSV file

    df.to_csv(file_path, index=False)

def get_GP_info(tables):
    table = tables[0]
    GP_info = []
    rows = table.find_all('tr')
    for row in rows[1:]:  # Skipping the header row
        cur_GP_info = {}
        data = row.find_all('td')
        if data:  # Check if there is data in the row
            GP_nr = data[0].text.strip()  # GP number
            cur_GP_info.update({'GP_nr': GP_nr})
            GP_circuit = data[2].text.strip()  # GP Circuit name
            cur_GP_info.update({'GP_circuit': GP_circuit})
            GP_place = data[3].text.strip() # GP place
            cur_GP_info.update({'GP_place': GP_place})
            GP_date = data[4].text.strip()
            cur_GP_info.update({'GP_date': GP_date})
            GP_info.append(cur_GP_info)
    return GP_info

def get_GP_length(GP_info):
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
            GP_info[i].update({'GP_length': length})
        else:
            GP_info[i].update({'GP_length': 'Not found'})
    return GP_info
    
def save_GP_info_to_csv():
    # convert to .csv files
    df = pd.DataFrame(get_GP_length(get_GP_info(tables)), columns=['GP_nr', 'GP_circuit', 'GP_place', 'GP_date', 'GP_length'])

    # Specify the file path for the CSV file
    # get current working directory
    cwd = os.getcwd()
    if year == 2024:
        file_path = os.path.join(cwd, 'f1_GP_info_2024.csv')
    else:    
        file_path = os.path.join(cwd, 'f1_GP_info_2023.csv')

    # Save the DataFrame to a CSV file

    df.to_csv(file_path, index=False)

save_GP_info_to_csv()
#save_driver_info_to_csv()