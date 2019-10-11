import os
import sys
sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)) + '/../')
sys.path.insert(2, os.path.dirname(os.path.abspath(__file__)) + '/../models/')
import unittest
import mysql.connector
from unittest.mock import patch
from FlightsReservationsManager import FlightsReservationsManager
from FlightsReservationsAPIClient import FlightsReservationsAPIClient
from utils import setUpDatabase, dropDatabase, truncateTable, setUpMockResponse, setUpDatabaseContent
from cfg import testingConfig

class TestFlightsReservationsManager(unittest.TestCase):

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
    self.connection = testingConfig.getDatabaseConnection();
    self.cursor = self.connection.cursor()
    self.reservationsManager = FlightsReservationsManager(self.connection)
  
  def tearDown(self):
    truncateTable(self.connection, 'flights_reservations')
	
  """
  Test for fetchReservationsFromSourceAndSaveLocally method.
  In this case the mock api response is empty. Checks if no new records have been stored in 
  the database table.
  """
  @patch.object(FlightsReservationsAPIClient, 'requestReservations')
  def testFetchReservationsFromSourceAndSaveLocallyStoresNothingIfResponseIsEmpty(self, mockResponse):
    setUpMockResponse(mockResponse, 200, self.auxFilesDirectory + 'responseEmptyReservations.json')
    expectedNumberOfStoredReservations = 0
    self.reservationsManager.fetchReservationsFromSourceAndSaveLocally()
    result = self.cursor.execute("SELECT * FROM `flights_reservations`")
    records = self.cursor.fetchall()
    numberOfStoredReservations = self.cursor.rowcount

    self.assertEqual(numberOfStoredReservations, expectedNumberOfStoredReservations)
  
  """
  Test for fetchReservationsFromSourceAndSaveLocally method.
  In this case the mock api response is not empty. Checks if all the new records have been stored in 
  the database table.
  """
  @patch.object(FlightsReservationsAPIClient, 'requestReservations')
  def testFetchReservationsFromSourceAndSaveLocallyStoresAllReservations(self, mockResponse):
    setUpMockResponse(mockResponse, 200, self.auxFilesDirectory + 'responseMultipleReservations.json')
    expectedNumberOfStoredReservations = 23
    self.reservationsManager.fetchReservationsFromSourceAndSaveLocally()
    result = self.cursor.execute("SELECT * FROM `flights_reservations`")
    records = self.cursor.fetchall()
    numberOfStoredReservations = self.cursor.rowcount

    self.assertEqual(numberOfStoredReservations, expectedNumberOfStoredReservations)

  """
  Test for fetchReservationsFromSourceAndSaveLocally method.
  In this case the mock api response is a single reservation. Checks if the reservation data is stored
  correctly in the database table.
  """
  @patch.object(FlightsReservationsAPIClient, 'requestReservations')
  def testFetchReservationsFromSourceAndSaveLocallyStoresReservationDataCorrectly(self, mockResponse):
    setUpMockResponse(mockResponse, 200, self.auxFilesDirectory + 'responseSingleReservation.json')
    expectedStoredReservation = ('dda0fbff-65e3-43a8-bae8-18acb2ee09ee', 'China', 'Hong Kong', '2019-11-15 16:58:28')
    self.reservationsManager.fetchReservationsFromSourceAndSaveLocally()
    result = self.cursor.execute("SELECT `reservation_id`, `country`, `city`, `date` FROM `flights_reservations` WHERE `reservation_id` = %s", ('dda0fbff-65e3-43a8-bae8-18acb2ee09ee',))
    record = self.cursor.fetchone()
    storedReservation = (record[0], record[1], record[2], record[3].strftime('%Y-%m-%d %H:%M:%S'))

    self.assertEqual(storedReservation, expectedStoredReservation)

  """
  Test for getReservationsForDestination method.
  In this case the given destination includes country and city, and it does not match with any stored reservation.
  Checks if the returned list is empty.
  """
  @patch.object(FlightsReservationsAPIClient, 'requestReservations')
  def testGetReservationsForCountryAndCityDestinationWithoutReservationsReturnsAnEmptyList(self, mockResponse):
    setUpDatabaseContent(self.connection, self.auxFilesDirectory + 'flights_reservations.sql')
    setUpMockResponse(mockResponse, 200, self.auxFilesDirectory + 'responseMultipleReservations.json')
    expectedReservations = []
    reservations = self.reservationsManager.getReservationsForDestination('France', 'Paris')
  
    self.assertEqual(reservations, expectedReservations)
  
  """
  Test for getReservationsForDestination method.
  In this case the given destination includes country and city, and it matches with some of the stored reservations.
  Checks if the returned list includes them and in descending order by date.
  """
  @patch.object(FlightsReservationsAPIClient, 'requestReservations')
  def testGetReservationsForCountryAndCityDestinationWithSomeReservationsReturnsAListWithThem(self, mockResponse):
    setUpDatabaseContent(self.connection, self.auxFilesDirectory + 'flights_reservations.sql')
    setUpMockResponse(mockResponse, 200, self.auxFilesDirectory + 'responseMultipleReservations.json')
    expectedReservations = [
      {"date": "2020-01-11T18:24:01", "reservationId": "a044ec7d-d1f1-4098-8b76-d892e48b0321"}, 
      {"date": "2019-11-01T14:51:16", "reservationId": "e169ba40-8601-4193-a79e-0e2b1fce1f6f"},
      {"date": "2019-10-28T05:16:10", "reservationId": "963adb3a-1cdd-42ac-978a-9e495ab564e7"}
    ]
    reservations = self.reservationsManager.getReservationsForDestination('Argentina', 'Buenos Aires')
    
    self.assertEqual(reservations, expectedReservations)

  """
  Test for getReservationsForDestination method.
  In this case the given destination includes only the country, and it does not match with any stored reservation.
  Checks if the returned list is empty.
  """
  @patch.object(FlightsReservationsAPIClient, 'requestReservations')
  def testGetReservationsForCountryDestinationWithoutReservationsReturnsAnEmptyList(self, mockResponse):
    setUpDatabaseContent(self.connection, self.auxFilesDirectory + 'flights_reservations.sql')
    setUpMockResponse(mockResponse, 200, self.auxFilesDirectory + 'responseMultipleReservations.json')
    expectedReservations = []
    reservations = self.reservationsManager.getReservationsForDestination('France')
    
    self.assertEqual(reservations, expectedReservations)
  
  """
  Test for getReservationsForDestination method.
  In this case the given destination includes only the country, and it matches with some of the stored reservations.
  Checks if the returned list includes them and in descending order by date.
  """
  @patch.object(FlightsReservationsAPIClient, 'requestReservations')
  def testGetReservationsForCountryDestinationWithSomeReservationsReturnsAListWithThem(self, mockResponse):
    setUpDatabaseContent(self.connection, self.auxFilesDirectory + 'flights_reservations.sql')
    setUpMockResponse(mockResponse, 200, self.auxFilesDirectory + 'responseMultipleReservations.json')
    expectedReservations = [
      {"date": "2020-01-12T19:15:39", "reservationId": "0a949eed-b861-48a3-9c54-4d8599858e75"},
      {"date": "2020-01-11T18:24:01", "reservationId": "a044ec7d-d1f1-4098-8b76-d892e48b0321"},
      {"date": "2019-12-16T11:45:38", "reservationId": "1a27702a-1183-483f-87d9-34e88432efae"},
      {"date": "2019-11-21T22:16:55", "reservationId": "370ad35e-5ab6-4925-8e42-ae8eef4dc73c"},
      {"date": "2019-11-11T08:11:26", "reservationId": "595d932f-586f-43fa-8fdb-2c2ec6175768"},
      {"date": "2019-11-01T14:51:16", "reservationId": "e169ba40-8601-4193-a79e-0e2b1fce1f6f"},
      {"date": "2019-10-28T05:16:10", "reservationId": "963adb3a-1cdd-42ac-978a-9e495ab564e7"}
    ]
    reservations = self.reservationsManager.getReservationsForDestination('Argentina')
    
    self.assertEqual(reservations, expectedReservations)

  """
  Test for getReservationsForDestination method.
  In this case the given destination includes a country with an invalid type. Checks if ValueError is thrown, 
  since a string is the expected type for the country.
  """
  def testGetReservationsForDestinationWithNonStringCountryRaisesValueError(self):
    self.assertRaises(ValueError, self.reservationsManager.getReservationsForDestination, 123, "Buenos Aires")

  """
  Test for getReservationsForDestination method.
  In this case the given destination includes a city with an invalid type. Checks if ValueError is thrown, 
  since a string is the expected type for the city.
  """
  def testGetReservationsForDestinationWithNonStringCityRaisesValueError(self):
    self.assertRaises(ValueError, self.reservationsManager.getReservationsForDestination, "Argentina", 123)

if __name__ == '__main__':
  unittest.main()