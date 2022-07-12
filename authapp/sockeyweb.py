from smartapi import SmartConnect #or from smartapi.smartConnect import SmartConnect
from smartapi import SmartWebSocket
#import smartapi.smartExceptions(for smartExceptions)

#create object of call
obj=SmartConnect(api_key="33KgzBX0")

#login api call

data = obj.generateSession("DIYD12736","Alone@1987")
refreshToken= data['data']['refreshToken']

#fetch the feedtoken
feedToken=obj.getfeedToken()
print(feedToken)



# feed_token=092017047
FEED_TOKEN=feedToken
CLIENT_CODE="DIYD12736"
# token="mcx_fo|224395"
token="nse_cm|26009&nse_fo|40746"    #SAMPLE: nse_cm|2885&nse_cm|1594&nse_cm|11536&nse_cm|3045
# token="mcx_fo|226745&mcx_fo|220822&mcx_fo|227182&mcx_fo|221599"
task="mw"   # mw|sfi|dp

ss = SmartWebSocket(FEED_TOKEN, CLIENT_CODE)

def on_message(ws, message):
    print("Ticks: {}".format(message))

def on_open(ws):
    print("on open")
    ss.subscribe(task,token)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("Close")

# Assign the callbacks.
ss._on_open = on_open
ss._on_message = on_message
ss._on_error = on_error
ss._on_close = on_close

ss.connect()