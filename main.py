from datetime import date, timedelta
from services import *

endDate = date.today()
startDate = endDate - timedelta(days=60)

usd = f'https://api.nbp.pl/api/exchangerates/rates/a/usd/{startDate}/{endDate}'
eur = f"https://api.nbp.pl/api/exchangerates/rates/a/eur/{startDate}/{endDate}"
chf = f"https://api.nbp.pl/api/exchangerates/rates/a/chf/{startDate}/{endDate}"


all_data = [usd, eur, chf]


#get_all_currency_data(all_data)

#get_currency_value(all_data)
interface()
