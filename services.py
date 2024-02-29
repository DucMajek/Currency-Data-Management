import csv
import requests

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

    test = exchange_currenct_to_usd(usd_value, eur_value, chf_value)
    return test

def exchange_currenct_to_usd(usd_currency, eur_currency, chf_currency):
    eur_currency_to_usd = []
    chf_currency_to_usd = []

    if len(usd_currency) == len(eur_currency) == len(chf_currency):
        for i in range(len(usd_currency)):
            eur = round(float(eur_currency[i] / usd_currency[i]), 2)
            chf = round(float(chf_currency[i] / usd_currency[i]), 2)
            eur_currency_to_usd.append(eur)
            chf_currency_to_usd.append(chf)

    return [eur_currency_to_usd, chf_currency_to_usd]


def get_all_currency_data(array_list):
    file_name = 'all_currency_data.csv'
    set_headers_in_csv(file_name)
    calculated_rates = {}
    test2 = get_currency_value(array_list)

    for i in range(len(test2[0])):
        calculated_rates = {
            "EUR=>USD": test2[0][i],
            "CHF=>USD": test2[1][i]
        }

    for x in array_list:
        res = requests.get(x)
        data = res.json()

        for rate in data['rates']:
            day = rate['effectiveDate']
            mid_rate = round(rate['mid'], 2)

            currency_info = {
                "Table": data["table"],
                "Currency": data["currency"],
                "Code": data["code"],
                "Date": day,
                "Exchange to PLN": mid_rate,
                "EUR=>USD": calculated_rates["EUR=>USD"],
                "CHF=>USD": calculated_rates["CHF=>USD"]
            }

            save_to_csv_file(file_name, currency_info)

def set_headers_in_csv(filename: str):
    with open(filename, 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Table', 'Currency', 'Code', "Date", 'Exchange to PLN', "EUR=>USD",
                                                     "CHF=>USD"])
        writer.writeheader()


def save_to_csv_file(file_name: str, data):
    with open(file_name, 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Table', 'Currency', 'Code', 'Date', 'Exchange to PLN', 'EUR=>USD',
                                                     'CHF=>USD'])
        writer.writerow(data)

