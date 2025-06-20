import os
from pydantic import BaseModel
from typing import Type
from langchain.tools import BaseTool
import requests
from model import WeatherModel, WeatherForecastModel, HotelModel, CurrencyConverterModel

    
class WeatherTool(BaseTool):
    name: str = 'WeatherTool'
    description: str = 'Tool to search for current weather for a given city'
    args_schema: Type[BaseModel] = WeatherModel
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._key = os.getenv('WEATHER_API_KEY')
        if not self._key:
            raise ValueError('WEATHER_API_KEY environment variable is not set.')
    
    def _run(self, city: str) -> str:
        """
        Weather tool to search for current weather for a given city

        Args:
            city (str): Name of the city

        Returns:
            str: The current temperature in °C
        """
        try:
            city = city.split(',')[0] # sometimes model appends the country with the city
            response = requests.get(f'https://api.weatherapi.com/v1/current.json?key={self._key}&q={city}&aqi=yes').json()
            return f'The current weather in {city} is {response['current']['temp_c']}°C with {response['current']['condition']['text']}.'
        except Exception as e:
            raise RuntimeError(f'Failed to fetch weather for {city}: {e}')
    
    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not supported.")
    

class WeatherForecastTool(BaseTool):
    name: str = 'WeatherForecastTool'
    description: str = 'Tool to search for weather forecast for a given city'
    args_schema: Type[BaseModel] = WeatherForecastModel
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._key = os.getenv('WEATHER_API_KEY')
        if not self._key:
            raise ValueError('WEATHER_API_KEY environment variable is not set.')
    
    def _run(self, city: str, days: int) -> str:
        """
        Weather forecast tool to get the weather forecast for a given city

        Args:
            city (str): Name of the city
            days (int): Number of days from current date till which the forecast is required

        Returns:
            str: Forecast for the number of days for a given city
        """
        try:
            city = city.split(',')[0]
            response = requests.get(f'https://api.weatherapi.com/v1/forecast.json?key={self._key}&q={city}&days={days}&aqi=yes').json()
            forecast = response['forecast']['forecastday']
            res = []
            for fc in forecast:
                res.append(f'On: {fc['date']}, max temp: {fc['day']['maxtemp_c']}°C, min temp: {fc['day']['mintemp_c']}°C, condition: {fc['day']['condition']['text']}')
            return '. '.join(res)
        except Exception as e:
            raise RuntimeError(f'Failed to fetch forecast for {city}: {e}')
    
    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not supported.")
        

class HotelTool(BaseTool):
    name: str = 'HotelTool'
    description: str = 'Tool to respond with hotel recommendations for the given query'
    args_schema: Type[BaseModel] = HotelModel
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._key = os.getenv('SERP_API_KEY')
        if not self._key:
            raise ValueError('SERP_API_KEY environment variable is not set.')
    
    def _run(self, city: str, check_in: str, check_out: str, num_of_adults: int, currency: str, budget: int = 0) -> dict[str, any]:
        """
        Tool to search for hotels in the given city based on checkin and checkout dates, number of adults, the currency in which the amount is required, and the user's budget

        Args:
            city (str): Name of the city
            check_in (str): Checkin date
            check_out (str): Checkout date
            num_of_adults (int): Number of adults
            currency (str): Currency in the amount is to be returned
            budget (int, optional): User's budget. Defaults to 0.

        Returns:
            dict[str, any]: Return the hotels based on input queries
        """
        try:
            city = city.split(',')[0]
            response = requests.get(f'https://serpapi.com/search.json?engine=google_hotels&q={city}&check_in_date={check_in}&check_out_date={check_out}&adults={num_of_adults}&currency={currency}&gl=us&hl=en&api_key={self._key}').json()
            hotels = response['ads']
            if not hotels:
                return []
            if budget:
                res = []
                for hotel in hotels:
                    if hotel['extracted_price'] <= budget:
                        res.append(hotel)
            else:
                res = hotels
            return res
        except Exception as e:
            raise RuntimeError(f'Failed to fetch hotels for {city}: {e}')
    
    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not supported.")
    

class CurrencyConverterTool(BaseTool):
    name: str = 'CurrencyConverterTool'
    description: str = 'Tool to convert the currency'
    args_schema: Type[BaseModel] = CurrencyConverterModel
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._key = os.getenv('CURRENCY_API_KEY')
        if not self._key:
            raise ValueError('CURRENCY_API_KEY environment variable is not set.')
    
    def _run(self, base_currency: str, currency: str) -> float:
        """
        Convert the base currency to the given currency

        Args:
            base_currency (str): Currency code for base currency
            currency (str): Currency code for required currency

        Returns:
            float: The conversion rate
        """
        try:
            response = requests.get(f'https://api.freecurrencyapi.com/v1/latest?apikey={self._key}&currencies={currency}&base_currency={base_currency}').json()
            return response['data'][currency]
        except Exception as e:
            raise RuntimeError(f'Unable to fetch currency conversion rate: {e}')
    
    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not supported.")
