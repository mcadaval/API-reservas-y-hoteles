import os
import sys
sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)) + '/models/')
from flask import Flask, jsonify, abort
from apscheduler.schedulers.background import BackgroundScheduler
from FlightsReservationsManager import FlightsReservationsManager
from HotelsManager import HotelsManager
from requests import exceptions
from cfg import productionConfig
import logging

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
      if config.showErrorLogs:
        app.logger.error(repr(e))
      abort(e.response.status_code)
    except ValueError as e:
      # status code 400 when is an input error
      if config.showErrorLogs:
        app.logger.error(repr(e))
      abort(400)
    except Exception as e:
      # status code 500 when other exception is thrown
      if config.showErrorLogs:
        app.logger.error(repr(e))
      abort(500)
  
  return app

def backgroundJob(config, logger):
  try:
    logger.debug('Requesting flights reservations and saving them in database.')
    flightsManager = FlightsReservationsManager(config.getDatabaseConnection())
    flightsManager.fetchReservationsFromSourceAndSaveLocally()
  
  except Exception as e:
    if config.showErrorLogs:
      logger.error(repr(e))

def setUpLoggerForBackgroundJob(config):
  logger = logging.getLogger('backgroundJobLogger')
  hdlr = logging.FileHandler(os.path.dirname(os.path.abspath(__file__)) + '/' + config.backgroundJobLogfile)
  formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
  hdlr.setFormatter(formatter)
  logger.addHandler(hdlr) 
  logger.setLevel(logging.DEBUG)
  return logger

def setUpBackgroundJob(config):
  logger = setUpLoggerForBackgroundJob(config)
  scheduler = BackgroundScheduler()
  scheduler.add_job(backgroundJob, 'interval', seconds = config.backgroundJobInterval, args = (config, logger))
  scheduler.start()

def initializeApp(app, config):
  if config.backgroundJobActivated:
    setUpBackgroundJob(config)
  app.run(debug = config.debug, use_reloader = False)

if __name__ == '__main__':
  app = createApp(productionConfig)
  initializeApp(app, productionConfig)