from datetime import datetime
from FlightsReservationsAPIClient import FlightsReservationsAPIClient

class FlightsReservationsManager:

  def __init__(self, mysqlConnection):
    self._connection = mysqlConnection
    self._cursor = self._connection.cursor()
    self._apiClient = FlightsReservationsAPIClient()
    self._flightsTableName = 'flights_reservations'
    self._reservations = []

  # def __del__(self):
  #   self._connection.close()

  def getReservationsForDestination(self, country, city = None):
    self._validateInputType(country, city)
    self.fetchReservationsFromSourceAndSaveLocally()
    reservations = self._fetchReservationsFromDB(country, city)
    return reservations

  def fetchReservationsFromSourceAndSaveLocally(self):
    self._requestReservations()
    self._saveReservationsInDatabase()

  def _fetchReservationsFromDB(self, country, city):
    query = "SELECT `reservation_id`, `date` FROM `" + self._flightsTableName + "` WHERE `country` = %s "
    
    if city != None:
      query +=  "AND `city` = %s "
      arguments = (country, city)
    else:
      arguments = (country,)

    query += "ORDER BY `date` DESC"

    result = self._cursor.execute(query, arguments)
    records = self._cursor.fetchall()
    reservations = []
    for row in records:
      reservations.append({'date' : row[1].strftime("%Y-%m-%dT%H:%M:%S"), 'reservationId' : row[0]})
    
    return reservations

  def _requestReservations(self):    
    response = self._apiClient.requestReservations()
    # to raise an HTTPError if the response is an http error
    response.raise_for_status()

    self._reservations = []
    responseJson = response.json()
    for reservation in responseJson:
      city, country = [x.strip() for x in reservation['destination'].split(',')]
      date = datetime.strptime(reservation['date'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')
      self._reservations.append((reservation['reservationId'], country, city, date))
  
  def _saveReservationsInDatabase(self):
    query = "INSERT INTO `" + self._flightsTableName + "` (`reservation_id`, `country`, `city`, `date`) VALUES (%s, %s, %s, %s)"
    self._cursor.executemany(query, self._reservations)
    self._connection.commit()

  def _validateInputType(self, country, city):
    if not isinstance(country, str):
      raise ValueError("Invalid value for 'country'. String is expected.")
    
    if not city is None and not isinstance(city, str):
      raise ValueError("Invalid value for 'city'. String is expected.")