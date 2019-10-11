from Config import Config

productionConfigParameters = {
  'mysqlArguments' : {
    'host' : 'myhost',
    'user' : 'myuser',
    'passwd' : 'mypassword',
    'database' : 'mydatabase',
  },
  'clientId' : 'myclientid',
  'clientSecret' : 'myclientsecret',
  'backgroundJobActivated' : True,
  'backgroundJobInterval' : 300,
  'debug' : False
}

testingConfigParameters = {
  'mysqlArguments' : {
    'host' : 'myhost',
    'user' : 'myuser',
    'passwd' : 'mypassword',
    'database' : 'mydatabase',
  },
  'clientId' : 'myclientid',
  'clientSecret' : 'myclientsecret',
  'backgroundJobActivated' : False,
  'backgroundJobInterval' : 300,
  'debug' : False
}

productionConfig = Config(productionConfigParameters)
testingConfig = Config(testingConfigParameters)