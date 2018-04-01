import utime
# Debug sleep for when using RX TX as gpio for rfid
# since the repl won't be availble after being
# reconfigured
utime.sleep(5)

import mfrc522
import picoweb
import load_sensor
import easydriver_esp
import acf_network as w
import coroutines as c
import tinyDB
import routes

db = tinyDB.TinyDB()

r = routes.Route(db)

cr = c.Coroutines(db)

funcs = [cr.networkRoutine]

app = picoweb.WebApp(__name__,r.ROUTES)

while cr.net.isConnected() == False:
    pass

app.run(debug=True, host=cr.net.wlan.ifconfig()[0], func_list=funcs)
