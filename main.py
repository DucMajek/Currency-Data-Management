import logging
from datetime import date, timedelta, datetime
from services import *
import time
import schedule

logging.basicConfig(filename='currency_data.log', level=logging.INFO)


# Function updating the CSV file at 12 PM
def run_at_12_pm():
    current_time = datetime.now().time()

    if current_time.hour == 24 and current_time.minute == 00:
        clear_excel_rows("all_currency_data.csv")
        get_all_currency_data(all_data)
        logging.info("Data updated at 12:00 PM")


endDate = date.today()
startDate = endDate - timedelta(days=60)

usd = f'https://api.nbp.pl/api/exchangerates/rates/a/usd/{startDate}/{endDate}'
eur = f"https://api.nbp.pl/api/exchangerates/rates/a/eur/{startDate}/{endDate}"
chf = f"https://api.nbp.pl/api/exchangerates/rates/a/chf/{startDate}/{endDate}"

all_data = [usd, eur, chf]

start()
get_all_currency_data(all_data)
get_selected_currency_data(all_data)


# Script running every day at 12 PM and automatically save the data to the CSV file
scheduled_task = schedule.every().day.at("12:00").do(run_at_12_pm)

try:
    while not scheduled_task.last_run:
        schedule.run_pending()
        time.sleep(1)

    logging.info("Program terminated after scheduled task.")

except KeyboardInterrupt:
    logging.info("Program stopped by the user.")
