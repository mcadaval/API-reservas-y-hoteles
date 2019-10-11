import os
import json

def setUpDatabase(mysqlConnection, database):
  cursor = mysqlConnection.cursor()
  fullDumpFilename = os.path.dirname(os.path.abspath(__file__)) + '/databaseStructure.sql'
  file = open(fullDumpFilename)
  sqlQueries = file.read().replace('api_database', database)
  cursor.execute(sqlQueries, multi = True)
  file.close()

  # for result in cursor.execute(sqlQueries, multi=True):
  #   if result.with_rows:
  #     print("Rows produced by statement '{}':".format(
  #       result.statement))
  #     print(result.fetchall())
  #   else:
  #     print("Number of rows affected by statement '{}': {}".format(
  #       result.statement, result.rowcount))
  # connection.close()
  # file.close()

def dropDatabase(mysqlConnection, database):
  cursor = mysqlConnection.cursor()
  query = "DROP DATABASE `" + database + "`";
  cursor.execute(query)

def truncateTable(mysqlConnection, table):
  cursor = mysqlConnection.cursor()
  query = "TRUNCATE TABLE `" + table + "`";
  cursor.execute(query)

def setUpDatabaseContent(connection, dumpFilename):
  cursor = connection.cursor()
  file = open(dumpFilename)
  sqlQueries = file.read()
  cursor.execute(sqlQueries, multi = True)
  connection.commit()
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