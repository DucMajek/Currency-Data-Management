import csv
import requests
import numpy as np

selected_data = []


def average(lst):
    return sum(lst) / len(lst)


# Function check the selected data is in array selected_data
def check_the_value_is_exist_in_array(value: str, array):
    for element in array:
        if value == element:
            print("Data is already in use")
            return True

    selected_data.append(value)


def menu(number: int):
    while number not in range(1, 4):
        try:
            number = int(input("Wrong number. Please choose again or the data you selected is already in use\n "
                               "1. Exchange => PLN \n 2. EUR => USD \n 3. CHF => USD \n"))
        except ValueError:
            print("Please enter a valid number.")

    if number == 1:
        check_the_value_is_exist_in_array("Exchange => PLN", selected_data)
    elif number == 2:
        check_the_value_is_exist_in_array("EUR => USD", selected_data)
    elif number == 3:
        check_the_value_is_exist_in_array("CHF => USD", selected_data)

    print(selected_data)


def start():
    start_program = True
    while start_program:
        try:
            lang = int(input("Select the currency which you are interested \n "
                             "1. Exchange => PLN \n 2. EUR => USD \n 3. CHF => USD \n"))
            menu(lang)

            end_loop = int(input("Do you want to choose another currency? \n 1.Yes \n 2.No \n"))
            while end_loop not in [1, 2]:
                end_loop = int(input("Choose a correct decision \n 1.Yes \n 2.No \n"))

            if end_loop == 2:
                start_program = False

        except ValueError:
            print("Please enter a valid number.")

    return selected_data


# These functions (get_currency_value and exchange_currency_to_usd) collaborate to fetch currency exchange
# rates from specified  URLs and convert them do US dollars, returning a list of converted rates
def get_currency_value(array_list):
    eur_value = []
    chf_value = []
    usd_value = []

    for x in array_list:
        try:
            res = requests.get(x)
            res.raise_for_status()
            data = res.json()

            if data["code"] == "EUR":
                for rate in data['rates']:
                    mid_rate = round(rate['mid'], 2)
                    eur_value.append(mid_rate)

            elif data["code"] == "CHF":
                for rate in data['rates']:
                    mid_rate = round(rate['mid'], 2)
                    chf_value.append(mid_rate)

            else:
                for rate in data['rates']:
                    mid_rate = round(rate['mid'], 2)
                    usd_value.append(mid_rate)

        except requests.RequestException as e:
            print(f"Error fetching data: {e}")

    output = exchange_currency_to_usd(usd_value, eur_value, chf_value)
    return output


def exchange_currency_to_usd(usd_currency, eur_currency, chf_currency):
    eur_currency_to_usd = []
    chf_currency_to_usd = []

    if len(usd_currency) == len(eur_currency) == len(chf_currency):
        for i in range(len(usd_currency)):
            try:
                eur = round(float(eur_currency[i] / usd_currency[i]), 2)
                chf = round(float(chf_currency[i] / usd_currency[i]), 2)
                eur_currency_to_usd.append(eur)
                chf_currency_to_usd.append(chf)
            except ZeroDivisionError as e:
                print(f"Error dividing by zero: {e}")

    return [eur_currency_to_usd, chf_currency_to_usd]


