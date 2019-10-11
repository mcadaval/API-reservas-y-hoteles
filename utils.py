import os
import json

def setUpDatabase(mysqlConnection, database):
  cursor = mysqlConnection.cursor()
  fullDumpFilename = os.path.dirname(os.path.abspath(__file__)) + '/db/databaseSchema.sql'
  file = open(fullDumpFilename)
  # read file content (queries) and replace the default db name for the given one
  sqlQueries = file.read().replace('api_database', database)
  cursor.execute(sqlQueries, multi = True)
  file.close()

def dropDatabase(mysqlConnection, database):
  cursor = mysqlConnection.cursor()
  query = "DROP DATABASE `" + database + "`";
  cursor.execute(query)

def truncateTable(mysqlConnection, table):
  cursor = mysqlConnection.cursor()
  query = "TRUNCATE TABLE `" + table + "`";
  cursor.execute(query)

def setUpDatabaseContent(mysqlConnection, dumpFilename):
  cursor = mysqlConnection.cursor()
  file = open(dumpFilename)
  sqlQueries = file.read()
  cursor.execute(sqlQueries, multi = True)
  mysqlConnection.commit()
  file.close()

def setUpMockResponse(mockResponse, HTTPstatusCode, responseContentFile, sideEffect = None):
  mockResponse.return_value.status_code = HTTPstatusCode
  if not responseContentFile is None:
    file = open(responseContentFile)
    jsonContent = json.load(file)
    mockResponse.return_value.json.return_value = jsonContent
    file.close()
  
  if not sideEffect is None:
    mockResponse.side_effect = sideEffect