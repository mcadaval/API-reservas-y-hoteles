import os
import sys
sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)) + '/../')
from cfg import productionConfig
from utils import setUpDatabase
import mysql.connector

if __name__ == '__main__':
  
  try:
    connection = mysql.connector.connect(
      host = productionConfig.mysqlArguments['host'],
      user = productionConfig.mysqlArguments['user'],
      passwd = productionConfig.mysqlArguments['passwd']
    )
    setUpDatabase(connection, productionConfig.mysqlArguments['database'])
    connection.close()
  
  except Exception as e:
    print(repr(e))
