import requests
import pandas as pd
import numpy as np 
from typing import Dict, List

headers= {
    "apikey": "uwb8nVVW2CIzC5kpogNNQ7L6859oo3BB"
    }

# URL takes in a string of each base currency
CURRENCIES = ['AUD','CAD','CHF','DKK','EUR','GBP','HKD','IDR','INR','JPY','MXN','SEK','SGD','THB','USD','VND']

# Fridays date has been used as the date to pull exchange rates from.
DATE = '2022-07-14'

# Class to pull and create objects for each currency (base rate) and its available pairs.
class ExchangeRatesApi:
    
    # Initialise the API with the api key (headers)
    def __init__(self, headers: Dict[str, str]):
        self.url = "https://api.apilayer.com/exchangerates_data/"
        self.headers = headers

    # Method to return an JSON api response for a base rate and its pairs
    def api_call(self, currency: str, date: str) -> Dict[str, str]:
        url = self.url + f"{date}&base={currency}"        
        
        # Catch general error if the api isnt working. 
        try:
            response = requests.request("GET", url, headers=self.headers)
            result = response.json()
        except requests.exceptions.RequestException as err:
            print ("Failed to fetch any data from exchangeratesapi.io",err)
        
        return result

    # JSON response needs to be converted to an array so that it can be manipulated
    def convert_json_to_dataframe(self, json_response: Dict[str, str]) -> pd.DataFrame:
        base_rate = []
        pairs = []
        for i, j in json_response['rates'].items():
            pairs.append([i,j])
        base_rate.append(json_response['base'])
        base_rate.extend([base_rate[0]] * (len(pairs) - len(base_rate)))
        final_array = np.column_stack((base_rate, pairs))

        # Convert array to a Pnadas DataFrame 
        exchange_rates_df = pd.DataFrame(final_array)
        exchange_rates_df.columns=["currency_from", "currency_to", "exchange_rate"]
        return exchange_rates_df 

    # Add all currency pairs to one DataFrame and convert to csv
    def get_rates_and_convert_to_CSV(self, currencies: List[str], date: str) -> pd.DataFrame:
        currency_data = []
        for currency in currencies:  
            json_result = self.api_call(currency, date)
            currency_df = self.convert_json_to_dataframe(json_response=json_result)
            currency_data.append(currency_df)
        all_currencies = pd.concat(currency_data)
        all_currencies.to_csv('2022-07-14.csv', index=False)
        return all_currencies 

def extract_and_save_currency_rates(apiKey: Dict[str, str], currencies: List[str], date:str) -> pd.DataFrame:
    exchange_rate_obj = ExchangeRatesApi(headers=apiKey)
    exchange_rate_obj.get_rates_and_convert_to_CSV(currencies=currencies, date=date)

if __name__ == '__main__':
    extract_and_save_currency_rates(apiKey=headers, currencies=CURRENCIES, date=DATE)
