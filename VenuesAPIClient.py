import requests
from datetime import datetime

class VenuesAPIClient:

  def requestHotelsNear(self, destination, clientId, clientSecret):
    url = "https://api.foursquare.com/v2/venues/search?near=" + destination + "&intent=browse&query=hotel&client_id=" + clientId + "&client_secret=" + clientSecret + "&v=" + datetime.now().strftime("%Y%m%d")
    response = requests.get(url)
    return response