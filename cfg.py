from Config import Config

productionConfigParameters = {
  'mysqlArguments' : {
    'host' : 'myhost',
    'user' : 'myuser',
    'passwd' : 'mypassword',
    'database' : 'api_database',
  },
  'clientId' : 'myclientid',
  'clientSecret' : 'myclientsecret',
  'backgroundJobActivated' : True,              # set to True to enable background job execution
  'backgroundJobInterval' : 300,                # interval in seconds between each execution of the background job
  'backgroundJobLogfile' : 'backgroundJob.log', # logfile for basic debug of the background job
  'debug' : True,                               # set to True to run flask in debug mode
  'showErrorLogs' : True                        # set to True to print error logs in console (from requests)
}

# note: some of the parameters are useless for testing config since they are not used
testingConfigParameters = {
  'mysqlArguments' : {
    'host' : 'myhost',
    'user' : 'myuser',
    'passwd' : 'mypassword',
    'database' : 'api_database_test',
  },
  'clientId' : 'myclientid',
  'clientSecret' : 'myclientsecret',
  'backgroundJobActivated' : False,              # set to True to enable background job execution
  'backgroundJobInterval' : 300,                 # interval in seconds between each execution of the background job
  'backgroundJobLogfile' : 'backgroundJob.log',  # logfile for basic debug of the background job
  'debug' : False,                               # set to True to run flask in debug mode
  'showErrorLogs' : False                        # set to True to print error logs in console (from requests)
}

productionConfig = Config(productionConfigParameters)
testingConfig = Config(testingConfigParameters)