# Function processes selected currency data, saves it to a CSV file,
# and provides statistical measures for the specified currencies if selected.
def get_selected_currency_data(array_list):
    file_name = 'selected_currency_data.csv'
    try:
        set_headers_in_csv(file_name)
        calculated_rates = {}
        data_of_currency = get_currency_value(array_list)
        eur_usd_values = []
        chf_usd_values = []
        for i in range(len(data_of_currency[0])):
            calculated_rates = {
                "EUR => USD": data_of_currency[0][i],
                "CHF => USD": data_of_currency[1][i]
            }

        eur_usd_values.append(calculated_rates["EUR => USD"])
        chf_usd_values.append(calculated_rates["CHF => USD"])

        for x in array_list:
            res = requests.get(x)
            res.raise_for_status()
            data = res.json()

            for rate in data['rates']:
                day = rate['effectiveDate']
                mid_rate = round(rate['mid'], 2)

                for i in range(len(selected_data)):
                    if selected_data[i] == "EUR => USD":
                        currency_info = {
                            "EUR => USD": calculated_rates["EUR => USD"],
                        }
                        save_selected_data_to_csv(file_name, currency_info)

                    if selected_data[i] == "CHF => USD":
                        currency_info = {
                            "CHF => USD": calculated_rates["CHF => USD"],
                        }
                        save_selected_data_to_csv(file_name, currency_info)

                    if selected_data[i] == "Exchange => PLN":
                        currency_info = {
                            "Code": data["code"],
                            "Date": day,
                            "Exchange => PLN": mid_rate,
                        }
                        save_selected_data_to_csv(file_name, currency_info)

        if "EUR => USD" in selected_data:
            eur_usd_average = average(eur_usd_values)
            median_value = np.median(eur_usd_values)
            min_value = min(eur_usd_values)
            max_value = max(eur_usd_values)
            print("{\n\tEUR => USD Average:", eur_usd_average,
                  "\n\tMedian:", median_value,
                  "\n\tMin:", min_value,
                  "\n\tMax:", max_value,
                  "\n}")

        if "CHF => USD" in selected_data:
            chf_usd_average = average(chf_usd_values)
            median_value = np.median(chf_usd_values)
            min_value = min(eur_usd_values)
            max_value = max(eur_usd_values)
            print("{\n\tCHF => USD Average:", chf_usd_average,
                  "\n\tMedian:", median_value,
                  "\n\tMin:", min_value,
                  "\n\tMax:", max_value,
                  "\n}")

    except Exception as e:
        print(f"An error occurred: {e}")


# Function is responsible for fetching currency exchange rate data, processing it,
# and persistently storing the relevant information in a CSV file
def get_all_currency_data(array_list):
    file_name = 'all_currency_data.csv'
    try:
        set_headers_in_csv(file_name)
        calculated_rates = {}
        data_of_currency = get_currency_value(array_list)

        for i in range(len(data_of_currency[0])):
            calculated_rates = {
                "EUR => USD": data_of_currency[0][i],
                "CHF => USD": data_of_currency[1][i]
            }

        for x in array_list:
            res = requests.get(x)
            res.raise_for_status()
            data = res.json()

            for rate in data['rates']:
                day = rate['effectiveDate']
                mid_rate = round(rate['mid'], 2)

                currency_info = {
                    "Code": data["code"],
                    "Date": day,
                    "Exchange => PLN": mid_rate,
                    "EUR => USD": calculated_rates["EUR => USD"],
                    "CHF => USD": calculated_rates["CHF => USD"]
                }

                save_all_to_csv(file_name, currency_info)

    except Exception as e:
        print(f"An error occurred: {e}")


# Clear all rows in CSV file
def clear_excel_rows(file_name):
    try:
        with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([])

    except Exception as e:
        print(f"An error occurred: {e}")


# Set headers in CSV file
def set_headers_in_csv(filename: str):
    with open(filename, 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Code', "Date", 'Exchange => PLN', "EUR => USD",
                                                     "CHF => USD"])
        writer.writeheader()


# Saving all fetched data to the CSV  file by appending
def save_all_to_csv(file_name: str, data):
    try:
        with open(file_name, 'a', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['Code', 'Date', 'Exchange => PLN', 'EUR => USD',
                                                         'CHF => USD'])
            writer.writerow(data)

    except Exception as e:
        print(f"An error occurred while saving to CSV: {e}")


# Saving selected data by user in CSV  file
def save_selected_data_to_csv(file_name: str, data):
    try:
        with open(file_name, 'a', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['Code', 'Date', 'Exchange => PLN', 'EUR => USD',
                                                         'CHF => USD'])
            writer.writerow(data)

            keys_to_display = ['Exchange => PLN', 'EUR => USD', 'CHF => USD']
            keys_string = ', '.join([f"'{key}'" for key in keys_to_display if key in data])
            print(f"Data for {{{keys_string}}} has been saved!")

    except Exception as e:
        print(f"An error occurred while saving to CSV: {e}")
