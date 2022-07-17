import requests
import pandas as pd
import numpy as np 
from typing import Dict, List
from pprint import pprint as pp

headers= {
    "apikey": "YOUR API KEY"
    }

# URL takes in a string of each base currency
currencies = ['AUD','CAD','CHF','DKK','EUR','GBP','HKD','IDR','INR','JPY','MXN','SEK','SGD','THB','USD','VND']

# Fridays date has been used as the date to pull exchange rates from.
date = '2022-07-14'

# Class to pull and create objects for each currency (base rate) and its available pairs.
class ExchangeRatesApi:
    
    # Initialise the API with the api key (headers)
    def __init__(self, headers: Dict[str, str]):
        self.url = "https://api.apilayer.com/exchangerates_data/"
        self.headers = headers

    # Method to return an JSON api response for a base rate and its pairs
    def getRates(self, currencies: List[str], date: str) -> Dict[str, str]:
        self.currencies = currencies
        self.date = date
        url = self.url + f"{self.date}&base={self.currencies}"        
        
        # Catch general error if the api isnt working. 
        try:
            response = requests.request("GET", url, headers=self.headers)
            result = response.json()
        except requests.exceptions.RequestException as err:
            print ("Failed to fetch any data from exchangeratesapi.io",err)
        
        return result

    # JSON response needs to be converted to an array so that it can be manipulated
    def convertToArray(self, json_response: Dict[str, str]) -> List[pd.DataFrame]:
        base_rate = []
        pairs = []
        for i, j in json_response['rates'].items():
            pairs.append([i,j])
        base_rate.append(json_response['base'])
        base_rate.extend([base_rate[0]] * (len(pairs) - len(base_rate)))
        final_array = np.column_stack((base_rate, pairs))
        return final_array
    
    # Method to convert array to a Pandas DataFrame
    def convertToDataframe(self, array: List[pd.DataFrame]) -> pd.DataFrame:
        exchange_rates_df = pd.DataFrame(array)
        exchange_rates_df.columns=["currency_from", "currency_to", "exchange_rate"]
        return exchange_rates_df 

# Method to loop through currencies and create currency objects to be saved to a csv file. 
def extract_and_save_currency_rates(apiKey: Dict[str, str], currencies: List[str], date:str) -> pd.DataFrame:
    currency_data = []
    for currency in currencies:  
        exchange_rate_obj = ExchangeRatesApi(headers=apiKey)
        json_result = exchange_rate_obj.getRates(currency, date)
        currency_array = exchange_rate_obj.convertToArray(json_result)
        currency_df = exchange_rate_obj.convertToDataframe(currency_array)
        currency_data.append(currency_df)
    all_currencies = pd.concat(currency_data)
    all_currencies.to_csv('2022-07-14.csv', index=False)
    return all_currencies 
   

extract_and_save_currency_rates(apiKey=headers, currencies=currencies, date=date)
