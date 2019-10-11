import os
import sys
sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)) + '/../')
sys.path.insert(2, os.path.dirname(os.path.abspath(__file__)) + '/../models/')
import unittest
import mysql.connector
import api
from unittest.mock import patch
from utils import setUpDatabase, dropDatabase, truncateTable, setUpMockResponse
from cfg import testingConfig
from FlightsReservationsAPIClient import FlightsReservationsAPIClient
from VenuesAPIClient import VenuesAPIClient

class TestApi(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    connection = mysql.connector.connect(
      host = testingConfig.mysqlArguments['host'],
      user = testingConfig.mysqlArguments['user'],
      passwd = testingConfig.mysqlArguments['passwd']
    )
    setUpDatabase(connection, testingConfig.mysqlArguments['database'])
    connection.close()

  @classmethod
  def tearDownClass(cls):
    connection = mysql.connector.connect(
      host = testingConfig.mysqlArguments['host'],
      user = testingConfig.mysqlArguments['user'],
      passwd = testingConfig.mysqlArguments['passwd']
    )
    dropDatabase(connection, testingConfig.mysqlArguments['database'])
    connection.close()

  def setUp(self):
    self.auxFilesDirectory = os.path.dirname(os.path.abspath(__file__)) + '/auxFiles/'
    app = api.createApp(testingConfig)
    self.api = app.test_client()
    self.api.testing = True
  
  def tearDown(self):
    truncateTable(testingConfig.getDatabaseConnection(), 'flights_reservations')
	
  """
  Test for api request with country and city.
  In this case both mock api responses are successfull and with data. Checks if the api response is the expected one.
  """
  @patch.object(FlightsReservationsAPIClient, 'requestReservations')
  @patch.object(VenuesAPIClient, 'requestHotelsNear')
  def testApiWorksCorrectlyWithCountryAndCityAsArguments(self, mockVenuesAPIResponse, mockReservationsAPIResponse):
    setUpMockResponse(mockReservationsAPIResponse, 200, self.auxFilesDirectory + 'responseMultipleReservations.json')
    setUpMockResponse(mockVenuesAPIResponse, 200, self.auxFilesDirectory + 'responseMultipleHotelsBuenosAires.json')
    expectedStatusCode = 200
    expectedResponse = {
      'hotels' : [
        {"name": "Sheraton Buenos Aires Hotel & Convention Center", "address": "San Martín 1225/1275 (esq. Av. Leandro N. Alem), 1104 Buenos Aires, Buenos Aires F.D., Argentina"},
        {"name": "Four Seasons Hotel Buenos Aires", "address": "Posadas 1086/88 (esq. Cerrito), C1011ABB Buenos Aires, Buenos Aires F.D., Argentina"},
        {"name": "Hotel Madero", "address": "Rosario Vera Peñaloza 360 (e/ Olga Cossettini y Juana Manso), C1107CLA Buenos Aires, Buenos Aires F.D., Argentina"}
      ],
      'reservations' : [
        {"date": "2020-01-11T18:24:01", "reservationId": "a044ec7d-d1f1-4098-8b76-d892e48b0321"}, 
        {"date": "2019-11-01T14:51:16", "reservationId": "e169ba40-8601-4193-a79e-0e2b1fce1f6f"},
        {"date": "2019-10-28T05:16:10", "reservationId": "963adb3a-1cdd-42ac-978a-9e495ab564e7"}
      ]
    }
    response = self.api.get('/recomendationSystem/Argentina/Buenos Aires/')

    self.assertEqual(response.status_code, expectedStatusCode)
    self.assertEqual(response.json, expectedResponse)

  """
  Test for api request only with country.
  In this case both mock api responses are successfull and with data. Checks if the api response is the expected one.
  """
  @patch.object(FlightsReservationsAPIClient, 'requestReservations')
  @patch.object(VenuesAPIClient, 'requestHotelsNear')
  def testApiWorksCorrectlyOnlyWithCountryAsArgument(self, mockVenuesAPIResponse, mockReservationsAPIResponse):
    setUpMockResponse(mockReservationsAPIResponse, 200, self.auxFilesDirectory + 'responseMultipleReservations.json')
    setUpMockResponse(mockVenuesAPIResponse, 200, self.auxFilesDirectory + 'responseMultipleHotelsArgentina.json')
    expectedStatusCode = 200
    expectedResponse = {
      'hotels' : [
        {"address": "San Martín 1225/1275 (esq. Av. Leandro N. Alem), 1104 Buenos Aires, Buenos Aires F.D., Argentina", "name": "Sheraton Buenos Aires Hotel & Convention Center"},
        {"address": "Mendoza 970 (e/ Junin y Hipólito Yrigoyen), W3400CCL Corrientes, Corrientes, Argentina", "name": "Gran Hotel Guaraní"},
        {"address": "Posadas 1086/88 (esq. Cerrito), C1011ABB Buenos Aires, Buenos Aires F.D., Argentina", "name": "Four Seasons Hotel Buenos Aires"},
        {"address": "Rosario Vera Peñaloza 360 (e/ Olga Cossettini y Juana Manso), C1107CLA Buenos Aires, Buenos Aires F.D., Argentina", "name": "Hotel Madero"},
        {"address": "Av. Belgrano 1041, 5500 Mendoza, Mendoza, Argentina", "name": "Diplomatic Hotel"}
      ],
      'reservations' : [
        {"date": "2020-01-12T19:15:39", "reservationId": "0a949eed-b861-48a3-9c54-4d8599858e75"},
        {"date": "2020-01-11T18:24:01", "reservationId": "a044ec7d-d1f1-4098-8b76-d892e48b0321"},
        {"date": "2019-11-11T08:11:26", "reservationId": "595d932f-586f-43fa-8fdb-2c2ec6175768"},
        {"date": "2019-11-01T14:51:16", "reservationId": "e169ba40-8601-4193-a79e-0e2b1fce1f6f"},
        {"date": "2019-10-28T05:16:10", "reservationId": "963adb3a-1cdd-42ac-978a-9e495ab564e7"}
      ]
    }
    response = self.api.get('/recomendationSystem/Argentina/')

    self.assertEqual(response.status_code, expectedStatusCode)
    self.assertDictEqual(response.json, expectedResponse)

  """
  Test for api request with country and city.
  In this case the reservations api response is a 400 status. Checks if the api response is the expected one.
  """
  @patch.object(FlightsReservationsAPIClient, 'requestReservations')
  def testApiRespondsWith400StatusWhenValueErrorIsDetected(self, mockReservationsAPIResponse):
    setUpMockResponse(mockReservationsAPIResponse, 400, None, ValueError)
    expectedStatusCode = 400
    response = self.api.get('/recomendationSystem/invalidCountry/Buenos Aires/')

    self.assertEqual(response.status_code, expectedStatusCode)

  """
  Test for api request with country and city.
  In this case the reservations api response is a 500 error status. Checks if the api response is the expected one.
  """
  @patch.object(FlightsReservationsAPIClient, 'requestReservations')
  def testApiRespondsWith500StatusWhenOtherErrorIsDetected(self, mockReservationsAPIResponse):
    setUpMockResponse(mockReservationsAPIResponse, 500, None, Exception)
    expectedStatusCode = 500
    response = self.api.get('/recomendationSystem/Argentina/')

    self.assertEqual(response.status_code, expectedStatusCode)

if __name__ == '__main__':
  unittest.main()