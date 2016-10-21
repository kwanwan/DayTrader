import sys

print('Starting create-daytrader-resources.py ...')

propertiesIS = java.io.FileInputStream("create-daytrader-resources.properties")
properties = Properties()
properties.load(propertiesIS)

iddomain = properties.get("iddomain")
wlsusername = properties.get("wlsusername")
wlspassword = properties.get("wlspassword")
wlsadminhost = properties.get("wlsadminhost")
wlsadminport = properties.get("wlsadminport")
targetcluster = properties.get("targetcluster")
targetserver = properties.get("targetserver")
dbhost = properties.get("dbhost")
dbport = properties.get("dbport")
dbpdb = properties.get("dbpdb")

# Computed variables
domainsufix=iddomain+'.oraclecloud.internal'
dnssufix='.compute-'+domainsufix

connect(wlsusername,wlspassword,'t3://'+wlsadminhost+':'+wlsadminport)
edit()

startEdit()

cmo.createJDBCSystemResource('jdbc/datasources/TradeDataSource')
cd('/JDBCSystemResources/jdbc/datasources/TradeDataSource/JDBCResource/jdbc/datasources/TradeDataSource')
cmo.setName('jdbc/datasources/TradeDataSource')

cd('/JDBCSystemResources/jdbc/datasources/TradeDataSource/JDBCResource/jdbc/datasources/TradeDataSource/JDBCDataSourceParams/jdbc/datasources/TradeDataSource')
set('JNDINames',jarray.array([String('jdbc/datasources/TradeDataSource')], String))

cd('/JDBCSystemResources/jdbc/datasources/TradeDataSource/JDBCResource/jdbc/datasources/TradeDataSource/JDBCDriverParams/jdbc/datasources/TradeDataSource')
cmo.setUrl('jdbc:oracle:thin:@//'+dbhost+':'+dbport+'/'+dbpdb+'.'+domainsufix)
cmo.setDriverName('oracle.jdbc.OracleDriver')
cmo.setPassword('trade')
cd('/JDBCSystemResources/jdbc/datasources/TradeDataSource/JDBCResource/jdbc/datasources/TradeDataSource/JDBCDriverParams/jdbc/datasources/TradeDataSource/Properties/jdbc/datasources/TradeDataSource')
cmo.createProperty('user')
cd('/JDBCSystemResources/jdbc/datasources/TradeDataSource/JDBCResource/jdbc/datasources/TradeDataSource/JDBCDriverParams/jdbc/datasources/TradeDataSource/Properties/jdbc/datasources/TradeDataSource/Properties/user')
cmo.setValue('trade')

cd('/JDBCSystemResources/jdbc/datasources/TradeDataSource/JDBCResource/jdbc/datasources/TradeDataSource/JDBCDataSourceParams/jdbc/datasources/TradeDataSource')
cmo.setGlobalTransactionsProtocol('EmulateTwoPhaseCommit')

cd('/JDBCSystemResources/jdbc/datasources/TradeDataSource')
set('Targets',jarray.array([ObjectName('com.bea:Name='+targetcluster+',Type=Cluster')], ObjectName))
#Replace it with your respective cluster name.

activate()

startEdit()

cd('/')
cmo.createJDBCSystemResource('jdbc/datasources/NoTxTradeDataSource')

cd('/JDBCSystemResources/jdbc/datasources/NoTxTradeDataSource/JDBCResource/jdbc/datasources/NoTxTradeDataSource')
cmo.setName('jdbc/datasources/NoTxTradeDataSource')

cd('/JDBCSystemResources/jdbc/datasources/NoTxTradeDataSource/JDBCResource/jdbc/datasources/NoTxTradeDataSource/JDBCDataSourceParams/jdbc/datasources/NoTxTradeDataSource')
set('JNDINames',jarray.array([String('jdbc/datasources/NoTxTradeDataSource')], String))

cd('/JDBCSystemResources/jdbc/datasources/NoTxTradeDataSource/JDBCResource/jdbc/datasources/NoTxTradeDataSource/JDBCDriverParams/jdbc/datasources/NoTxTradeDataSource')
cmo.setUrl('jdbc:oracle:thin:@//'+dbhost+':'+dbport+'/'+dbpdb+'.'+domainsufix)
cmo.setDriverName('oracle.jdbc.OracleDriver')
cmo.setPassword('trade')

cd('/JDBCSystemResources/jdbc/datasources/NoTxTradeDataSource/JDBCResource/jdbc/datasources/NoTxTradeDataSource/JDBCDriverParams/jdbc/datasources/NoTxTradeDataSource/Properties/jdbc/datasources/NoTxTradeDataSource')
cmo.createProperty('user')

cd('/JDBCSystemResources/jdbc/datasources/NoTxTradeDataSource/JDBCResource/jdbc/datasources/NoTxTradeDataSource/JDBCDriverParams/jdbc/datasources/NoTxTradeDataSource/Properties/jdbc/datasources/NoTxTradeDataSource/Properties/user')
cmo.setValue('trade')

cd('/JDBCSystemResources/jdbc/datasources/NoTxTradeDataSource/JDBCResource/jdbc/datasources/NoTxTradeDataSource/JDBCDataSourceParams/jdbc/datasources/NoTxTradeDataSource')
cmo.setGlobalTransactionsProtocol('EmulateTwoPhaseCommit')

