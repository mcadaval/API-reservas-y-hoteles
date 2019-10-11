import requests

class FlightsReservationsAPIClient:

  def requestReservations(self):
    url = 'https://brubank-flights.herokuapp.com/flight-reservations'
    response = requests.get(url)
    return response