import Import_data
import insert_data

debug = False

def main():
    if debug:
        insert= insert_data.database_connection()
        insert.insert_all_data()
    else:
        input_choice = input("Do you want to create CSVs or insert data into database? \nType CSVs[0] or insert[1]: ")

        while(input_choice == "0"):
            input_year = input("\nEnter the year for which you want to create CSVs: ")
            data = Import_data.Import_data_class(int(input_year))
            while (True):
                # check for user input into the console
                user_input = input("\nWhat data do you want to import? \nType the number within brackets: Drivers[0], GPs[1], countries[2], statuses[3], points[4] or all[5]? \nTo change the year[6], to insert data into database[7] or to exit[8]: ")
                if(user_input == "0"):
                    data.save_driver_info_to_csv()
                elif(user_input == "1"):
                    data.save_GP_info_to_csv()
                elif(user_input == "2"):
                    data.save_country_info_to_csv
                elif(user_input == "3"):
                    data.save_status_info_to_csv()
                elif(user_input == "4"):
                    data.save_points_race_to_csv()
                elif(user_input == "5"):
                    data.save_driver_info_to_csv()
                    data.save_GP_info_to_csv()
                    data.save_country_info_to_csv
                    data.save_status_info_to_csv()
                    data.save_points_race_to_csv()
                    data.save_country_of_driver_to_csv()
                elif(user_input == "6"):
                    input_year = input("Enter the year for which you want to import data: ")
                    data.change_year(int(input_year))
                elif(user_input == "7"):
                    input_choice = "1"
                    break
                elif(user_input == "8"):
                    break


        while(input_choice == "1"):
            insert= insert_data.database_connection()
            user_input = input("\nWhat data do you want to insert? \nType the number within brackets: Countries[0], GPs[1], functions[2], drivers[3], driver_countries[4], \nconstructors[5], constructor_driver[6], points[7] or all[8]? \nTo exit[9]")
            if(user_input == "0"):
                insert.insert_countries()
            elif(user_input == "1"):
                insert.insert_GPs()
            elif(user_input == "2"):
                insert.insert_functions()
            elif(user_input == "3"):
                insert.insert_drivers_info()
            elif(user_input == "4"):
                insert.insert_driver_countries()
            elif(user_input == "5"):
                insert.insert_constructors()
            elif(user_input == "6"):    
                insert.insert_constructor_driver()
            elif(user_input == "7"):
                insert.insert_points_race()
            elif(user_input == "8"):
                insert.insert_countries()
                insert.insert_GPs()
                insert.insert_functions()
                insert.insert_drivers_info()
                insert.insert_driver_countries()
                insert.insert_constructors()
                insert.insert_constructor_driver()
                insert.insert_points_race()
            elif(user_input == "9"):
                break
        


if __name__ == "__main__":
    main()