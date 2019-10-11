import os
import sys
sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)) + '/../')
sys.path.insert(2, os.path.dirname(os.path.abspath(__file__)) + '/../models/')
import unittest
from unittest.mock import patch
from HotelsManager import HotelsManager
from VenuesAPIClient import VenuesAPIClient
from cfg import testingConfig
from utils import setUpMockResponse
from requests import exceptions

class TestHotelsManager(unittest.TestCase):

  def setUp(self):
    self.auxFilesDirectory = os.path.dirname(os.path.abspath(__file__)) + '/auxFiles/'
    self.hotelsManager = HotelsManager(testingConfig.clientId, testingConfig.clientSecret)
  	
  """
  Test for getHotelsInDestination method.
  In this case the given destination includes country and city, and no hotels are found.
  Checks if the returned list is empty.
  """
  @patch.object(VenuesAPIClient, 'requestHotelsNear')
  def testGetHotelsInCountryAndCityDestinationWithoutHotelsReturnsAnEmptyList(self, mockResponse):
    setUpMockResponse(mockResponse, 200, self.auxFilesDirectory + 'responseEmptyHotels.json')
    expectedHotels = []
    hotels = self.hotelsManager.getHotelsInDestination('France', 'Paris')
    
    self.assertEqual(hotels, expectedHotels)
  
  """
  Test for getHotelsInDestination method.
  In this case the given destination includes country and city, and some hotels are found.
  Checks if the returned list includes those hotels.
  """
  @patch.object(VenuesAPIClient, 'requestHotelsNear')
  def testGetHotelsInCountryAndCityDestinationWithSomeHotelsReturnsAListThatIncludesThem(self, mockResponse):
    setUpMockResponse(mockResponse, 200, self.auxFilesDirectory + 'responseMultipleHotelsBuenosAires.json')
    expectedHotels = [
      {"name": "Sheraton Buenos Aires Hotel & Convention Center", "address": "San Martín 1225/1275 (esq. Av. Leandro N. Alem), 1104 Buenos Aires, Buenos Aires F.D., Argentina"},
      {"name": "Four Seasons Hotel Buenos Aires", "address": "Posadas 1086/88 (esq. Cerrito), C1011ABB Buenos Aires, Buenos Aires F.D., Argentina"},
      {"name": "Hotel Madero", "address": "Rosario Vera Peñaloza 360 (e/ Olga Cossettini y Juana Manso), C1107CLA Buenos Aires, Buenos Aires F.D., Argentina"}
    ]
    hotels = self.hotelsManager.getHotelsInDestination('Argentina', 'Buenos Aires')
    
    self.assertEqual(hotels, expectedHotels)

  """
  Test for getHotelsInDestination method.
  In this case the given destination includes only the country, and no hotels are found.
  Checks if the returned list is empty.
  """
  @patch.object(VenuesAPIClient, 'requestHotelsNear')
  def testGetHotelsInCountryDestinationWithoutHotelsReturnsAnEmptyList(self, mockResponse):
    setUpMockResponse(mockResponse, 200, self.auxFilesDirectory + 'responseEmptyHotels.json')
    expectedHotels = []
    hotels = self.hotelsManager.getHotelsInDestination('France')
    
    self.assertEqual(hotels, expectedHotels)
  
  """
  Test for getHotelsInDestination method.
  In this case the given destination includes only the country, and some hotels are found.
  Checks if the returned list includes those hotels.
  """
  @patch.object(VenuesAPIClient, 'requestHotelsNear')
  def testGetHotelsInCountryDestinationWithSomeHotelsReturnsAListWithThem(self, mockResponse):
    setUpMockResponse(mockResponse, 200, self.auxFilesDirectory + 'responseMultipleHotelsArgentina.json')
    expectedHotels = [
      {"name": "Sheraton Buenos Aires Hotel & Convention Center", "address": "San Martín 1225/1275 (esq. Av. Leandro N. Alem), 1104 Buenos Aires, Buenos Aires F.D., Argentina"},
      {"name": "Gran Hotel Guaraní", "address": "Mendoza 970 (e/ Junin y Hipólito Yrigoyen), W3400CCL Corrientes, Corrientes, Argentina"},
      {"name": "Four Seasons Hotel Buenos Aires", "address": "Posadas 1086/88 (esq. Cerrito), C1011ABB Buenos Aires, Buenos Aires F.D., Argentina"},
      {"name": "Hotel Madero", "address": "Rosario Vera Peñaloza 360 (e/ Olga Cossettini y Juana Manso), C1107CLA Buenos Aires, Buenos Aires F.D., Argentina"},
      {"name": "Diplomatic Hotel", "address": "Av. Belgrano 1041, 5500 Mendoza, Mendoza, Argentina"}
    ]
    hotels = self.hotelsManager.getHotelsInDestination('Argentina')
    
    self.assertEqual(hotels, expectedHotels)

  """
  Test for getHotelsInDestination method.
  In this case the given destination includes a country with an invalid type. Checks if ValueError is thrown,
  since a string is the expected type for the country.
  """
  def testGetHotelsInDestinationWithNonStringCountryRaisesValueError(self):
    self.assertRaises(ValueError, self.hotelsManager.getHotelsInDestination, 123, "Buenos Aires")

  """
  Test for getHotelsInDestination method.
  In this case the given destination includes a city with an invalid type. Checks if ValueError is thrown, 
  since a string is the expected type for the city.
  """
  def testGetHotelsInDestinationWithNonStringCityRaisesValueError(self):
    self.assertRaises(ValueError, self.hotelsManager.getHotelsInDestination, "Argentina", 123)

  """
  Test for getHotelsInDestination method.
  In this case the given destination includes an invalid country. Checks if ValueError is thrown, 
  since it is not geocodable.
  """
  @patch.object(VenuesAPIClient, 'requestHotelsNear')
  def testGetHotelsInCountryDestinationWithInvalidCountryRaisesValueError(self, mockResponse):
    setUpMockResponse(mockResponse, 200, self.auxFilesDirectory + 'responseInvalidInputHotels.json')
    
    self.assertRaises(ValueError, self.hotelsManager.getHotelsInDestination, "invalidCountry")
  
  """
  Test for getHotelsInDestination method.
  In this case the given destination includes an invalid city. Checks if ValueError is thrown, 
  since it is not geocodable.
  """
  @patch.object(VenuesAPIClient, 'requestHotelsNear')
  def testGetHotelsInCountryAndCityDestinationWithInvalidCityRaisesValueError(self, mockResponse):
    setUpMockResponse(mockResponse, 200, self.auxFilesDirectory + 'responseInvalidInputHotels.json')
    
    self.assertRaises(ValueError, self.hotelsManager.getHotelsInDestination, "Argentina", "invalidCity")

  """
  Test for getHotelsInDestination method.
  In this case the source api responds with an internal server error (500). Checks if HTTPError is thrown.
  """
  @patch.object(VenuesAPIClient, 'requestHotelsNear')
  def testGetHotelsInDestinationRaisesHTTPErrorWhenSourceDoesNotRespond(self, mockResponse):
    setUpMockResponse(mockResponse, 200, self.auxFilesDirectory + 'responseInternalServerErrorHotels.json')
    
    self.assertRaises(exceptions.HTTPError, self.hotelsManager.getHotelsInDestination, "Argentina", "Buenos Aires")

if __name__ == '__main__':
  unittest.main()