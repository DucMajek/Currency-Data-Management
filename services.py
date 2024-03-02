import csv
import requests

test = []

def check_the_value_is_exist_in_array(value: str, array):
    for element in array:
        if value == element:
            print("Data is already in use")
            return True

    test.append(value)

def menu(number: int):
    while number not in range(1, 6):
        number = int(input("Wrong number. Please choose again or the data you selected is already in use\n "
                           "1. Exchange => PLN \n 2. EUR => USD \n 3. CHF => USD \n"))
    if number == 1:
        check_the_value_is_exist_in_array("Exchange => PLN", test)
    elif number == 2:
        check_the_value_is_exist_in_array("EUR => USD", test)
    elif number == 3:
        check_the_value_is_exist_in_array("CHF => USD", test)

    print(test)

def interface():
    start = True
    while start:
        lang = int(input("Select the currency which you are interested \n "
                         "1. Exchange => PLN \n 2. EUR => USD \n 3. CHF => USD \n"))
        menu(lang)

        end_loop = int(input("Do you want choose another one currency? \n 1.Yes \n 2.No \n"))
        while end_loop not in [1, 2]:
            end_loop = int(input("Choose a correct decision \n 1.Yes \n 2.No \n"))

        if end_loop == 2:
            start = False

    return test


def get_currency_value(array_list):
    eur_value = []
    chf_value = []
    usd_value = []

    for x in array_list:
        res = requests.get(x)
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

    output = exchange_currency_to_usd(usd_value, eur_value, chf_value)
    return output


def exchange_currency_to_usd(usd_currency, eur_currency, chf_currency):
    eur_currency_to_usd = []
    chf_currency_to_usd = []

    if len(usd_currency) == len(eur_currency) == len(chf_currency):
        for i in range(len(usd_currency)):
            eur = round(float(eur_currency[i] / usd_currency[i]), 2)
            chf = round(float(chf_currency[i] / usd_currency[i]), 2)
            eur_currency_to_usd.append(eur)
            chf_currency_to_usd.append(chf)

    return [eur_currency_to_usd, chf_currency_to_usd]


def get_selected_currency_data(array_list, selected_data):
    file_name = 'selected_currency_data.csv'
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
        data = res.json()

        for rate in data['rates']:
            day = rate['effectiveDate']
            mid_rate = round(rate['mid'], 2)

            for i in range(len(selected_data)):
                if selected_data[i] == "EUR => USD":
                    currency_info = {
                        "EUR => USD": calculated_rates["EUR => USD"],
                    }
                    save_all_to_csv(file_name, currency_info)

                if selected_data[i] == "CHF => USD":
                    currency_info = {
                        "CHF => USD": calculated_rates["CHF => USD"],
                    }
                    save_all_to_csv(file_name, currency_info)

                if selected_data[i] == "Exchange => PLN":
                    currency_info = {
                        "Code": data["code"],
                        "Date": day,
                        "Exchange => PLN": mid_rate,
                    }
                    save_all_to_csv(file_name, currency_info)


def get_all_currency_data(array_list):
    file_name = 'all_currency_data.csv'
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



def set_headers_in_csv(filename: str):
    with open(filename, 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Code', "Date", 'Exchange => PLN', "EUR => USD",
                                                     "CHF => USD"])
        writer.writeheader()


def save_all_to_csv(file_name: str, data):
    with open(file_name, 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Code', 'Date', 'Exchange => PLN', 'EUR => USD',
                                                     'CHF => USD'])
        writer.writerow(data)
        #print(f"Data for {', '.join(data)} has been saved!")