cd('/JDBCSystemResources/jdbc/datasources/NoTxTradeDataSource')
set('Targets',jarray.array([ObjectName('com.bea:Name='+targetcluster+',Type=Cluster')], ObjectName))
# Replace it with your respective cluster name.
activate()

startEdit()

cd('/')
cmo.createJMSServer('MyJMSServer')

cd('/JMSServers/MyJMSServer')
set('Targets',jarray.array([ObjectName('com.bea:Name='+targetserver+',Type=Server')], ObjectName))
#Replace it with your respective Managed Server name.
activate()

startEdit()

cd('/')
cmo.createJMSSystemResource('MyJMSModule')

cd('/JMSSystemResources/MyJMSModule')
set('Targets',jarray.array([ObjectName('com.bea:Name='+targetcluster+',Type=Cluster')], ObjectName))
# Replace it with your respective cluster name.

cmo.createSubDeployment('MySubDeployment')

cd('/JMSSystemResources/MyJMSModule/JMSResource/MyJMSModule')
cmo.createConnectionFactory('jms/myQueueConnectionFactory')

cd('/JMSSystemResources/MyJMSModule/JMSResource/MyJMSModule/ConnectionFactories/jms/myQueueConnectionFactory')
cmo.setJNDIName('jms/myQueueConnectionFactory')

cd('/JMSSystemResources/MyJMSModule/JMSResource/MyJMSModule/ConnectionFactories/jms/myQueueConnectionFactory/SecurityParams/jms/myQueueConnectionFactory')
cmo.setAttachJMSXUserId(false)

cd('/JMSSystemResources/MyJMSModule/JMSResource/MyJMSModule/ConnectionFactories/jms/myQueueConnectionFactory/ClientParams/jms/myQueueConnectionFactory')
cmo.setClientIdPolicy('Restricted')
cmo.setSubscriptionSharingPolicy('Exclusive')
cmo.setMessagesMaximum(10)

cd('/JMSSystemResources/MyJMSModule/JMSResource/MyJMSModule/ConnectionFactories/jms/myQueueConnectionFactory/TransactionParams/jms/myQueueConnectionFactory')
cmo.setXAConnectionFactoryEnabled(true)

cd('/JMSSystemResources/MyJMSModule/SubDeployments/MySubDeployment')
set('Targets',jarray.array([ObjectName('com.bea:Name=MyJMSServer,Type=JMSServer')], ObjectName))

cd('/JMSSystemResources/MyJMSModule/JMSResource/MyJMSModule/ConnectionFactories/jms/myQueueConnectionFactory')
cmo.setSubDeploymentName('MySubDeployment')

cd('/JMSSystemResources/MyJMSModule/JMSResource/MyJMSModule')
cmo.createConnectionFactory('jms/myTopicConnectionFactory')

cd('/JMSSystemResources/MyJMSModule/JMSResource/MyJMSModule/ConnectionFactories/jms/myTopicConnectionFactory')
cmo.setJNDIName('jms/myTopicConnectionFactory')

cd('/JMSSystemResources/MyJMSModule/JMSResource/MyJMSModule/ConnectionFactories/jms/myTopicConnectionFactory/SecurityParams/jms/myTopicConnectionFactory')
cmo.setAttachJMSXUserId(false)

cd('/JMSSystemResources/MyJMSModule/JMSResource/MyJMSModule/ConnectionFactories/jms/myTopicConnectionFactory/ClientParams/jms/myTopicConnectionFactory')
cmo.setClientIdPolicy('Restricted')
cmo.setSubscriptionSharingPolicy('Exclusive')
cmo.setMessagesMaximum(10)

cd('/JMSSystemResources/MyJMSModule/JMSResource/MyJMSModule/ConnectionFactories/jms/myTopicConnectionFactory/TransactionParams/jms/myTopicConnectionFactory')
cmo.setXAConnectionFactoryEnabled(true)

cd('/JMSSystemResources/MyJMSModule/SubDeployments/MySubDeployment')
set('Targets',jarray.array([ObjectName('com.bea:Name=MyJMSServer,Type=JMSServer')], ObjectName))

cd('/JMSSystemResources/MyJMSModule/JMSResource/MyJMSModule/ConnectionFactories/jms/myTopicConnectionFactory')
cmo.setSubDeploymentName('MySubDeployment')

cd('/JMSSystemResources/MyJMSModule/JMSResource/MyJMSModule')
cmo.createQueue('jms/TradeBrokerQueue')

cd('/JMSSystemResources/MyJMSModule/JMSResource/MyJMSModule/Queues/jms/TradeBrokerQueue')
cmo.setJNDIName('jms/TradeBrokerQueue')
cmo.setSubDeploymentName('MySubDeployment')

cd('/JMSSystemResources/MyJMSModule/SubDeployments/MySubDeployment')
set('Targets',jarray.array([ObjectName('com.bea:Name=MyJMSServer,Type=JMSServer')], ObjectName))

cd('/JMSSystemResources/MyJMSModule/JMSResource/MyJMSModule')
cmo.createTopic('jms/TradeStreamerTopic')

cd('/JMSSystemResources/MyJMSModule/JMSResource/MyJMSModule/Topics/jms/TradeStreamerTopic')
cmo.setJNDIName('jms/TradeStreamerTopic')
cmo.setSubDeploymentName('MySubDeployment')

cd('/JMSSystemResources/MyJMSModule/SubDeployments/MySubDeployment')
set('Targets',jarray.array([ObjectName('com.bea:Name=MyJMSServer,Type=JMSServer')], ObjectName))
activate()