from flask import Flask, jsonify, abort, current_app
from apscheduler.schedulers.background import BackgroundScheduler
from FlightsReservationsManager import FlightsReservationsManager
from HotelsManager import HotelsManager
from requests import exceptions
from cfg import productionConfig

def createApp(config):
  app = Flask(__name__)
  app.config['JSON_AS_ASCII'] = False
  connection = config.getDatabaseConnection()
  
  @app.route('/recomendationSystem/<string:country>/')
  @app.route('/recomendationSystem/<string:country>/<string:city>/')
  def main(country, city = None):
    try:
      flightsManager = FlightsReservationsManager(connection)
      reservations = flightsManager.getReservationsForDestination(country, city)
      hotelsManager = HotelsManager(config.clientId, config.clientSecret)
      hotels = hotelsManager.getHotelsInDestination(country, city)
      return jsonify(reservations = reservations, hotels = hotels)
    
    except exceptions.HTTPError as e:
      # use status code returned by the consumed apis, when is an error status
      print(repr(e))
      abort(e.response.status_code)
    except ValueError as e:
      # status code 400 when is an input error
      print(repr(e))
      abort(400)
    except Exception as e:
      # status code 500 when other exception is thrown
      print(repr(e))
      abort(500)
  
  return app

def backgroundJob(connection):
  try:
    print("Running background job")
    flightsManager = FlightsReservationsManager(connection)
    flightsManager.fetchReservationsFromSourceAndSaveLocally()
  
  except Exception as e:
    print(repr(e))

def setUpBackgroundJob(config):
  scheduler = BackgroundScheduler()
  scheduler.add_job(backgroundJob, 'interval', seconds = config.backgroundJobInterval, args = (config.getDatabaseConnection(),))
  scheduler.start()

def initializeApp(app, config):
  if config.backgroundJobActivated:
    setUpBackgroundJob(config)
  app.run(debug = config.debug, use_reloader = False)

if __name__ == '__main__':
  app = createApp(productionConfig)
  initializeApp(app, productionConfig)