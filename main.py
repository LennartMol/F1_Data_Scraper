import Import_data

debug = False

def main():
    if debug:
        data = Import_data.Import_data_class(2023)
        data.save_points_race_to_csv()
    else:
        input_year = input("Enter the year for which you want to import data: ")
        data = Import_data.Import_data_class(int(input_year))
        while (True):
            # check for user input into the console
            user_input = input("What data do you want to export to CSV? \nType the number within brackets: Drivers[0], GPs[1], countries[2], statuses[3] or all[4]. \nTo change the year[5] or to exit[6]: ")
            if(user_input == "0"):
                data.save_driver_info_to_csv()
            elif(user_input == "1"):
                data.save_GP_info_to_csv()
            elif(user_input == "2"):
                data.save_country_info_to_csv()
            elif(user_input == "3"):
                data.save_status_info_to_csv()
            elif(user_input == "4"):
                data.save_status_info_to_csv()
                data.save_driver_info_to_csv()
                data.save_GP_info_to_csv()
                data.save_country_info_to_csv()
                data.save_country_of_driver_to_csv()
                data.save_points_race_to_csv()
            elif(user_input == "5"):
                input_year = input("Enter the year for which you want to import data: ")
                data.change_year(int(input_year))
            elif(user_input == "6"):
                break


if __name__ == "__main__":
    main()