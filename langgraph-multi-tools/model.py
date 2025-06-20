from pydantic import BaseModel, Field


class WeatherModel(BaseModel):
    city: str = Field(description='Name of the city')
    
    
class WeatherForecastModel(WeatherModel):
    days: int = Field(description='Number of days from current date till which the forecast is required', default=1)
    
    
class HotelModel(BaseModel):
    city: str = Field(description='City or hotel name to be searched')
    check_in: str = Field(description='Date for checking in to the hotel, should be in the format YYYY-MM-DD')
    check_out: str = Field(description='Date for checking out from the hotel, should be in the format YYYY-MM-DD')
    num_of_adults: int = Field(description='Number of adults on the trip')
    currency: str = Field(description='Currency in which the guests would pay, this would be the currency code')
    budget: int = Field(description='Total budget for the hotels', default=0)
    
    
class CurrencyConverterModel(BaseModel):
    base_currency: str = Field(description='Base currency from which the conversions are required')
    currency: str = Field(description='Currency to which the base currency is to be converted')
