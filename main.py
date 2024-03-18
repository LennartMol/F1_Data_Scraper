import Import_data

debug = True

def main():
    if debug:
        data = Import_data.Import_data_class(2023)
        data.save_status_info_to_csv()
    else:
        input_year = input("Enter the year for which you want to import data: ")
        data = Import_data.Import_data_class(int(input_year))
        while (True):
            # check for user input into the console
            user_input = input("What data do you want to import? (drivers, GP, country, status, all, exit, changeYear): ")
            if(user_input == "drivers"):
                data.save_driver_info_to_csv()
            elif(user_input == "GP"):
                data.save_GP_info_to_csv()
            elif(user_input == "country"):
                data.save_country_info_to_csv()
            elif(user_input == "status"):
                data.save_status_info_to_csv()
            elif(user_input == "all"):
                data.save_status_info_to_csv()
                data.save_driver_info_to_csv()
                data.save_GP_info_to_csv()
                data.save_country_info_to_csv()
            elif(user_input == "exit"):
                break
            elif(user_input == "changeYear"):
                input_year = input("Enter the year for which you want to import data: ")
                data.change_year(int(input_year))


if __name__ == "__main__":
    main()