import requests  #install package requests
import json
from datetime import date, timedelta

def get_last_rate(arr_rates):
    size = len(arr_rates)
    return arr_rates[size]


endDate = date.today()
startDate = endDate - timedelta(days=60)
usd = f"http://api.nbp.pl/api/exchangerates/rates/a/usd/{startDate}/{endDate}"
eur = f"http://api.nbp.pl/api/exchangerates/rates/a/eur/{startDate}/{endDate}"
chf = f"http://api.nbp.pl/api/exchangerates/rates/a/chf/{startDate}/{endDate}"



res = requests.get(usd)
data = res.json()
response = json.loads(res.text)

for rate in data['rates']:
    mid_rate = round(rate['mid'], 2)

print(rate) # {'no': '041/A/NBP/2024', 'effectiveDate': '2024-02-27', 'mid': 3.9682}
print(response)
print(f"1 {response['code']} = {mid_rate}") # 1 USD = 3.97


res = requests.get(eur)
response = json.loads(res.text)
print(response)

res = requests.get(chf)
response = json.loads(res.text)
print(response)