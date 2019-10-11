from requests import exceptions
from VenuesAPIClient import VenuesAPIClient

class HotelsManager:

  def __init__(self, clientId, clientSecret):
    self._clientId = clientId
    self._clientSecret = clientSecret
    self._apiClient = VenuesAPIClient()
    self._hotels = []

  def getHotelsInDestination(self, country, city = None):
    self._validateInputType(country, city)
    self._getHotelsFromSource(country, city)
    return self._hotels
  
  def _getHotelsFromSource(self, country, city):
    destination = country
    if not city is None:
      destination += ', ' + city

    response = self._apiClient.requestHotelsNear(destination, self._clientId, self._clientSecret)
    # to raise an HTTPError if the response is an http error
    response.raise_for_status()
    
    self._hotels = []
    responseJson = response.json()

    # destination existence validation provided by the consumed api
    if responseJson['meta']['code'] == 400:
      raise ValueError('Error')
    elif responseJson['meta']['code'] != 200:
      raise exceptions.HTTPError('Error')
      
    hotels = responseJson['response']['venues']
    for hotelData in hotels:
      self._hotels.append({'name' : hotelData['name'], 'address' : ', '.join(hotelData['location']['formattedAddress'])})
    
  def _validateInputType(self, country, city):
    if not isinstance(country, str):
      raise ValueError("Invalid value for 'country'. String is expected.")
    
    if not city is None and not isinstance(city, str):
      raise ValueError("Invalid value for 'city'. String is expected.")
