import mysql.connector

class Config:

  def __init__(self, configJson):
    self.mysqlArguments = configJson['mysqlArguments']
    self.clientId = configJson['clientId']
    self.clientSecret = configJson['clientSecret']
    self.backgroundJobActivated = configJson['backgroundJobActivated']
    self.backgroundJobInterval = configJson['backgroundJobInterval']
    self.debug = configJson['debug']
    self.connection = None

  def getDatabaseConnection(self):
    if self.connection is None:
      self.connection = mysql.connector.connect(
        host = self.mysqlArguments['host'],
        user = self.mysqlArguments['user'],
        passwd = self.mysqlArguments['passwd'],
        database = self.mysqlArguments['database']
      )
    return self.connection