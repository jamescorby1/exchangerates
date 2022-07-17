import requests 
from datetime import datetime
from exchangerate import headers, ExchangeRatesApi



"""
This file contains some small unit tests for the API. Pytest's unit test framework has been used. 

"""

def test_get_available_GBP_pairs_for_today():
    date = datetime.today().strftime('%Y-%m-%d')
    url = (f"https://api.apilayer.com/exchangerates_data/{date}&base=GBP")
    response = requests.request("GET", url, headers=headers)
    result = response.json()


    assert len(result['base']) == 1
    assert result['base'] == 'GBP'
    assert response.status_code == 200

def test_get_rates_method():
    currency = 'GBP'
    date = datetime.today().strftime('%Y-%m-%d')
    er = ExchangeRatesApi(headers=headers)
    response = er.getRates(currencies=[currency], date=date)

    assert len(response['base'] == 1)
    assert response.status_code == 200


